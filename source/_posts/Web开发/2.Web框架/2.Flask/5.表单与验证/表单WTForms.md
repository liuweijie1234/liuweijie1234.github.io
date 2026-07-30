---
title: Flask 表单与验证（WTForms）
date: 2026-07-30 11:20:00
tags:
- Flask
- WTForms
- 表单
categories:
- Web开发
- Flask
---

## 一、Flask-WTF 简介

`Flask-WTF` 基于 `WTForms`，提供表单类、CSRF 保护、文件上传。

```bash
pip install flask-wtf
```

## 二、定义表单

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(2, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20)])
    confirm = PasswordField('确认', validators=[EqualTo('password')])
    submit = SubmitField('注册')
```

## 三、视图与模板

```python
from flask import render_template, redirect, url_for, flash

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('注册成功')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
```

```html
<form method="post">
  {{ form.csrf_token }}
  {{ form.username.label }} {{ form.username() }}
  {% for e in form.username.errors %}<span>{{ e }}</span>{% endfor %}
  {{ form.submit() }}
</form>
```

## 四、常用验证器

`DataRequired`、`Length`、`NumberRange`、`Email`、`Regexp`、`EqualTo`、`URL`、`Optional`。自定义验证器：

```python
def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('用户名已存在')
```

## 五、文件上传字段

```python
from flask_wtf.file import FileField, FileAllowed
avatar = FileField('头像', validators=[FileAllowed(['png', 'jpg'])])
```

## 六、最佳实践

- 始终渲染并校验 CSRF token。
- 错误用 `flash` + 模板 `get_flashed_messages` 反馈。
- 模型表单可用 `model_form`（或自写）缩短代码；但更推荐显式定义。
- 服务端校验不可省，前端校验仅提升体验。
