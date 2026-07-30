---
title: Python3 pyhttpx（TLS 指纹请求库）
date: 2026-07-30 10:00:00
tags:
- Python
- 爬虫
categories:
- Python
---

## 说明

`pyhttpx` 是一个国产的 HTTP 请求库，特点是**自实现 TLS 握手层，可以模拟浏览器的 TLS/JA3 指纹**，用于绕过基于 TLS 指纹的反爬（此类站点用 requests 会直接被拒绝或返回异常页面）。

```bash
pip install pyhttpx
```

- 项目地址：https://github.com/zero3301/pyhttpx
- API 风格与 requests 类似，迁移成本低。

## 基本用法

```python
import pyhttpx

# 默认即带浏览器风格 TLS 指纹
session = pyhttpx.HttpSession()

resp = session.get(
    "https://tls.peet.ws/api/all",       # 该站点可回显你的 TLS 指纹
    headers={"User-Agent": "Mozilla/5.0"},
)
print(resp.status_code)
print(resp.text)
```

## POST 与代理

```python
import pyhttpx

session = pyhttpx.HttpSession()

# 表单 / JSON
resp = session.post("https://httpbin.org/post", data={"a": 1})
resp = session.post("https://httpbin.org/post", json={"a": 1})

# 代理
resp = session.get(
    "https://httpbin.org/ip",
    proxies={"https": "127.0.0.1:7890"},
)
```

## 同类工具对比

| 库 | 说明 |
| --- | --- |
| `curl_cffi` | 绑定 curl-impersonate，模拟 Chrome/Firefox 指纹，社区活跃度高 |
| `tls_client` | Go tls-client 的 Python 绑定 |
| `requests_go` | 基于 Go 的 TLS 指纹请求库 |
| `pyhttpx` | 纯 Python 实现 TLS 层 |

> 实践建议：优先尝试 `curl_cffi`（见 {% post_link Python/13.爬虫/请求/curl_cffi %}），无法解决时再对比其他库的指纹效果。
