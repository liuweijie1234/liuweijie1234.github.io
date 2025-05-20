import time
import random
import string

from urllib.parse import urlencode
from flask import request, redirect, current_app
from flask_restful import Resource, reqparse
from werkzeug.security import gen_salt
from extensions.ext_database import db
from models.account import OAuth2Client, OAuth2AuthorizationCode, Account
from controllers.console import api
from services.account_service import AccountService, TenantService
from libs.helper import extract_remote_ip


class CreateFreeClient(Resource):
    """创建免登录的 OAuth2 客户端"""

    def _check_client_id_unique(self, id):
        exists = OAuth2Client.query.filter(OAuth2Client.client_id == id).first()
        if exists:
            raise ValueError(f"客户端ID '{id}' 已存在")
    
    def _validate_redirect_uris(self, uris):
        if not isinstance(uris, list):
            raise ValueError("redirect_uris 必须是一个数组")
        
        for uri in uris:
            if not isinstance(uri, str):
                raise ValueError("每个 URI 必须是字符串")
            if not uri.startswith(('http://', 'https://')):
                raise ValueError(f"无效的 URI 格式: {uri}")

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('client_name', type=str, required=True, 
                              help='客户端名称不能为空')
            parser.add_argument('client_id', type=str, required=True, 
                              help='客户端id不能为空')
            parser.add_argument('redirect_uris', type=list, required=True, location='json',
                              help='回调地址不能为空')
            parser.add_argument('client_uri', type=str)
            parser.add_argument('logo_uri', type=str)
            parser.add_argument('scope', type=str)
            args = parser.parse_args()
 
            self._check_client_id_unique(args.client_id)
            self._validate_redirect_uris(args.redirect_uris)
            
            client_id = args.client_id
            client_secret = gen_salt(48)
            client_id_issued_at = int(time.time())
            client_secret_expires_at = int(time.time()) + 3600 * 24 * 365 * 1 # 1年

            client = OAuth2Client(
                client_id=client_id,
                client_secret=client_secret,
                client_id_issued_at=client_id_issued_at,
                client_secret_expires_at=client_secret_expires_at,
            )

            client_metadata = {
                "redirect_uris": args.redirect_uris,  
                "token_endpoint_auth_method": "client_secret_basic", 
                "grant_types": ["authorization_code"], 
                "response_types": ["code"],
                "client_name": args.client_name,
            }
            
            if args.client_uri:
                client_metadata["client_uri"] = args.client_uri
            if args.logo_uri:
                client_metadata["logo_uri"] = args.logo_uri
            if args.scope:
                client_metadata["scope"] = args.scope
            
            client.set_client_metadata(client_metadata)

            db.session.add(client)
            db.session.commit()

            return {
                'code': 0,
                'data': {
                    'client_id': client.client_id,
                    'client_secret': client.client_secret,
                    'message': '创建成功'
                }
            }, 200

        except Exception as e:
            db.session.rollback()
            return {
                'code': 1,
                'message': f'创建失败: {str(e)}'
            }, 500


class GenerateAuthorizationCode(Resource):
    """生成授权码接口"""

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('client_id', type=str, required=True, location='args',
                              help='client_id 不能为空')
            parser.add_argument('redirect_uri', type=str, required=True,location='args',
                              help='redirect_uri 不能为空')
            parser.add_argument('response_type', type=str, required=True,location='args',
                              help='response_type 不能为空')
            parser.add_argument('state', type=str, required=True,location='args',
                              help='state 不能为空')
            args = parser.parse_args()

            if args.response_type != 'code':
                raise ValueError("response_type 必须为 'code'")

            client = OAuth2Client.query.filter_by(client_id=args.client_id).first()

            if not client:
                raise ValueError("无效的客户端ID")

            if args.redirect_uri not in client.client_metadata.get('redirect_uris', []):
                raise ValueError("无效的回调地址")

            auth_code = OAuth2AuthorizationCode(
                user_id=None,
                code= gen_salt(48),
                client_id=client.client_id,
                redirect_uri=args.redirect_uri,
                response_type=args.response_type,
                scope='openid profile email',  # 设置默认scope
                auth_time=int(time.time()),
            )

            db.session.add(auth_code)
            db.session.commit()

            params = {
                'code': auth_code.code,
                'state': args.state
            }
            redirect_uri = f"{args.redirect_uri}?{urlencode(params)}"
            return redirect(redirect_uri)

        except Exception as e:
            db.session.rollback()

            if hasattr(args, 'redirect_uri') and hasattr(args, 'state'):
                error_params = {
                    'error': 'invalid_request',
                    'error_description': str(e)
                }
                if args.state:
                    error_params['state'] = args.state
                error_redirect_uri = f"{args.redirect_uri}?{urlencode(error_params)}"
                return redirect(error_redirect_uri)
            
            return {
                'code': 1,
                'message': f'授权失败: {str(e)}'
            }, 400


class UserService:
    """用户服务"""
    
    @staticmethod
    def _generate_random_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))
    

    @staticmethod
    def get_or_create_user(name, phone=None, email=None, tenant=None):
        try:
            if not phone and not email:
                raise ValueError("电话和邮箱至少需要提供一个")
            
            user = None
            if phone:
                user = Account.query.filter_by(phone=phone).first()
                if user:
                    return user, None
            if email:
                user = Account.query.filter_by(email=email).first()
                if user:
                    return user, None
   
            if not user:
                # 生成随机密码
                # password = UserService._generate_random_password()
                password = "Aa123456"
                
                user = AccountService.create_account(
                    email=email, 
                    name=name, 
                    phone=phone,
                    interface_language='zh-Hans', 
                    password=password
                )
                
            if not tenant:
                tenant = TenantService.get_default_tenant()
            TenantService.create_tenant_member(tenant, user)
                
            return user, None
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Create user error: {str(e)}")
            return None, str(e)



class GenerateAccessToken(Resource):
    """生成访问令牌接口"""
    
    def _validate_authorization_code(self, code, client_id, redirect_uri):
        auth_code = OAuth2AuthorizationCode.query.filter_by(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri
        ).first()
        
        if not auth_code:
            raise ValueError("无效的授权码")
        return auth_code
    
    def _validate_client(self, client_id, client_secret):
        client = OAuth2Client.query.filter_by(
            client_id=client_id,
            client_secret=client_secret
        ).first()
        
        if not client:
            raise ValueError("无效的客户端凭证")
        return client
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('client_id', type=str, required=True)
            parser.add_argument('client_secret', type=str, required=True)
            parser.add_argument('authorization_code', type=str, required=True)
            parser.add_argument('redirect_uri', type=str, required=True)
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('phone', type=str)
            parser.add_argument('email', type=str)
            args = parser.parse_args()
  
            self._validate_client(args.client_id, args.client_secret)
 

            auth_code = self._validate_authorization_code(
                args.authorization_code,
                args.client_id,
                args.redirect_uri
            )
        
            user, error = UserService.get_or_create_user(
                name=args.name,
                phone=args.phone,
                email=args.email
            )
     
            if error:
                raise ValueError(f"用户创建失败: {error}")
            
            token_pair = AccountService.login(
                account=user,
                ip_address=extract_remote_ip(request)
            )
     
            db.session.delete(auth_code)
            db.session.commit()
            
            return {
                'code': 0,
                'data': token_pair.model_dump()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {
                'code': 1,
                'message': f'生成令牌失败: {str(e)}'
            }, 400


api.add_resource(CreateFreeClient, '/oauth/create_free_client')
api.add_resource(GenerateAuthorizationCode, '/oauth/authorize_code')
api.add_resource(GenerateAccessToken, '/oauth/access_token')

