---
title: Python3 gevent 协程库
date: 2026-07-30 10:00:00
tags:
- Python
- 并发编程
categories:
- Python
---

## 说明

`gevent` 是基于 **greenlet（轻量级协程）+ libev/libuv 事件循环** 的并发库。
它通过**猴子补丁**把标准库中的阻塞 IO（socket、time.sleep 等）替换为协程友好的实现，让同步风格的代码自动获得异步并发能力——这是它与 asyncio（需要显式 async/await）最大的区别。

```bash
pip install gevent
```

## 基本用法

```python
import gevent

def task(name, seconds):
    print(f"{name} 开始")
    gevent.sleep(seconds)      # 模拟 IO，交出控制权
    print(f"{name} 结束")
    return name

# spawn 创建协程，joinall 等待全部完成
jobs = [
    gevent.spawn(task, "A", 2),
    gevent.spawn(task, "B", 1),
]
gevent.joinall(jobs, timeout=10)
print([j.value for j in jobs])   # 获取返回值 ['A', 'B']
```

## monkey patch：让阻塞库变协程

```python
from gevent import monkey
monkey.patch_all()      # 必须放在所有其他 import 之前！

import time
import requests
import gevent

def fetch(url):
    start = time.time()
    resp = requests.get(url)          # 被 patch 后自动非阻塞
    print(url, resp.status_code, f"{time.time() - start:.2f}s")

urls = ["https://httpbin.org/delay/2"] * 3
gevent.joinall([gevent.spawn(fetch, u) for u in urls])
# 3 个请求并发执行，总耗时约 2s 而不是 6s
```

## 协程池：控制并发量

```python
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import requests

pool = Pool(5)          # 最多 5 个并发

def fetch(url):
    return requests.get(url).status_code

urls = [f"https://httpbin.org/get?i={i}" for i in range(20)]
results = pool.map(fetch, urls)
```

## gevent vs asyncio

| 项 | gevent | asyncio |
| --- | --- | --- |
| 编程风格 | 同步写法，隐式切换 | async/await 显式切换 |
| 生态改造 | monkey patch 即可复用 requests 等同步库 | 需要 aiohttp/httpx 等异步库 |
| 可控性 | 切换点不可见，排查问题较难 | 切换点明确 |
| 归属 | 第三方 | 标准库（官方方向） |

## 注意事项

- `monkey.patch_all()` 必须在**所有 import 之前**执行，否则部分模块 patch 不生效。
- 只对 IO 密集型任务有效；CPU 密集型任务会阻塞整个事件循环。
- 与 C 扩展的阻塞调用（如某些数据库驱动）不兼容时，协程会退化为串行。
