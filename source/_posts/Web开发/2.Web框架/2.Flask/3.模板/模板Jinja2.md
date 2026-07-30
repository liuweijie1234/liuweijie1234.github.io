---
title: Flask 模板（Jinja2）
date: 2026-07-30 11:10:00
tags:
- Flask
- Jinja2
- 模板
categories:
- Web开发
- Flask
---

## 一、Jinja2 简介

Flask 默认模板引擎是 **Jinja2**，语法与 Django 模板类似但更灵活（支持在模板中调用函数、宏）。

## 二、渲染模板

```python
from flask import render_template

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
```

模板目录默认是 `templates/`。

## 三、变量、控制结构

{% raw %}
```html
<h1>{{ name }}</h1>

{% if user %}
  <p>欢迎 {{ user }}</p>
{% else %}
  <p>请登录</p>
{% endif %}

<ul>
{% for item in items %}
  <li>{{ loop.index }}. {{ item }}</li>
{% endfor %}
</ul>
```
{% endraw %}

## 四、模板继承

`base.html`：

{% raw %}
```html
<html><body>{% block content %}{% endblock %}</body></html>
```
{% endraw %}

子模板：

{% raw %}
```html
{% extends 'base.html' %}
{% block content %}<h1>首页</h1>{% endblock %}
```
{% endraw %}

## 五、宏（Macro）

{% raw %}
```html
{% macro input(name, value='') %}
  <input type="text" name="{{ name }}" value="{{ value }}">
{% endmacro %}

{{ input('username') }}
```
{% endraw %}

宏类似「模板里的函数」，复用表单片段很方便。

## 六、过滤器

{% raw %}
```html
{{ name|capitalize }}
{{ list|join(', ') }}
{{ text|truncate(30) }}
{{ None|default('无') }}
```
{% endraw %}

## 七、自动转义与 XSS

Jinja2 对 `{{ }}` 默认转义。仅对可信内容用 `|safe`，动态用户输入必须保持转义。

## 八、最佳实践

- 用 `extends`/`include`/`macro` 消除重复。
- 复杂逻辑前置到视图；模板只做展示。
- 静态文件用 `url_for('static', filename='style.css')`。
