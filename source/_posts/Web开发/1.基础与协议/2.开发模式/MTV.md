

### 在 Django 中，什么是 MTV（Model - Template - View）架构？请解释每个部分的作用。

- **Model（模型）** ：
Model 是数据模型，用于定义数据的结构和关系，对应数据库中的表。它使用 Django 的模型类来创建，例如：

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publish_date = models.DateField()
```
这里定义了一个 Book 模型，对应数据库中的 book 表，包含 title（书名）、author（作者）和 publish_date（出版日期）三个字段。

- **Template（模板）** ：
- 
模板是用于定义网页结构和样式的文件，它将数据和 HTML 结构分离。Django 模板使用模板语言来动态地插入数据。
例如，一个简单的模板文件（book_list.html）：
```HTML
<!DOCTYPE html>
<html>
<head>
    <title>Book List</title>
</head>
<body>
    <h1>Book List</h1>
    <ul>
        {% for book in book_list %}
            <li>{{ book.title }} - {{ book.author }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```
在这个模板中，{% for book in book_list %} 是循环语句，用于遍历 book_list 变量中的书籍对象，并将书名和作者插入到 HTML 中。

- **View（视图）** ：
视图是处理用户请求并返回响应的函数或类。它从模型获取数据，并将数据传递给模板进行渲染。例如：

```python
from django.shortcuts import render
from .models import Book

def book_list_view(request):
    book_list = Book.objects.all()
    return render(request, 'book_list.html', {'book_list': book_list})
```
这里的 book_list_view 函数是一个视图，它从数据库中获取所有书籍对象（Book.objects.all()），然后将这些对象传递给 book_list.html 模板，并返回渲染后的 HTML 响应。
