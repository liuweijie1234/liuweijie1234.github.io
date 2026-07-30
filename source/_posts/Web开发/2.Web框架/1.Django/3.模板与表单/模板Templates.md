---
title: Django 模板（Templates）
date: 2026-07-30 10:10:00
tags:
- Django
- 模板
- DTL
categories:
- Web开发
- Django
---

## 一、模板系统的作用

模板负责**表现层**：把视图传入的上下文（context）渲染成 HTML。Django 自带模板语言 **DTL（Django Template Language）**，也支持 Jinja2。

## 二、配置与查找

`settings.py`：

```python
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],          # 全局模板目录
    'APP_DIRS': True,                          # 自动查找各 app 下的 templates/
}]
```

查找顺序：先 `DIRS`，再各 app 的 `templates/`。为避免同名冲突，建议在 app 内再建一层以 app 命名的子目录：`blog/templates/blog/list.html`。

## 三、变量与标签

{% raw %}
```html
<h1>{{ article.title }}</h1>
<p>作者：{{ article.author.name|default:'匿名' }}</p>

{% if user.is_authenticated %}
  <a href="{% url 'logout' %}">退出</a>
{% else %}
  <a href="{% url 'login' %}">登录</a>
{% endif %}

<ul>
{% for item in articles %}
  <li>{{ forloop.counter }}. {{ item.title }}</li>
{% empty %}
  <li>暂无文章</li>
{% endfor %}
</ul>
```
{% endraw %}

## 四、常用过滤器

| 过滤器 | 作用 |
|--------|------|
| `default` | 默认值 |
| `length` | 长度 |
| `date:"Y-m-d"` | 日期格式化 |
| `slice:":10"` | 切片 |
| `safe` | 关闭自动转义（慎用，防 XSS） |
| `truncatechars:30` | 截断 |

## 五、模板继承（extends / block）

`base.html`：

{% raw %}
```html
<!doctype html>
<html>
<body>
  {% block content %}{% endblock %}
  {% block footer %}<footer>© me</footer>{% endblock %}
</body>
</html>
```
{% endraw %}

子模板：

{% raw %}
```html
{% extends 'base.html' %}
{% block content %}
  <h1>{{ title }}</h1>
{% endblock %}
```
{% endraw %}

`include` 复用片段：

{% raw %}
```html
{% include 'partials/header.html' with user=user %}
```
{% endraw %}

## 六、自定义过滤器与标签

```python
# blog/templatetags/blog_extras.py
from django import template
register = template.Library()

@register.filter
def upper_first(value):
    return value[:1].upper() + value[1:]

@register.simple_tag
def current_time(format='%Y'):
    from datetime import datetime
    return datetime.now().strftime(format)
```

模板中使用：`{% load blog_extras %}`。

## 七、自动转义与 XSS 防护

DTL 默认自动转义 `& < > " '`，能有效防 XSS。只有**确实**要输出可信 HTML 时才用 `|safe` 或 `{% autoescape off %}`，且内容必须经清洗（如 `bleach`）。

## 八、最佳实践

- 用 `extends`/`include` 消除重复，保持模板「瘦」。
- 复杂展示逻辑放在视图里算好再传，模板只做最简单判断。
- 静态资源用 `{% static '...' %}`（见 `7.缓存与数据库/静态文件.md`）。
- 大段 Python 逻辑不要写进模板，自定义标签/过滤器封装。
