---
title: Python3 GIL 全局解释器锁
date: 2026-07-30 10:00:00
tags:
- Python
- 并发编程
categories:
- Python
---

## 什么是 GIL

GIL（Global Interpreter Lock，全局解释器锁）是 **CPython 解释器**的一把互斥锁：同一时刻只允许一个线程执行 Python 字节码。

- 它是 CPython 的实现细节，不是 Python 语言特性（Jython、PyPy-STM 等无此限制）。
- 存在原因：CPython 的内存管理（引用计数）不是线程安全的，GIL 用最简单的方式保证了线程安全。

## 带来的影响

- **CPU 密集型**：多线程无法利用多核，甚至因为锁竞争比单线程更慢。
- **IO 密集型**：线程在等待 IO 时会**释放 GIL**，其他线程可以运行，所以多线程对 IO 密集型仍然有效。

```python
import time
from threading import Thread

def count(n):
    while n > 0:
        n -= 1

N = 50_000_000

# 单线程
start = time.time()
count(N); count(N)
print("单线程:", time.time() - start)

# 双线程（CPU 密集型，因 GIL 并不会更快）
start = time.time()
t1, t2 = Thread(target=count, args=(N,)), Thread(target=count, args=(N,))
t1.start(); t2.start(); t1.join(); t2.join()
print("双线程:", time.time() - start)
```

## 如何绕过 GIL

| 方案 | 说明 |
| --- | --- |
| 多进程 `multiprocessing` | 每个进程有独立解释器和 GIL，可利用多核（CPU 密集型首选） |
| C 扩展 | numpy 等库在 C 层计算时会释放 GIL |
| `concurrent.futures.ProcessPoolExecutor` | 进程池的高层封装 |
| 换解释器/新版本 | Python 3.13+ 提供实验性的 free-threading（no-GIL）构建 |

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as ex:
    results = list(ex.map(count, [N, N]))   # 真正并行
```

## 线程 / 进程 / 协程切换开销对比

| 项 | 进程 | 线程 | 协程 |
| --- | --- | --- | --- |
| 切换者 | 操作系统 | 操作系统 | 用户程序（事件循环） |
| 切换开销 | 最大（页表、上下文） | 中等（内核态切换） | 最小（用户态函数调用级） |
| 内存占用 | 大（独立地址空间） | 中（默认栈约 8MB） | 小（KB 级） |
| 数据共享 | 需 IPC | 共享内存需加锁 | 单线程内共享，通常无需加锁 |
| 适用 | CPU 密集型 | IO 密集型 | 高并发 IO 密集型 |

## 选型结论

- CPU 密集型 → 多进程（或 C 扩展/numpy 向量化）。
- IO 密集型、并发量中等 → 多线程。
- IO 密集型、高并发（上千连接）→ 协程（asyncio / gevent）。
