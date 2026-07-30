---
title: Tornado 异步 IO 与协程
date: 2026-07-30 12:25:00
tags:
- Tornado
- 异步
- 协程
categories:
- Web开发
- Tornado
---

## 一、为什么异步

Tornado 单线程运行在 IOLoop 上，**一个耗时的同步调用会阻塞所有请求**。异步让出控制权，I/O 等待期间处理别的请求，从而高并发。

## 二、原生协程（推荐）

```python
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient

class ProxyHandler(tornado.web.RequestHandler):
    async def get(self):
        client = AsyncHTTPClient()
        resp = await client.fetch('https://example.com')
        self.write({'len': len(resp.body)})
```

`async/await` 是 Tornado 5+ 推荐写法；旧版 `@tornado.gen.coroutine` + `yield` 已逐步淘汰。

## 三、调用阻塞代码

阻塞函数要丢到线程/进程池：

```python
import tornado.ioloop

def blocking_task():
    import time; time.sleep(2); return 42

class H(tornado.web.RequestHandler):
    async def get(self):
        res = await tornado.ioloop.IOLoop.current().run_in_executor(None, blocking_task)
        self.write({'res': res})
```

CPU 密集用 `concurrent.futures.ProcessPoolExecutor`。

## 四、异步客户端

Tornado 自带 `AsyncHTTPClient`；数据库用异步驱动（如 `motor` 对应 MongoDB、`aiomysql` 对应 MySQL），避免同步驱动阻塞事件循环。

## 五、超时与并发

```python
resp = await client.fetch(url, request_timeout=5)
# 并发多个请求
from tornado.gen import multi
results = await multi([client.fetch(u) for u in urls])
```

## 六、最佳实践

- 全程 async：handler、DB、HTTP 都用异步实现，别混同步阻塞。
- 阻塞代码务必 `run_in_executor`。
- 长连接/WebSocket 是 Tornado 的主场（见 `3.WebSocket`）。
- 部署配合多进程（`tornado.process.fork_processes`）吃满多核。
