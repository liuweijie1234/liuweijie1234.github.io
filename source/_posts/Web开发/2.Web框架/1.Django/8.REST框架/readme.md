---
title: django rest framework
date: 2022-11-24 15:00:00
tags:
- django rest framework
categories:
- Django
---

## 零、参考

文档（中文）：https://q1mi.github.io/Django-REST-framework-documentation/

官方文档（英文）：https://www.django-rest-framework.org/

[挑战全网最全之django REST framework（DRF）教程](https://blog.csdn.net/litaimin/article/details/122976825)

## 一、什么是 Django Rest Framework？

Django REST framework是一个开源的第三方扩展库，它为Django Web框架提供了一组强大的工具和API，用于快速构建RESTful Web服务。

其主要目的是为开发人员提供一种简单、易于使用且高度可定制的方式来构建Web应用程序的API接口。

相较于传统基于模板的Web应用程序，RESTful Web服务更加灵活，可扩展性更好，并且更适合于现代化的分布式系统。

Django REST framework提供了许多有用的功能，如序列化、视图、认证、权限管理等，这些功能使得创建RESTful API变得非常简单。

优点：

- **简单易用**： Django REST framework的API设计符合RESTful风格，易于理解和使用。
- **高可定制性**：开发人员可以通过重载或自定义各种类和方法，轻松地扩展和修改框架的行为和功能。
- **强大的文档支持**：Django REST framework提供了自动生成API文档的功能，节省了开发人员大量的文档编写时间。
- **可扩展性**：Django REST framework提供了许多插件和额外的功能，可以轻松扩展API的功能和性能。

缺点：

- **学习成本较高**：虽然Django REST framework能够提高Web服务的开发效率，但需要一定的学习成本。
- **运行速度略低**：与其他纯粹基于WSGI的框架相比，Django REST framework的性能略低，尤其是在处理大量数据和高并发请求时。

与主流对比：
Django REST framework与Flask、Tornado等Python Web框架相比，具有更高的可扩展性和更好的API设计规范。
相较于Node.js的Express、Koa等Web框架，Django REST framework提供了更丰富的功能和更强大的文档支持。

总的来说，Django REST framework在Python Web应用程序中是一种非常有竞争力的RESTful API框架。


## 二、安装和配置

### 安装

```bash
pip install django-rest-framework
```

### 配置

添加 rest_framework 应用至 django 

在settings.py 的 INSTALLED_APPS 中添加 rest_framework

```python
INSTALLED_APPS = [
    'rest_framework',
]
```

## 序列化器

序列化器（Serializers）是REST Framework中最核心的部分之一。

序列化器是Django REST framework中用于将Python对象转换为可渲染的格式的组件。

其主要作用是将Python对象转换为JSON、XML等常用格式，以便于前端或其他系统使用。

### 概念

DRF的序列化：就是把后端的 querySet 或 models对象 通过DRF序列化处理，变成前端能识别的数据（json,xml等），通过视图的Response返回json给前端

视图类序列化过程

1）ORM操作得到数据
2）将数据序列化成可以返回给前台的数据
3）返回数据给前台


DRF的反序列化：就是前端的提交的数据(json等)通过DRF的反序列化，进行对数据的校验，之后变成python对象(models对象)保存到数据库

视图类反序列化过程
1）从请求对象中获取前台提交的数据
2）交给序列化类完成反序列化(数据的校验)
3）借助序列化类完成数据入库
4）反馈给前台处理结果

### 种类

在Django REST framework中，序列化器主要分为以下两种：

- **ModelSerializer**：用于快速地创建针对Model实例的序列化器；

- **Serializer**：用于创建自定义序列化器，可以从头开始配置。

### 序列化示例

将数据库模型类转换成字典，并通过视图的Response返回json给前端。

所以我们的关注点是：

- 创建序列化对象，
- 传入待序列化的模型实例 或 QuerySet查询集
- 分页


#### 1.创建序列化器对象

- 务必传入instance，且不传入data，instance为 模型实例 或 querySet查询集


- 若要序列化的 查询集querySet 或对象实例 并不不是单个对象实例，实例化时，必须传入`many=True`

```python
queryset = Book.objects.all()
s = BookSerializer(instance=queryset, many=True)
```


#### 2.data属性获取数据

通过data属性可以获取序列化后的数据

```python
queryset = Book.objects.all()
s = BookSerializer(instance=queryset, many=True)
s.data # 序列化以后的数据
```

#### 3.返回序列化后的数据

通过视图的Response将序列化以后的数据，即：data属性 返回成json字符串
```python
class BookListView(APIView):
    def get(self, request, *args, **kwargs):
            queryset = Book.objects.all()  
            s = BookSerializer(instance=queryset, many=True)
            return Response(s.data, status=status.HTTP_200_OK)
```

#### 4.分页

一般都会搭配drf的分页，这个记录在[分页器](#分页)中。


### 数据序列化为 JSON 或其他格式

序列化器默认将数据序列化为 JSON格式，可以通过设置 media_type 参数来指定其他格式

```python
from rest_framework.renderers import XMLRenderer
from django.http import HttpResponse
from .serializers import MySerializer

def my_view(request):
   data = {'foo': 'bar'}
   serializer = MySerializer(data=data)
   xml_renderer = XMLRenderer()
   content = xml_renderer.render(serializer.data, media_type='application/xml')
   return HttpResponse(content)
```

### 反序列化 示例

反序列化则是将其他格式转换为Python对象

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    foo = serializers.CharField()
    bar = serializers.IntegerField()

data = {
    'foo': 'hello',
    'bar': 123,
}

serializer = MySerializer(data=data)
if serializer.is_valid():
    obj = serializer.save()

```

反序列化可以通过Serializer类的is_valid()方法来实现。如果输入数据有效，则可以通过调用save()方法将数据保存到数据库中。



## 基于函数的写法

### 装饰器 @api_view 用法

`@api_view(http_method_names=['GET'], exclude_from_schema=False)`

exclude_from_schema 参数标记API视图来忽略任何自动生成的视图,

@api_view 装饰器 是 Django REST Framework 提供的一个装饰器，用于将视图函数转换为 API 视图。

@api_view 装饰器 将请求对象传递给被装饰的函数，并返回响应对象。

使用该装饰器时，需要在视图函数上添加该装饰器，并指定 HTTP 请求方法，

- 示例

snippets/views.py

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

snippets/urls.py

```python
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```




## 基于类的写法

### View

```python
import json
from django.core import serializers
from django.http import HttpResponse,JsonResponse
class GoodsListView(View):
    def get(self,request):
        goods=Goods.objects.all()
        json_data=serializers.serialize("json",goods)
        json_data=json.loads(json_data)
        # 或者return HttpResponse(json.dumps(json_data), content_type="application/json")
        return JsonResponse(json_data,safe=False)
```


## APIView (视图基类)

`rest_framework/views.py`

APIView 继承了 django 的 View 父类，APIView 是一个基于类的视图，用于处理HTTP请求并生成HTTP响应。

```python
from django.views.generic import View


class APIView(View):
    # 渲染器
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # 解析器
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES
    # 身份认证类
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    # 流量控制类/频率组件
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
    # 权限检查类/权限组件
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    # 内容协商类
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
    # 元数据类
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    # 版本控制类
    versioning_class = api_settings.DEFAULT_VERSIONING_CLASS

    as_view()

    get_permissions()

    check_permissions()
```
[renderer_classes 渲染组件详解](https://www.jianshu.com/p/cd51baae5594)
[renderer_classes 渲染器详解](https://www.cnblogs.com/zouzou-busy/p/12078129.html)

[parser_classes 解析器详解](https://www.cnblogs.com/zouzou-busy/p/12078097.html)

- 示例

snippets/views.py

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # 视图类序列化过程，就是三步
        # 1）ORM操作得到数据
        snippets = Snippet.objects.all()
        # 2）将数据序列化成可以返回给前台的数据
        serializer = SnippetSerializer(snippets, many=True)
        # 3）返回数据给前台
        return Response(serializer.data)

    def post(self, request, format=None):
        # 视图类反序列化过程
        # 1）从请求对象中获取前台提交的数据
        serializer = SnippetSerializer(data=request.data)
        # 2）交给序列化类完成反序列化(数据的校验)
        if serializer.is_valid():
            # 3）借助序列化类完成数据入库
            serializer.save()
        # 4）反馈给前台处理结果
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

snippets/urls.py:

```python
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

[drf框架 - 认证组件 | 权限组件 | 频率组件](https://www.cnblogs.com/wwbplus/p/11933061.html)

### 方法

#### handle_exception

handle_exception方法是APIView类的一个方法，用于处理异常并生成相应的错误响应。

handle_exception方法的作用是捕获异常并生成适当的错误响应。默认情况下，该方法会返回一个包含错误信息的JSON响应。

```python
def handle_exception(self, exc):
    """
    Handle any exception that occurs, by returning an appropriate response,
    or re-raising the error.
    """
    if isinstance(exc, (exceptions.NotAuthenticated,
                        exceptions.AuthenticationFailed)):
        # WWW-Authenticate header for 401 responses, else coerce to 403
        auth_header = self.get_authenticate_header(self.request)

        if auth_header:
            exc.auth_header = auth_header
        else:
            exc.status_code = status.HTTP_403_FORBIDDEN

    exception_handler = self.get_exception_handler()

    context = self.get_exception_handler_context()
    response = exception_handler(exc, context)

    if response is None:
        self.raise_uncaught_exception(exc)

    response.exception = True
    return response
```

```python
class MyAPIView(APIView):
    def handle_exception(self, exc):
        if isinstance(exc, APIException):
            # 处理APIException或其子类的异常
            return self.response_class(
                data={'error': str(exc)},
                status=exc.status_code
            )
        else:
            # 处理其他异常
            return super().handle_exception(exc)
```

重写父类的handle_exception

```python
class WifimacRetrieveView(generics.RetrieveAPIView):
    """
    GET接口：TreeATE传递SN，查询最新的数据，返回SN和wifi mac
    """
    queryset = Wifimac.objects.all()
    serializer_class = WifimacModelSerializer
    lookup_field = 'sn'
    lookup_url_kwarg = 'sn'

    def handle_exception(self, exc):
        if isinstance(exc, Wifimac.DoesNotExist):
            return Response({'error': f'Wifimac with sn={self.kwargs["sn"]} does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs.get(self.lookup_url_kwarg, '')}
        obj = Wifimac.objects.filter(**filter_kwargs).order_by('-id').first()

        if not obj:
            raise Wifimac.DoesNotExist()

        return obj
```
我们自定义了handle_exception方法来处理异常。
首先，我们检查异常类型是否是APIException或其子类，如果是，则返回一个包含错误信息和对应状态码的JSON响应。如果不是APIException的子类，则调用父类的handle_exception方法来处理异常。

## generics views(通用视图)

如果通用视图不适合你的API的需求，你可以选择使用常规 APIView 类，或重用通用视图使用的mixins和基类来组成你自己的一组可重用的通用视图。

使用方法:

```python
from rest_framework import generics
```

### generics.GenericAPIView

`rest_framework/generics.py`

**提供的关于序列化器使用的属性与方法**

属性：

- queryset: 指定视图所操作的模型查询集。可以通过重写 get_queryset() 方法来自定义查询集。
- serializer_class: 指定视图所使用的序列化器，用于在请求/响应中进行对象的序列化和反序列化。可以通过重写 get_serializer_class() 方法来动态改变序列化器。
- lookup_field: 指定用于查找单个对象的字段名，默认为 'pk'。
- lookup_url_kwarg: 指定用于从 URL 参数中获取查找字段值的名称，默认为 'pk'。
- paginate_by: 指定默认的分页大小，即每页包含多少个对象。可以通过重写 paginate_queryset() 方法来自定义分页逻辑。
- pagination_class: 指定分页器的类。默认为 PageNumberPagination。
- filter_backends: 指定后端过滤器的类列表。可以通过重写 filter_queryset() 来自定义过滤逻辑。
- authentication_classes: 指定身份验证器的类列表。在请求被处理前，会对请求进行身份验证。
- permission_classes: 指定访问权限的类列表。在请求被处理前，会对请求进行权限检查。


方法：

- get_queryset(): 返回该视图所操作的模型查询集。可以通过重写该方法来自定义查询逻辑。
- get_object(): 根据 lookup_field 和 lookup_url_kwarg 查找单个对象，并返回该对象。如果未找到，会抛出 404 异常。可以通过重写该方法来自定义查找逻辑。
- get_serializer(): 返回该视图所使用的序列化器实例。可以通过重写该方法来动态改变序列化器。
- get_serializer_class(): 返回该视图所使用的序列化器类。可以通过重写该方法来动态改变序列化器。
- paginate_queryset(): 对查询集进行分页处理，返回一页结果数据和分页信息。
- filter_queryset(): 对查询集进行过滤处理，返回符合条件的结果数据。
- get_authentication_classes(): 返回身份验证器类列表。可以通过重写该方法来动态改变身份验证器。
- get_permissions(): 返回访问权限类列表。可以通过重写该方法来动态改变访问权限。
- check_permissions(): 检查请求是否有足够的权限访问该视图。
- initial(): 在视图处理请求前执行一些初始化操作。
- handle_exception(): 处理视图中的异常。可以通过重写该方法来自定义异常处理逻辑。


**提供的关于数据库查询的属性与方法**

属性：

- queryset 指明使用的数据查询集

方法：

- get_queryset(self) 

用途：该方法用于获取查询集（QuerySet），即一组符合特定条件的数据库对象。
返回值：返回一个查询集（QuerySet）对象。
示例用法：
```python
from django.views.generic import ListView

class MyListView(ListView):
    model = MyModel

    def get_queryset(self):
        queryset = super().get_queryset()
        # 添加特定条件过滤查询集
        queryset = queryset.filter(some_field='some_value')
        return queryset
```


- get_object(self)

用途：该方法用于获取单个具体的对象。
返回值：返回一个模型实例（Model instance）对象。
示例用法：
```Python
from django.views.generic import DetailView

class MyDetailView(DetailView):
    model = MyModel

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # 对获取的对象进行进一步处理
        obj.some_field = 'updated_value'
        return obj
```

```python

from rest_framework import mixins, views

class GenericAPIView(views.APIView):
    #类属性说明
    #指明使用的数据查询集
    queryset = None
    #指明视图使用的序列化器
    serializer_class = None
    lookup_field = 'pk'
    lookup_url_kwarg = None
    #过滤器
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    #分页器 
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    #类方法说明
    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset
        def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
```

### generics.CreateAPIView

主要用于处理HTTP POST请求，即创建资源。

```python
class CreateAPIView(mixins.CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

[mixins.CreateModelMixin参考](#mixins.CreateModelMixin)
[GenericAPIView参考](#generics.GenericAPIView)

属性和方法：

- queryset：指定可以查询的数据集合，迭代器或查询对象。默认为Model.objects.all()。
- serializer_class：指定用于序列化和反序列化请求和响应数据的序列化器类。必须定义。
- permission_classes：指定用于授权请求的权限类列表。默认为空列表，即允许任何人访问。
- authentication_classes：指定用于身份验证的认证类列表。默认为空列表，即不进行身份验证。
- create(self, request, *args, **kwargs)：实际执行创建操作的方法。

使用CreateAPIView时，需要在派生类中定义queryset和serializer_class属性。然后，在create()方法中使用serializer对象将请求数据序列化为模型对象，并将其保存到数据库。如果出现错误，则抛出ValidationError异常并返回错误响应。


工作流程：

1、用户发送HTTP POST请求到API端点。
2、DRF将请求路由到相应的 CreateAPIView 视图。
3、DRF使用serializer_class属性初始化一个序列化器对象，并将请求数据传递给该对象。
4、序列化器验证请求数据，并将其转换为模型实例。
5、视图将模型实例保存到数据库，并返回创建成功的响应。
6、如果出现错误，DRF将抛出ValidationError异常，并返回错误响应。

### generics.ListAPIView

```python
class ListAPIView(mixins.ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
```
[GenericAPIView参考](#generics.GenericAPIView)


### generics.RetrieveAPIView

RetrieveAPIView是用于检索单个模型实例的通用视图。它通常用于查看单个对象的详细信息。

```python
class RetrieveAPIView(mixins.RetrieveModelMixin,
                      GenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
```

[mixins.RetrieveModelMixin 参考](#mixins.RetrieveModelMixin)

[GenericAPIView参考](#generics.GenericAPIView)

工作流程：

当用户发送GET请求时，
get()方法会调用retrieve()方法，
retrieve()方法会使用 get_object() 方法找到要检索的对象，
然后使用get_serializer()方法序列化该对象并返回。

这个过程的上下文由get_serializer_context()方法提供。

一般重写get_object()方法 





### generics.DestroyAPIView

generics.DestroyAPIView 是 Django REST Framework 中的一个类视图，用于处理 HTTP DELETE 请求。

```python
class DestroyAPIView(mixins.DestroyModelMixin,
                     GenericAPIView):
    """
    Concrete view for deleting a model instance.
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

工作流程：
1、用户发送 HTTP DELETE 请求到API端点。
2、DRF将请求路由到相应的 DestroyAPIView 视图的delete 方法。
3、获取指定对象（object）：在 delete 方法中，DRF 调用 get_object 方法来获取要删除的对象。默认情况下，`get_object` 方法使用 URL 中提供的 pk 参数来获取对象。您可以通过重写该方法来自定义获取对象的方式。
4、删除指定对象：一旦找到了要删除的对象，DRF 将调用 perform_destroy 方法，该方法负责将对象从数据库中删除。默认情况下，perform_destroy 方法只是调用对象的 delete 方法，从而将其从数据库中删除。但是，如果您需要实现一些其他逻辑（如记录删除操作），则可以在此处覆盖默认行为。
5、返回响应：如果对象已成功删除，则 DRF 将向客户端发送一个 HTTP 204 No Content 响应，表示删除成功。如果未能删除对象，则 DRF 将向客户端发送一个 HTTP 404 Not Found 响应，表示未找到要删除的对象。


### generics.UpdateAPIView

```python
class UpdateAPIView(mixins.UpdateModelMixin,
                    GenericAPIView):
    """
    Concrete view for updating a model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
```

### generics.ListCreateAPIView

```python
class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

### generics.RetrieveUpdateAPIView

```python
class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
```

### generics.RetrieveDestroyAPIView

```python
class RetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             GenericAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

### generics.RetrieveUpdateDestroyAPIView

```python
class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```



### mixins (拓展类)

Mixin扩展类依赖与GenericAPIView，需要继承GenericAPIView。

`rest_framework/mixins.py`

#### mixins.CreateModelMixin

创建视图扩展类，提供`create(request, *args, **kwargs)`方法快速实现创建资源的视图，成功返回201状态码。

如果序列化器对前端发送的数据验证失败，返回400错误。

![](/images/11397602-843f4deb130bcf07.webp)

```python
class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```

#### mixins.ListModelMixin

列表视图扩展类，提供`list(request, *args, **kwargs)`方法快速实现列表视图，返回200状态码。

该Mixin的list方法会对数据进行过滤和分页。

```python
class ListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

#### mixins.RetrieveModelMixin

详情视图扩展类，提供`retrieve(request, *args, **kwargs)`方法，可以快速实现返回一个存在的数据对象。

如果存在，返回200， 否则返回404。

```python
class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

#### mixins.UpdateModelMixin

更新视图扩展类，提供`update(request, *args, **kwargs)`方法，可以快速实现更新一个存在的数据对象。

同时也提供`partial_update(request, *args, **kwargs)`方法，可以实现局部更新。

成功返回200，序列化器校验数据失败时，返回400错误。


```python
class UpdateModelMixin:
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
```


#### mixins.DestroyModelMixin

删除视图扩展类，提供`destroy(request, *args, **kwargs)`方法，可以快速实现删除一个存在的数据对象。

成功返回204，不存在返回404。

```python
class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
```


### 通用视图+Mixins 示例

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

或

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```

## viewsets (视图集)

`from rest_framework import viewsets`

### viewsets.ViewSetMixin

ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等

视图集只在使用as_view()方法的时候，才会将action动作与具体请求方式对应上

例如，创建一个绑定“GET”和“POST”方法的具体视图到“列表”和“创建”操作...

```python
view = MyViewSet.as_view({'get': 'list', 'post': 'create'})
```

list() 提供一组数据
retrieve() 提供单个数据
create() 创建数据
update() 保存数据
destory() 删除数据

方法：

as_view()

initialize_request()

reverse_action()

get_extra_actions()

get_extra_action_url_map()


### viewsets.ViewSet

```python
class ViewSet(ViewSetMixin, views.APIView):
    """
    The base ViewSet class does not provide any actions by default.
    """
    pass
```

- 示例

```python
class BookInfoViewSet(viewsets.ViewSet):

    def list(self, request):
        books = BookInfo.objects.all()
        serializer = BookInfoSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            books = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookInfoSerializer(books)
        return Response(serializer.data)

urlpatterns = [
    url(r'^books/$', BookInfoViewSet.as_view({'get':'list'}),
    url(r'^books/(?P<pk>\d+)/$', BookInfoViewSet.as_view({'get': 'retrieve'})
]

```

### viewsets.GenericViewSet

使用ViewSet通常并不方便，因为list、retrieve、create、update、destory等方法都需要自己编写，
而这些方法与前面讲过的Mixin扩展类提供的方法同名，
所以我们可以通过继承Mixin扩展类来复用这些方法而无需自己编写。
但是Mixin扩展类依赖与GenericAPIView，所以还需要继承GenericAPIView。

GenericViewSet就帮助我们完成了这样的继承工作，继承自GenericAPIView与ViewSetMixin，
在实现了调用`as_view()`时传入字典（如`{‘get’:‘list’}`）的映射处理工作的同时，
还提供了 GenericAPIView 提供的基础方法，可以直接搭配 Mixin扩展类 使用。


```python
class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass
```

- 示例

```python
class GetPostUsersView(GenericViewSet,RetrieveModelMixin,UpdateModelMixin,CreateModelMixin):
    queryset = Users.objects.all()
    serializer_class = Userserializers

    def get(self,request,pk):
        return self.retrieve(request,pk)

    def post(self,request,pk):
        return self.update(request)

    def put(self, request, *args, **kwargs):
        return self.create(request)
```

```python
class UsersViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersModelsSerializer

    def latest(self, request):#自定义接口，与url中的as_view内的接口名称对应
        """
        返回最新的用户信息
        get users/latest/
        """
        users = Users.objects.latest('id')  # latest 倒序取第一个
        serializer = self.get_serializer(users)
        return Response(serializer.data)

    def update_uage(self, request, pk):#自定义接口，与url中的as_view内的接口名称对应
        """
        修改用户的年龄数据
        put users/3/update_uage/
        """
        users = self.get_object()
        users.uage = request.data.get('age')
        users.save()
        serializer = self.get_serializer(users)
        return Response(serializer.data)

# ulrs.py
    url(r'^users/latest/$', views.UsersViewSet.as_view({'get': 'latest'})),#自定义接口
    url(r'^users/(?P<pk>\d+)/age/$', views.UsersViewSet.as_view({'put': 'update_uage'})),#自定义接口
```

### viewsets.ReadOnlyModelViewSet

```python
class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass
```

### viewsets.ModelViewSet

属性：
queryset  指明该视图集在查询数据时使用的查询集
serializer_class 指明该视图在进行序列化和反序列化时使用的序列化器
pagination_class  分页
filter_backends    过滤器
search_fields
permission_classes  
authentication_classes 


方法：

get_serializer_class
get_permissions

create
list
update
destroy
retrieve


```python
class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
```

#### viewsets.ModelViewSet 示例

##### 创建模型操作类

```python
from django.db import models


class Student(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=2555)
    sex = models.BooleanField(verbose_name="性别", default=1)
    age = models.IntegerField(verbose_name="年龄", help_text="年龄不能小于0")
    classmate = models.CharField(verbose_name="班级编号", max_length=5)
    description = models.TextField(verbose_name="个性前面", max_length=1000)

    class Meta:
        db_table = "tb_student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name
```


##### 创建序列化器

```python
from rest_framework import serializers
from stuapi.models import Student


class StudentModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = "__all__"
        fields = ['id', 'name', 'age']
```

序列化器的 Meta中 

model 指明该序列化器出来的数据字段从模型类 Student 参考生成

fields 指明该序列化器包含模型类中的那些字段，`"__all__"`指明包含所有字段

##### 编写视图

在 students 应用的 view.py 中创建视图 StudentModelViewSet ，这是一个视图集合

```python
from rest_framework.viewsets import ModelViewSet
from stuapi.models import Student
from .serializers import StudentModelSerializers


class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializers
```
queryset 指明该视图集在查询数据时使用的查询集
serializer_class 指明该视图在进行序列化和反序列化时使用的序列化器

##### 定义路由

在 students 应用的 urls.py 中定义路由信息

```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("students2", views.StudentModelViewSet, basename="students2")


urlpatterns = [

] + router.urls
```

最后把 students 子应用中的路由文件加载到总路由文件中

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include("stuapi.urls")),
    path('api/', include("students.urls")),
]

```

##### 运行测试

运行django

在浏览器访问网址 http://127.0.0.1:8000/api/ ,可以看到DRF 提供的API Web浏览页面

![](/images/微信截图_20221128105911.png)

##### Django restframework实现批量操作

https://blog.csdn.net/eagle5063/article/details/124479790

#### 视图集中定义附加action动作


在视图集中，除了上述默认的方法动作外，还可以添加自定义动作。

举例：
```python
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

class BookInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def latest(self, request):
        """
        返回最新的图书信息
        """
        book = BookInfo.objects.latest('id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def read(self, request, pk):
        """
        修改图书的阅读量数据
        """
        book = self.get_object()
        book.bread = request.data.get('read')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
url的定义

urlpatterns = [
    url(r'^books/$', views.BookInfoViewSet.as_view({'get': 'list'})),
    url(r'^books/latest/$', views.BookInfoViewSet.as_view({'get': 'latest'})),
    url(r'^books/(?P<pk>\d+)/$', views.BookInfoViewSet.as_view({'get': 'retrieve'})),
    url(r'^books/(?P<pk>\d+)/read/$', views.BookInfoViewSet.as_view({'put': 'read'})),
]
```
##### action属性

在视图集中，我们可以通过action对象属性来获取当前请求视图集时的action动作是哪个。

例如：

```python
def get_serializer_class(self):
    if self.action == 'create':
        return OrderCommitSerializer
    else:
        return OrderDataSerializer
```


## 路由（Routers）

https://q1mi.github.io/Django-REST-framework-documentation/api-guide/routers_zh/

对于视图集ViewSet，我们除了可以自己手动指明请求方式与动作action之间的对应关系外，还可以使用Routers来帮助我们快速实现路由信息。

```python
# 1） 创建router对象，并注册视图集，例如

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'books', BookInfoViewSet, base_name='book')

# 如上述代码会形成的路由如下：
# ^books/$    name: book-list
# ^books/{pk}/$   name: book-detail

#-----------------------------------------------------

# 2）添加路由数据
urlpatterns = [
    ...
    url(r'^', include(router.urls))
]
```

在视图集中，如果想要让Router自动帮助我们为自定义的动作生成路由信息，需要使用rest_framework.decorators.action装饰器。

以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。

action装饰器可以接收两个参数：

- methods: 声明该action对应的请求方式，列表传递
- detail: 声明该action的路径是否与单一资源对应，及是否是xxx//action方法名/
    - True 表示路径格式是xxx//action方法名/
    - False 表示路径格式是xxx/action方法名/

```python
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

class BookInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    # detail为False 表示路径名格式应该为 books/latest/
    @action(methods=['get'], detail=False)
    def latest(self, request):
        """
        返回最新的图书信息
        """
        ...

    # detail为True，表示路径名格式应该为 books/{pk}/read/
    @action(methods=['put'], detail=True)
    def read(self, request, pk):
        """
        修改图书的阅读量数据
        """
        ...

# ---------------------------------------------------
# 由路由器自动为此视图集自定义action方法形成的路由会是如下内容：
# ^books/latest/$    name: book-latest
# ^books/{pk}/read/$  name: book-read

```


## Serializers 序列化器

### 序列化器

#### Serializer

Serializer类是底层序列化类，高级的序列化类的底层功能是由它实现的

针对单表、多表的单查群查和单增单改操作

在使用Serializer类时，反序列化中的插入和更新数据库操作都要自己重写父类的create和update方法

如果默认的序列化输出无法满足我们的需求，那么可以重写 to_representation() 改变序列化的输出

```python
# serializers.py

# 导入DRF的序列化中的serializers类
from rest_framework import serializers
from django.conf import settings
from . import models


# 序列化操作*********************************************************

"""
1）设置序列化字段，字段名与字段类型要与处理的model类属性名对应一只(参与序列化的字段不需要设置条件，因为只是后端提供数据给前端)
2）想要给前端哪些数据，就序列化哪些数据即可，没写的字段不会参与序列化，也就不会提供给前端
3）自定义序列化字段(方法一)，字段类为固定的SerializerMethodField()，字段的值由 get_自定义字段名(self, model_obj) 方法提供，所以你要手动写这个方法，
并返回一个值作为自定义的字段的值（一般值都与参与序列化的model对象(model_obj)有关），自定义的序列化字段默认read_only=True，且不可修改
"""
class UserSerializer(serializers.Serializer):
    # 1）字段名与字段类型要与处理的model类对应
    # 2）不提供的字段，就不参与序列化给前台
    # 3）可以自定义序列化字段，采用方法序列化，方法固定两个参数，第二个参数就是参与序列化的model对象
    #       (注意：不建议自定义字段名与模型类中的字段名重名，由get_自定义字段名方法的返回值提供字段值)
    username = serializers.CharField()
    # sex = serializers.IntegerField()  # sex是模型类中定义为有chioce属性的字段

    # sex = serializers.SerializerMethodField()  # 不建议这样命名
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return obj.get_sex_display()

    # 注：在高级序列化与高级视图类中，drf默认帮我们处理图片等子资源
    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        return '%s%s%s' % (settings.BASE_URL, settings.MEDIA_URL, obj.img)
    

# 反序列化操作**********************************************************

"""
1）系统校验字段与自定义校验字段定义没有区别：字段 = serializers.字段类型(条件)
2）自定义校验字段是不能直接入库的，需要设置入库规则，或将其移除不入库(这类字段就是参与全局校验用的)
3）所有字段都可以设置对应局部钩子进行校验，钩子方法 validate_字段名(self, 字段值value)
    规则：成功直接返回value，失败抛出校验失败信息ValidationError('错误信息')
4）一个序列化类存在一个全局钩子可以对所有字段进行全局校验，钩子方法 validate(self, 所有字段值字典attrs)
    规则：成功直接返回attrs，失败抛出校验失败信息ValidationError({'异常字段', '错误信息'})
5）重写create方法实现增入库，返回入库成功的对象
6）重写update方法实现改入库，返回入库成功的对象
"""
class UserDeSerializer(serializers.Serializer):
    # 系统校验字段
    username = serializers.CharField(min_length=3, max_length=16, error_messages={
        'min_length': '太短',
        'max_length': '太长'
    })
    password = serializers.CharField(min_length=3, max_length=16)

    # 不写，不参与反序列化，写就必须参与反序列化(但可以设置required=False取消必须)
    # required=False的字段，前台不提供，走默认值，提供就一定进行校验；不写前台提不提供都采用默认值
    sex = serializers.BooleanField(required=False)

    # 自定义校验字段：从设置语法与系统字段没有区别，但是这些字段不能参与入库操作，需要在全局钩子中，将其取出
    re_password = serializers.CharField(min_length=3, max_length=16)

    # 局部钩子：
    #   方法就是 validate_校验的字段名(self, 校验的字段数据)
    #   校验规则：成功直接返回value，失败抛出校验失败信息
    def validate_username(self, value):
        if 'g' in value.lower():
            raise serializers.ValidationError('名字中不能有g')
        return value

    # 全局钩子：
    #   方法就是 validate(self, 所有的校验数据)
    #   校验规则：成功直接返回attrs，失败抛出校验失败信息
    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.pop('re_password')
        if password != re_password:
            raise serializers.ValidationError({'re_password': '两次密码不一致'})
        return attrs

    # 在视图类中调用序列化类的save方法完成入库，Serializer类能做的增入库走create方法，改入库走update方法
    # 但Serializer没有提供两个方法的实现体
    def create(self, validated_data):
        return models.User.objects.create(**validated_data)

    # instance要被修改的对象，validated_data代表校验后用来改instance的数据
    def update(self, instance: models.User, validated_data):
        # 用户名不能被修改
        validated_data.pop('username')
        models.User.objects.filter(pk=instance.id).update(**validated_data)
        return instance
```

#### ModelSerializer(重点)

ModelSerializer类能够让你自动创建一个具有模型中相应字段的Serializer类。

ModelSerializer类是高级的序列化类，完成针对单表、多表的单查、群查和单增单改操作序列化和反序列化

在使用ModelSerializer类时，反序列化中的插入和更新数据库操作不需要重写create和update方法

ModelSerializer类和常规的Serializer类一样，不同的是：

- 它根据模型自动生成一组字段。
- 它自动生成序列化器的验证器validators，比如unique_together验证器。
- 它默认简单实现了.create()方法和.update()方法。

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # fields = '__all__'
        fields = ('id', 'account_name', 'users', 'created')
        # exclude = ('users',) 
```
fields 属性显式的设置要序列化的字段
exclude 属性设置成一个从序列化器中排除的字段列表


- 针对单表、多表的单查群查和单增单改操作

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from . import models

class UserV3APIView(APIView):
    
    # 序列化***********************************************************************
    # 单查群查
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            user_obj = models.User.objects.filter(is_delete=False, pk=pk).first()
            if not user_obj:
                return Response({
                    'status': 1,
                    'msg': 'pk error',
                }, status=400)

            user_ser = serializers.UserModelSerializer(user_obj, many=False)
            return Response({
                'status': 0,
                'msg': 'ok',
                'results': user_ser.data
            })
        else:
            user_query = models.User.objects.filter(is_delete=False).all()

            user_ser = serializers.UserModelSerializer(user_query, many=True)

            return Response({
                'status': 0,
                'msg': 'ok',
                'results': user_ser.data
            })
	
    # 反序列化*******************************************************************
    # 单增
    def post(self, request, *args, **kwargs):
        user_ser = serializers.UserModelSerializer(data=request.data)
        if user_ser.is_valid():
            # 入库
            user_obj = user_ser.save()
            return Response({
                'status': 0,
                'msg': 'ok',
                'results': serializers.UserModelSerializer(user_obj).data
            })
        else:
            return Response({
                'status': 1,
                'msg': user_ser.errors,
            })

```


ModelSerializer类的序列化和反序列化都在一起做，所以需要我们根据不同情况对相应的字段进行 序列化还是反序列化还是既需要序列化又需要反序列化 的限制。

```python
# serializers.py

""" ModelSerializer类序列化与反序列化总结
1）序列化类继承ModelSerializer，所以需要在配置类Meta中进行序列化和反序列化的配置
2）model配置：绑定序列化相关的模型表
3）fields配置：采用 插拔式 设置所有参与序列化与反序列化字段
4）extra_kwargs配置（配置系统字段的校验条件、错误信息和该字段的序列化、反序列化选择）：
    划分系统字段为三种：只读，即只序列化(read_only)、只写，即只反序列化(write_only)、可读可写，即序列化和反序列化都有(为空就是可读又可写)
    字段是否必须：required=True/False
    选填字段（模型表中有默认值的字段）：若在extra_kwargs进行配置，一般设置required=False（当然具体情况具体分析），前端不提供则用默认值，前端提供，则用提供的
5）自定义序列化字段：（自定义的序列化字段默认read_only=True，且不可修改）
    第一种(不提倡)：在序列化类中用SerializerMethodField()来实现，若是以此方法自定义了序列化字段，则必须在field中配置该字段，否则报错
    第二种(提倡)：在模型类中用@property来实现，可插拔
6）自定义反序列化字段：
    同Serializer类，且校验条件只能在其定义时字段类的括号中设置，或是在钩子中设置，而在extra_kwargs中对其设置是无效的
    自定义的反序列化字段必须设置 write_only=True
    自定义的反序列化字段最后要pop出来
7）局部钩子，全局钩子都同Serializer类用法一致。（在配置类Meta外部配置钩子）
8）不需要重写create和update方法
"""
class UserModelSerializer(serializers.ModelSerializer):
    # 第一种自定义序列化字段：该字段必须在fields中设置，不推荐这种自定义序列化字段的方式
    # gender = serializers.SerializerMethodField()
    # def get_gender(self, obj):
    #     return obj.get_sex_display()


    # 自定义反序列化字段同Serializer类，且规则只能在此声明中设置，或是在钩子中设置，
    # 在extra_kwargs中对其设置的无效
    # 注：自定义反序列化字段必须设置 write_only
    re_password = serializers.CharField(min_length=3, max_length=16, write_only=True)

    class Meta:
        model = models.User
        # fields采用 插拔式 设置所有参与序列化与反序列化字段
        fields = ('username', 'gender', 'icon', 'password', 'sex', 're_password')
        extra_kwargs = {
            'username': {  # 系统字段，不设置read_only和write_only，则默认都参加
                'min_length': 3,
                'max_length': 10,
                'error_messages': {  # 当在settings文件中配置了国际化文字为中文后，就不需要再自己写中文的错误信息了，在前端会自动转成中文的错误信息
                    'min_length': '太短',
                    'max_length': '太长'
                }
            },
            'gender': {
                'read_only': True,  # 自定义的序列化字段默认就是read_only，且不能修改，但可以省略不写
            },
            'password': {
                'write_only': True,
            },
            'sex': {  # 像sex有默认值的字段，为选填字段（'required': True可以将其变为必填字段）
                'write_only': True,
                # 'required': True
            }
        }


    # 局部全局钩子同Serializer类，是与 Meta类的代码 同缩进的
    def validate_username(self, value):
        if 'g' in value.lower():
            raise serializers.ValidationError('名字中不能有g')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.pop('re_password')
        if password != re_password:
            raise serializers.ValidationError({'re_password': '两次密码不一致'})
        return attrs

    # create和update方法不需要再重写，ModelSerializer类已提供，且支持所有关系下的连表操作

```

```python
# models.py
from django.db import models
class User(models.Model):
    SEX_CHOICES = (
        (0, '女'),
        (1, '男'),
    )

    username = models.CharField(max_length=64, verbose_name='用户名', blank=True, unique=True)
    password = models.CharField(max_length=64, verbose_name='密码')
    sex = models.IntegerField(choices=SEX_CHOICES, default=0, verbose_name='性别')
    img = models.ImageField(upload_to='img', default='img/default.png', verbose_name='头像')
    # 开发中，数据不会直接删除，通过字段控制
    is_delete = models.BooleanField(default=False, verbose_name='是否注销')
    # 数据库数据入库，一般都会记录该数据第一次入库时间，有时候还会记录最后一次更新时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 第二种自定义序列化字段方式（插拔式，提倡使用）
    @property
    def gender(self):
        return self.get_sex_display()

    @property
    def icon(self):
        from django.conf import settings
        return '%s%s%s' % (settings.BASE_URL, settings.MEDIA_URL, self.img)


    class Meta:  # 配置类，给所属类提供配置信息
        db_table = 'old_boy_user'
        verbose_name_plural = '用户表'

    def __str__(self):  # 不要在这里进行连表操作，比如admin页面可能会崩溃
        return self.username
```

##### 指定嵌套序列化

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
        depth = 1
```
depth 选项应该设置一个整数值，表明应该遍历的关联深度，用于生成嵌套关联。


##### 指定明确字段

（增加额外或者重写默认字段）

```python
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Account
```

##### 指定只读字段

添加字段 read_only=True 属性 设置该字段为只读 也可以 使用 Meta 的 read_only_fields 选项。

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
        read_only_fields = ('account_name',)
```

模型中已经设置editable=False的字段和默认就被设置为只读的AutoField字段都不需要添加到read_only_fields选项中。


对于特殊情况，只读字段是模型级别 unique_together 约束的一部分，需要提供read_only=True和default=…关键字参数。

`user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())`

有关UniqueTogetherValidator和CurrentUserDefault类的文档请参考 [验证器文档](#Validators(验证器))

##### 附加关键字参数

extra_kwargs

```python
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
```

#### HyperlinkedModelSerializer

参考 https://q1mi.github.io/Django-REST-framework-documentation/api-guide/serializers_zh/#hyperlinkedmodelserializer

#### ListSerializer

ListSerializer类是群操作序列化类，辅助完成单表、多表的群增和群改操作

#### BaseSerializer

该类实现与Serializer类相同的基本API：

.data - 返回传出的原始数据。
.is_valid() - 反序列化并验证传入的数据。
.validated_data - 返回经过验证后的传入数据。
.errors - 返回验证期间的错误。
.save() - 将验证的数据保留到对象实例中。

它还有可以覆写的四种方法，具体取决于你想要序列化类支持的功能：

.to_representation() - 重写此方法来改变读取操作的序列化结果（输出）。
.to_internal_value() - 重写此方法来改变写入操作的序列化结果。
.create() 和 .update() - 重写其中一个或两个来改变保存实例时的动作。


### 序列化字段

from rest_framework import serializers

<font color="red">字段名 = serializers.字段类型(参数)</font>

#### 布尔字段类型

##### BooleanField

说明：布尔值的表示。

字段构造：`BooleanField()`

对应 django.db.models.fields.BooleanField

##### NullBooleanField

说明：表示布尔值，也接受None为有效值。

字段构造：`NullBooleanField()`

对应 django.db.models.fields.NullBooleanField.

#### 字符串字段类型

##### CharField

说明：表示文本

字段构造：`CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)`

对应 django.db.models.fields.CharField 或 django.db.models.fields.TextField。

| 参数名称 | 作用 |
|--|--|
| max_length | 最大长度 |
| min_lenght | 最小长度 |
| allow_blank | 是否允许为空 |
| trim_whitespace | 是否截断空白字符 |

##### EmailField

说明：表示文本形式，将文本验证为有效的电子邮件地址。

字段构造：`EmailField(max_length=None, min_length=None, allow_blank=False)`

对应 django.db.models.fields.EmailField

##### RegexField

说明：表示文本形式，用于验证给定值是否与某个正则表达式匹配。

字段构造：`RegexField(regex, max_length=None, min_length=None, allow_blank=False)`

对应 django.forms.fields.RegexField

使用Django的django.core.validators.RegexValidator进行验证。

##### SlugField

说明：一个验证输入满足表达式`[a-zA-Z0-9_-]+`的RegexField字段。

字段构造：`SlugField(maxlength=50, min_length=None, allow_blank=False) 正则字段，验证正则模式 [a-zA-Z0-9-]+`

对应 django.db.models.fields.SlugField

##### URLField

说明：一个验证输入满足URL格式的RegexField字段。要求使用以下格式的完全限定网址`http://<host>/<path>`.

字段构造：`URLField(max_length=200, min_length=None, allow_blank=False)`

对应 django.db.models.fields.URLField 

使用Django的 django.core.validators.URLValidator进行验证

##### UUIDField

字段构造：`UUIDFieldUUIDField(format='hex_verbose')`

确保输入为有效UUID字符串的字段。该to_internal_value方法将返回一个uuid.UUID实例。

在输出时，该字段将返回标准连字符格式的字符串，例如：

`"de305d54-75b4-431b-adb2-eb6b9e546013"`

format: 确定uuid值的表示格式
1） 'hex_verbose' 如"5ce0e9a5-5ffa-654b-cee0-1238041fb31a" 
2） 'hex' 如 "5ce0e9a55ffa654bcee01238041fb31a" 
3） 'int' 如: "123456789012312313134124512351145145114" 
4） 'urn' 如: "urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"
所有格式均被to_internal_value接受。

##### FilePathField

说明：一个字段，其选择仅限于文件系统上某个目录中的文件名

字段构造：`FilePathField(path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None, **kwargs)`

对应 django.forms.fields.FilePathField

| 参数名称 | 作用 |
|--|--|
| path | 目录的绝对文件系统路径，应从中选择此FilePathField。 |
| match | FilePathField将用于过滤文件名的正则表达式（作为字符串）。 |
| recursive | 指定是否应包含路径的所有子目录。默认值为False。 |
| allow_files | 指定是否应包含指定位置的文件。默认值为True。这个参数和下面的 allow_folders 必须有一个为 True。 |
| allow_folders | 指定是否应包含指定位置的文件夹。默认值为False。 这个参数和上面的 allow_files 必须有一个为 True。 |


##### IPAddressField

说明：确保输入为有效IPv4或IPv6字符串的字段。

字段构造：`IPAddressField(protocol='both', unpack_ipv4=False, **options)`

| 参数名称 | 作用 |
|--|--|
| protocol | 将有效输入限制为指定的协议。接受的值是“两个”（默认），“ IPv4”或“ IPv6”。匹配不区分大小写。|
| unpack_ipv4 | 解压缩IPv4映射的地址，如:: ffff：192.0.2.1。如果启用此选项，则该地址将解压缩为192.0.2.1。默认设置为禁用。只能在协议设置为“ both”时使用。|

#### 数字字段类型

##### IntegerField

说明：表示整数

字段构造：`IntegerField(max_value=None, min_value=None)`

| 参数名称 | 作用 |
|--|--|
| max_value | 最小值 |
| min_value | 最大值 |


对应：
django.db.models.fields.IntegerField,
django.db.models.fields.SmallIntegerField,
django.db.models.fields.PositiveIntegerField,
django.db.models.fields.PositiveSmallIntegerField

##### FloatField

说明：表示浮点

字段构造：`FloatField(max_value=None, min_value=None)`

对应 django.db.models.fields.FloatField

##### DecimalField

说明：表示十进制形式，在Python中由Decimal实例表示。

字段构造：`DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None)`

| 参数名称 | 作用 |
|--|--|
| max_digits | 最大位数 
| decimal_places | 小数点位置
| coerce_to_string | 如果表示形式应该返回字符串值就设置为True, 或者应该返回Decimal对象的话就设置为 False。除非覆盖，否则默认为设置中COERCE_DECIMAL_TO_STRING设置键相同值的True值。 如果Decimal对象由序列化程序返回，则最终输出格式将由渲染器确定。请注意，设置localize会将值强制设为True。|
| max_value | 验证提供的数字不大于此值。|
| min_value | 验证提供的数字不小于此值。|
| localize | 设置为True启用以基于当前语言环境本地化输入和输出。这也将迫使coerce_to_string到True。默认为False。请注意，如果你USE_L10N=True在设置文件中进行了设置，则会启用数据格式设置。|
| rounding | 设置取值到配置精度的舍入模式。有效值是[decimal 模块的舍入模式][python-decimal-rounding-modes]。默认是None。|

使用示例：

要验证最大为999且分辨率为2位小数的数字，请使用：
```python
serializers.DecimalField(max_digits=5, decimal_places=2)
```

并使用十进制小数位数来验证小于十亿的数字：
```python
serializers.DecimalField(max_digits=19, decimal_places=10)
```

#### 日期时间字段类型

##### DateTimeField

说明：表示日期和时间。

字段构造：`DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None)`

对应 django.db.models.fields.DateTimeField.

| 参数名称 | 作用 |
|--|--|
| format | 代表输出格式的字符串。如果未指定，则默认为与DATETIME_FORMAT设置键相同的值，'iso-8601'除非设置，否则为默认值。设置为格式字符串表示to_representation应将返回值强制为字符串输出。格式字符串如下所述。将此值设置为None表示应由to_representation返回Python datetime对象。在这种情况下，日期时间编码将由渲染器确定。|
| input_formats | 表示可用于解析日期的输入格式的字符串列表。如果未指定，DATETIME_INPUT_FORMATS将使用该设置，默认为['iso-8601']。|
| default_timezone | 一个pytz.timezone表示的时区。如果没有指定，并且USE_TZ设置打开，这个参数的默认值是[当前时区][django-current-timezone]。如果USE_TZ没有打开，会使用原始的日期对象。|

##### DateField

说明：表示日期

字段构造：`DateField(format=api_settings.DATE_FORMAT, input_formats=None)`

对应 django.db.models.fields.DateField


##### TimeField

说明：表示时间

字段构造：`TimeField(format=api_settings.TIME_FORMAT, input_formats=None)`

对应 django.db.models.fields.TimeField

##### DurationField

说明：表示时间间隔

字段构造：`DurationField()`

对应 django.db.models.fields.DurationField

- max_value 验证提供的间隔不大于这个值。
- min_value 验证提供的间隔不小于这个值。

#### 选择字段类型

##### ChoiceField

说明：可以接受有限选择集中的值的字段。

字段构造：`ChoiceField(choices)`

choices与Django的用法相同

##### MultipleChoiceField

说明：一个可以接受一组零个，一个或多个值的字段，这些值是从一组有限的选择中选择的。接受一个强制性参数。to_internal_value返回set包含所选值的

字段构造：`MultipleChoiceField(choices)`


#### 文件上传字段

##### FileField

说明：表示文件。执行Django的标准FileField验证。

字段构造：`FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

对应 django.forms.fields.FileField.

- max_length - 指定文件名的最大长度。
- allow_empty_file - 指定是否允许空文件。
- use_url - 如果设置为True则URL字符串值将用于输出表示。如果设置为False则文件名字符串值将用于输出表示。默认为UPLOADED_FILES_USE_URL设置键的值，除非另有设置，否则为默认值True。


##### ImageField

说明：表示图片。 验证上传的文件内容是否与已知图像格式匹配。

字段构造：`ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

对应 django.forms.fields.ImageField.

需要安装Pillow包或PIL包。推荐使用Pillow包，因为PIL包已经不积极维护。

#### 复合字段

##### ListField

说明：验证对象列表的字段类。

字段构造：`ListField(child=, min_length=None, max_length=None)`

- child - 应该用于验证列表中对象的字段实例。如果未提供此参数，则将不验证列表中的对象。
- min_length - 验证列表中包含的元素不少于此数量。
- max_length - 验证列表中所包含的元素数量不超过此数量。

例如，要验证整数列表，可以使用如下所示的内容：

```python
scores = serializers.ListField(
   child=serializers.IntegerField(min_value=0, max_value=100)
)
```

ListField类还支持声明式样式，该样式允许你编写可重用的列表字段类。

```python
class StringListField(serializers.ListField):
    child = serializers.CharField()
```
现在，我们可以在整个应用程序中重用自定义的StringListField类，而不必为其提供child参数


##### DictField

说明：一个验证对象字典的字段类。 DictField 中的key都总是假定为字符串值

字段构造：`DictField(child=)`


##### JSONField

说明：一个字段类，用于验证传入的数据结构是否包含有效的JSON原语。在其备用二进制模式下，它将表示并验证JSON编码的二进制字符串。

字段构造：`JSONField(binary)`

- binary - 如果设置为True则该字段将输出并验证JSON编码的字符串，而不是原始数据结构。默认为False。
- encoder - 使用这个编码器序列化输入的对象。默认是None。

#### 杂项字段

##### ReadOnlyField

说明：一个字段类，仅返回该字段的值而无需修改。

ModelSerializer当包含与属性而不是模型字段相关的字段名称时，默认情况下使用此字段。

字段构造：`ReadOnlyField()`

例如，如果has_expired是Account模型的属性，则以下序列化器将自动将其生成为ReadOnlyField：
```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'has_expired')
```

##### HiddenField

说明：一个字段类，它不基于用户输入获取值，而是从默认值或可调用对象获取其值。

字段构造：`HiddenField()`

例如，要包括一个始终提供当前时间的字段作为序列化程序验证数据的一部分，则可以使用以下内容：
```python
modified = serializers.HiddenField(default=timezone.now)
```

HiddenField通常只有在你需要基于某些预先提供的字段值来运行某些验证，而又不想将所有这些字段公开给最终用户时，才需要使用该类。

有关 HiddenField 的更多示例，请参照[validators](#Validators(验证器)) 文档。


##### ModelField


说明：可以绑定到任意模型字段的通用字段。 ModelField类将序列化/反序列化任务委托给与其关联的model字段。 此字段可用于为自定义模型字段创建序列化程序字段，而不必创建新的自定义序列化程序字段。

该字段用于ModelSerializer对应于自定义模型字段类。

字段构造：`ModelField(model_field=<Django ModelField instance>)`

ModelField一般用于内部使用，但如果需要的话可以通过你的API使用。

为了正确地实例化ModelField，必须传递一个附加到实例化模型的字段。

例如：`ModelField(model_field=MyModel()._meta.get_field('custom_field'))`。


##### SerializerMethodField

说明：这是一个只读字段。它通过在附加的序列化器类上调用一个方法来获取其值。它可以用于将任何类型的数据添加到对象的序列化表示中。

字段构造：`SerializerMethodField(method_name=None)`

- method_name - 要调用的序列化程序上的方法的名称。如果未包括，则默认为`get_<field_name>`。

值由固定的命名规范方法 `get_字段名` 的返回值提供

method_name参数引用的序列化程序方法应接受单个参数（除了之外self），该参数是要序列化的对象。它应该返回要包含在对象的序列化表示中的任何内容

```python
class BluetoothSerializer(serializers.ModelSerializer):

    plant = serializers.SerializerMethodField()

    # 自定义方法
    def get_plant(self, obj):
        return obj.get_plant_display()

    class Meta:
        model = Bluetooth
        # fields = "__all__"
        fields = ('sn', 'password', 'mac', 'barcode', 'create_time', 'plant')
```

##### 自定义字段

如果要创建自定义字段，则需要继承Field类，然后重写.to_representation()和.to_internal_value()方法之一或二者。
这两种方法用于在初始数据类型和原始的可序列化数据类型之间进行转换。
基本数据类型通常是任何数字，字符串，布尔，date/time/datetime或None。

它们也可以是仅包含其他原始对象的任何列表或字典之类的对象。

根据您使用的渲染器，可能支持其他类型。

to_representation() 调用该方法可将初始数据类型转换为原始的可序列化数据类型。

to_internal_value() 调用该方法可将原始数据类型恢复为其内部python表示形式。如果数据无效，则此方法应抛出一个 serializers.ValidationError。

###### 基础自定义字段

一个序列化代表RGB颜色值的类

```python
class Color:
    """
    A color represented in the RGB colorspace.
    """
    def __init__(self, red, green, blue):
        assert(red >= 0 and green >= 0 and blue >= 0)
        assert(red < 256 and green < 256 and blue < 256)
        self.red, self.green, self.blue = red, green, blue

class ColorField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, value):
        return "rgb(%d, %d, %d)" % (value.red, value.green, value.blue)

    def to_internal_value(self, data):
        data = data.strip('rgb(').rstrip(')')
        red, green, blue = [int(col) for col in data.split(',')]
        return Color(red, green, blue)
```
默认情况下，字段值被视为映射到对象上的属性。如果需要自定义如何访问和设置字段值，则需要覆盖`.get_attribute()`和/或`.get_value()。`


```python
class ClassNameField(serializers.Field):
    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance

    def to_representation(self, value):
        """
        Serialize the value's class name.
        """
        return value.__class__.__name__
```


###### 抛出验证异常

我们上面的`ColorField`类目前不执行任何数据验证。 为了指示无效数据，我们应该引发一个`serializers.ValidationError`，如下所示：
```python
def to_internal_value(self, data):
    if not isinstance(data, str):
        msg = 'Incorrect type. Expected a string, but got %s'
        raise ValidationError(msg % type(data).__name__)

    if not re.match(r'^rgb\([0-9]+,[0-9]+,[0-9]+\)$', data):
        raise ValidationError('Incorrect format. Expected `rgb(#,#,#)`.')

    data = data.strip('rgb(').rstrip(')')
    red, green, blue = [int(col) for col in data.split(',')]

    if any([col > 255 or col < 0 for col in (red, green, blue)]):
        raise ValidationError('Value out of range. Must be between 0 and 255.')

    return Color(red, green, blue)
```
`.fail()`方法是引发的快捷方式`ValidationError`，它从`error_messages`字典中获取消息字符串。例如：

```python
default_error_messages = {
    'incorrect_type': 'Incorrect type. Expected a string, but got {input_type}',
    'incorrect_format': 'Incorrect format. Expected `rgb(#,#,#)`.',
    'out_of_range': 'Value out of range. Must be between 0 and 255.'
}

def to_internal_value(self, data):
    if not isinstance(data, str):
        self.fail('incorrect_type', input_type=type(data).__name__)

    if not re.match(r'^rgb\([0-9]+,[0-9]+,[0-9]+\)$', data):
        self.fail('incorrect_format')

    data = data.strip('rgb(').rstrip(')')
    red, green, blue = [int(col) for col in data.split(',')]

    if any([col > 255 or col < 0 for col in (red, green, blue)]):
        self.fail('out_of_range')

    return Color(red, green, blue)
```

###### 使用source='*'

这里我们来看一个例子，一个 平面 的DataPoint模型，有x_coordinate和y_coordinate字段。

```python
class DataPoint(models.Model):
    label = models.CharField(max_length=50)
    x_coordinate = models.SmallIntegerField()
    y_coordinate = models.SmallIntegerField()
```
使用自定义字段和source='*'，我们可以生成坐标对的嵌套表示：
```python
class CoordinateField(serializers.Field):

    def to_representation(self, value):
        ret = {
            "x": value.x_coordinate,
            "y": value.y_coordinate
        }
        return ret

    def to_internal_value(self, data):
        ret = {
            "x_coordinate": data["x"],
            "y_coordinate": data["y"],
        }
        return ret


class DataPointSerializer(serializers.ModelSerializer):
    coordinates = CoordinateField(source='*')

    class Meta:
        model = DataPoint
        fields = ['label', 'coordinates']
```

注意这个例子不能进行验证。部分因为这个原因，在真实的项目中，使用有source='*'参数的序列化器和两个有自己的source参数指向关联的字段的IntegerField实例来表示嵌套坐标更好。

- to_representation 传入整个DataPoint对象，必须将其映射到所需的输出。

```python
>>> instance = DataPoint(label='Example', x_coordinate=1, y_coordinate=2)
>>> out_serializer = DataPointSerializer(instance)
>>> out_serializer.data
ReturnDict([('label', 'Example'), ('coordinates', {'x': 1, 'y': 2})])
```

- 除非我们的字段时只读的，to_internal_value必须映射回适合更新目标对象的字典。使用source='*'，to_internal_value的返回可以更新验证的数据字典，而不是单个键。

```python
>>> data = {
...     "label": "Second Example",
...     "coordinates": {
...         "x": 3,
...         "y": 4,
...     }
... }
>>> in_serializer = DataPointSerializer(data=data)
>>> in_serializer.is_valid()
True
>>> in_serializer.validated_data
OrderedDict([('label', 'Second Example'),
             ('y_coordinate', 4),
             ('x_coordinate', 3)])
```

为了完整性，让我们再次做同样的事情，但使用上面建议的嵌套序列化程序方法：
```python
class NestedCoordinateSerializer(serializers.Serializer):
    x = serializers.IntegerField(source='x_coordinate')
    y = serializers.IntegerField(source='y_coordinate')


class DataPointSerializer(serializers.ModelSerializer):
    coordinates = NestedCoordinateSerializer(source='*')

    class Meta:
        model = DataPoint
        fields = ['label', 'coordinates']
```

这里在IntegerField声明中处理目标和源属性对(x和x_coherate，y和y_cocoate)之间的映射。它就是接受`source=‘*’`的 NestedConsulateSerializer

我们的新DataPointSerializer与自定义字段方法行为相同。

序列化：
```python
>>> out_serializer.data
ReturnDict([('label', 'testing'),
            ('coordinates', OrderedDict([('x', 1), ('y', 2)]))])
```
反序列化：
```python
>>> in_serializer = DataPointSerializer(data=data)
>>> in_serializer.is_valid()
True
>>> in_serializer.validated_data
OrderedDict([('label', 'still testing'),
             ('x_coordinate', 3),
             ('y_coordinate', 4)])
```
我们同样有内置的验证器：
```python
>>> invalid_data = {
...     "label": "still testing",
...     "coordinates": {
...         "x": 'a',
...         "y": 'b',
...     }
... }
>>> invalid_serializer = DataPointSerializer(data=invalid_data)
>>> invalid_serializer.is_valid()
False
>>> invalid_serializer.errors
ReturnDict([('coordinates',
             {'x': ['A valid integer is required.'],
              'y': ['A valid integer is required.']})])
```
因此，嵌套序列化程序方法将是第一个尝试的方法。当嵌套的序列化程序变得不可行或过于复杂时，您可以使用自定义字段方法。


### 序列化关系字段

关系字段用于表示模型关系


#### API参考

为了解释各种类型的关系字段，我们将在示例中使用几个简单的模型。我们的模型将用于音乐专辑，以及每张专辑中列出的曲目。
```python
class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
```

#### StringRelatedField

类型：字符串相关字段

说明：可用于使用其`__str__`方法来表示关系的目标。

该字段是只读的。

参数：

many- 如果应用于一对多关系，则应将此参数设置为True。

示例：

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

```json
//序列化输出
{
    'album_name': 'Things We Lost In The Fire',
    'artist': 'Low',
    'tracks': [
        '1: Sunflower',
        '2: Whitetail',
        '3: Dinosaur Act',
        ...
    ]
}
```

#### PrimaryKeyRelatedField

类型：主键相关字段

说明：可用于使用其主键来表示关系的目标。

默认情况下，此字段是可读写的，但您可以使用`read_only`标志更改此行为。

参数：

- queryset- 验证字段输入时用于模型实例查找的查询集。关系必须显式设置查询集，或设置`read_only=True`.
- many- 如果应用于一对多关系，则应将此参数设置为True。
- allow_null- 如果设置为True，该字段将接受None可为空关系的值或空字符串。默认为False.
- pk_field- 设置一个字段来控制主键值的序列化/反序列化。例如，`pk_field=UUIDField(format='hex')`将 UUID 主键序列化为其紧凑的十六进制表示形式。

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

```json
//序列化输出
{
    'album_name': 'Undun',
    'artist': 'The Roots',
    'tracks': [
        89,
        90,
        91,
        ...
    ]
}
```

[PrimaryKeyRelatedField的使用](https://www.cnblogs.com/zonghan/p/16213252.html)

#### HyperlinkedRelatedField

类型：超链接相关字段

说明：可用于使用超链接表示关系的目标。

默认情况下，此字段是可读写的，但您可以使用`read_only`标志更改此行为。

参数：

- view_name- 应该用作关系目标的视图名称。如果您使用的是标准路由器类，这将是一个格式为`<modelname>-detail`. **必填项**。
- queryset- 验证字段输入时用于模型实例查找的查询集。关系必须显式设置查询集，或设置read_only=True.
- many- 如果应用于一对多关系，则应将此参数设置为True。
- allow_null- 如果设置为True，该字段将接受None可为空关系的值或空字符串。默认为False.
- lookup_field- 应该用于查找的目标上的字段。应对应于引用视图上的 URL 关键字参数。默认为'pk'。
- lookup_url_kwarg- 与查找字段对应的 URL conf 中定义的关键字参数的名称。默认使用与 相同的值lookup_field。
- format- 如果使用格式后缀，超链接字段将对目标使用相同的格式后缀，除非使用format参数覆盖。


```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='track-detail'
    )

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

```json
//序列化输出
{
    'album_name': 'Graceland',
    'artist': 'Paul Simon',
    'tracks': [
        'http://www.example.com/api/tracks/45/',
        'http://www.example.com/api/tracks/46/',
        'http://www.example.com/api/tracks/47/',
        ...
    ]
}
```

> 注意：此字段专为映射到接受单个 URL 关键字参数的 URL 的对象而设计，如使用lookup_field和lookup_url_kwarg参数设置的那样。
> 
> 这适用于包含单个主键或 slug 参数作为 URL 一部分的 URL。
> 
> 如果您需要更复杂的超链接表示，您需要自定义该字段，如下面的[自定义超链接字段](#自定义超链接字段)部分所述。

#### SlugRelatedField

类型：Slug相关字段

说明：可以使用目标上的字段来表示关系的目标。

默认情况下，此字段是可读写的，但您可以使用read_only标志更改此行为。

当SlugRelatedField用作读写字段时，您通常会希望确保 slug 字段对应于带有unique=True.

参数：

- slug_field- 目标上应该用来表示它的字段。这应该是唯一标识任何给定实例的字段。例如，username。 必需的
- queryset- 验证字段输入时用于模型实例查找的查询集。关系必须显式设置查询集，或设置read_only=True.
- many- 如果应用于一对多关系，则应将此参数设置为True。
- allow_null- 如果设置为True，该字段将接受None可为空关系的值或空字符串。默认为False.

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
     )

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

```json
//序列化输出
{
    'album_name': 'Dear John',
    'artist': 'Loney Dear',
    'tracks': [
        'Airport Surroundings',
        'Everything Turns to You',
        'I Was Only Going Out',
        ...
    ]
}
```

#### HyperlinkedIdentityField

类型：超链接身份字段

说明：该字段可以作为身份关系应用，例如'url' HyperlinkedModelSerializer 上的字段。它也可以用于对象的属性。

该字段始终是只读的。

参数：

- view_name- 应该用作关系目标的视图名称。如果您使用的是标准路由器类，这将是一个格式为`<model_name>-detail`. **必填项**。
- lookup_field- 应该用于查找的目标上的字段。应对应于引用视图上的 URL 关键字参数。默认为'pk'。
- lookup_url_kwarg- 与查找字段对应的 URL conf 中定义的关键字参数的名称。默认使用与 相同的值lookup_field。
- format- 如果使用格式后缀，超链接字段将对目标使用相同的格式后缀，除非使用format参数覆盖。

```python
class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'track_listing']
```

```json
//序列化输出
{
    'album_name': 'The Eraser',
    'artist': 'Thom Yorke',
    'track_listing': 'http://www.example.com/api/track_list/12/',
}
```
#### 自定义关系字段

参考 https://q1mi.github.io/Django-REST-framework-documentation/api-guide/relations/#custom-relational-fields

#### 自定义超链接字段

参考 https://q1mi.github.io/Django-REST-framework-documentation/api-guide/relations/#custom-hyperlinked-fields

### 嵌套关系

与之前讨论的对另一个实体的引用相反，被引用的实体也可以嵌入或嵌套 在引用它的对象的表示中。这种嵌套关系可以通过使用序列化器作为字段来表达。

如果该字段用于表示一对多关系，则应将many=True标志添加到序列化程序字段。

#### 只读的嵌套序列化
```python
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

将序列化为这样的嵌套表示：

```python
>>> album = Album.objects.create(album_name="The Grey Album", artist='Danger Mouse')
>>> Track.objects.create(album=album, order=1, title='Public Service Announcement', duration=245)
<Track: Track object>
>>> Track.objects.create(album=album, order=2, title='What More Can I Say', duration=264)
<Track: Track object>
>>> Track.objects.create(album=album, order=3, title='Encore', duration=159)
<Track: Track object>
>>> serializer = AlbumSerializer(instance=album)
>>> serializer.data
{
    'album_name': 'The Grey Album',
    'artist': 'Danger Mouse',
    'tracks': [
        {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
        {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
        {'order': 3, 'title': 'Encore', 'duration': 159},
        ...
    ],
}
```
#### 可写的嵌套序列化

默认情况下，嵌套序列化程序是只读的。如果您想支持对嵌套序列化程序字段的写入操作，您需要创建create()和/或update()方法以明确指定应如何保存子关系。

```python
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album

>>> data = {
    'album_name': 'The Grey Album',
    'artist': 'Danger Mouse',
    'tracks': [
        {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
        {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
        {'order': 3, 'title': 'Encore', 'duration': 159},
    ],
}
>>> serializer = AlbumSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.save()
<Album: Album object>
```

### 字段参数

| 参数名称 | 说明 |
|--|--|
| read_only | True 时表明字段仅用于**序列化输出**（只读字段），包含在API输出中，不包含在创建或更新的操作， 默认是False |
| Write_only | True 时表明该字段仅用于**反序列化输入**，不用做序列化的输出，也就是只用于数据校验， 默认是False |
| required | 表明该字段在**反序列化**时必须输入，默认True |
| default | **反序列化**时使用的默认值，部分更新操作不会接受default的值 |
| allow_null | 表明该字段是否允许传入None，默认False |
| validators | 该字段使用的验证器 |
| error_messages | 包含错误编号与错误信息的字典 |
| label | 用于HTML展示API页面时，显示的字段名称 |
| help_text | 	用于HTML展示API页面时，显示的字段帮助提示信息 |

- source(适用于自定义字段)

source="数据库字段名"， 定义字段名称必须喝数据库中字段名称相同

source="get_数据库字段名_display"

source=外键字段名.字段名


### 配置元类Meta

```python
class Meta:
    model = User
    fields = ('email', 'username', 'password')
```

- model 指明模型类对象，来指明此序列化类是为哪张表提供序列化服务。
- fields 指明参与该序列化器的字段
    - `fields = "__all__"`  # 指明 数据库表所有字段 + 自定义的所有字段 进行序列化或反序列化
    - （具体参与序列化还是反序列化，还得看字段的write_only 和 read_only 属性）
- exclude = ['id', 'password'] # 排除掉具体某些字段
- read_only_fields 指定多个字段为只读
    - 希望将多个字段指定为只读，而不是显式地为每个字段添加read_only=True属性
    - read_only_fields = ["id"]
    - 只读字段只做序列化,不做反序列化
    - 模型中已经设置 editable=False 的字段 和 默认就被设置为只读的 AutoField 字段都不需要添加到 read_only_fields 选项中。
- extra_kwargs 给隐式字段添加额外参数
    - 使用 extra_kwargs 选项在字段上指定任意附加关键字参数
    - 一般给默认字段添加，这样就不需要在序列化器中显式得再声明一遍该字段。

比如模型类中的password最大长度是150,想修改到20，直接可以通过extra_kwargs为password字段添加参数
```python
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                },
            'user_type': {
                'source': 'get_user_type_display'
                }
            }
        }
```
如果字段已在序列化程序类中显式声明，则extra_kwargs中此字段将被忽略。

注意只是为此字段添加参数，不会改变字段的类型，如果想改变字段的类型，请显示的定义字段来达到覆盖

当然，如果你你不嫌麻烦，可以通过显示定义的方式重新覆盖。

- depth 外键关系序列化
    - 当Meta写入了depth 将自动序列化外键的连表 depth 代表找嵌套关系的第几层。 depth = 1表示找1层关系
    - 注意：当序列化类META定义了depth时，这个序列化类中引用字段（外键）则自动变为只读。
    - 一般数据库表由于性能原因不使用外键，而且定义depth后，外键自动变为只读，我们一般不使用depth
```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book        
        fields = "__all__"
        depth = 1  # 建议1或2或3
```

### Validators(验证器)

#### serializer.is_valid()


serializer.is_valid() 是在 Django 中用于验证序列化器数据的方法。

它的作用是检查传入的数据是否符合序列化器的定义规则，验证数据的有效性，并返回一个布尔值表示数据是否有效。

is_valid() 方法可以接收一个可选的参数 raise_exception，默认为 False。

当 raise_exception 参数为 True 时，如果数据无效，则会引发异常 ValidationError，可以通过捕获该异常来处理验证错误。
当 raise_exception 参数为 False 时，方法将仅返回验证结果，而不会引发异常。

```python
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class MySerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()

data = {'name': 'John', 'age': 25}
serializer = MySerializer(data=data)

try:
    serializer.is_valid(raise_exception=True)  # 验证数据并引发异常
    print('数据有效')
except ValidationError as e:
    print('数据无效:', e)

# 或者使用非异常方式处理验证结果
is_valid = serializer.is_valid()
if is_valid:
    print('数据有效')
else:
    print('数据无效:', serializer.errors)
```


#### validators模块

自带的validators模块中的校验函数，根据不同的场景选择使⽤不同的校验函数

##### 唯一检验器 UniqueValidator 

用来强制执行模型字段的`unqieru=True`约束。

- queryset **必要参数** - 这是应该对其强制执行唯一性检查的结果集。
- message - 当验证器失败时应该使用的错误信息。
- lookup - 用于查找现存的实例中有验证值的查询。默认是'exact'。

验证器应该使用在序列化器类中

```python

from rest_framework.validators import UniqueValidator

extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                },
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此用户名已注册')],
​
            },
        }
```

###### 条件验证器 UniqueTogether 

用来强制执行模型实例的unqieru=True约束。

- queryset **必要参数** - 这是应该对其强制执行唯一性检查的结果集。
- fields **必要参数** - 一个需要联合唯一字段的列表或者元组。他们必须是序列化类中的字段。
- message - 当验证器失败时应该使用的错误信息。

验证器应该使用在序列化器类中

```python
from rest_framework.validators import UniqueTogetherValidator

class ExampleSerializer(serializers.Serializer):
    # ...
    class Meta:
        # ToDo项目属于一个父列表，并且被一个定义的`position`字段排序。
        # 同一个列表中不能共有同一个位置。
        validators = [
            UniqueTogetherValidator(
                queryset=ToDoItem.objects.all(),
                fields=['list', 'position']
            )
        ]
```
> 提示: UniqueTogetherValidator类始终施加一个隐式约束，即它应用的所有字段始终被视为必需的。具有default值的字段是个例外，因为即使在用户输入中省略了这些字段，它们也总是提供一个默认值。

###### 时间唯一验证器

UniqueForDateValidator
UniqueForMonthValidator
UniqueForYearValidator

用来对模型实例强制执行unique_for_date，unique_for_month和unique_for_year约束

- queryset **必要参数** - 这是应该对其强制执行唯一性检查的结果集。
- field **必要参数** - 将根据其验证给定日期范围中的唯一性的字段名。这必须是序列化类中的字段。
- date_field **必要参数** - 将用于确定唯一性约束的日期范围的字段名称这必须是序列化类中的字段。
- message - 当验证器失败时应该使用的错误信息。

验证器应该使用在序列化器类中

```python
from rest_framework.validators import UniqueForYearValidator

class ExampleSerializer(serializers.Serializer):
    # ...
    class Meta:
        # 博客发布应该有一个当前年份唯一的别名
        validators = [
            UniqueForYearValidator(
                queryset=BlogPostItem.objects.all(),
                field='slug',
                date_field='published'
            )
        ]
```
#### 高级字段默认值

- 使用 `HiddenField`。这个字段会在`validated_data`中体现，但是不会在序列化器输出时使用。
- 使用设置了`read_only=True`的标准字段，同时包含`default=…`参数。这个字段将会在序列化器输出中使用，但是不会被用户直接设置。

##### CurrentUserDefault

当前用户默认，用来代表当前用户的默认类。为了使用他，在实例化序列化器时，'request'必须包含在上下文(context)的字典中

```python
owner = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
```

##### CreateOnlyDefault()

仅创建默认

一个仅在创建操作中设置默认值的默认类。在更新操作中会被省略。

他只接收一个参数，可以是一个默认值或者在创建操作中可调用。

```python
created_at = serializers.DateTimeField(
    default=serializers.CreateOnlyDefault(timezone.now)
)
```

#### 自定义验证器

##### 基于函数


需要在序列化器类以外定义，通常会单独创建一个validators.py文件 从其引入函数

```python
def is_contains_keyword(value):
    if '项目' not in value:
        raise serializers.ValidationError('项目名称中必须得包含“项目”关键字')
def is_not_contain_x(value):
    if'X'in value.upper():
        raise serializers.ValidationError("项⽬名字段name不能包含x的⼤⼩写字符")

...

name = serializers.CharField(max_length=20, validators=[is_contains_keyword, is_not_contain_x])
```

##### 基于类

使用`__call__`方法来些基于类的验证器。基于类的验证器可以让你参数化并且可以重复使用。

```python
class MultipleOf:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value % self.base != 0:
            message = 'This field must be a multiple of %d.' % self.base
            raise serializers.ValidationError(message)
```
- 访问上下文

在一些高级的案例中，你可能希望验证器将序列化器字段作为附加上下文使用。
你可以通过在验证器上设置 `requires_context = True` 属性来实现。
`_call_` 方法将使用 `serializer_field` 或 `serializer` 作为附加参数被调用。

```python
requires_context = True

def __call__(self, value, serializer_field):
    ...
```

#### 局部钩子

自定义校验方法，字段级别的验证器

使用方法：`validate_字段名`

注意事项：
- ⼀定要返回校验之后的值
- 不需要放在validators的列表中就可以⽣效，在序列化器里定义即可

```python
def validate_mobile(self, mobile):
    # 手机号是否注册
    if User.objects.filter(mobile=mobile).count():
        raise serializers.ValidationError("用户已经存在")
    ​
    # 验证手机号是否合法
    if not re.match(settings.REGEX_MOBILE,mobile):
        raise serializers.ValidationError('手机号码非法')
    ​
    # 验证验证码发送频率
    one_minute_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds =0)
    if VerifyCode.objects.filter(add_time__gt=one_minute_ago,mobile=mobile).count():
        raise serializers.ValidationError('请超过60s后再次发送')
    ​
    return mobile
```

#### 全局钩子

自定义多字段校验器方法, 对多字段进行扩展验证的逻辑

使用方法：

方法名固定为validate，形参为attrs，attrs为待校验字段组成的字典

attrs返回一个QueryDict，字段名可以通过字典的方法进行取值，如：attrs['name'] 或者 attrs.get('name')

注意事项：

- 必须返回形参attrs


```python
def validate(self, attrs):
​
    # 写校验逻辑
    # 判断注册时填写的两次密码是否一致
    if attrs.get('password') != attrs.get('passwordConfirm'):
        raise serializers.ValidationError('两次密码不一致')
​
    return attrs  # 全局钩⼦validate最后都要return attrs

```

可以通过修改REST framework全局配置中的NON_FIELD_ERRORS_KEY来控制错误字典中的键名。

```python
REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'validate_errors'
}
```

【数据校验顺序】

1.对每个字段类型，参数进行校验

2.调用局部钩子validate_字段名 进行校验

3.全局钩子validate进行校验

4.使用字段选项中的validators执行外部函数的校验


### 序列化器的使用

在开发REST API的视图中，虽然每个视图具体操作的数据不同，但增、删、改、查的实现流程基本套路化，所以这部分代码也是可以复用简化编写的：

增：校验请求数据 -> 执行反序列化过程 -> 保存数据库 -> 将保存的对象序列化并返回
删：判断要删除的数据是否存在 -> 执行数据库删除
改：判断要修改的数据是否存在 -> 校验请求的数据 -> 执行反序列化过程 -> 保存数据库 -> 将保存的对象序列化并返回
查：查询数据库得到数据库模型对象或querySet -> 将数据序列化并返回


Serializer的构造方法为：
```python
ser = StudentSerializer(instance=None, data=empty, **kwarg)
```

说明：

- 用于**序列化**时，必须将模型类对象或querySet查询集 传入instance参数，且不传入data
- 用于**反序列化**时，必须将被反序列化的字典传入data参数
- 除了instance和data参数外，在构造Serializer对象时，还可通过context参数额外添加数据，如：
```python
serializer = StudentSerializer(account, context={'request': request})
```
通过context参数附加的数据，可以通过Serializer实例的context属性获取，如在create方法中：`self.context['request']`。

使用场景：
在视图类中，可以通过request得到登陆用户request.user，在序列化类中，要完成数据库数据的校验与入库操作，可能会需要知道当前的登录用户，
但序列化类无法访问request对象，在视图类中实例化序列化对象时，可以通过context参数将request对象传递进去

```python
book_ser = BookSerializer(context = {'request': request}, instance = objs, data = new_request_data, partial = True, many = True)
```
在create，update，或validate方法中就可以通过`self.context['request']` 拿到request

#### 反序列化

反序列化即将如json等字符串转换成python对象的过程

我们可以通过视图的request拿到字典格式的前端数据，序列化器可以对其进行校验，并保存到数据库中。

所以我们的关注点是：

- 创建序列化对象 (从请求对象中获取前台提交的数据)
- 调用数据验证 (交给序列化类完成反序列化)
- 对数据进行持久化 (数据入库)，包括：新增create 或者 更新update
- 反馈给前台处理结果


##### 1.创建序列化器对象

1) 创建序列化器对象, 务必传入data

data为字典格式，默认此字典必须包含所有需要反序列化的字段，否则会抛出异常

2) 默认所有的required字段都必须参与反序列化，除非此字段read_only为true

当然如果此字典中还包括了一些无关的字段，序列化器会忽略掉，没有经过后期校验的字段不会出现在validated_data中

```python
s = CreateUserSerializer(data=all_list)
```

3) 如果data传递的字典中没有囊括所有需要反序列化的字段，需要增加参数 `partial=True`（表示部分更新）

如果未传instance，则表示部分添加（前提是，未传字段对应的数据库字段允许未空!!)

如果传了instance，则表示对此模型实例进行部分更新

```python
# 当数据库允许为空，但是序列化器要求必须字段填写的时候，可以使用以下方式避开
serializer = StudentSerializer(data=part_lsit, partial=True)
​
# 更新学生的部分字段信息
updated_server = ServerManager.objects.get(id=request.data['id'])
s = ServerManagerSerializer(instance=updated_server, data=updated_data, partial=True) 
```

注意：在执行保存前，我们都有对数据进行校验，如果我们漏传序列化字段，可能在数据校验那关就不通过
所以要么是真正的部分更新成功，要么会报错，不太会出现漏传却部分更新成功的情况，基本都是我们刻意进行的部分更新。


4) 传递data后，可以通过**序列化器实例的initial_data属性** 获取将要进行验证的数据

##### 2.调用数据验证is_valid()

进行数据持久化之前，必须调用序列化器实例的 `is_valid()` 方法进行数据校验

```python
s = CreateUserSerializer(data=all_list)
s.is_valid()  # 成功返回True, 失败返回False
```

1） 在调用valid()方法以后，序列化器实例的 validated_data ， errors，都会变成可获得的

s.validated_data 验证成功后，可以通过**序列化器实例的validated_data属性** 获取通过验证的数据
s.errors 验证失败，可以通过s.errors获取错误信息

2） is_valid(raise_exception=True)

is_valid方法还可以在验证失败时抛出异常serializers.ValidationError，可以通过raise_exception=True参数开启，

一旦检出错误，程序就会终止，自动return。所以我们一般不使用这个参数，直接判断is_valid是否为false，拿s.errors返回即可


##### 3.调用save()数据持久化

1） 调用save()方法

在数据校验成功后，调用序列化器的save() 方法进行数据的保存或更新

- 调用序列化器的save()方法后，如果未传instance，save方法则会调序列化器的create()方法

- 调用序列化器的save()方法后，如果传了instance，save方法则会调序列化器的update()方法

所以save()方法本质是调用序列化器的create或update方法，save()返回值自然也是create()或者update()方法的返回值

```python
s = CreateUserSerializer(data=created_list)
if s.is_valid():
    s.save()
```

2）额外传参

在对序列化器进行save()保存时，可以额外传递数据，这些数据会直接放到validated_data中，当然create和update就可以获取到
```python
s.save(owner=request.user)  # owner=request.user 会新增在validated_data字典中
```

3) 获取 data (模型实例)

在调用save()方法以后，序列化器实例的 data 会变成可获得的

s.data 即为反序列化传入数据 成攻创建或更新的数据库模型实例 序列化以后的数据。

4） 重写 save() 方法

实际上，save方法也可重写，只不过很少需要

我们可能不需要创建新的实例，而是使用validated_data中的数据发送电子邮件或做其他的事情。

这些情况下，可以选择直接重写 .save()，因为这样更具有可读性和意义。

请注意，在上面的情况下，我们现在必须直接访问序列化器 validated_data 属性。

```python
def save(self):
    email = self.validated_data['email']
    message = self.validated_data['message']
    return send_email(from=email, message=message)
```


5) 重写 create方法和update方法

- 如果序列化类继承Serializer，必须重写create方法和update方法，才能实现反序列化数据的新增和更新

- 如果序列化器类继承ModelSerializer，ModelSerializer自带了create方法和update方法

ModelSerializer中create方法是对此模型类执行create操作，传参为validated_data

ModelSerializer中update方法是对此模型类执行update操作，传参为instance, validated_data


ModelSerializer默认create和update方法基本相当于：

```python
def create(self, validated_data):
    return ExampleModel.objects.create(**validated_data)
def update(self, instance, validated_data):
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance
# 注：ModelSerializer中的update是使用 instance.key = value 的方式进行修改的。
# 如果此模型类没有这个字段，就不会实际进行持久化，也不会报错，所以 ModelSerializer 的update方法实际上可以不用修改。
```

- setattr() 说明

将给定对象的命名属性设置为指定值。
    
`setattr(x, 'y', v)` 等同于 “x.y = v”

```python
class Person:
    def __init__(self):
        pass
 
p = Person()
setattr(p, 'name', 'kiran')
print(f"name: {p.name}")
# name: kiran
```


但一般我们总是重写，主要有以下情况：


- 情况一：需要删除 validated_data 中不能保存在数据库中的字段

进行反序列化校验的参数通常都不一定最后要保存到数据库模型中，数据库也可能没有此字段，
比如手机验证码，没有必要保存到数据库中，数据库可能也压根没有此字段。
且主要因为数据库模型的创建方法ExampleModel.objects.create无法接收不是数据库字段的参数，会报错。
所以我们一般要把validated_data中不能保存在数据库中的字段删除。

注： ModelSerializer中的update()方法是使用`instance.key = value`的方式进行修改的。
如果此模型类没有这个字段，就不会实际进行持久化，也不会报错，
所以update方法不用担心validated_data有多余字段的问题，
这个情况下就不用重写ModelSerializer中的update()方法了。


- 情况二：调用外部函数

比如用户密码，需要对明文密码进行哈希处理后再存入数据库，就需要重写

```python
def create(self, validated_data):
    
    # 删除  validated_data 中不能保存在数据库中的字段
    del validated_data['passwordConfirm']
    del validated_data['smsCode']
    
    # 先调用ModelSerializer的create方法保存数据，但password现在是铭文的
    user = super().create(validated_data)
    
    # 调用set_password方法重新哈希设置密码  set_password方法是AbstractBaseUser模型类
    user.set_password(validated_data['password'])
    user.save()
    
    return user  
```


## 认证和授权

如何保护你的 API 并限制用户访问？

### 认证

注意： 不要忘了认证本身不会允许或拒绝传入的请求，它只是简单识别请求携带的凭证。

一共有三种认证方式：

- BasicAuthentication：HTTP基础认证。

前端将用户名和密码以Base64编码的形式，设置在Authorization HTTP头中，后端用以认证用户。

- TokenAuthentication：基于Token的认证。

使用Authorization HTTP头里面的Token认证用户。

- SessionAuthentication：使用Djnago的会话后台来认证。

使用Django Session Backend认证用户。


### 授权

建议自定义

常见的四4种权限控制的类别：

- AllowAny 允许所有用户
- IsAuthenticated 仅通过认证的用户
- IsAdminUser 仅管理员用户
- IsAuthenticatedOrReadOnly 认证的用户可以完全操作，否则只能get读取

自定义权限：
如需自定义权限，需继承`rest_framework.permissions.BasePermission`父类，并实现以下两个任何一个方法或全部

- `.has_permission(self, request, view)`

是否可以访问视图， view表示当前视图对象

- `.has_object_permission(self, request, view, obj)`

是否可以访问数据对象， view表示当前视图， obj为数据对

## 请求与响应

### request

前端传递 Body JSON格式数据，使用 `request.data` 获取数据，不需要对json格式判断，适用于POST等

前端传递 url 查询字符串参数，使用 `request.query_params` 

参考 https://q1mi.github.io/Django-REST-framework-documentation/api-guide/requests_zh/

### Responses

将JsonResponse改为Response（Response需要导入）

`from rest_framework.response import Response`

常用属性：
1）.data

传给response对象的序列化后，但尚未render处理的数据

2）.status_code

状态码的数字

3）.content

经过render处理后的响应数据

参考 https://q1mi.github.io/Django-REST-framework-documentation/api-guide/responses_zh/



### 自定义返回数据格式

https://www.jianshu.com/p/c0be24752584

https://www.cnblogs.com/yimeimanong/p/16185229.html

如何返回不同类型的响应？

## 缓存

https://q1mi.github.io/Django-REST-framework-documentation/api-guide/caching_zh/


在 Django REST framework 中，可以使用装饰器 @cache_page 和 @method_cache 来对接口添加缓存。这两个装饰器都是从 Django 的缓存框架中继承而来的。

### @cache_page 装饰器

可以缓存整个 API 视图的响应结果。

```python
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response

class MyAPIView(APIView):
    @cache_page(60 * 15) # 缓存该 API 视图 15 分钟
    def get(self, request):
        # 处理视图逻辑
        data = {'hello': 'world'}
        return Response(data)
```

这个示例代码使用了 cache_page 装饰器来为 MyAPIView 类的 get() 方法添加缓存策略，缓存有效期为 15 分钟。

### @method_cache 装饰器

可以缓存 API 视图中某个 HTTP 方法的响应结果。

```python
from django.views.decorators.cache import method_cache
from rest_framework.views import APIView
from rest_framework.response import Response

class MyAPIView(APIView):
    @method_cache(60 * 15, key_prefix='myapi:get') # 缓存 GET 请求 15 分钟
    def get(self, request):
        # 处理视图逻辑
        data = {'hello': 'world'}
        return Response(data)

    def post(self, request):
        # 处理视图逻辑
        data = {'hello': 'world'}
        return Response(data)
```

这个示例代码使用了 method_cache 装饰器来为 MyAPIView 类的 get() 方法添加缓存策略，缓存有效期为 15 分钟。在 @method_cache 装饰器中，可以通过 key_prefix 参数来设置缓存键名的前缀。

需要注意的是，与 Django 的缓存框架一样，缓存装饰器也存在缓存雪崩问题，在高并发情况下容易导致缓存失效。因此，需要对缓存进行合理的配置和管理。



## 频率/限流


`from rest_framework import throttling`

https://www.cnblogs.com/zouzou-busy/p/11581999.html
https://q1mi.github.io/Django-REST-framework-documentation/api-guide/throttling_zh/

## 过滤

https://q1mi.github.io/Django-REST-framework-documentation/api-guide/filtering_zh/

## 分页（Pagination）


### 全局配置

我们可以在配置文件中设置全局的分页方式，如：

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':  'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100  # 每页数目
}
```
### 自定义分页器

也可通过自定义Pagination类，来为视图添加不同分页行为。在视图中通过`pagination_class`属性来指明。

```python
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
class BookDetailView(RetrieveAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    pagination_class = LargeResultsSetPagination
```

注意：如果在视图内关闭分页功能，只需在视图内设置

```python
pagination_class = None
```

### 分页器


#### PageNumberPagination

第一种 PageNumberPagination  看第n页，每页显示n条数据，

前端访问网址形式：

```bash
GET  http://api.example.org/books/?page=4
```

可以在子类中定义的属性：

```python
page_size 每页数目
page_query_param 前端发送的页数关键字名，默认为"page"
page_size_query_param 前端发送的每页数目关键字名，默认为None
max_page_size 前端最多能设置的每页数量
```

```python
from rest_framework.pagination import PageNumberPagination

class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10

class BookListView(ListAPIView):
    queryset = BookInfo.objects.all().order_by('id')
    serializer_class = BookInfoSerializer
    pagination_class = StandardPageNumberPagination

# 127.0.0.1/books/?page=1&page_size=2
```


#### LimitOffsetPagination

第二种 LimitOffsetPagination 在第n个位置向后查看n条数据，

前端访问网址形式：

```bash
GET http://api.example.org/books/?limit=100&offset=400
```

可以在子类中定义的属性：

```python
default_limit 默认限制，默认值与PAGE_SIZE设置一直
limit_query_param limit参数名，默认'limit'
offset_query_param offset参数名，默认'offset'
max_limit 最大limit限制，默认None
```

```python
class LimitSet(pagination.LimitOffsetPagination):
    # 每页默认几条
    default_limit = 3
    # 设置传入页码数参数名
    page_query_param = "page"
    # 设置传入条数参数名
    limit_query_param = 'limit'
    # 设置传入位置参数名
    offset_query_param = 'offset'
    # 最大每页显示条数
    max_limit = None


from rest_framework.pagination import LimitOffsetPagination

class BookListView(ListAPIView):
    queryset = BookInfo.objects.all().order_by('id')
    serializer_class = BookInfoSerializer
    pagination_class = LimitSet
```

#### CursorPagination

第三种 CursorPagination 加密游标的分页 把上一页和下一页的id记住


https://www.cnblogs.com/zouzou-busy/p/11588193.html

```python
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

pagination_class = [PageNumberPagination]
```

## 跨域

https://www.cnblogs.com/zouzou-busy/p/11601002.html



## 测试

如何测试你的 API？


## 报错

[TypeError: 'ModelBase' object is not iterable](https://blog.csdn.net/weixin_45949073/article/details/109765896)