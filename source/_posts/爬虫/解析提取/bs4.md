---
title: 网页解析库 BeautifulSoup4
date: 2023-12-15 10:00:00
tags:
- [Python]
- [爬虫]
categories:
- [Python]
- [爬虫]
---

## 安装


```
pip3 install beautifulsoup4
```

[官方文档](https://beautifulsoup.readthedocs.io/zh-cn/latest/)

## 节点选择器


### 选择元素

```python
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'lxml')
print(soup.title)
print(type(soup.title))
print(soup.title.string)
print(soup.head)
print(soup.p)
print(type(soup.p))
```

### 提取节点信息

- 获取节点名称

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'lxml')
tag = soup.b
print(tag.name)
```

- 获取节点属性

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="Dormouse"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.p.attrs)
print(soup.p.attrs['name'])
```

- 获取节点内容

如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。

如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'lxml')
tag = soup.b
print(tag.string)
```

.strings 获取多个内容


```python
for string in soup.strings:
    print(repr(string))
```

.stripped_strings 获取多个内容（除多余空白或者换行内容）


### 获取子节点

获取子节点也可以理解为嵌套选择，我们知道在一个节点中可能包含其他的节点

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="Dormouse"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.head.title)
print(soup.head.title.string)
```

### 关联选择


#### 选取子节点和子孙节点

- 获取子节点

可以调用**contents**属性，将 tag 的子节点以列表的方式输出

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="Dormouse"><b>The Dormouse's story</b></p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.p.contents)
```

可以调用**children**属性，将 tag 的子节点 以 list 生成器对象输出

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(list(soup.p.children))
for i in soup.p.children:
    print(i)
```

- 获取子孙节点

可以调用**descendants**属性

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><span>Elsie</span>Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.p.descendants)
for child in soup.p.descendants:
    print(child)
```

#### 父节点和祖先节点

- 获取父节点

可以直接调用**parent**属性

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>

<p class="story">
Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
<p>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
</p>
</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.a.parent)
```

- 获取祖先节点

可以调用**parents**属性，递归得到元素的所有父辈节点

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>

<p class="story">
Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
<p>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
</p>
</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.a.parents)
for i, parent in enumerate(soup.a.parents):
    print(i, parent)
```
#### 兄弟节点

可以使用 next_sibling、previous_sibling、next_siblings、previous_siblings 这四个属性

兄弟节点可以理解为和本节点处在统一级的节点，.next_sibling 属性获取了该节点的下一个兄弟节点，.previous_sibling 则与之相反，如果节点不存在，则返回 None 

注意：实际文档中的 tag 的 .next_sibling 和 .previous_sibling 属性通常是字符串或空白，因为空白或者换行也可以被视作一个节点，所以得到的结果可能是空白或者换行

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>


<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>hello
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.a.next_sibling)
print(list(soup.a.next_siblings))
print(soup.a.previous_sibling)
print(list(soup.a.previous_siblings))

```

.next_siblings 和 .previous_siblings 属性可以对当前节点的兄弟节点迭代输出


```python
for sibling in soup.a.next_siblings:
    print(repr(sibling))
```

- 前后节点

通过 .next_elements 和 .previous_elements 的迭代器就可以向前或向后访问文档的解析内容，就好像文档正在被解析一样


```python
for element in last_a_tag.next_elements:
    print(repr(element))
```



## 方法选择器

参考文档: https://cuiqingcai.com/1319.html

### find_all()


```python
find_all( name , attrs , recursive , text , **kwargs )
```

name 参数 name 参数可以查找所有名字为 name 的 tag, 字符串对象会被自动忽略掉 


传字符串 最简单的过滤器是字符串。在搜索方法中传入一个字符串参数，Beautiful Soup 会查找与字符串完整匹配的内容，下面的例子用于查找文档中所有的标签

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="Dormouse"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.find_all('a'))
print(len(soup.find_all('a')))
```
传正则表达式 如果传入正则表达式作为参数，Beautiful Soup 会通过正则表达式的 match () 来匹配内容。下面例子中找出所有以 b 开头的标签，这表示 和标签都应该被找到

```python
import re
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
```

传列表 如果传入列表参数，Beautiful Soup 会将与列表中任一元素匹配的内容返回。下面代码找到文档中所有标签和标签

```python
soup.find_all(["a", "b"])
# [<b>The Dormouse's story</b>,
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```


```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="Dormouse"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><span>Elsie</span></a>,
<a href="http://example.com/lacie" class="sister" id="link2"><span>Lacie</span></a> and
<a href="http://example.com/tillie" class="sister" id="link3"><span>Tillie</span></a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.find_all(attrs={'id': 'link1'}))
print(soup.find_all(attrs={'name': 'Dormouse'}))

print(soup.find_all(class_ = 'sister'))
print(soup.find_all(id = 'link2'))
```

### find()

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="Dormouse"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><span>Elsie</span></a>,
<a href="http://example.com/lacie" class="sister" id="link2"><span>Lacie</span></a> and
<a href="http://example.com/tillie" class="sister" id="link3"><span>Tillie</span></a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.find(name='a'))
print(type(soup.find(name='a')))

```

find ( )方法返回第一个a节点的元素，类型是Tag类型

### 其他方法

find_parents() 和find_parent()：前者返回所有祖先节点，后者返回直接父节点。

find_next_siblings()和find_next_sibling()：前者返回后面的所有兄弟节点，后者返回后面第一个兄弟节点。

find_previous_siblings() 和 find_previous_sibling()：前者返回前面的所有兄弟节点，后者返回前面第一个兄弟节点。


## CSS选择器

使用CSS选择器的时候，需要调用select( ) 方法，将属性值或者是节点名称传入选择器即可

```python
from bs4 import BeautifulSoup

html_doc = """
<div class="panel">
    <div class="panel-heading">
        <h4>Hello World</h4>   
    </div>
    
    <div class="panel-body">
        <ul class="list" id="list-1">
           <li class="element">Foo</li>
           <li class="element">Bar</li>
           <li class="element">Jay</li>
        </ul>
        
        <ul class="list list-samll" id="list-2">
           <li class="element">Foo</li>
           <li class="element">Bar</li>
           <li class="element">Jay</li>
        </ul>
    </div>
    </div>
</div>
"""

soup = BeautifulSoup(html_doc, 'lxml')
print(soup.select('.panel .panel-heading')) # 获取class为panel-heading的节点
print(soup.select('ul li')) # 获取ul下的li节点
print(soup.select('#list-2 li')) # 获取id为list-2下的li节点
print(soup.select('ul'))    # 获取所有的ul节点
print(type(soup.select('ul')[0]))

```

### 嵌套选择

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'lxml')
for ul in soup.select('ul'):
    print(ul.select('li'))
```

### 获取属性

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'lxml')
for ul in soup.select('ul'):
    print(ul['id'])
    print(ul.attrs['id'])
```

### 获取文本

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'lxml')
for li in soup.select('li'):
    print('String:', li.string)
    print('get text:', li.get_text())
```


## 案例


### 爬取B站弹幕


```python
import requests
from bs4 import BeautifulSoup


class DanMu(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
        }
        self.url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=276746872'

    # 获取网页信息
    def get_html(self):
        response = requests.get(self.url, headers=self.headers)
        html = response.content.decode('utf-8')
        return html

    # 保存弹幕
    def get_info(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        file = open('弹幕.txt', 'w', encoding='utf-8')
        for d in soup.find_all(name='d'):
            danmu = d.string
            file.write(danmu)
            file.write('\n')



if __name__ == '__main__':
    danmu = DanMu()
    danmu.get_info()

```


### 爬取软科大学排名

https://www.shanghairanking.cn/
这是“最好大学网站”中各所大学的排名信息,我们要从中爬取排名、地区、大学名称和总分等信息。

功能描述

- 输入：大学排名url链接
- 输出：大学排名信息的输出，包括排名、地区、大学名称和总分
- 技术路线：requests库 + bs4库
- 定向爬虫：仅对输入url进行爬取，不扩展爬取

程序设计

- 从网页上获取大学排名网页内容，构造get_html()函数
- 提取网页内容中所需信息，构造parse_html()函数
- 按照指定格式输出结果，构造print_univlist()函数
- 调用上述三个函数，输出大学排名信息


代码实现

通过查看网页代码，发现符合这些特点:

所有大学的信息都在tbody标签下 , 每一个大学的信息标签都在tr标签下，排名、地区、大学名称和总分在td标签下 。

```python
import requests
import bs4
from bs4 import BeautifulSoup

# 构造网页内容获取函数
def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

# 构造获取大学排名信息, 提取html中的关键信息加到ulist中
def parse_html(ulist, html):
    soup = BeautifulSoup(html, "html.parser")  # 创建BeautifulSuop对象
    #首先找到tbody ,找到所有大学的相关信息，并遍历tbody的孩子标签
    for tr in soup.find('tbody').children:
        # 过滤tr的类型
        if isinstance(tr, bs4.element.Tag):
            # 找到每一所大学的所有td标签
            tds = tr.find_all('td')
            univ = {
                'num': tds[0].string,    # 排名
                'name': tds[1].string,   # 大学名称
                'area': tds[2].string,   # 地区
                'score': tds[3].string   # 总分
            }
            ulist.append(univ)

# 构造输出函数
def print_univlist(ulist):
    #格式化输出 chr(12288)，中文填充
    x = chr(12288)
    tplt = "{0:<10}\t{1:{4}<15}\t{2:<10}\t{3:<10}"
    print(tplt.format('排名', '学校名称', '地区', '总分',chr(12288)))
    for i in ulist:
        print(tplt.format(i['num'], i['name'], i['area'], i['score'],chr(12288)))

uinfo = []
url = "http://zuihaodaxue.com/Greater_China_Ranking2019_0.html"
html = get_html(url)
parse_html(uinfo, html)
print_univlist(uinfo)

```

