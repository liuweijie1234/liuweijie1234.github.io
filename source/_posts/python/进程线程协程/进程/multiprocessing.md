---
title: Python3 进程 multiprocessing 
date: 2022-08-15 10:14:00
tags:
- Python
- multiprocessing
categories:
- Python
---

## 概念

进程是具有一定独立功能的程序在一个数据集合上的一次运行活动。在 Python 中，可以使用 multiprocessing 模块来创建进程

进程可以绕过 GIL(全局解释器锁) 的限制，在 CPU 密集型任务中可以更好地利用多核 CPU。但是进程的创建和切换开销比线程大，并且进程间的通信比线程间通信复杂。

参考：
- [multiprocessing](https://docs.python.org/zh-cn/3/library/multiprocessing.html)
- https://zhuanlan.zhihu.com/p/64702600


### Process 类

通过创建一个 Process 对象然后调用它的 start() 方法来生成进程，可以使用 with 上下文来生成。


```python
from multiprocessing import Process

def f(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

### 进程之间交换对象


#### 队列

[Queue](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Queue) 类是一个近似 queue.Queue 的克隆

> {% post_link python/module/Queue %}

#### 管道

[Pipe()](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Pipe) 函数返回一个由管道连接的连接对象，默认情况下是双工（双向）


### 进程间同步变量

跟 threading 一样 使用的是 Lock


### 进程间共享变量

#### 共享内存

使用 Value 或 Array 将数据存储在共享内存映射中

#### 服务进程

由 Manager() 返回的管理器对象控制一个服务进程，该进程保存 Python 对象并允许其他进程使用代理操作它们。


### 进程池 - Pool

[Python进程池multiprocessing.Pool的用法](https://www.cnblogs.com/ailiailan/p/11850710.html)

在Windows上要想使用进程模块，就必须把有关进程的代码写在 `if __name__ == "__main__":` 内，否则在Windows下使用进程模块会产生异常。Unix/Linux下则不需要。

Pool类可以提供指定数量的进程供用户调用，当有新的请求提交到Pool中时，如果池还没有满，就会创建一个新的进程来执行请求。如果池满，请求就会告知先等待，直到池中有进程结束，才会创建新的进程来执行这些请求。

```python

# 导入进程模块
import multiprocessing
 
# 最多允许3个进程同时运行
pool = multiprocessing.Pool(processes = 3)
```

1、**apply_async** — 该函数用于传递不定参数，主进程会被阻塞直到函数执行结束，但它是非阻塞的且支持结果返回后进行回调，函数原型如下：

```python
apply_async(func[, args=()[, kwds={}[, callback=None]]])
```

2、**map()** — Pool类中的map方法，与内置的map函数用法基本一致，它会使进程阻塞直到结果返回，函数原型如下：

```python
map(func, iterable, chunksize=None)
```
注意：虽然第二个参数是一个迭代器，但在实际使用中，必须在整个队列都就绪后，程序才会运行子进程。

3、**map_async()** — 与map用法一致，但是它是非阻塞的。其有关事项见apply_async，函数原型如下：

```python
map_async(func, iterable, chunksize, callback)
```

4、**close()** — 关闭进程池（pool），使其不在接受新的任务。

5、**terminal()** — 结束工作进程，不在处理未处理的任务。

6、**join()** — 主进程阻塞等待子进程的退出， join方法要在close或terminate之后使用。


```python
# -*- coding：utf-8 -*-
import multiprocessing
import time


def func(msg):
    print("in:", msg)
    time.sleep(3)
    print("out,", msg)


if __name__ == "__main__":
    # 这里设置允许同时运行的的进程数量要考虑机器cpu的数量，进程的数量最好别小于cpu的数量，
    # 因为即使大于cpu的数量，增加了任务调度的时间，效率反而不能有效提高
    pool = multiprocessing.Pool(processes=3)
    item_list = ['processes1', 'processes2', 'processes3', 'processes4', 'processes5', ]
    count = len(item_list)
    for item in item_list:
        msg = "python教程 %s" % item
        # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        pool.apply_async(func, (msg,))

    pool.close()
    pool.join()
```

### 示例


[Python 爬虫进阶六之多进程的用法](https://cuiqingcai.com/3335.html)