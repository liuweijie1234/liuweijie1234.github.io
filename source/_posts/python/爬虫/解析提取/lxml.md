---
title: 网页解析库 lxml
date: 2023-12-14 10:00:00
tags:
- [Python]
- [爬虫]
categories:
- [Python]
- [爬虫]
---




## 安装

```python
pip3 install lxml
```



## XPath常用规则


| 表达式 | 描述 |
| -- | -- |
| nodename | 选取此节点的所有子节点 |
| / | 从当前节点选取直接子节点 |
| // | 从当前节点选取子孙节点 |
| . | 选取当前节点 |
| .. | 选取当前节点的父节点 |
| @ | 选取属性 |
| * | 通配符，选择所有元素节点与元素名 |
| @* | 选取所有属性 |
| [@attrib] | 选取具有给定属性的所有元素 |
| [@attrib='value'] | 选取给定属性具有给定值的所有元素 |
| [tag] | 选取所有具有指定元素的直接子节点 |
| [tag='text'] | 选取所有具有指定元素并且文本内容是text节点 |


## 读取文本解析节点

```python
from lxml import etree

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">第一个</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0"><a href="link5.html">a属性</a>
     </ul>
 </div>
'''
html = etree.HTML(text)  # 初始化生成一个XPath解析对象
result = etree.tostring(html, encoding='utf-8')  # 解析对象输出代码
print(type(html))  # <class 'lxml.etree._Element'>
print(type(result))  # <class 'bytes'>
print(result.decode('utf-8'))

#etree会修复HTML文本节点
<html><body><div>
    <ul>
         <li class="item-0"><a href="link1.html">第一个</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0"><a href="link5.html">a属性</a>
     </li></ul>
 </div>
</body></html>
```


test.html的内容

```html
<div>
  <ul>
    <li class="item-0"><a href="link1.html">first item</a></li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-inactive"><a href="link3.html">third item</a></li>
    <li class="item-1"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
  </ul>
</div>
```


```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())  # 按照etree.HTMLParser()的解析方式 解析test.html文件
result = etree.tostring(html)
print(result.decode('utf-8'))
```



## 获取所有节点

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//*')  #//代表获取子孙节点，*代表获取所有
result_li =html.xpath('//li')  #获取所有子孙节点的li节点
print(result)
```


## 获取子节点

| 表达式 | 描述 |
| -- | -- |
| / | 从当前节点选取直接子节点 |
| // | 从当前节点选取子孙节点 |


```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a')  # 所有 li 节点的所有直接子节点 a

result1 = html.xpath('//ul//a')  # 获取 ul 节点下的所有子孙节点 a
print(result)
```



## 获取父节点

| 表达式 | 描述 |
| -- | -- |
| .. | 选取当前节点的父节点 |
| parent:: | 获取父节点 |

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//a[@href="link4.html"]/../@class')  # 选中 href 属性为 link4.html 的 a 节点，然后获取其父节点，再获取其 class 属性
#result = html.xpath('//a[@href="link4.html"]/parent::*/@class')
print(result)
```

## 属性匹配

| 表达式 | 描述 |
| -- | -- |
| @ | 选取属性 |
| * | 通配符，选择所有元素节点与元素名 |
| @* | 选取所有属性 |
| [@attrib] | 选取具有给定属性的所有元素 |
| [@attrib='value'] | 选取给定属性具有给定值的所有元素 |
| [tag] | 选取所有具有指定元素的直接子节点 |
| [tag='text'] | 选取所有具有指定元素并且文本内容是text节点 |

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]')  # 选取 class 为 item-0 的 li 节点
print(result)

```

## 文本获取


```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]/text()') #获取li下所有子节点的内容
result1=html.xpath('//li[@class="item-1"]//text()') #获取li下所有子孙节点的内容
result2 = html.xpath('//li[@class="item-0"]/a/text()')  # 选取了 li 节点，又利用 / 选取了其直接子节点 a，然后再选取其文本
print(result)
print(result1)
print(result2)
```


## 属性获取


使用@符号即可获取节点的属性

```python
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a/@href')  #获取所有li节点下所有a节点的href属性
result1 = html.xpath('//li//@href')  #获取所有li子孙节点的href属性
print(result)
```

## 属性多值匹配

如果某个属性的值有多个时，我们可以使用contains()函数来获取

```python
from lxml import etree
text = '''
<li class="li li-first"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)
result = html.xpath('//li[@class="li"]/a/text()')
result1 = html.xpath('//li[contains(@class, "li")]/a/text()')
print(result)
print(result1)

```

## 多属性匹配

可以使用 and、or、!= 等[**运算符**](https://www.w3school.com.cn/xpath/xpath_operators.asp) 来连接

```python
from lxml import etree
text = '''
<li class="li li-first" name="item"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
print(result)

```


## 按序选择


有时候，我们在选择的时候某些属性可能同时匹配多个节点，但我们只想要其中的某个节点，如第二个节点或者最后一个节点，

这时可以利用中括号引入索引的方法获取特定次序的节点：


```python
from lxml import etree

text1 = '''
<div>
    <ul>
         <li class="aaa" name="item"><a href="link1.html">第一个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第二个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第三个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第四个</a></li> 
     </ul>
 </div>
'''

html = etree.HTML(text1, etree.HTMLParser())
result = html.xpath('//li[contains(@class,"aaa")]/a/text()')  # 获取所有li节点下a节点的内容
result1 = html.xpath('//li[1][contains(@class,"aaa")]/a/text()')  # 获取第一个
result2 = html.xpath('//li[last()][contains(@class,"aaa")]/a/text()')  # 获取最后一个
result3 = html.xpath('//li[position()>2 and position()<4][contains(@class,"aaa")]/a/text()')  # 获取第一个
result4 = html.xpath('//li[last()-2][contains(@class,"aaa")]/a/text()')  # 获取倒数第三个

print(result)
print(result1)
print(result2)
print(result3)
print(result4)

#
['第一个', '第二个', '第三个', '第四个']
['第一个']
['第四个']
['第三个']
['第二个']
```

这里使用了last()、position()函数，在XPath中，提供了100多个函数，包括存取、数值、字符串、逻辑、节点、序列等处理功能

[函数使用说明](https://www.w3school.com.cn/xpath/xpath_functions.asp)


## 节点轴选择

XPath 提供了很多节点轴选择方法，包括获取子元素、兄弟元素、父元素、祖先元素等，示例如下：

```python
from lxml import etree


text1='''
<div>
    <ul>
         <li class="aaa" name="item"><a href="link1.html">第一个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第二个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第三个</a></li>
         <li class="aaa" name="item"><a href="link1.html">第四个</a></li> 
     </ul>
 </div>
'''

html=etree.HTML(text1,etree.HTMLParser())
result=html.xpath('//li[1]/ancestor::*')  # 获取所有祖先节点
result1=html.xpath('//li[1]/ancestor::div')  #获取div祖先节点
result2=html.xpath('//li[1]/attribute::*')  #获取所有属性值
result3=html.xpath('//li[1]/child::*')  #获取所有直接子节点
result4=html.xpath('//li[1]/descendant::a')  #获取所有子孙节点的a节点
result5=html.xpath('//li[1]/following::*')  #获取当前子节之后的所有节点
result6=html.xpath('//li[1]/following-sibling::*')  #获取当前节点的所有同级节点
```

更多轴的用法可以参考：http://www.w3school.com.cn/xpath/xpath_axes.asp