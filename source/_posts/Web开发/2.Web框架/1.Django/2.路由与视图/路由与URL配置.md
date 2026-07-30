---
title: Django 路由与 URL 配置
date: 2026-07-30 10:00:00
tags:
- Django
- 路由
- URLconf
categories:
- Web开发
- Django
---

## 一、路由的本质

Django 使用 **URLconf（URL configuration）** 把请求的 URL 映射到对应的视图函数/类视图上。它本质上是一张「正则表达式/路径 → 视图」的路由表。

请求进入 Django 后，流程是：

```
请求 URL → URLconf 逐条匹配 → 命中某条 pattern → 调用对应 view(request, ...) → 返回 HttpResponse
```

源码层面，`django.urls` 模块下的 `path()` / `re_path()` 构造 `RoutePattern` / `RegexPattern`，由 `URLResolver` 递归解析，最终通过 `URLPattern.resolve()` 找到视图并注入捕获的参数。

## 二、两种路由写法

### 1. path()：直观的路径转换器（推荐）

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
```

内置路径转换器：`str`、`int`、`slug`、`uuid`、`path`。

### 2. re_path()：正则匹配

```python
from django.urls import re_path

urlpatterns = [
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
]
```

> 经验：能用 `path()` 就用 `path()`，正则只在需要复杂约束时使用。

## 三、捕获参数如何传给视图

```python
# views.py
from django.http import HttpResponse

def article_detail(request, year, month, slug):
    return HttpResponse(f'year={year}, month={month}, slug={slug}')
```

URL 捕获的参数按名称注入视图函数签名；多余的参数也可通过 `kwargs` 传入：

```python
path('blog/<int:year>/', views.year_archive, {'foo': 'bar'})
```

## 四、包含（include）与 APP 级路由

大型项目按 app 拆分路由：

```python
# 项目 urls.py
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'   # 命名空间，配合反向解析
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
]
```

## 五、反向解析（reverse / 模板 tag）

不要在代码里硬编码 URL，使用 `name` 反向解析：

```python
from django.urls import reverse

reverse('blog:detail', args=[3])          # => '/blog/3/'
reverse('blog:detail', kwargs={'pk': 3})  # => '/blog/3/'
```

模板中：

```html
<a href="{% url 'blog:detail' article.pk %}">{{ article.title }}</a>
```

## 六、最佳实践

- 始终设置 `app_name` 命名空间，避免 name 冲突。
- 路由尽量扁平、语义化（资源名复数：`/articles/` 优于 `/articleList/`）。
- 把版本前缀留给 API：`path('api/v1/', include('api.v1.urls'))`。
- 公共前缀提取到 `include()` 的 `prefix` 上，保持各 app 路由清爽。
- 用 `404`/`400` 的自定义 handler：`handler404 = 'blog.views.page_not_found'`。

## 七、常见坑

- `path()` 末尾的 `/` 与 `APPEND_SLASH`：默认 `APPEND_SLASH=True`，访问 `/blog` 会 302 到 `/blog/`。
- 路由顺序敏感：更具体的规则放前面，避免被宽泛规则提前命中。
- 正则里忘记 `$` 结尾会导致前缀匹配多个路径。
