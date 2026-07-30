---
title: 网页解析库 pyquery
date: 2022-08-15 10:22:00
tags:
- [Python]
- [爬虫]
categories:
- [Python]
- [爬虫]
---


## 安装

```bash
pip3 install pyquery
```

[官方文档](https://pythonhosted.org/pyquery/)

[崔庆才 pyquery 文章](https://cuiqingcai.com/2636.html)

## 初始化

### 字符串初始化

```python
from pyquery import PyQuery as pq

html = '''
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
</div>
'''
doc = pq(html)
print(f'doc:{doc}')
print(f'type:{type(doc)}')
print(doc('li'))
```

### URL初始化

```python
from pyquery import PyQuery as pq

doc = pq(url="http://www.baidu.com", encoding='utf-8')
print(doc('head'))
```


### 文件初始化


```python
from pyquery import PyQuery as pq

doc = pq(filename='index.html')
print(doc)
```

## CSS选择器

```python
from pyquery import PyQuery as pq

html = '''
<ul id="container">
    <li class="wow fadeIn">
        <div class="d-flex latest-small-thumb">
            <div class="post-thumb d-flex mr-15 border-radius-10 img-hover-scale overflow-hidden">
                <a class="color-white" href="single.html" tabindex="0">
                    <img src="assets/imgs/news/thumb-11.jpg" alt="">
                </a>
            </div>
            <div class="post-content media-body align-self-center">
                <h5 class="post-title mb-15 text-limit-3-row font-medium">
                    <a href="single.html" tabindex="0">9 Things I Love About Shaving My Head During Quarantine</a>
                </h5>
            </div>
        </div>
    </li>
</ul>
'''

doc = pq(html)
print(doc('#container .fadeIn'))

```


## 节点选择器


### 查找子元素

```python
from pyquery import PyQuery as pq

html = '''
<ul id="container">
    <li class="wow fadeIn">
        <div class="d-flex latest-small-thumb">
            <div class="post-thumb d-flex mr-15 border-radius-10 img-hover-scale overflow-hidden">
                <a class="color-white" href="single.html" tabindex="0">
                    <img src="assets/imgs/news/thumb-11.jpg" alt="">
                </a>
            </div>
            <div class="post-content media-body align-self-center">
                <h5 class="post-title mb-15 text-limit-3-row font-medium">
                    <a href="single.html" tabindex="0">9 Things I Love About Shaving My Head During Quarantine</a>
                </h5>
            </div>
        </div>
    </li>
</ul>
'''

doc = pq(html)
items = doc('#container')
lis = items.find('li')
print(type(lis))
print(lis)
```

### 兄弟元素

```python
from pyquery import PyQuery as pq

html = '''
<ul id="container">
    <li class="wow fadeIn">
        <div class="d-flex latest-small-thumb">
            <div class="post-thumb d-flex mr-15 border-radius-10 img-hover-scale overflow-hidden">
                <a class="color-white" href="single.html" tabindex="0">
                    <img src="assets/imgs/news/thumb-11.jpg" alt="">
                </a>
            </div>
            <div class="post-content media-body align-self-center">
                <h5 class="post-title mb-15 text-limit-3-row font-medium">
                    <a href="single.html" tabindex="0">9 Things I Love About Shaving My Head During Quarantine</a>
                </h5>
            </div>
        </div>
    </li>
</ul>
'''

doc = pq(html)
div = doc('#container .post-thumb')
print(div.siblings())

```

### 获取属性

```python
from pyquery import PyQuery as pq

html = '''
<ul id="container">
    <li class="wow fadeIn">
        <div class="d-flex latest-small-thumb">
            <div class="post-thumb d-flex mr-15 border-radius-10 img-hover-scale overflow-hidden">
                <a class="color-white" href="single.html" tabindex="0">
                    <img src="assets/imgs/news/thumb-11.jpg" alt="">
                </a>
            </div>
            <div class="post-content media-body align-self-center">
                <h5 class="post-title mb-15 text-limit-3-row font-medium">
                    <a href="single.html" tabindex="0">9 Things I Love About Shaving My Head During Quarantine</a>
                </h5>
            </div>
        </div>
    </li>
</ul>
'''

doc = pq(html)
a = doc('#container .post-content a')
print(a)
print(a.attr('href'))
print(a.attr.href)
print(a.attr("id", "plop"))
print(a.attr("id", "hello"))


```

### 获取文本

```python
from pyquery import PyQuery as pq

html = '''
<ul id="container">
    <li class="wow fadeIn">
        <div class="d-flex latest-small-thumb">
            <div class="post-thumb d-flex mr-15 border-radius-10 img-hover-scale overflow-hidden">
                <a class="color-white" href="single.html" tabindex="0">
                    <img src="assets/imgs/news/thumb-11.jpg" alt="">
                </a>
            </div>
            <div class="post-content media-body align-self-center">
                <h5 class="post-title mb-15 text-limit-3-row font-medium">
                    <a href="single.html" tabindex="0">9 Things I Love About Shaving My Head During Quarantine</a>
                </h5>
            </div>
        </div>
    </li>
</ul>
'''

doc = pq(html)
a = doc('#container .post-content a').text()
print(a)
```

## 类操作

```python
from pyquery import PyQuery as pq

html = '''
<ul id="container">
    <li class="wow fadeIn">
        <div class="d-flex latest-small-thumb">
            <div class="post-thumb d-flex mr-15 border-radius-10 img-hover-scale overflow-hidden">
                <a class="color-white" href="single.html" tabindex="0">
                    <img src="assets/imgs/news/thumb-11.jpg" alt="">
                </a>
            </div>
            <div class="post-content media-body align-self-center">
                <h5 class="post-title mb-15 text-limit-3-row font-medium">
                    <a href="single.html" tabindex="0">9 Things I Love About Shaving My Head During Quarantine</a>
                </h5>
            </div>
        </div>
    </li>
</ul>
'''

doc = pq(html)
li = doc('#container li')
print(li)
li.removeClass('fadeIn')
print(li)
li.addClass('fadeIn')
print(li)
li.css('font-size', '16px')
print(li)
li.css({'background-color': 'yellow'})
print(li)
```