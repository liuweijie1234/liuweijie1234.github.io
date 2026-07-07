---
title: Python3 异步请求库 httpx
date: 2022-08-15 10:22:00
tags:
- Python module
- httpx
categories:
- Python
---


HTTPX 是 Python 3 的一个功能齐全的 HTTP 客户端，它提供同步和异步 API，并支持 HTTP/1.1 和 HTTP/2。

> 注意：httpx 要求 Python 版本 >=3.7。

### 安装

```bash
pip install httpx


pip install httpx[http2]
```


### 使用

主要用法与 requests 库类似, Client 对象与 requests 中的 Session对象类似

访问 HTTP/2 的网站

```python
import httpx

url = 'https://spa16.scrape.center/'

with httpx.Client(http2=True) as client:
    response = client.get(url=url)

    print(response.status_code)
    print(response.headers)
    print(response.text)
```


异步请求


```python
import httpx
import asyncio

async def fetch(url):
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url=url)
        print(response.status_code)


if __name__ == '__main__':
    url ='https://httpbin.org/get'
    asyncio.get_event_loop().run_until_complete(fetch(url))
```

FastAPI 支持 async def，你可以在API层面异步调用第三方接口，避免同步阻塞。

```python
from fastapi import FastAPI
import httpx

app = FastAPI()

async def fetch_api_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

@app.get("/data")
async def get_data():
    data = await fetch_api_data("https://third-party-api.com/data")
    return data

```

事件钩子

HTTPX允许您向客户端注册“事件挂钩”，每次发生特定类型的事件时都会调用这些挂钩。

目前有两个事件挂钩：

request-在请求完全准备好之后，但在将其发送到网络之前调用。已通过请求实例。
response-在从网络获取响应之后，但在将其返回给调用者之前调用。已通过响应实例。

这些允许您安装客户端范围的功能，如日志记录、监视或跟踪。


```python
def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = httpx.Client(event_hooks={'request': [log_request], 'response': [log_response]})

# 单独添加
client = httpx.Client()
client.event_hooks['request'] = [log_request]
client.event_hooks['response'] = [log_response, raise_on_4xx_5xx]

```

[案例:Python 异步爬虫获取豆瓣TOP250电影](https://gairuo.com/m/python-asyncio-douban-top250)


[httpx 模块教程](https://juejin.cn/post/6844904052707295246)