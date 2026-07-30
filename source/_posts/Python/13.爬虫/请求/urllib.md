---
title: Python3 urllib（标准库 HTTP 客户端）
date: 2026-07-30 10:00:00
tags:
- Python
- 爬虫
categories:
- Python
---

## 说明

`urllib` 是 Python 标准库中的 HTTP 工具包，无需安装，包含 4 个子模块：

- `urllib.request`：发送请求
- `urllib.parse`：URL 解析与编码
- `urllib.error`：异常定义
- `urllib.robotparser`：解析 robots.txt

实际项目中一般用 `requests`/`httpx`（API 更友好），urllib 适合无法安装第三方库的环境。

## GET 请求

```python
from urllib import request, parse

url = "https://httpbin.org/get?" + parse.urlencode({"wd": "python"})
req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with request.urlopen(req, timeout=10) as resp:
    print(resp.status)                        # 200
    print(resp.getheader("Content-Type"))
    html = resp.read().decode("utf-8")        # 返回 bytes，需手动 decode
```

## POST 请求

```python
from urllib import request, parse
import json

# 表单提交：data 需为 bytes
data = parse.urlencode({"user": "tom"}).encode("utf-8")
req = request.Request("https://httpbin.org/post", data=data, method="POST")

# JSON 提交
data = json.dumps({"user": "tom"}).encode("utf-8")
req = request.Request(
    "https://httpbin.org/post", data=data,
    headers={"Content-Type": "application/json"},
)
with request.urlopen(req) as resp:
    print(json.loads(resp.read()))
```

## 异常处理

```python
from urllib import request, error

try:
    resp = request.urlopen("https://httpbin.org/status/404", timeout=5)
except error.HTTPError as e:      # 4xx/5xx
    print(e.code, e.reason)
except error.URLError as e:       # 网络不通、DNS 失败、超时等
    print(e.reason)
```

## 使用代理 / Cookie

```python
from urllib import request
from http.cookiejar import CookieJar

# 代理
proxy_handler = request.ProxyHandler({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
})

# Cookie 自动管理
cookie_handler = request.HTTPCookieProcessor(CookieJar())

opener = request.build_opener(proxy_handler, cookie_handler)
resp = opener.open("https://httpbin.org/get")
```

## 下载文件

```python
from urllib import request
request.urlretrieve("https://httpbin.org/image/png", "demo.png")
```
