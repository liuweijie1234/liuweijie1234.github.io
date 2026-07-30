---
title: Flask 数据库（Flask-SQLAlchemy）
date: 2026-07-30 11:25:00
tags:
- Flask
- SQLAlchemy
- ORM
categories:
- Web开发
- Flask
---

## 一、Flask-SQLAlchemy 简介

`Flask-SQLAlchemy` 是 SQLAlchemy 的 Flask 封装，提供 ORM 与声明式模型。

```bash
pip install flask-sqlalchemy
```

## 二、初始化

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```

## 三、定义模型

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    user_id = db.Column(db.ForeignKey('user.id'))
```

## 四、CRUD

```python
db.create_all()                              # 建表（仅开发）
u = User(username='bob')
db.session.add(u); db.session.commit()
users = User.query.filter_by(username='bob').all()
u.username = 'alice'; db.session.commit()
db.session.delete(u); db.session.commit()
```

## 五、关系查询

```python
user = User.query.get(1)
user.posts                        # 关联文章（backref）
Post.query.join(User).filter(User.username == 'bob').all()
```

## 六、迁移（Flask-Migrate）

生产环境用 **Flask-Migrate（Alembic）** 管理 schema 变更：

```bash
pip install flask-migrate
flask db init
flask db migrate -m "add user"
flask db upgrade
```

## 七、最佳实践

- 关闭 `SQLALCHEMY_TRACK_MODIFICATIONS`（省内存）。
- 用 `Flask-Migrate` 做迁移，别手动 `create_all` 上线。
- 大量写入用 `bulk_save_objects` / `session.bulk_insert_mappings` 提升性能。
- 注意连接池与超时（`SQLALCHEMY_ENGINE_OPTIONS`）。
