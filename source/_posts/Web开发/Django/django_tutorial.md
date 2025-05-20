---
title: Django 教程
date: 2022-08-15 15:52:00
tags:
- Django
categories:
- Django
---

> Django 版本：3.2

![](/images/learning.png)

## 0. 了解Django

[Django 官方入门教程](https://docs.djangoproject.com/zh-hans/3.2/intro/)

[Django 总体文档内容](https://docs.djangoproject.com/zh-hans/3.2/contents/)

[Django 内置模块文档](https://docs.djangoproject.com/zh-hans/3.2/py-modindex/)

[Python 框架：Django 基础知识](https://bk.tencent.com/s-mart/community/question/936?type=answer)

### 概念

- BS/CS 架构

[C/S架构，B/S架构](https://blog.csdn.net/weixin_47008635/article/details/115221400)

- MVC/MTV 开发模式

[Django MTV和MVC的区别](http://c.biancheng.net/view/7288.html)


- FBV(function based views)/CBV(class based views) 开发模式

[详解Django中FBV开发模式与CBV开发模式的区别.](https://blog.csdn.net/qq_45906219/article/details/110500902)




### 工作流程

待补充

## 1. 开发环境搭建

### 1.1 Python 环境搭建

[Python 官网](https://www.python.org/)
[Python 下载](https://www.python.org/downloads/)
[Python 下载 (windows)](https://www.python.org/downloads/windows/)

### 1.2 Pycharm 搭建虚拟环境

{% post_link django/virtual_environment %}

### 1.3 安装 MySQL

{% post_link sql/install %}

### 1.4 安装 Django

[官方文档：Django 安装](https://docs.djangoproject.com/zh-hans/3.2/intro/install/)

```bash
pip install django==3.2
```

```bash
python
>>> import django
>>> print(django.get_version())
3.2
```

#### 1.4.1 创建 Django 项目

```bash
django-admin startproject project_name
```

#### 1.4.2 创建 Django 应用

进入项目目录后

- 创建应用

```bash
django-admin startapp polls

python manage.py startapp polls
```

[Django 中多个 app 放入同一文件夹apps](https://www.cnblogs.com/duoxuan/p/9435791.html)

[Django 常用命令 django-admin.py 和 manage.py 用法解释](https://bk.tencent.com/s-mart/community/question/888?type=answer)

#### 1.4.3 配置修改

项目下的 settings.py 修改

改成中文和相应时区

```python
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'
#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
```

settings.py 中的 DATABASES 列表，做如下修改成MySQL

```python
'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'blog_project_db',
       'USER': 'root',
       'PASSWORD': '123456',
       'HOST': 'localhost',
       'PORT': '3306',
   }
```
- sql 依赖(MySQL)

python3 以上版本需要使用 pymysql

```bash
pip install pymysql
```

项目下的 init.py 添加

```python
import pymysql
pymysql.install_as_MySQLdb()
```

#### 1.4.4 迁移数据库表结构

```bash
# 为模型的改变生成迁移文件
python manage.py makemigrations

# 应用数据库迁移,将Model中的操作转换为数据库语言
python manage.py migrate
```

执行 python manage.py migrate 
报错 
pymysql.err.InternalError: (1813, "Tablespace '`ate`.`kanbansystem_workorder`' exists.")
django.db.utils.InternalError: (1050, "Table '`ate`.`kanbansystem_workorder`' already exists")

https://blog.csdn.net/joexiaoh/article/details/106423342

python manage.py migrate --fake


#### 1.4.5 创建超级管理员

```bash
python manage.py createsuperuser

python manage.py createsuperuser --username=admin --email=vip@django.cn
```

#### 1.4.6 启动服务

- 指定环境变量

PYTHONUNBUFFERED=1;
DJANGO_SETTINGS_MODULE=settings;

- 启动服务

```bash
python manage.py runserver 8080
```

## 2. Django 模型

创建 Django 应用的典型流程是，先建立数据模型，然后搭建管理站点，之后你的员工（或者客户）就可以向网站里填充数据了。

[Django models 官方文档](https://docs.djangoproject.com/zh-hans/3.2/ref/models/)

### 2.1 数据库配置

使用不同的数据库 或者使用多个数据库 都需要在项目下的 settings.py 配置

> 注意：密码可以使用环境变量替代

- sqlite3

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- mysql

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_project_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

[多数据库配置](https://docs.djangoproject.com/zh-hans/3.2/topics/db/multi-db/)


```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    'readonly': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'readonlyuser',
        'PASSWORD': 'readonlypassword',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# views.py

from django.shortcuts import render
from myapp.models import MyModel

def my_view(request):
    # 使用默认连接池
    results = MyModel.objects.all()

    # 使用 readonly 连接池
    results = MyModel.objects.using('readonly').all()

    return render(request, 'my_template.html', {'results': results})
```



### 2.2 模型

[models 字段 官方文档](https://docs.djangoproject.com/zh-hans/3.2/ref/models/fields/)

#### 2.2.0 模型配置

settings.py 文件， 找到 INSTALLED_APPS 设置，添加相应的app并激活

```python
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'mysite.blog',
)
```

#### 2.2.1 字段类型

| model 字段类型 | 类型 | 参数/描述/功能 |
|--|--|--|
| models.AutoField |  自增列 | 如果没有的话，默认会生成一个名称为 id 的列，如果要显示的自定义一个自增列，必须将给列设置为主键 primary_key=True |
| models.CharField　|　字符串 | 指定 max_length 参数设置最大长度 |
| models.BooleanField　|　布尔类型 | 值为True或 False |
| models.DateField　|　日期类型 | auto_now=True 每次保存模型对象时，自动设置该字段为当前时间。通常用于记录最后修改时间。<br> auto_now_add=True 创建模型对象时，自动设置该字段为当前时间。通常用于记录创建时间 |
| models.DateTimeField　|　日期类型 | 同 models.DateField |
| models.TimeField　| 时间 | HH:MM[:ss[.uuuuuu]] |
| models.EmailField　|　字符串类型 | （正则表达式邮箱） |
| models.FloatField　|　浮点类型 | |
| models.IntegerField　|　整型 | |
| models.BigIntegerField　|　长整型 | |
| models.TextField　| 字符串类型 | 同 CharField， 可以设置更长的字符串(超过4000个字符) |
| models.IPAddressField　|　字符串类型 | （ip4正则表达式） |
| models.GenericIPAddressField　| 字符串类型 | 参数protocol可以是：both、ipv4、ipv6 |
| models.URLField　| 字符串（地址正则表达式） | |
| models.ImageField  | 图片类型 | |
| models.FilePathField | 文件类型 | |


#### 2.2.2 关系字段

##### 2.2.2.1 一对一

**models.OneToOneField(其他表)**

例如 ModelA 中有字段指向 ModelB

ModelA 只能对应 ModelB 中特定的值，同样 ModelB 也只能对应 ModelA 中特定的值

```python
b = models.OneToOneField(ModelB，related_name="info", on_delete=models.CASCAED)
```
[一对一关联模型 API 用法示例文档](https://docs.djangoproject.com/zh-hans/3.2/topics/db/examples/one_to_one/)

##### 2.2.2.2 一对多（外键）

**models.ForeignKey(其他表)**

ForeignKey 是用来建立与其他模型之间的关联。
在关系数据库中，会自动为外键创建索引并强制实施参照完整性约束，这意味着当我们尝试删除与某个外键相关的对象时，如果还有其他对象仍然与此外键相关，则会出现错误。

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=50)
```
在上面的代码示例中，Book 模型有一个 author 属性，它是一个 ForeignKey 字段，它指向 Author 模型。
在这种情况下，每个 Book 对象都关联到一个 Author 对象，而每个 Author 可能对应多个 Book 对象。


**【参数说明】**
to：ForeignKey 关联的目标模型。可以是模型类对象、模型的全名字符串或应用名称与模型名称的组合字符串。通常是省略

related_name: 此关系的反向名称。它允许通过引用另一个模型来访问此模型。
related_query_name：反向查询名称。例如，如果在 Book 模型中有外键 author，related_query_name 可以设置为 "book"，这样就可以使用 Author.objects.filter(book__title='Moby Dick') 查询所有写了 Moby Dick 这本书的作者。
limit_choices_to：一个 Q 对象（或其他满足 QuerySet API 的对象）用于限制可用的关联对象。例如，models.ForeignKey(Author, limit_choices_to={'is_staff': True}) 将只能选择 is_staff 为 True 的作者作为外键对象。

to_field：将关联目标模型的哪个字段用作外键。如果未指定，则默认使用主键（即 id）作为外键。

[on_delete](https://docs.djangoproject.com/zh-hans/3.2/ref/models/fields/#django.db.models.ForeignKey.on_delete): 定义在删除关联对象时如何处理外键

| 参数 | 作用 | 示例 | 
| -- | -- | -- |
| on_delete=None | 删除关联表中的数据时,当前表与其关联的field的行为 |  |
| **on_delete=models.CASCADE** | 级联删除。即删除关联对象时，删除包含该外键的所有对象。 |  |
| on_delete=models.DO_NOTHING | 删除关联数据,什么也不做 |  |
| on_delete=models.PROTECT | 保护。即不允许删除关联对象，只有在解除关联之前才能删除该对象。若单独删除关联数据,引发错误ProtectedError |  |
| on_delete=models.RESTRICT | 引发 RestrictedError 来防止删除被引用的对象 |  |
| on_delete=models.SET_NULL | 将外键设置为 NULL。即当关联对象被删除时，将外键设置为 NULL（前提FK字段需要设置为可空,一对一同理） | `on_delete=models.SET_NULL, blank=True, null=True` |
| on_delete=models.SET_DEFAULT | 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理） | `on_delete=models.SET_DEFAULT, default='默认值'` |
| on_delete=models.SET |  删除关联数据 |  a. 与之关联的值设置为指定值,设置：models.SET(值)<br> b. 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)  |

[一对多关联模型 API 用法示例文档](https://docs.djangoproject.com/zh-hans/3.2/topics/db/examples/many_to_one/)

> 注意：外键(ForeignKey) 和 一对一(OneToOneField) 的时候，必须添加 `on_delete` 参数，
> 若不设置 related_name，可以基于"**外键模型小写_set**"来获取外键模型
> 请注意，add()、create()、remove()、clear() 和 set() 都会对所有类型的相关字段立即应用数据库变化。
> 换句话说，没有必要在关系的任何一端调用 save()。

[Django 关联对象 参考](https://docs.djangoproject.com/zh-hans/3.2/ref/models/relations/)

[Django中外键使用详解](https://blog.csdn.net/xujin0/article/details/83552349)

[Django数据库——外键与查询条件](https://blog.csdn.net/yuaicsdn/article/details/118786211)

[通过主表查询子表、通过子表查询主表、字段 related_name 的作用](https://blog.csdn.net/hpu_yly_bj/article/details/78939748)

##### 2.2.2.3 多对多

**models.ManyToManyField(其他表)**

例如 每个 Student 对象可以关联到多个 Course 对象，并且每个 Course 对象也可以被多个 Student 关联。因此，我们使用了 ManyToManyField 字段来表示这种关系，而不是 ForeignKey。

```python
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    name = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course)
```

[多对多关联模型 API 用法示例文档](https://docs.djangoproject.com/zh-hans/3.2/topics/db/examples/many_to_many/)

#### 2.2.3 字段选项

- model 的常用参数设置

| model 设置参数 | 参数描述/功能 |
|--|--|
| **null=(True/False)** | 数据库中字段是否可以为空 |
| blank=(True/False) | django 的 Admin界面 中添加数据时是否可允许空值, 允许表单中该字段为空 |
| primary_key=(True/False) | 主键，对 AutoField 设置主键后，就会代替原来的自增 id 列 |
| auto_now=(True/False) | 每次保存模型对象时，自动设置该字段为当前时间。通常用于记录最后修改时间。 |
| auto_now_add=(True/False) | 创建模型对象时，自动设置该字段为当前时间。通常用于记录创建时间。 |
| default='xxxx' | 字段的默认值 |
| choices=(xx,xx,xx) | 可选择列表项，通常是一个列表或者元组 |
| max_length=(int) | 最大长度，多和字符串类型配合使用 |
| verbose_name='xxxx' | 设置更易读的字段名，用于 Django Admin 后台以及错误信息 |
| db_column | 数据库中的字段名称 |
| **unique=(True/False)** | 是否可以重复,True为不能重复 |
| db_index=(True/False) | 是否设置为索引 |
| editable=(True/False) | 在Admin里是否可编辑 |
| error_messages='xxxx' | 错误提示 |
| auto_created=(True/False) | 是否自动创建 |
| help_text='xxxx' | 为字段提供帮助信息，在表单和 Django Admin 后台显示。 |
| upload-to='xxxx' | 上传到哪个位置，与 ImageField,FfileField 配合使用 |

[choices 详解](https://blog.csdn.net/qqizz/article/details/80020367)

> 注意: 可以维护递归的关联关系，使用self指定

#### 2.2.4 索引

https://docs.djangoproject.com/zh-hans/3.2/ref/models/indexes/

#### 2.2.5 模型 类 

https://docs.djangoproject.com/zh-hans/3.2/ref/models/class/

#### 2.2.6 模型 方法

https://docs.djangoproject.com/zh-hans/3.2/topics/db/models/#model-attributes

#### 2.2.7 Meta 选项(元选项)

db_table 作用：修改数据库表的默认的名称

```python
  # 书籍信息模型
  class BookInfo(models.Model):
      name = models.CharField(max_length=20)  # 图书名称
 
      class Meta:  # 元信息类
          db_table = 'bookinfo'  # 自定义表的名字
          ordering = ['name']  # 数据排序
```

[Meta 字段详解 官方文档](https://docs.djangoproject.com/zh-hans/3.2/ref/models/options/)

[Meta 详解](https://blog.csdn.net/bbwangj/article/details/79967858)


#### 2.2.8 模型继承

[模型继承 官方文档](https://docs.djangoproject.com/zh-hans/3.2/topics/db/models/#model-inheritance)

[Django中Model继承的三种方式](https://blog.csdn.net/weixin_43789195/article/details/86363456)

#### 2.2.9 实例

[模型实例参考](https://docs.djangoproject.com/zh-hans/3.2/ref/models/instances)

### 2.3 数据库迁移

#### 2.3.1 迁移命令

- 创建数据库表

```bash
# 为模型的改变生成迁移文件
python manage.py makemigrations [app_label [app_label ...]]
```

[makemigrations 详解](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-makemigrations)

```bash
# 应用数据库迁移,将Model中的操作转换为数据库语言
python manage.py migrate

# 收集静态文件
python manage.py collectstatic
```

[migrate 详解](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-migrate)

```bash
# 查看具体数据库操作
(venv) E:\project\django_study\mysite>python manage.py sqlmigrate blog 0001
--
-- Create model Author
--
CREATE TABLE `blog_author` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(50) NOT NULL, `email` varchar(254) NOT NULL);
--
-- Create model Book
--
CREATE TABLE `blog_book` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(200) NOT NULL);
CREATE TABLE `blog_book_authors` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `book_id` bigint NOT NULL, `author_id` bigint NOT NULL);
ALTER TABLE `blog_book_authors` ADD CONSTRAINT `blog_book_authors_book_id_author_id_0a5bb3b3_uniq` UNIQUE (`book_id`, `author_id`);
ALTER TABLE `blog_book_authors` ADD CONSTRAINT `blog_book_authors_book_id_35eae5ed_fk_blog_book_id` FOREIGN KEY (`book_id`) REFERENCES `blog_book` (`id`);
ALTER TABLE `blog_book_authors` ADD CONSTRAINT `blog_book_authors_author_id_fa034e3d_fk_blog_author_id` FOREIGN KEY (`author_id`) REFERENCES `blog_author` (`id`);

```
[迁移概述](https://docs.djangoproject.com/zh-hans/3.2/topics/migrations/)

#### 2.3.2 操作参考

https://docs.djangoproject.com/zh-hans/3.2/ref/migration-operations/

#### 2.3.4 SchemaEditor

https://docs.djangoproject.com/zh-hans/3.2/ref/schema-editor/

#### 2.3.5 编写迁移语句

https://docs.djangoproject.com/zh-hans/3.2/howto/writing-migrations/

### 2.4 Model API（CRUD）

- 常用

[数据库 执行查询 参考](https://docs.djangoproject.com/zh-hans/3.2/topics/db/queries/)

[QuerySet API 参考](https://docs.djangoproject.com/zh-hans/3.2/ref/models/querysets/)

- 不常用

[查找 API 参考](https://docs.djangoproject.com/zh-hans/3.2/ref/models/lookups/)

[模型 _meta API¶](https://docs.djangoproject.com/zh-hans/3.2/ref/models/meta/)


#### 2.4.1 插入数据

创建好数据库进行数据添加，可以通过如下操作进行

```python
from blog.models import Category, Tag
c = Category('test category')
c.save()
t = Tag('test tag')
t.save()
```

打开数据库可以看到插入的数据

#### 2.4.2 查找数据

- 查找某个表所有数据

```python
# 查找某个表所有的数据，返回<QuerySet[...]>
from blog.models import Category
c_list = Category.objects.all()
```

##### 1、特定条件(get 、filter)

- get()

```python
# 查找单个特定的数据，
# 如果数据不存在会抛出错误 blog.models.DoesNotExist，存在则返回 model 对象，如果重写了 __str__ 方法，则返回该方法所指定的值
# 如果数据存在多个也会抛出异常

>>> Publisher.objects.get(country="U.S.A.")
Traceback (most recent call last):
    ...
MultipleObjectsReturned: get() returned more than one Publisher --
    it returned 2! Lookup parameters were {'country': 'U.S.A.'}

# get() 一般建议捕获异常
try:
    p = Publisher.objects.get(name='Apress')
except Publisher.DoesNotExist:
    print "Apress isn't in the database yet."
else:
    print "Apress is in the database."
    print(p.name)
```

- filter()

如果需要执行更复杂的查询（例如，使用 OR 语句的查询），可以使用 Q 对象 （*args）。

```python
from django.db.models import Q
from .models import Bluetooth

def query_bluetooth(request):
    sn = request.GET.get('sn', '')  # 获取请求中的参数 sn
    esn = request.GET.get('esn', '')  # 获取请求中的参数 esn
    
    if sn and esn:
        results = Bluetooth.objects.filter(Q(sn=sn) & Q(esn=esn))
    elif sn:
        results = Bluetooth.objects.filter(sn=sn)
    elif esn:
        results = Bluetooth.objects.filter(esn=esn)
    else:
        results = Bluetooth.objects.all()
    
    for item in results:
        print(item.sn, item.esn)
    # 返回结果
    return HttpResponse(results)
```


```python
# 查找满足符合特定条件的数据
# 若不存在，返回为空，存在则返回 QuerySet 对象

c_test = Category.objects.filter(name='test category', id__lt=10)
c_test = Category.objects.filter(id__range=[0, 10])

# 还可以使用 startswith，istartswith, endswith, iendswith 等条件
```

- field 查找条件

**"__" 的常用操作**
大于：__gt
大于等于：__gte
小于：__lt
小于等于：__lte
包含：__contains (__icontains 加i忽略大小写)
开头是：__startswith
结尾是：__endswith
其中之一：__in  (传一个列表)
范围：__range
值为空：__isnull

时间查询: date,year,month,day,week_day,hour,minute,second

[下划线 字段查询](https://docs.djangoproject.com/zh-hans/3.2/ref/models/querysets/#field-lookups)

```python
# 大于，小于操作
Categroy.objects.fileter(id__gt=1, id__lt=10) # 查找 id 介于 1 和 10 之间的数据
# in
Category.objects.filter(id__in=[11, 22, 33]) # 查找 id 为 11，22，33 的值
Category.objects.exclude(id__in=[11, 22, 33]) # not in
# contains
Category.objects.filter(name__contains="test") # 查找 name 字段包含 test 的值
Category.objects.filter(name__icontains="test") # 大小写不敏感
# range
Caregory.objects.filter(id__range=[1, 10]) # 查找 id 介于 1 和 10 之间的数据，即 between and
# 类似的包括 startwith, istartwith, endwith, iendwith 等

# isnull
Category.objects.filter(name__isnull=True)  # 查找 name 字段为空
Category.objects.filter(name__isnull=False)  # 查找 name 字段不为空
# 时间查询
Blog.objects.filter(create_time__year=2018)  # 查询年为2018年的内容
Blog.objects.filter(create_time__month=3)  # 查询月

# dates 方法
Blog.objects.dates('create_time', 'year','DESC')  # 分别为：时间字段，查询返回年year，年月month，年月日day，最后一个参数是排序方式ASC正序，DESC倒序从大到小。
```

- .values() 和 .values_list()

```python
# .values() 取出某一列，每个元素是一个字典，
print(Category.objects.filter(name='test category').values('name', 'id'))
# <QuerySet [{'name': 'test category', 'id': 1}]>
```

values_list() 用于获取查询结果集的指定字段列表，返回一个 QuerySet 列表。

values_list()可以接受两个参数：

- flat: 如果为True，则只返回一个包含指定列值的单一列表。默认为False，返回一个由元组构成的列表。
- fields: 它是可选的参数，是一个字符串列表，指定需要返回的列名。如果不提供该参数，将返回所有列。

```python
# 获取指定字段列表
print(Category.objects.filter(name='test category').values_list('name', 'id'))
# <QuerySet [('test category', 1)]>

# 获取单一列表
print(Category.objects.filter(name='test category').values_list('name', flat=True))
# <QuerySet ['test category']>
```

##### 2、查询条件外的数据

推荐使用 filter, 避免使用.exclude()方法带来的性能开销。

```python
# exclude 查询条件外的数据 （不包含）
Category.objects.exclude(id__gt=2)   即查找 不包含 id 大于 2 的数据
```

##### 3、数据排序

通过 `order_by()` 进行结果排序

指定逆向排序，在前面加一个减号 `-`前缀

```python
Category.objects.all().order_by('-id') # 逆序排序，逆序排序只需要在排序字段前加"-"号即可
```

也可以在 models.py 的 class Meta 元选项添加 ordering 字段

```python
class Meta:**
    ordering = ['-id']
```

##### 4、数据切片

限制返回的数据，利用 Python 的切片即可

```python
# 筛选某个范围内的数据 类似于 SQL 语句中的 OFFSET 10 LIMIT 10
Category.objects.all()[10: 20] # 获取列表中 10-20 的数据
```

> 注意，不支持Python的负索引(negative slicing)：

虽然不支持负索引，但是我们可以使用其他的方法。 比如，稍微修改 order_by() 语句来实现：

```python
Publisher.objects.order_by('-name')[0]
```

##### 5、aggregate 和 annotate

参考：https://zhuanlan.zhihu.com/p/50974992

- aggregate 操作符：聚合

aggregate方法支持的聚合操作有 Count, Avg, Max, Min或者Sum

```python
# aggregate 操作符(出了求和 Count 还有 Avg, Max, Min 等，通过 django.db.models 导入)
from django.db.models import Sum,Avg,Max,Min,Count

print(Category.objects.aggregate(Count('name')))    # {'name__count': 5}

# 也可以指定结合后的字段名
print(Category.objects.aggregate(category_count=Count('name)))  # {'category_count': 5}

# 计算学生平均年龄, 返回字典。age和avg间是双下划线哦
Student.objects.all().aggregate(Avg('age'))
{ 'age__avg': 12 }

# 学生平均年龄，返回字典。all()不是必须的。
Student.objects.aggregate(Avg('age'))
{ 'age__avg: 12' }

# 计算学生总年龄, 返回字典。
Student.objects.aggregate(Sum('age'))
{ 'age__sum': 144 }

# 学生平均年龄, 设置字典的key
Student.objects.aggregate(average_age = Avg('age'))
{ 'average_age': 12 }

# 学生最大年龄，返回字典
Student.objects.aggregate(Max('age'))
{ 'age__max': 12 }

# 同时获取学生年龄均值, 最大值和最小值, 返回字典
Student.objects.aggregate(Avg('age‘), Max('age‘), Min('age‘))
{ 'age__avg': 12, 'age__max': 18, 'age__min': 6, }

# 根据Hobby反查学生最大年龄。查询字段student和age间有双下划线哦。
Hobby.objects.aggregate(Max('student__age'))
{ 'student__age__max': 12 }
```

- annotate 操作符: 分组

返回包含有新增统计字段的查询集，一般结合filter使用，注意前后顺序

```python
# 假设 Post 表中有个字段指向 Category
# category = models.ForeignKey(Category) 在表 Category 中需要统计某个 category 下 post 数量，
# 但是表 Category 中没有 post_count 字段，那么可以通过 annotate 操作符来进行统计
c_list = Category.objects.annotate(post_count=Count('post'))
print(c_list[0].post_count) # 12
```

#### 2.4.3 聚合函数

[查询表达式](https://docs.djangoproject.com/zh-hans/3.2/ref/models/expressions/)

##### F 对象

F对象用于在查询中使用字段值作为查询条件，例如对某个字段进行数学计算后再与另一个字段进行比较，或者对某个字段的值进行自增/自减操作等。

```python
# 假设有一个名为Book的模型，包含title、price和discount字段。现在我们想要查询价格大于平均价格的图书，并将这些图书的折扣都设置为10%。

from django.db.models import Avg, F

# 计算平均价格
avg_price = Book.objects.aggregate(avg=Avg('price'))['avg']

# 查询价格大于平均价格的图书
books = Book.objects.filter(price__gt=avg_price)

# 设置折扣为10%
books.update(discount=F('price') * 0.1)
```

##### Q 对象

Q对象用于构建多个条件之间的逻辑关系，例如AND、OR等。通过使用Q对象可以将多个查询条件组合在一起，以便生成更复杂的查询表达式。

1. 或者

或者就是在每个Q对象之间加一个`|`

```python
from django.db.models import Q

def get(self,request):
    """Q对象,用于逻辑判断或者的情况"""
    # 查询年龄小于16的或者大于18的
    student_list = Student.objects.filter(Q(age__lt=16)|Q(age__gt=18)).all()
    print(student_list)
    return HttpResponse("ok")
```

2. 与、非

与就是在每个Q对象之间加一个`&`.

非就是在每个Q对象之间加一个`~`.

但是 Q 对象一般只用于或者的使用，只有多嵌套复杂的查询条件才会使用`&`和`~`进行与和非的意思.

[条件表达式](https://docs.djangoproject.com/zh-hans/3.2/ref/models/conditional-expressions/)


##### Q对象和F对象 的区别在于：

- Q对象用于组合多个查询条件，而F对象用于处理字段值；
- Q对象可以通过and和or等操作符来组合多个查询条件，而F对象只能操作一个字段的值；
- Q对象返回一个Q对象，可以继续链式操作，而F对象返回一个类似于sql语句的表达式；


##### When

##### Case


[Django中 select_for_update 方法的应用](https://blog.csdn.net/kaikai0803/article/details/97278180)
[Django update_or_create()方法](https://blog.csdn.net/qq_35968173/article/details/107639786)

浅谈 get_or_create(**kwargs)
https://bk.tencent.com/s-mart/community/question/1064?type=answer

##### 数据库函数

[数据库函数](https://docs.djangoproject.com/zh-hans/3.2/ref/models/database-functions/)
[数据库函数之文本函数](https://blog.csdn.net/weixin_43354181/article/details/125252120)

#### 多表查询

https://blog.csdn.net/weixin_46371752/article/details/126375988

#### 关联查询


Django ORM 优化之select_related
https://www.jianshu.com/p/937464304096

Django查询优化之select_related和prefetch_related
https://developer.aliyun.com/article/538196

https://blog.csdn.net/qq_52385631/article/details/126695685




关于Django ORM 数据库查询使用优化
https://bk.tencent.com/s-mart/community/question/993?type=answer

Django开发中常用到的数据库操作总结
https://bk.tencent.com/s-mart/community/question/958?type=answer

#### 内连接/子查询

[OuterRef Exists Subquery](https://blog.csdn.net/sheqianweilong/article/details/113838061)

https://www.cnblogs.com/zonghan/p/17039500.html

[QuerySet API 参考](https://docs.djangoproject.com/zh-hans/3.2/ref/models/querysets/)

#### 2.4.4 修改数据

对存在的数据进行修改，可通过如下操作进行

```python
c = Category.objects.get(name='test category')
c.name = 'new test category'
c.save()
```

```python
>>> Publisher.objects.update(name='Apress Publishing')
2   # 表示受影响的记录条数
```

#### 2.4.5 删除数据

对存在数据库中的数据进行删除，可以通过`delete()`操作进行

```python
# 删除某条特定的数据
c = Category.objects.get(name='new test category')
c.delete()

Category.objects.filter(country='USA').delete()
# 删除全部的数据
Category.objects.all().delete()

```


#### 事务


```python
from django.db import transaction

@transaction.atomic
def my_view(request):
    do_stuff()
```

[Django中事务的三种简单用法](https://blog.just666.com/2018/07/10/django-transactions/)

#### 2.4.6 原生 SQL 命令

使用 raw SQL 进行查询

```python
from django.db import connection
from .models import Bluetooth

def query_bluetooth(request):
    sn = request.GET.get('sn', '')  # 获取请求中的参数 sn
    esn = request.GET.get('esn', '')  # 获取请求中的参数 esn
    
    if sn and esn:
        sql = "SELECT * FROM bluetooth WHERE sn=%s AND esn=%s"
        params = [sn, esn]
    elif sn:
        sql = "SELECT * FROM bluetooth WHERE sn=%s"
        params = [sn]
    elif esn:
        sql = "SELECT * FROM bluetooth WHERE esn=%s"
        params = [esn]
    else:
        sql = "SELECT * FROM bluetooth"
        params = []
    
    # 执行原生 SQL 查询
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        # 获取全部查询到的数据
        results = cursor.fetchall()
    
    # 返回结果
    return HttpResponse(results)
```

### 2.5 思考

#### get() 和 filter() 的区别

1、get

输入参数：get的参数只能是model中定义的哪些字段，只支持严格匹配。

`Entry.objects.get(id='foo') # raises Entry.DoesNotExist`

返回参数：get 返回值是一个定义的model对象，只有一条记录返回的时候才正常,也就说明get的查询字段必须是主键或者唯一约束的字段。当返回多条记录或者是没有找到记录的时候都会抛出异常

2、filter

输入参数：filter的参数可以是字段也可以是扩展的where查询关键字，如in，like，返回QuerySet包含与给定查找参数匹配的新对象。

返回参数：filter返回QuerySet对象，有没有匹配的记录都可以。

filter有缓存数据的功能，第一次查询数据库并生成缓存，下次再调用filter方法的话，直接取得缓存的数据，get方法每次执行都是直接查询数据库的。


## 4. Django Admin 管理工具

【包括界面管理、创建管理员等】

Django Admin 管理工具是django.contrib的一部分

用户鉴别系统(django.contrib.auth)
支持匿名会话(django.contrib.sessioins)
用户评注系统(django.contrib.comments)
```python
from django.contrib import admin

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('first_name', 'last_name')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    **fields = ('title', 'authors', 'publisher', 'publication_date')**
    filter_horizontal = ('authors',)
    **raw_id_fields = ('publisher',)**
```


## 5. Django 表单

### 基础

#### 概览

[表单基础概念](https://docs.djangoproject.com/zh-hans/3.2/topics/forms/)

[django - 表单(form)验证及错误提示设置](https://blog.csdn.net/xxm524/article/details/48369623)



`action=""`意味着表单将提交给与当前页面相同的URL。

#### 表单API

https://docs.djangoproject.com/zh-hans/3.2/ref/forms/api/

#### 内建字段

https://docs.djangoproject.com/zh-hans/3.2/ref/forms/fields/

#### 内建部件

https://docs.djangoproject.com/zh-hans/3.2/ref/forms/widgets/

### 进阶

#### 针对模型的表单
https://docs.djangoproject.com/zh-hans/3.2/topics/forms/modelforms/

#### 表单资源
https://docs.djangoproject.com/zh-hans/3.2/topics/forms/media/

#### 表单集
https://docs.djangoproject.com/zh-hans/3.2/topics/forms/formsets/

#### 自定义验证
https://docs.djangoproject.com/zh-hans/3.2/ref/forms/validation/



## 3. Django 视图

### 3.1 URLconf


### 路由规则

[path() 详解](https://docs.djangoproject.com/zh-hans/3.2/ref/urls/#django.urls.path)

[include() 详解](https://docs.djangoproject.com/zh-hans/3.2/ref/urls/#django.urls.include)

1. 首先在应用文件夹下创建 urls.py 文件，用来配置视图的 url，然后我们需要在项目下的 urls.py 文件中将该应用的 urls 配置进去

```python
# 在项目下 urls.py 文件配置应用的 urls.py 文件
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # include 作用：在 django 匹配 url 时候匹配完 blog/ 后，再次匹配下层地址，所以在 blog/ 
    # 后面不可以添加 "$" 符号，不然会导致不能匹配到地址，namespace 为了区分不同应用下同名的模版
    url(r'^blog/', include('blog.urls', namespace="blog")),
]
```

```python
from django.urls import path        # 字符串路由
from django.urls import re_path     # 正则路由

path("公共url地址(又叫路由前缀)",include("子应用目录名.路由模块"))

# path("路由url","视图函数","路由别名"),
path('index',views.index,name="home"),
re_path("正则模式", views.视图函数, name="路由别名")
```

2. 在应用文件夹下的 views.py 文件中加入视图

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello django")
```

3. 在应用下的 urls.py 文件中将视图文件配置进去

```python
from django.conf.urls import url
from . import views

# 加上 app_name, 值同 include 中 namespace 的值，否则可能会找不到 url
app_name = 'blog'
urlpatterns = [
    # 当模版引用本地 url 时候需要用到 name 字段值，例如
    # <a href="{% url 'blog:home' %}"><b>Home</b></a>
    url(r'^home$', views.home, name=home),
]
```

4. 命令行将代码运行

```powershell
python manage.py runserver 192.168.x.xxx:8080
```

然后可以通过网址 "http://192.168.x.xxx:8080/blog/index" 访问编写的界面


5. 当 url 中带入参数进行传递时，例如

```python
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError as e:
        print(e)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return HttpResponse("{} hours later is {}".format(offset, dt))
```

那么我们在 url 配置的时候需要将 offset 参数传入到 url 中去，需要涉及到正则表达式

```python
urlpatterns = [
# ?P<offset> 为传递的参数字段名，紧随其后的是参数值的匹配正则
# 可以通过 http://192.168.x.xxx:8080/time/ahead/(offset)/ 来访问相应网址
    url(r'^time/ahead/(?P<offset>\d{1, 2})/$', view.hours_ahead, name="time_ahead")
]
```

**reverse()** 在配置 url 时候的大用处(这里先提下，项目中会接触到)

```python
# 假设我们有个网址为 192.168.x.xxx:8080/post/1/ 其中 1 为 post 的 id 根据 id 不同显示不同 post
# 网址的正则为 url(r'post/(?P<pk>[0-9]+)/$', view.post, name="post_detail")
class Post(models.Model):
title = models.CharField("标题", max_length=100)

def get_post_url(self):
    # reverse 会自动指向 'blog:post_detail' 所指向的 url，kwargs 为传入的参数值
    return reverse('blog:post_detail', kwargs={'pk': self.pk})
```
### 反向解析


### 会话技术

cookies , token, session



### 3.2 使用模板建立视图(模板层)

[模板概述](https://docs.djangoproject.com/zh-hans/3.2/topics/templates/)

1. 首先在项目根目录下创建 templates 文件夹，用来放视图模版，然后在项目下的 settings.py 文件中注册 templates 文件夹，使 django 能够在 templates 文件夹中找到相应的模版，在 TEMPLATES 中的 DIRS 列表中加入如下代码

```python
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

2. 在 templates 文件夹下再创建放应用模版的文件夹 例如 blog ，然后在 blog 创建 index.html 作为 index 视图的模版

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
<h1>{{ welcome }}</h1>
</body>
</html>
```

3. 修改视图文件函数

```python
from django.shortcuts import render

def index(request):
# context 中的参数名和模版中 {{ }} 包裹的相同
return render(request, 'blog\index.html', context={
        'title': "My Blog Home",
        'welcome': "Welcome to My Blog"
})

# 或者可以用以下方法来写
def index(request):
title = "My Blog Home"
welcome = "Welcome to My Blog"
return render(request, 'blog\index.html', locals())
```

然后我们就可以看到如下的界面，django 会把 view 的值传到模版中去

![第一次使用模版](/images/2888797-99a3d2fad9cfa623.png)

使用模版的话，我们就需要了解一下模版内置的标签和过滤器，这对我们日后的开发可以提高很多效率

#### 3.2.1 内置模版标签

[官网-内置模板标签和过滤器](https://docs.djangoproject.com/zh-hans/3.2/ref/templates/builtins/)

- 继承模版标签:

```html
{% extends %}
```

- 变量标签:

用两个大括号括起来的文字 (例如 `{{ post_title }})` 称为变量 (variable)，这意味着在此处插入指定变量的值

- 判断标签:

```html
{% if %} 
{% else %}
{% end if%}
```

```text
- {% if %} 标签接受 and, or 或者 not 关键字来对多个变量做判断，或者对变量取反 (not)
- 不允许在同一个标签中同时使用 and 和 or，但可以多次使用同一个逻辑操作符
- 不支持用圆括号来组合比较操作
- 没有 {% elif %} 标签，只能 {% if %} 嵌套达到效果
- 一定要用 {% endif %} 关闭每一个 {% if %} 标签
```

eg:

```html
{% if {{ str }} %}
    <p>Value is not null</p>
{% else %}
    <p>Value is null</p>
{% endif %}
```

- 循环标签: 

```html
{% for %}
{% empty %}
{% endfor %}
```

```text
- 给标签增加一个 reversed 使得该列表被反向迭代  eg: {% for s in s_list reversed%}
- 可以嵌套使用 {% for %} 标签
- 执行循环之前通常先检测列表的大小，因此 for 标签支持一个可选的 {% empty %} 分句
- 不支持 break 和 continue，退出循环时候，可以改变正在迭代的变量，让其仅仅包含需要迭代的项目。
- 每个 {% for %} 循环里有一个称为 forloop 的模板变量，这个变量存在一些表示循环进度信息的属性，模板解析器碰到 {% endfor %} 标签后，forloop 就不可访了
```

| 属性 | 描述 |
| -- | -- |
| forloop.counter      | 显示循环的执行次数，从1开始计数 |
| forloop.counter0     | 显示循环的执行次数，从0开始计数 |
| forloop.revcounter   | 倒数显示循环的次数，从1开始 |
| forloop.revcounter0  | 倒数显示循环的次数，从0开始 |
| forloop.first        | 判断如果本次是循环的第一次，则结果为 True |
| forloop.last         | 判断如果本次是循环的最后一次，则结果为 True |
| forloop.parentloop   | 当前循环的上一级循环的 forloop 对象的引用(嵌套循环情况下) |

eg:

```html
{% for country in countries %}
    <table>
    {% for city in country %}
        <tr>
        <td>Country {{ forloop.parentloop.counter }}</td>
        <td>City {{ forloop.counter }}</td>
        <td>{{ city }}</td>
        </tr>
    {% endfor %}
    </table>
{% empty%}
    <p>There is no country</p>
{% endfor %}
```

- 比较标签: `{% ifequal/ifnotequal%} [{% else %}可省略]  {% endifqual/ifnotequal%} 标签    `

比较两个变量的值并且显示一些结果，支持可选的 `{% else %}` 标签；只有模板变量，字符串，整数和小数可以作为 `{% ifequal %}` 标签的参数

- 转移标签: `{% autoescape %}{% endautoescape %}` 关闭代码块中的自动转义，父类已经关闭则子类也关闭

#### 3.2.2 内置模版过滤器

模板过滤器是在变量被显示前修改它的值的一个简单方法，以 "|" 拼接，过滤器的参数跟随冒号之后并且总是以双引号包含，

例如 `{{ value|add:"2" }}` 返回值为 value + 2 的值

| 过滤器 | 用法 | 代码 |
| -- | -- | -- |
| add |  对象相加，如果是数字则是数字加法，列表则是列表的和，无法相加为空。| `{{ value|add:"2" }}` |
| last | 获取列表/元组的最后一个成员  |  `{{ list|last }}` | 
| first | 获取列表/元组的第一个成员  |    `{{ list|first }}` | 
| length | 获取数据的长度       |  `{{ list|length }}` | 
| defualt | 当变量没有值的情况下，系统输出默认值  |  `{{ str|defualt="默认值" }}` | 
| safe   |   让系统不要对内容中的html代码进行实体转义  |  `{{ htmlcontent|sate }}` | 
| upper  |  字母转换成大写   |  `{{ str|upper }}` | 
| lower  |  字母转换成小写   |  `{{ str|lower }}` | 
| title  |  每个单词首字母转成大写   |  `{{ str|title }}` | 
| date   |  日期时间格式转换  |   `{{ value | date:"D Y-m-d H:i:s" }}` | 
| cut    |  从内容中截取掉相同字符的内容   |  `{{ content|cut:"hello" }}` | 
| list   |  把内容转换成列表格式     |  `{{ content|list }}` | 
| escape  |  把内容中的HTML特殊符号转换成实体字符   |  `{{ content|escape }}` | 
| filesizeformat  |  把文件大小的数值转换成单位表示   |  `{{ filesize|filesizeformat }}` | 
| join   |  按指定字符拼接内容   |  `{{ list|join("-") }}` | 
| random  |  随机提取某个成员    |  `{{ list|random }}` | 
| slice |   按切片提取成员     |  `{{ list|slice:":-2" }}` | 
| truncatechars  |  按字符长度截取内容   |  `{{ content|truncatechars:30 }}` | 
| truncatewords  |  按单词长度截取内容   |  `{{ content|truncatewords:3 }}` | 


案例：[怎么样在Django里实现联动下拉列表选项？](https://www.django.cn/article/show-12.html)

#### 3.2.3 自定义过滤器和标签

[自定义模板过滤器和标签¶](https://docs.djangoproject.com/zh-hans/3.2/howto/custom-template-tags/)

1. 在应用目录下创建 templatetags 文件夹，同时建立空文件 `__ init __.py` 和过滤器文件 例如 `custom_filter.py` 
2. 在 `custom_filter.py` 文件中添加过滤器


```python
from django import template
from blog.models import Category
# register 是 template.Library 的实例，是所有注册标签和过滤器的数据结构
register = template.Library()

# 自定义过滤器
@register.filter("sex")
def check_sex(sex): # 过滤器必须有一个以上的参数
    return "男" if int(sex) == 1 else "女"

@register.filter
def get_value(dic, key_name):
    return dic.get(key_name)

@register.filter
def get_attr(d, m):
    if hasattr(d, m):
        return getattr(d, m)
    
# 自定义标签
@register.simple_tag
def get_all_category
    return Category.objects.all()
```

**引用自定义过滤器时需要先导入再使用**

```html
{% load custom_filter %}
<html lang="en">
<body>
<h1>{{ articles|get_value:"article"|get_attr:"id" }}</h1>
    {% get_all_category as category_list %}
    <ul>
        {% for category in category_list %}
        <li>
                <a href="#">{{ category.name }}</a>
        </li>
        {% empty %}
        There is no category!
        {% endfor%}
    </ul>
</body>
</html>
```

最终所展现的效果是这样的(这边只放一部分效果，整体效果可以下载项目自行运行查看)

![使用过滤器添加分类列表](/images/2888797-484be5f05be72101.png)


[自定义模板的后端](https://docs.djangoproject.com/zh-hans/3.2/howto/custom-template-backend/)


#### 3.2.4 静态文件处理

静态文件主要包括我们需要用到的 css，js 文件等，使用静态文件我们只需要以下两步即可
1. 在应用目录下创建 static 文件夹，可以将常用的 css 文件，js 文件等放入该文件夹

2. 在需要引用静态文件的模版中做如下处理

```html
{# 引入静态文件，只有加载标签模版后才能使用 {% static %} 标签 #}
{% load staticfiles %}
{# 在需要引入的地方引入相应文件，例如在 static 文件夹下有个 blog 文件夹，需要引用其 #}
{# 中的 css/bootstrap.min.css 文件可以通过如下方式进行引入 #}
<link rel="stylesheet" href="{% static 'blog/css/bootstrap.min.css' %}">
```

### 3.3 基于类的通用视图

#### 3.3.1 基于类的视图 View

[基于类的视图](https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/)

[基于类的视图详解](https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/intro/)

[内置的基于类的通用视图](https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/generic-display/)

[Django 基于类的通用视图详解](https://blog.csdn.net/SL_World/article/details/83415971)

[【Django】基于类的视图Class Based View](https://blog.csdn.net/gongxifacai_believe/article/details/104077920)

类视图的声明必须继承于 `django.views.View`

类试图的方法名称都是固定的，如下[get,post,patch,put,delete]

每一个类视图都可以绑定一个路由，只要是这个类方法都会共用这个路由

```python

from django.http import HttpResponse
from django.views import View

class 功能+View(View):
    def get(self,request):
        # 响应http->get请求 -> 获取数据
        return  HttpResponse('result')
​
    def post(self,request):
        # post请求 -> 添加数据
        return  HttpResponse('result')
​
    def patch(self,request):
        # patch请求 -> 修改一个数据的单个属性(字段
        return  HttpResponse('result')
​
    def put(self,request):
        # put请求 -> 修改整个数据
        return  HttpResponse('result')
​
    def delete(self,request):
        # delete 请求 ->删除数据
        return  HttpResponse('result')
```

```python
#改造前
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyForm

def myview(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
    else:
        form = MyForm(initial={'key': 'value'})

    return render(request, 'form_template.html', {'form': form})

#改造后
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm

class MyFormView(View):
    form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
# urls.py

from django.urls import path
from django.contrib import admin
from django.views.decorators.csrf import  csrf_exempt
from test1 import views

urlpatterns = [
    path('useview',views.MyFormView.as_view()),
    path('useviewpara', csrf_exempt(views.useClassView.as_view(news='用指定属性值访问视图类'))),
]
```

Diango 在解析 URL时，如果URL与模式匹配，则调用相应的视图函数。在配置基于类的视图时，需将 URL 模式映射到视图类的 as_view()方法

Diango 处理视图类的基本步骤如下。

第一步: 执行 as_view()方法，创建一个类的实例。
第二步: 调用 setup0方法初始化实例的属性。
第三步: 调用 dispatch()方法，根据 HTTP 请求方式(GET或POST等)调用匹配的实例方法。如果没有匹配的实例方法，则返回 HttpResponseNotAllowed 响应。


#### 类的继承和覆盖

```python
from django.http import HttpResponse
from django.views.generic import View

# 类的继承
class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)

class MorningGreetingView(GreetingView):
    greeting = "Morning to ya"

# 类的覆盖
# urls.py
urlpatterns = [
    url(r'^about/', GreetingView.as_view(greeting="G'day")),
]

```



#### 3.3.2 TemplateView

TemplateView 扩展基类来使它能渲染模板。

```python
# some_app/views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"

# urls.py
from django.urls import path
from some_app.views import AboutView

urlpatterns = [
    path('about/', AboutView.as_view()),
]

```

使用装饰类

```python
decorators = [never_cache, login_required]

@method_decorator(decorators, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```

#### 3.3.3 使用 基于Mixin 的类视图

[在基于类的视图中使用 mixins](https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/mixins/)

#### 3.3.3 装饰类


```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class ProtectedView(TemplateView):
	template_name = 'secret.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ProtectedView, self).dispatch(*args, **kwargs)

```

#### 3.3.3 listView：使用多个 Django 对象


Multi object list view：多个对象的List View

model ：指定django 使用 模型
queryset ：查询集
get_queryset : 三者关系，与 Article.objects.all()  作用类似
content_object_name ：返回list
template_name ：`<app_label>/<model_name>_list.html`

1、model: 模型，在视图中设置model属性可以指定所需查询的模型类。
2、template_name: 模板名称，即渲染该视图时使用的模板文件。
3、context_object_name: 上下文变量名称，即在渲染模板时使用的上下文变量名，默认为object_list。
4、paginate_by: 分页大小，即每页显示的条目数。
5、ordering: 数据排序规则，可以根据某个字段进行排序。
6、get_queryset(): 获取查询集，可以通过这个方法来自定义查询集。
7、get_context_data(): 获取上下文数据，可以通过这个方法来添加其他的上下文变量。




ListView 的工作流程如下：

1、首先，我们需要定义一个继承自 ListView 的视图类，并指定要使用的模型类。例如，如果我们想要展示一个名为 Book 的模型类的列表，可以定义如下的视图类：

```Python
from django.views.generic import ListView
from .models import Book

class BookListView(ListView):
    model = Book
```

2、接着，我们需要在 urls.py 文件中将该视图类与对应的 URL 路径进行绑定。例如，如果我们想要将 BookListView 显示在路径 "/books/" 下，可以编写如下的代码：

```Python
from django.urls import path
from .views import BookListView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
]
```

3、当用户访问 "/books/" 路径时，Django 会自动调用 BookListView 的 get() 方法来处理请求。在 get() 方法中，ListView 会根据指定的模型类获取所有的对象实例，并将它们传递给模板进行渲染。

4、默认情况下，ListView 使用名为 "object_list" 的变量来传递模型实例列表到模板中。

我们可以通过定义 template_name 属性来指定要使用的模板文件，以及 context_object_name 属性来指定传递给模板的变量名。例如：

```Python
class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
```

5、在模板中，我们可以通过以下方式访问传递过来的模型实例列表：

```html
{% for book in books %}
    <div>{{ book.title }}</div>
{% endfor %}
```

- 其他示例

```python
# urls.py
from django.urls import path
from books.views import PublisherBookListView

urlpatterns = [
    path('books/<publisher>/', PublisherBookListView.as_view()),
]

# views.py
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from books.models import Book, Publisher

class PublisherBookListView(ListView):

    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['publisher'] = self.publisher
        return context
```




#### 3.3.4 DetailView：使用单个 Django 对象



[使用基于类的视图处理表单](https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/generic-editing/)

```python
from django.views.generic import DetailView
from books.models import Book, Publisher

class PublisherDetailView(DetailView):

    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()
        return context
```
[get_context_data解释](https://docs.djangoproject.com/zh-hans/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data)
将合并当前类的所有父类的上下文数据，返回用于显示对象的上下文数据。


```python
from django.views.generic import DetailView
from books.models import Publisher

class PublisherDetailView(DetailView):

    context_object_name = 'publisher'
    queryset = Publisher.objects.all()
```
指定 model = Publisher 只是 queryset = Publisher.objects.all() 的简写


**get_object** 来查找对象

```python
# urls.py
from django.urls import path
from books.views import AuthorDetailView

urlpatterns = [
    #...
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
# views.py
from django.utils import timezone
from django.views.generic import DetailView
from books.models import Author

class AuthorDetailView(DetailView):

    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj
```


#### 3.3.5 RedirectView 

用于 HTTP 重定向





#### 3.3.7 进阶

[在基于类的视图中使用混入](https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/mixins/)

[内置基于类的视图 API](https://docs.djangoproject.com/zh-hans/3.2/ref/class-based-views/)

[基于类的通用视图——扁平化索引](https://docs.djangoproject.com/zh-hans/3.2/ref/class-based-views/flattened-index/)

[装饰类视图：Django内置method_decorator](https://blog.csdn.net/JosephThatwho/article/details/101109514)

### 3.4 参考

#### 3.4.1 内置视图

https://docs.djangoproject.com/zh-hans/3.2/ref/views/

#### 3.4.2 request请求/响应对象

```python
request # <WSGIRequest: GET '/students/index'>
request.method #获取http请求方法， 用法： if request.method == 'POST':
request.path # 获取请求路径部分，不包含域名和查询字符串。用法：if request.path == '/about/':
request.path_info # 请求路径
request.get_port() # 返回请求的端口号
get_host()  # 返回请求的主机名。
get_full_path()  # 返回请求的完整路径，包括查询参数。
get_raw_uri()  # 返回未编码的请求URI

request.GET  #包含HTTP GET参数的字典，获取Query就是url?后的东西
request.GET.get("name", default=None)       # 根据指定的键获取一个值， "/search/?name=example"
request.GET.getlist()   # 根据指定的键获取所有值，以列表格式返回
request.GET.dict()      # 转化为原生字典(会去重)
request.GET.values() 
request.GET.setlist()

request.POST  # 包含HTTP POST参数的字典，只能获取表单数据 <QueryDict: {}>
request.POST.get('username')  # 获取Post请求的表单字段

request.data  # 主要用于接收以 JSON 或 XML 格式传递的数据

request.body  # 类型：字节串（bytes）, 作用：获取HTTP请求的原始主体内容。若是json 可能需要转码 data = json.loads(request.body)


request.headers  # 获取头部信息
request.headers.get("Company")

request.META   # 一个包含HTTP请求的元数据的字典，如HTTP头部信息和服务器变量等。
request.META.get('REMOTE_ADDR')

request.COOKIES  # 一个包含HTTP请求中所有cookie的字典。


request.FILES  # 获取上传文件
request.FILES.get('myfile')
request.session

request.scheme  # 返回 URL 的协议部分，通常是 "http" 或 "https"。用法： if request.scheme == 'https':

request.is_ajax()  # 判断当前请求是否为 Ajax 请求。 用法：if request.is_ajax():
is_secure()  # 如果请求是通过HTTPS协议发出，则返回True。

```
如果你在 Postman 中使用 "form-data" 或 "raw" 作为参数传递方式调用一个 POST 接口，你可以按照以下方式获取这些参数：

1、如果你使用 "form-data" 方式传递参数，可以通过读取 request.POST.get('参数名') 来获取具体字段的值。例如，如果你的参数中有一个字段名为 'username'，你可以使用 request.POST.get('username') 来获取对应的值。

2、如果你使用 "raw" 方式传递参数，通常可以选择不同的内容类型，如 JSON、XML 或纯文本。根据你选择的内容类型，你可以使用相应的方法从请求中获取数据。

- 如果你选择了 JSON 类型，在 Django REST Framework 等框架中，可以通过 request.data.get('参数名') 来获取 JSON 数据中指定字段的值。

- 如果你选择了 XML 类型，则需要使用相应的库来解析 XML，并从中提取所需的参数值。

- 如果你选择了纯文本类型（如普通字符串），可以使用 request.body 来获取整个请求主体的内容，然后根据需要进行解析和处理。

常用json 处理
```python
import json
body_dict = json.loads(request.body)
print(body_dict) 
```

https://docs.djangoproject.com/zh-hans/3.2/ref/request-response/

#### 3.4.3 TemplateResponse 对象

https://docs.djangoproject.com/zh-hans/3.2/ref/template-response/

### 3.5 文件上传

文件导入/上传

### 3.6 文件下载

#### HttpResponse类

HttpResponse类是Django中用于响应HTTP请求的主要类。它可以返回各种内容类型，如HTML、JSON、XML、文件等。


HttpResponse的常用参数说明

#### content_type 参数

content_type 参数指定了HTTP响应的内容类型（Content-Type），告诉客户端返回的内容是什么类型。常见的值包括：

对于普通文本内容：
text/plain 注意： 一般在使用‘text/plain’时，都会添加‘charset=utf-8’，否则是会乱码的。
text/html
text/css（css文件）
text/javascript（js文件）
text/csv（csv文件）


application/json（json文件）
application/xml（xml文件）

对于Excel文件：'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


对于下载文件：可以根据文件类型设置，如'application/octet-stream'

#### Content-Disposition 参数

Content-Disposition 是一个HTTP响应头，用于指示客户端如何处理响应体的内容。它通常用于下载文件时指定文件名。常见的用法包括：

attachment; filename=filename.ext：将响应作为附件下载，并指定文件名为 filename.ext
inline：将响应体直接显示在浏览器中，如果浏览器支持该内容类型的显示。

```python
from django.http import HttpResponse
import codecs  # 用于处理编码

# 创建一个HttpResponse对象
response = HttpResponse()

# 设置响应内容类型为Excel文件
response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

# 设置Content-Disposition为attachment，指定下载的文件名为exported_data.xlsx
response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'

# 如果需要在文件中写入 BOM (Byte Order Mark)，可以使用 codecs.BOM_UTF8
response.write(codecs.BOM_UTF8)

# 在这里写入Excel文件的内容，例如使用openpyxl库生成Excel内容，并将其写入response

# 最后返回response对象
return response
```

#### 常用方法

set_cookie：用来设置cookie信息
delete_cookie：用来删除cookie信息。
write：HttpResponse是一个类似于文件的对象，可以用来写入数据到数据体（content）中。

#### 使用 openpyxl等第三方库 手动生成Excel文件

##### 第三方库 csv

```python
import csv
from django.http import HttpResponse
from myapp.models import MyModel

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    file_name = "test.csv"
    response['Content-Disposition'] = 'attachment; filename={0}'.format(escape_uri_path(str(file_name)))

    writer = csv.writer(response)

    # 获取MyModel中的所有数据
    queryset = MyModel.objects.all()
    # 写入csv表头（即MyModel的字段名）
    writer.writerow([field.name for field in MyModel._meta.fields])
    # 逐行写入数据
    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in MyModel._meta.fields])

    return response
```

##### 第三方库 openpyxl

```bash
pip install openpyxl
```

```python
from openpyxl import Workbook
from django.http import HttpResponse

def export_to_excel(request):
    # 创建一个Workbook对象
    wb = Workbook()
    ws = wb.active

    # 查询数据并写入Excel
    queryset = MyModel.objects.all()
    for row_num, obj in enumerate(queryset, start=1):
        ws.cell(row=row_num, column=1, value=obj.field1)
        ws.cell(row=row_num, column=2, value=obj.field2)
        ws.cell(row=row_num, column=3, value=obj.field3)

    # 设置响应头
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'

    # 将Workbook保存到HttpResponse中
    wb.save(response)

    return response
```



##### 第三方库 django-excel

```bash
pip install django-excel
```

```python
from django.http import HttpResponse
from django_excel_to_response import ExcelResponse

def export_to_excel(request):
    # 查询数据
    data = MyModel.objects.all().values('field1', 'field2', 'field3')

    # 导出Excel
    return ExcelResponse(data, output_name='exported_data')

```

#### 使用 django-import-export 导入导出数据

可以参考django-import-export或django-csv-export的文档。

```bash
pip install django-import-export
```

```python
from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource

class MyModelResource(ModelResource):
    class Meta:
        model = MyModel
        fields = ('field1', 'field2', 'field3')

class MyModelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = MyModelResource

admin.site.register(MyModel, MyModelAdmin)

```


### 3.4 中间件

[中间件基础知识](https://www.runoob.com/django/django-middleware.htmlr)

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # 安全监测相关的中间件，防止页面过期，js跨站脚本攻击xss
    'django.contrib.sessions.middleware.SessionMiddleware',     # session加密和读取和保存session相关
    'django.middleware.common.CommonMiddleware',                # 通用中间件，用于给url进行重写
    'django.middleware.csrf.CsrfViewMiddleware',              # 防止网站遭到csrf攻击
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 用户认证的中间件
    'django.contrib.messages.middleware.MessageMiddleware',     # 错误提示信息的中间件【提示错误信息，一次性提示】
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # 用于防止点击劫持的攻击
]
```
[Django中间件实现操作日志记录](https://blog.csdn.net/weixin_42278281/article/details/119041163?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-119041163-blog-126116044.pc_relevant_multi_platform_whitelistv3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-119041163-blog-126116044.pc_relevant_multi_platform_whitelistv3&utm_relevant_index=2)



[在 Django Admin 中使用 LogEntry 监视用户操作](https://medium.datadriveninvestor.com/monitoring-user-actions-with-logentry-in-django-admin-8c9fbaa3f442)

[Django利用LogEntry生成历史操作实战记录](https://www.qetool.com/scripts/view/9764.html)



## 7. 小技巧

### 日志

https://docs.djangoproject.com/zh-hans/3.2/topics/logging/

### 分页

https://www.django.cn/article/show-34.html


https://docs.djangoproject.com/zh-hans/3.2/topics/pagination/

### 缓存


在 Django 中，可以通过缓存机制来减少接口请求的响应时间。Django 支持多种缓存后端，如 Memcached、Redis 和数据库等。以下是一个使用 Django 缓存的示例代码：

```python
from django.core.cache import cache

def get_data_from_db():
    # 从数据库中获取数据
    pass

def get_data():
    data = cache.get('data')
    if not data:
        data = get_data_from_db()
        cache.set('data', data, timeout=3600) # 设置缓存有效期为1小时
    return data
```
在这个示例代码中，get_data() 函数首先尝试从缓存中获取数据，如果缓存不存在，则从数据库中获取数据并将其缓存起来。cache.set() 方法用于设置缓存，timeout 参数指定缓存的有效期。

需要注意的是，缓存机制只适用于不经常变化的数据。如果数据经常变化，缓存会导致数据不一致。此外，在高并发的情况下，缓存可能会导致缓存雪崩问题，因此需要对缓存进行合理的配置和管理。

另外，Django 还提供了一些内置的缓存装饰器，如 cache_page 和 cache_control 等，可以方便地为视图函数添加缓存策略。例如：

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15) # 缓存该视图 15 分钟
def my_view(request):
    # 处理视图逻辑
    pass
```

这个示例代码使用了 cache_page 装饰器来为 my_view 视图函数添加缓存策略，缓存有效期为 15 分钟。需要注意的是，缓存装饰器只适用于视图函数，对于其他类型的接口需要手动调用缓存机制。

### 配置连接池

Django并没有默认的连接池技术，但可以通过第三方库实现连接池。下面以使用mysql-connector-python库为例介绍如何在Django中配置连接池技术。

1、安装mysql-connector-python库

可以使用pip安装mysql-connector-python库：pip install mysql-connector-python

2、配置连接池

在settings.py文件中添加如下配置项：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'pool_name': 'mypool',
            'pool_size': 5,
            'max_pool_size': 10,
            'min_pool_size': 5,
            'pool_reset_session': True,
            'max_conn_lifetime': 300,
            'connect_timeout': 30,
            'validate_query': 'SELECT 1',
            'charset': 'utf8mb4',
            'use_pure': True,
        },
    }
}
```

这里使用了mysql-connector-python库提供的连接池选项。

pool_name指定连接池的名称；
pool_size指定连接池的初始大小；
max_pool_size 指定连接池的最大容量；
min_pool_size 指定连接池的最小容量；
pool_reset_session 指定是否在每个连接请求之后重置会话状态；
max_conn_lifetime 指 最大连接生命周期为 300 秒，即连接使用超过 300 秒后会被回收
connect_timeout 指定连接超时时间；
validate_query 指定连接验证查询语句，测试数据库连接是否可用
charset指定字符集；
use_pure指定是否使用纯Python连接器。


设置了连接验证查询语句为 SELECT 1，SELECT 1 这个查询语句是一种比较常用的方式，因为它不涉及具体的表和字段，只需要检查数据库是否能够正确地处理这条简单的查询即可。

在 Django 中，如果你设置了连接验证查询语句为 SELECT 1，那么在获取连接时，Django 会先执行这条查询语句来测试连接的可用性。如果该查询能够成功执行并返回结果，那么就说明连接正常，可以被使用；否则就意味着连接出现了问题，需要进行相应的处理，例如重新建立连接或者从连接池中移除该连接等操作。


```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'poolclass': pool.QueuePool,
            'creator': pymysql,
            'maxconnections': 10,
            'mincached': 5,
            'maxcached': 10,
            'autocommit': True,
            'charset': 'utf8mb4',
            'use_unicode': True
        }
    }
}
```
poolclass: 指定连接池的类型。在这个示例中，我们使用了 QueuePool 类型。
creator: 指定创建连接的工厂方法。我们使用 pymysql。
maxconnections: 指定连接池中最大连接数。
mincached: 指定初始化时建立的空闲连接数。
maxcached: 指定连接池中最多允许的空闲连接数。
autocommit: 指定是否默认开启自动提交模式。
charset: 连接的字符集编码。在这个示例中，我们使用了 utf8mb4。
use_unicode: 指定是否使用 Unicode 编码。


3、使用连接池

在Django应用程序中，在需要访问数据库的地方，可以使用Django提供的ORM或原生SQL语句来访问数据库，连接池会自动管理和分配数据库连接。

```python
from django.db import connection

# 使用ORM查询

result = MyModel.objects.filter(name='test')

# 使用原生SQL查询

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM my_table")
    result = cursor.fetchall()
```

以上就是在Django中使用mysql-connector-python库实现连接池技术的方法。需要注意的是，不同的第三方库可能提供不同的连接池选项，具体使用方法请参考相应的文档。



### 信号(Signals)

[Django Signals之pre_save & post_save ，pre_delete & post_delete](https://blog.csdn.net/Lockey23/article/details/80805758)

[信号 官方文档](https://docs.djangoproject.com/zh-hans/3.2/ref/signals/ )

### Celery


### 国际化

### 安全

### 联动查询





## 6. Django Restful 接口编写 (django-rest-framework)

### 概念


### 6.1 序列类 serializers

#### 6.1.1 继承 serializers.Serializers 实现


#### 6.1.2 继承 serializers.ModelSerializer 实现

### 6.2 请求及响应 

#### 6.2.1 Ruquest

#### 6.2.2 Response




### 6.3 视图重构

#### 6.3.1 通过注解 @api_view 重构

```python
from rest_framework.decorators import api_view
@api_view(['POST','GET'])
def xx(request):
    pass
```

#### 6.3.2 通过类 APIView 重构
```python
from rest_framework.views import APIView

class xxxxx(APIView):

    def post(self, request):
        pass
```
APIView 是 Django 自带的基础视图类，只提供了基本的请求处理方法（如 get()、post() 等），需要自行编写请求参数解析、响应数据序列化等功能。
如果需要更高级的功能，比如认证、授权、限流等，需要自行实现或使用第三方库。


- **`@api_view` 和 `APIView`  的区别和优劣**

@api_view 和 APIView 都是 Django Rest Framework 中用于编写 Web API 视图的类或装饰器，它们之间的主要区别在于：

- @api_view 是一个装饰器，用于将基于函数的视图转换为 DRF 的 API 视图，从而可以使用 DRF 提供的请求解析、响应序列化等功能。与 APIView 不同，@api_view 基于函数的视图使用的是 HTTP 函数（如 GET()、POST() 等）来进行请求处理。
- APIView 则是一个类，继承自 Django 自带的 View 类，并针对 Web API 的场景进行了改进和扩展。与 @api_view 不同，APIView 依赖于类实例方法（如 get()、post() 等）来处理请求。

优劣方面，可以总结如下：

- @api_view 更加简单且易于使用，适合编写基础的 Web API，无需过多的配置和类定义。但是，其灵活性不如 APIView，难以实现一些高级功能。
- APIView 更加灵活，可以通过重写类方法来实现自定义逻辑，同时提供了更多的请求处理和响应生成方法。但是，相比 @api_view，开发成本稍高，需要更多的代码和类定义。

因此，选择使用 @api_view 还是 APIView 取决于您的具体需求。如果您需要编写简单的 Web API，可以使用 @api_view；如果您需要更灵活的功能和更好的扩展性，则可以选择使用 APIView。


#### 6.3.3 通过 mixins 和 generics 类重构

#### 6.3.4 通过通用视图类重构

#### 6.3.5 通过 ViewSet 和 Router 重构

### 6.4 权限及认证 Permissions&Authenricated




## 8. 报错

[Django 运行时出现 ModuleNotFoundError: No module named 'settings'](https://blog.csdn.net/qq_35526165/article/details/103359738)


## Linux项目上线

### Python安装配置

### MySQL安装配置

### redis安装配置

### git安装配置

### Nginx安装配置

### uwsgi安装

### supervisor安装配置

## Windows项目上线

### Python安装配置

### MySQL安装配置

### redis安装配置

### Apache安装配置

### Nssm安装配置



pymysql.err.OperationalError: (1040, 'Too many connections')

这个错误提示表明数据库连接数过多，需要优化接口来降低连接数。以下是一些可能的解决方法：

1、增加数据库最大连接数：可以在数据库配置文件中增加最大连接数，但这只是一个临时解决方案，并不是根本解决问题的方法。

2、减少接口请求频率：如果请求过于频繁，可以考虑减少请求频率或者增加缓存机制。

3、使用连接池：可以使用连接池技术来管理数据库连接，减少连接数并提高效率。

4、优化SQL查询语句：可以通过优化SQL查询语句来提高查询效率，使用索引、避免全表扫描、减少 JOIN 操作等方法可以优化 SQL 查询语句，从而减少连接数。

5、使用异步IO：使用异步IO可以减少等待时间，提高接口响应速度，从而减少连接数。



pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'172.16.3.33' (using password: YES)")

您可以使用以下命令为用户 'root'@'172.16.3.33' 授予访问MySQL数据库的权限：
```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.16.3.33' IDENTIFIED BY 'password';

flush privileges;
```

GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.16.3.33' IDENTIFIED BY 'kaadas168';


其中，'password'应替换为实际的密码。

如果您只想授予特定数据库的访问权限，而不是所有数据库，请将星号（*）替换为数据库名称。例如，如果要授予对名为test_db的数据库的访问权限，可以使用以下命令：
```sql
GRANT ALL PRIVILEGES ON test_db.* TO 'root'@'172.16.3.33' IDENTIFIED BY 'password';
flush privileges;
```
请注意，这些命令需要具有足够特权的帐户才能运行。因此，您需要以具有适当特权的用户身份登录到MySQL服务器。
