from flask_restful import Resource, reqparse
from flask import request, jsonify
from controllers.console import api
from services.captcha_service import CaptchaService


class GenerateCaptchaApi(Resource):
    """用于生成验证码"""
    
    def get(self):
        user_ip = request.remote_addr  # 获取用户的IP地址
        result = CaptchaService.generate(user_ip)

        # 如果 result 是元组，说明是错误情况
        if isinstance(result, tuple):
            return result
            
        # 正常情况下直接返回结果
        return result


class ValidateCaptchaApi(Resource):
    """验证验证码接口"""

    def post(self):
        """验证验证码接口"""
        user_ip = request.remote_addr

        parser = reqparse.RequestParser()
        parser.add_argument('position', type=int, required=True, location='json')
        args = parser.parse_args()
        user_position = args['position']  # 用户提交的滑块位置

        if user_position is None:
            return {"status": "error", "message": "缺少位置参数"}, 400

        # 验证用户输入
        try:
            success, message = CaptchaService.validate_slide_captcha(user_ip, user_position)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        if success:
            return {"status": "success", "message": message}, 200
        else:
            return {"status": "error", "message": message}, 400


# 将资源添加到api
api.add_resource(GenerateCaptchaApi, '/validator/generate')
api.add_resource(ValidateCaptchaApi, '/validator/validate')

