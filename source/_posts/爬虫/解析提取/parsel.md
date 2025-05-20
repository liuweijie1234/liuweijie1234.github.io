---
title: 网页解析库 parsel
date: 2023-12-19 10:22:00
tags:
- [Python]
- [爬虫]
categories:
- [Python]
- [爬虫]
---


## 简介

parsel 这个库可以对 HTML 和 XML 进行解析，并支持使用 XPath 和 CSS Selector 对内容进行提取和修改，同时它还融合了正则表达式提取的功能。

功能灵活而又强大，同时它也是 Python 最流行爬虫框架 Scrapy 的底层支持。

参考 https://cuiqingcai.com/202232.html

## 安装


```bash
pip3 install parsel
```

## 初始化


```python
from parsel import Selector

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

selector = Selector(text=html)  # 创建了一个 Selector 对象，传入了 text 参数

items = selector.css('.item-0')
print(len(items), type(items), items)  # 
items2 = selector.xpath('//li[contains(@class, "item-0")]')
print(len(items2), type(items), items2)
```


## 提取文本

```python
from parsel import Selector
selector = Selector(text=html)
items = selector.css('.item-0')
for item in items:
    text = item.xpath('.//text()').get()
    print(text)

result = selector.xpath('//li[contains(@class, "item-0")]//text()').get()  # get()返回第一个对应节点内容
print(result)

result = selector.xpath('//li[contains(@class, "item-0")]//text()').getall()  # getall()提取全部对应节点内容
print(result)

result = selector.css('.item-0 *::text').getall()
print(result)
```


## 提取属性



```python
from parsel import Selector

selector = Selector(text=html)
result = selector.css('.item-0.active a::attr(href)').get()
print(result)
result = selector.xpath('//li[contains(@class, "item-0") and contains(@class, "active")]/a/@href').get()
print(result)

```

## 正则提取


```python
from parsel import Selector
selector = Selector(text=html)
result = selector.css('.item-0').re('link.*')  # re 方法 提取所有符合的数据
print(result)
result = selector.css('.item-0 *::text').re('.*item')
print(result)
result = selector.css('.item-0').re_first('<span class="bold">(.*?)</span>')  # re_first 方法来提取第一个符合规则
print(result)
```