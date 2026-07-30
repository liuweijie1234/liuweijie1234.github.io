---
title: Django 视图（Views）
date: 2026-07-30 10:05:00
tags:
- Django
- 视图
- CBV
categories:
- Web开发
- Django
---

## 一、视图是什么

视图是**接收 HttpRequest、返回 HttpResponse 的可调用对象**。它负责处理业务、组装数据、选择模板或返回 JSON。

Django 支持两种视图：
- **函数视图（FBV）**：普通函数。
- **类视图（CBV）**：基于 `django.views.View` 的类，更适合复用与组合。

## 二、函数视图 FBV

```python
from django.http import HttpResponse

def hello(request):
    if request.method == 'POST':
        return HttpResponse('got post')
    return HttpResponse('hello')
```

### HttpRequest 常用属性

| 属性 | 说明 |
|------|------|
| `request.method` | GET/POST/... |
| `request.GET` / `request.POST` | 类字典对象（QueryDict） |
| `request.body` | 原始字节 |
| `request.FILES` | 上传文件 |
| `request.session` | 会话 |
| `request.user` | 当前用户（认证中间件注入） |
| `request.META` | 请求头与环境变量 |
| `request.headers` | 只读请求头（推荐替代 META） |

### 快捷函数

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect

def detail(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    return render(request, 'article/detail.html', {'obj': obj})

def api(request):
    return JsonResponse({'ok': True})
```

## 三、类视图 CBV

```python
from django.views import View

class ArticleDetail(View):
    def get(self, request, pk):
        return HttpResponse(f'get {pk}')
    def post(self, request, pk):
        return HttpResponse(f'post {pk}')
```

路由：`path('<int:pk>/', ArticleDetail.as_view(), name='detail')`。

### 常用通用视图（Generic Views）

```python
from django.views.generic import ListView, DetailView, CreateView

class ArticleListView(ListView):
    model = Article
    template_name = 'article/list.html'
    context_object_name = 'articles'
    paginate_by = 10

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/detail.html'
```

### 请求分发原理

`View.as_view()` 返回一个闭包，内部调用 `dispatch(request, *a, **kw)`，根据 `request.method.lower()` 找到对应的 `get/post/...` 方法。可以通过重写 `dispatch` 做统一的前置/后置处理（如登录校验、日志）。

## 四、装饰器与混入

函数视图加装饰器：

```python
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    ...
```

类视图加装饰器用 `method_decorator`：

```python
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    ...
```

复用逻辑用 `Mixin`：

```python
class JSONResponseMixin:
    def render_to_json(self, context):
        return JsonResponse(context)
```

## 五、返回不同类型的响应

- `HttpResponse`：原始文本/HTML。
- `render`：模板渲染。
- `JsonResponse`：JSON。
- `HttpResponseRedirect` / `redirect`：跳转。
- `FileResponse` / `StreamingHttpResponse`：文件/流式。
- `HttpResponseNotAllowed`：方法不允许。

## 六、最佳实践

- 视图保持「薄」：业务逻辑下沉到 forms、services、models 层，视图只做「取数据 → 调逻辑 → 选响应」。
- 列表页优先用 `ListView` + 分页；详情页用 `DetailView` + `get_object_or_404`。
- 统一异常处理：`try/except` 或自定义中间件返回标准错误结构。
- API 场景考虑直接上 DRF（见 `8.REST框架`）。
