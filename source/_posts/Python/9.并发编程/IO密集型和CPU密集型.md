---
title: Python3 IO 密集型与 CPU 密集型任务
date: 2026-07-30 10:00:00
tags:
- Python
- 并发编程
categories:
- Python
---

## 概念

- **IO 密集型**：大部分时间在等待网络/磁盘/数据库响应，CPU 空闲。如爬虫、Web 服务、文件读写。
- **CPU 密集型**：大部分时间在做计算，CPU 跑满。如加解密、图像处理、数据压缩、科学计算。

## 如何判断任务类型

1. **看代码行为**：耗时集中在 `requests`、数据库查询、文件读写 → IO 密集；集中在循环计算、序列化、正则 → CPU 密集。
2. **看监控指标**：
   - 运行时 CPU 使用率低、但任务很慢 → IO 密集；
   - 单核跑满 100% → CPU 密集。
   - Linux 下用 `top`（看 `%CPU` 与 `wa` 等待 IO 占比）、`iostat` 观察。
3. **用 profiler 定位**：`cProfile` 看时间花在计算函数还是 socket 等待上。

```python
import cProfile
cProfile.run("main()", sort="cumtime")
```

## IO 密集型：如何设置线程池大小

没有万能公式，常用估算（参考《Java 并发编程实战》的通用模型）：

```
线程数 ≈ CPU 核数 × (1 + 等待时间 / 计算时间)
```

- 等待时间占比越大，可以开的线程越多。例如等待:计算 = 9:1，8 核可估算 8 × 10 = 80 线程。
- 实践做法：从估算值出发做**压测**，观察吞吐量和响应时间拐点，取拐点前的值。
- 上限还受内存（每个线程默认栈约 8MB）、下游服务承受能力（连接数、限流）约束。
- Python `ThreadPoolExecutor` 的默认值是 `min(32, os.cpu_count() + 4)`，即偏向 IO 场景的保守值。

```python
from concurrent.futures import ThreadPoolExecutor
import requests

with ThreadPoolExecutor(max_workers=32) as ex:
    results = list(ex.map(requests.get, urls))
```

> 并发量继续上升（数千连接）时，线程内存与切换开销过大，应改用协程（asyncio/gevent）。

## CPU 密集型：如何分配进程数

- 受 GIL 限制，多线程无效，应使用**多进程**。
- 进程数一般取 **CPU 物理/逻辑核数**：`os.cpu_count()`；`ProcessPoolExecutor` 默认就是这个值。
- 纯计算任务开超过核数的进程只会增加切换开销，不会更快。
- 若任务同时混有 IO，可略高于核数（如核数 +1 ~ 2 倍）并压测确认。
- 注意给操作系统和其他服务预留核心（如取 `cpu_count() - 1`）。

```python
import os
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
    results = list(ex.map(heavy_compute, tasks))
```

## 选型速查

| 任务类型 | 首选方案 | 备选 |
| --- | --- | --- |
| IO 密集、中低并发 | 线程池 | - |
| IO 密集、高并发 | asyncio / gevent | 线程池 |
| CPU 密集 | 进程池 | numpy 等 C 扩展、Cython |
| 混合型 | 进程池 + 每进程内协程/线程 | - |
