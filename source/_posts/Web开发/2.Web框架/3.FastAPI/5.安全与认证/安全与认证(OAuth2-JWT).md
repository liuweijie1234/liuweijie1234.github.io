---
title: FastAPI 安全与认证（OAuth2 + JWT）
date: 2026-07-30 12:00:00
tags:
- FastAPI
- 认证
- OAuth2
- JWT
categories:
- Web开发
- FastAPI
---

## 一、认证方案概览

FastAPI 通过 `fastapi.security` 内置 OAuth2 密码流、API Key、HTTP Basic 等。最常见组合：**OAuth2 密码模式 + JWT**。

## 二、密码哈希

```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')

hashed = pwd.hash('plain')
pwd.verify('plain', hashed)     # True
```

**绝不明文存密码**；bcrypt/scrypt 优先。

## 三、OAuth2 密码流

```python
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

@app.post('/token')
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    if not user:
        raise HTTPException(status_code=400, detail='bad credentials')
    token = create_jwt(user.id)
    return {'access_token': token, 'token_type': 'bearer'}
```

`OAuth2PasswordRequestForm` 对应表单字段 `username`/`password`，与 `/docs` 授权按钮兼容。

## 四、签发与校验 JWT

```python
import jwt
from datetime import datetime, timedelta

def create_jwt(uid):
    payload = {'sub': str(uid), 'exp': datetime.utcnow() + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET, algorithm='HS256')

def decode_jwt(tok):
    return jwt.decode(tok, SECRET, algorithms=['HS256'])
```

## 五、保护路由（get_current_user 依赖）

```python
from fastapi.security import HTTPBearer
bearer = HTTPBearer()

def get_current_user(cred = Depends(bearer)):
    try:
        payload = decode_jwt(cred.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='token expired')
    return payload['sub']

@app.get('/me')
def me(uid = Depends(get_current_user)):
    return {'uid': uid}
```

## 六、刷新令牌与权限

- 用短效 access token + 长效 refresh token 提升安全。
- 角色/权限放进 JWT `scope`，在依赖里校验 `scope`。
- 生产用强随机 `SECRET`，放环境变量。

## 七、最佳实践

- 密码用 bcrypt 哈希；JWT 密钥绝不入库。
- access token 短时效，敏感操作二次校验。
- 用 `HTTPBearer`/`OAuth2` 让 `/docs` 可一键授权联调。
- 配合 HTTPS 传输 token（见 `10.部署/部署文档.md`）。
