---
title: Flask 蓝图（Blueprint）
date: 2026-07-30 11:05:00
tags:
- Flask
- 蓝图
- Blueprint
categories:
- Web开发
- Flask
---

## 一、为什么用蓝图

**蓝图（Blueprint）** 用于把路由、视图、模板、静态文件**模块化拆分**，再统一注册到 app。适合多模块/多团队的中大型项目。

## 二、定义与注册

```python
# auth.py
from flask import Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return 'login page'
```

```python
# app.py
from auth import auth_bp
app.register_blueprint(auth_bp)
```

访问 `/auth/login`。

## 三、蓝图常用参数

| 参数 | 作用 |
|------|------|
| `url_prefix` | URL 前缀 |
| `template_folder` | 蓝图私有模板目录 |
| `static_folder` | 蓝图私有静态目录 |
| `url_prefix` | 统一前缀 |
| `name` | 蓝图名（用于 `url_for('auth.login')`） |

## 四、子域名蓝图

```python
api = Blueprint('api', __name__, subdomain='api')
app.config['SERVER_NAME'] = 'example.com'
```

## 五、在应用工厂里注册

```python
def create_app():
    app = Flask(__name__)
    from .auth import auth_bp
    from .blog import blog_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    return app
```

## 六、最佳实践

- 一个功能域一个蓝图，目录结构：`app/auth/__init__.py`、`app/auth/routes.py`、`app/auth/templates/auth/`。
- 用 `url_for('蓝图名.视图名')` 反向解析，避免跨模块硬编码。
- 把蓝图注册集中在 `create_app`，保持 `__init__.py` 干净。
