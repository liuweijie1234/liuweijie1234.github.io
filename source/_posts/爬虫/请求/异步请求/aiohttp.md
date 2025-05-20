---
title: Python3 异步请求库 aiohttp
date: 2024-02-23 10:00:00
tags:
- Python
- aiohttp
categories:
- Python
---

aiohttp 是基于 asyncio (opens new window)实现的异步 HTTP 客户端/服务端，可用于实现异步爬虫。

https://cuiqingcai.com/202272.html


### httpx 和 aiohttp 有什么区别和优缺点


HTTPX和AIOHTTP都是用于Python的HTTP客户端库，它们都支持异步编程，但在某些方面有所不同。

HTTPX是一个功能丰富的HTTP客户端，支持同步和异步编程，提供了对HTTP/2协议的支持，以及自动解码JSON和其他常见格式的功能。
HTTPX还提供了对流式响应的支持，适用于需要下载大量数据的场景。它的API设计更加现代化，易于使用，并且性能良好。

AIOHTTP是专门为异步程序设计的HTTP客户端，构建在asyncio库之上，支持async/await语法。
它适用于已经熟悉asyncio并希望使用轻量级库进行HTTP请求的开发者。
AIOHTTP同样提供了对HTTP请求的支持，包括异步GET和POST请求等。

两者的区别在于HTTPX提供了更丰富的功能和更现代化的API设计，支持同步和异步编程，
而AIOHTTP则更专注于提供简单高效的API，适用于异步编程环境。

选择使用哪个库取决于开发者的具体需求和项目要求。

总的来说，HTTPX适用于更广泛的项目范围，而AIOHTTP则更适合在异步项目中使用，并且在性能方面表现出色。

### 基本使用

```python
import aiohttp
import asyncio  # aiohttp需要asyncio库

async def fetch(session, url):  # async 声明函数为异步函数
    async with session.get(url) as response:  # async 代表支持异步上下文管理器
        return await response.text(), response.status  # 返回协程对象的操作需要加 await

async def main():
    async with aiohttp.ClientSession() as session:
        html, status = await fetch(session, 'https://cuiqingcai.com')
        print(f'html: {html[:100]}...')
        print(f'status: {status}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```


```python
import aiohttp
from app.config import THIRD_PARTY_API_URL, API_KEY

async def request_third_party_api(params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            THIRD_PARTY_API_URL,
            json={"api_key": API_KEY, **params}
        ) as response:
            return await response.json()

async def query_third_party_result(task_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{THIRD_PARTY_API_URL}/result/{task_id}",
            params={"api_key": API_KEY}
        ) as response:
            return await response.json()
```


### URL参数设置

类似于requests库中的params参数，aiohttp也提供了params参数，用于设置URL参数。

```python
import aiohttp
import asyncio

async def main():
    params = {'name': 'germey', 'age': 25}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get', params=params) as response:
            print(await response.text())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### 其他HTTP方法

aiohttp也提供了其他HTTP方法的请求，包括GET、POST、PUT、DELETE、HEAD、OPTIONS、PATCH等。

```python
session.post('http://httpbin.org/post', data=b'data')
session.put('http://httpbin.org/put', data=b'data')
session.delete('http://httpbin.org/delete')
session.head('http://httpbin.org/get')
session.options('http://httpbin.org/get')
session.patch('http://httpbin.org/patch', data=b'data')
```

### POST请求

```python
import aiohttp
import asyncio

async def main():
    data = {'name': 'germey', 'age': 25}
    async with aiohttp.ClientSession(trust_env=False) as session:
        # 表单提交
        async with session.post('https://httpbin.org/post', data=data) as response:
            print(await response.text())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
'''
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "age": "25",
    "name": "germey"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "18",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "httpbin.org",
    "User-Agent": "Python/3.7 aiohttp/3.6.2",
    "X-Amzn-Trace-Id": "Root=1-5e85f0b2-9017ea603a68dc285e0552d0"
  },
  "json": null,
  "origin": "17.20.255.58",
  "url": "https://httpbin.org/post"
}
'''

async def main():
    data = {'name': 'germey', 'age': 25}
    async with aiohttp.ClientSession() as session:
        # JSON提交
        async with session.post('https://httpbin.org/post', json=data) as response:
            print(await response.text())

'''
{
  "args": {},
  "data": "{\"name\": \"germey\", \"age\": 25}",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "29",
    "Content-Type": "application/json",
    "Host": "httpbin.org",
    "User-Agent": "Python/3.7 aiohttp/3.6.2",
    "X-Amzn-Trace-Id": "Root=1-5e85f03e-c91c9a20c79b9780dbed7540"
  },
  "json": {
    "age": 25,
    "name": "germey"
  },
  "origin": "17.20.255.58",
  "url": "https://httpbin.org/post"
}
'''
```


### 响应

对于响应来说，我们可以用如下方法分别获取响应的状态码、响应头、响应体、响应体二进制内容、响应体 JSON 结果，示例如下：

```python
import aiohttp
import asyncio

async def main():
    data = {'name': 'germey', 'age': 25}
    async with aiohttp.ClientSession(trust_env=False) as session:
        async with session.post('https://httpbin.org/post', data=data) as response:
            print('status:', response.status)
            print('headers:', response.headers)
            print('body:', await response.text())
            print('bytes:', await response.read())
            print('json:', await response.json())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

```

这里我们可以看到有些字段前面需要加 await，有的则不需要。其原则是，如果它返回的是一个 coroutine 对象（如 async 修饰的方法），那么前面就要加 await，
具体可以看 aiohttp 的 API，其链接为：https://docs.aiohttp.org/en/stable/client_reference.html。


### 超时设置

aiohttp 提供了超时设置，可以设置连接超时和读取超时。

对于超时设置，我们可以借助 ClientTimeout 对象

```python
import aiohttp
import asyncio

async def main():
    # 设置连接超时为5秒，读取超时为10秒
    timeout = aiohttp.ClientTimeout(total=5, sock_read=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get('https://httpbin.org/get') as response:
            print('status:', response.status)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

```

如果超时的话，会抛出 TimeoutError 异常，其类型为 asyncio.TimeoutError，我们再进行异常捕获即可。

另外，声明 ClientTimeout 对象时还有其他参数，如 connect、socket_connect 等，详细可以参考官方文档：https://docs.aiohttp.org/en/stable/client_quickstart.html#timeouts。

### 并发限制

由于 aiohttp 可以支持非常大的并发，比如上万、十万、百万都是能做到的，但对于这么大的并发量，目标网站很可能在短时间内无法响应，而且很可能瞬时间将目标网站爬挂掉，所以我们需要控制一下爬取的并发量。

一般情况下，我们可以借助于 asyncio 的 Semaphore 来控制并发量，示例如下：

```python
import asyncio
import aiohttp

CONCURRENCY = 5
URL = 'https://www.baidu.com'

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

async def scrape_api():
    async with semaphore:
        print('scraping', URL)
        async with session.get(URL) as response:
            await asyncio.sleep(1)
            return await response.text()

async def main():
    global session
    session = aiohttp.ClientSession()
    scrape_index_tasks = [asyncio.ensure_future(scrape_api()) for _ in range(10000)]
    await asyncio.gather(*scrape_index_tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

这里我们设置 CONCURRENCY 为 5，表示最多只能有 5 个任务并发执行。

### 异步爬取实战

