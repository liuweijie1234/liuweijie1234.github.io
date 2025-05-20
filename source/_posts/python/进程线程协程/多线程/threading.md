---
title: Python3 多线程
date: 2022-08-15 10:22:00
tags:
- Python
categories:
- Python
---

### 多线程

Python 提供了 thread 和 threading 两个模块来实现多线程，`thread` 是低级模块，`threading` 是高级模块，对 `thread`进行了封装。

绝大多数情况下，我们只需要使用 threading 这个高级模块。

```python
import threading
import time


def loop():
    n = 0
    while n < 5:
        n = n + 1
        print('thread {} >>> {}' .format(threading.current_thread().name, n))
        time.sleep(1)


# 主线程，名称默认为MainThread
print('thread {} is running...' .format(threading.current_thread().name))
# 传入目标函数，并对线程起名
t = threading.Thread(target=loop, name='LoopThread')
t.start()
# 表示Main等LoopThread执行完之后再执行，否则就会出现main先执行完，loop还没执行完
t.join()
print('thread {} ended.' .format(threading.current_thread().name))
```

多线程会造成数据的不安全，在 Python 中可以通过加锁来保证数据安全：


在 Python 中，threading.Lock 是用来在多线程编程中进行线程同步的工具。

它可以在多个线程之间创建临界区，确保在任意时刻只有一个线程可以访问共享资源，避免出现竞争条件（race condition）和数据不一致的情况。


用法:
- 当多个线程需要访问共享资源时，可以使用 `threading.Lock` 对临界区进行加锁和解锁。
- 通过调用 `acquire()` 方法来获取锁，调用 `release()` 方法来释放锁。


```python
import threading
import time

# 定义共享资源
shared_resource = 0
threadLock = threading.Lock()

# 线程函数
def thread_function():
    global shared_resource

    # 获取锁
    threadLock.acquire()
    try:
        # 在临界区内对共享资源进行操作
        shared_resource += 1
        print(f"Thread {threading.current_thread().name} modified the shared resource to: {shared_resource}")
    finally:
        # 释放锁
        threadLock.release()

# 创建多个线程并启动
threads = []
for i in range(5):
    thread = threading.Thread(target=thread_function)
    threads.append(thread)
    thread.start()

# 等待所有线程执行结束
for thread in threads:
    thread.join()

# 输出最终结果
print("Final shared resource value:", shared_resource)
```

### ThreadLocal

ThreadLocal 就是给每个线程创建一个全局变量的副本，这样每个线程都只能读写自己的副本，可以任意读写互不干扰，也不用进行锁的管理。

```python
import threading

# 创建ThreadLocal:
local_school = threading.local()


def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, {} (in {})'.format(std, threading.current_thread().name))


def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=('Tom',), name='A')
t2 = threading.Thread(target=process_thread, args=('Jerry',), name='B')
t1.start()
t2.start()
```
### 线程池

```python
import requests
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor

# 定义请求的URL和参数
url = "http://192.168.0.109/getSn/"

body_json = {
    "barcode": "D173LBA41C210402A04196",
    "MAC": "000000000000",
    "series": "W90"
}

# 定义Excel表格
wb = Workbook()
ws = wb.active

# 写入表头
ws['A1'] = '状态码'
ws['B1'] = '响应时间'


# 定义一个函数来发送请求并记录结果
def send_request(i):
    response = requests.post(url, data=body_json)
    status_code = response.status_code
    elapsed_time = response.elapsed.total_seconds()

    # 将结果写入Excel表格
    ws.cell(row=i+2, column=1, value=status_code)
    ws.cell(row=i+2, column=2, value=elapsed_time)

# 使用ThreadPoolExecutor创建多个线程来发送请求
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for i in range(10):  # 循环发送10次请求
        future = executor.submit(send_request, i)
        futures.append(future)

    # 等待所有请求结束
    for future in futures:
        future.result()

# 保存Excel表格
wb.save('result.xlsx')
```

[python线程池 ThreadPoolExecutor 使用详解](https://blog.csdn.net/xiaoyu_wu/article/details/102820384)

[python多线程接口案例](https://blog.csdn.net/qq_43400993/article/details/105591240)


[Python 爬虫进阶五之多线程的用法](https://cuiqingcai.com/3325.html)