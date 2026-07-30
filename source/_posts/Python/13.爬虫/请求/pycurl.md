---
title: Python3 pycurl（libcurl 绑定）
date: 2026-07-30 10:00:00
tags:
- Python
- 爬虫
categories:
- Python
---

## 说明

`pycurl` 是 C 库 libcurl 的 Python 绑定，性能好、可控项极多（底层 TCP/TLS 细节），但 API 偏底层、写法繁琐。
常见使用场景：需要精细控制连接行为、测量各阶段耗时、复用 curl 命令经验。

```bash
pip install pycurl
# macOS 若编译失败，通常需要先安装 openssl 并设置编译环境变量
```

## GET 请求

```python
import pycurl
from io import BytesIO

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, "https://httpbin.org/get")
c.setopt(c.WRITEDATA, buffer)                       # 响应体写入 buffer
c.setopt(c.HTTPHEADER, ["User-Agent: Mozilla/5.0"])
c.setopt(c.FOLLOWLOCATION, True)                    # 跟随重定向
c.setopt(c.TIMEOUT, 10)
c.perform()

print(c.getinfo(c.RESPONSE_CODE))                   # 200
c.close()

body = buffer.getvalue().decode("utf-8")
print(body)
```

## POST 请求

```python
import pycurl, json
from io import BytesIO
from urllib.parse import urlencode

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, "https://httpbin.org/post")

# 表单
c.setopt(c.POSTFIELDS, urlencode({"user": "tom"}))

# JSON
# c.setopt(c.HTTPHEADER, ["Content-Type: application/json"])
# c.setopt(c.POSTFIELDS, json.dumps({"user": "tom"}))

c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()
```

## 代理与耗时统计

```python
c.setopt(c.PROXY, "http://127.0.0.1:7890")

c.perform()
c.getinfo(c.NAMELOOKUP_TIME)      # DNS 耗时
c.getinfo(c.CONNECT_TIME)         # TCP 连接耗时
c.getinfo(c.APPCONNECT_TIME)      # TLS 握手完成
c.getinfo(c.STARTTRANSFER_TIME)   # 首字节时间 TTFB
c.getinfo(c.TOTAL_TIME)           # 总耗时
```

## 与 requests 对比

| 项 | pycurl | requests |
| --- | --- | --- |
| 性能 | 高（C 实现） | 一般 |
| API | 底层、繁琐 | 简洁 |
| 安装 | 依赖系统 libcurl，可能编译失败 | 纯 Python，简单 |
| 适用 | 高性能采集、精细控制、耗时分析 | 绝大多数日常场景 |
