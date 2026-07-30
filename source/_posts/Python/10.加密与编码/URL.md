---
title: Python3 URL 编码与解析（urllib.parse）
date: 2026-07-30 10:00:00
tags:
- Python
- 编码
categories:
- Python
---

## 说明

URL 中只允许出现字母、数字和少数符号，中文、空格等字符需要进行**百分号编码（URL 编码）**。
Python 标准库 `urllib.parse` 提供了编码、解码和 URL 解析能力。

## quote / unquote：编码与解码

```python
from urllib.parse import quote, unquote

quote("python 爬虫")
# 'python%20%E7%88%AC%E8%99%AB'

quote("a/b/c")            # 默认不编码 '/'
# 'a/b/c'
quote("a/b/c", safe="")   # safe 指定不编码的字符，置空则全部编码
# 'a%2Fb%2Fc'

unquote("python%20%E7%88%AC%E8%99%AB")
# 'python 爬虫'
```

`quote_plus / unquote_plus` 会把空格转成 `+`（表单编码风格）：

```python
from urllib.parse import quote_plus
quote_plus("python 爬虫")   # 'python+%E7%88%AC%E8%99%AB'
```

## urlencode：字典转查询字符串

```python
from urllib.parse import urlencode

params = {"wd": "python", "page": 2}
urlencode(params)   # 'wd=python&page=2'

url = "https://www.baidu.com/s?" + urlencode(params)
```

## parse_qs / parse_qsl：查询字符串转字典

```python
from urllib.parse import parse_qs, parse_qsl

parse_qs("wd=python&page=2")
# {'wd': ['python'], 'page': ['2']}

parse_qsl("wd=python&page=2")
# [('wd', 'python'), ('page', '2')]
```

## urlparse / urlsplit：拆解 URL

```python
from urllib.parse import urlparse

r = urlparse("https://example.com:8080/path/index.html?id=1#top")
# ParseResult(scheme='https', netloc='example.com:8080',
#             path='/path/index.html', params='', query='id=1', fragment='top')
r.scheme, r.netloc, r.path, r.query
```

## urljoin：拼接相对链接（爬虫常用）

```python
from urllib.parse import urljoin

urljoin("https://example.com/a/b.html", "c.html")
# 'https://example.com/a/c.html'

urljoin("https://example.com/a/", "/static/img.png")
# 'https://example.com/static/img.png'
```
