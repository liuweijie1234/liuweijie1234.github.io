---
title: Python3 协程/异步 asyncio
date: 2022-08-15 10:22:00
tags:
- Python
- asyncio
categories:
- Python
---
# 第一部分：基础入门
## 异步编程基础
### 参考

https://cuiqingcai.com/202271.html

https://zhuanlan.zhihu.com/p/59671241

### 核心概念

协程适合用于高并发的 I/O 密集型任务，它通过事件循环来管理多个协程，能够在等待 I/O 操作时切换到其他协程执行，从而提高程序的并发性能。

asyncio 是 Python 内置的异步 I/O 框架，用于编写并发代码。它基于 事件循环 和 协程，通过 async/await 语法实现非阻塞代码。

**同步**：代码按顺序执行，每一步必须完成后才能执行下一步

**异步**：代码可以在等待某些操作（如 I/O）时暂停执行，让出控制权，待操作完成后再恢复执行

**协程(coroutines)**: 
使用 `async def` 定义的函数
调用时返回协程对象，不会立即执行
需要被事件循环调度执行
内部使用 await 等待其他协程或可等待对象

**事件循环(event_loop)**: 
- 异步程序的核心引擎
- 主要职责：
  - 执行协程
  - 处理回调
  - 执行网络I/O
  - 运行子进程
- 常用方法：
  - run_until_complete()：运行直到完成
  - create_task()：创建任务
  - run_forever()：一直运行
  - close()：关闭事件循环

什么是事件循环
如何创建和管理事件循环
asyncio.run()的幕后原理


**任务(Task)**： 
- 协程的封装，继承自 Future。用于在事件循环中调度执行
- 创建方式：
  - asyncio.create_task() (Python 3.7+)
  - asyncio.ensure_future()
  - loop.create_task()
- 任务状态：
  - pending：等待执行
  - running：正在执行
  - done：执行完成
  - cancelled：已取消


**Future**: 表示异步操作的最终结果（Task 是 Future 的子类）

**async**: 关键字，用于定义一个协程函数。

**await**: 关键字，用于等待协程的执行结果。用来挂起阻塞方法的执行。

理解async/await关键字

await 后面的对象必须是如下格式之一（具体可以参见 https://www.python.org/dev/peps/pep-0492/#await-expression）：

- 一个原生 coroutine 对象；
- 一个由 types.coroutine 修饰的生成器，这个生成器可以返回 coroutine 对象；
- 一个包含 `__await__` 方法的对象返回的一个迭代器。


async def 定义协程函数

await 挂起协程执行

协程的调用链

### 协程与线程的区别

```python
import asyncio
import time

async def task():
    await asyncio.sleep(0.01)  # 模拟10ms I/O

# 创建10k任务仅需<100MB内存
async def main():
    tasks = [asyncio.create_task(task()) for _ in range(10000)]
    await asyncio.gather(*tasks)

# 等价线程代码需要>80GB内存（现实中不可能实现）
```

# 第二部分：核心概念深入

## 协程

### 创建协程

方法一：直接定义 async 函数（推荐方式）：

方法二：使用@asyncio.coroutine装饰器（传统方式）

### 运行协程

```python
import asyncio

async def my_coroutine():
    print("开始协程")
    await asyncio.sleep(1)  # 模拟异步操作
    print("结束协程")

# 方法一：使用 asyncio.run() 运行协程
asyncio.run(my_coroutine()) # Python 3.7+ 

# 方法二：使用 asyncio.create_task() 创建任务 运行协程
async def main():
    task = asyncio.create_task(my_coroutine())
    await task

asyncio.run(main())
# 方法三：使用 asyncio.ensure_future() 创建任务 运行协程
async def main():
    task = asyncio.ensure_future(my_coroutine())
    await task

asyncio.run(main())

# 方法四：使用事件循环创建协程 运行协程
loop = asyncio.get_event_loop()
loop.run_until_complete(my_coroutine())
loop.close()
```

## 任务

### 创建任务

#### 使用 asyncio.create_task() 方法创建任务

```python
import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def task_example():
    print(f"开始时间 {time.strftime('%X')}")
    
    # 创建任务
    task1 = asyncio.create_task(say_after(1, 'Hello'))
    task2 = asyncio.create_task(say_after(2, 'World'))
    
    # 等待任务完成
    await task1
    await task2
    
    print(f"结束时间 {time.strftime('%X')}")

asyncio.run(task_example())
```

#### 使用 asyncio.ensure_future() 方法创建任务

```python
import asyncio

async def execute(x):
    print('Number:', x)
    return x  # 添加返回值

# 创建协程对象（但未执行）
coroutine = execute(1)
print('Coroutine:', coroutine)  # 打印协程对象 coroutine，此时协程还未运行

# 将协程转换为任务
task = asyncio.ensure_future(coroutine)  # 将协程对象 coroutine 封装成一个 Task 对象，并赋值给 task 变量
print('Task:', task)  # 打印 Task 对象 task，此时 Task 对象还未运行

loop = asyncio.get_event_loop()  # 获取事件循环
loop.run_until_complete(task)  # 运行事件循环，直到 Task 对象 task 执行完毕
print('Task:', task)  # 打印 Task 对象 task，此时 Task 对象已经执行完毕
loop.close()  # 关闭事件循环
```

#### 使用 事件循环 loop.create_task() 方法创建任务

```python
import asyncio  

async def execute(x):  
    print('Number:', x)

# 创建协程对象（但未执行）
coroutine = execute(1) 
print('Coroutine:', coroutine)  # 显示协程对象信息

# get_event_loop() 获取当前线程的事件循环对象
loop = asyncio.get_event_loop()  

# 将协程包装成任务（准备执行）
task = loop.create_task(coroutine)  # create_task 方法将 coroutiness 协程对象转化为 task 对象
print('Task:', task)  # 显示任务信息（状态为pending）

# 运行事件循环直到任务完成
loop.run_until_complete(task)  # 调用了 loop 对象的 run_until_complete 方法将协程注册到事件循环 loop 中，然后启动
print('Task:', task)   # 显示任务信息（状态变为finished）
loop.close()

"""输出
Coroutine: <coroutine object execute at 0x000001F697581780>

Task: <Task pending coro=<execute() running at E:\liuweijie1234\Apitest\xpath_test.py:3>>

Task: <Task finished coro=<execute() done, defined at E:\liuweijie1234\Apitest\xpath_test.py:3> result=1>
"""
```

### 任务取消

```python
async def long_running_task():
    try:
        print("任务开始")
        await asyncio.sleep(10)
        print("任务完成")
    except asyncio.CancelledError:
        print("任务被取消")
        raise

async def main():
    task = asyncio.create_task(long_running_task())
    await asyncio.sleep(1)
    task.cancel()  # 取消任务
    
    try:
        await task
    except asyncio.CancelledError:
        print("主函数捕获到取消异常")

asyncio.run(main())
```

### 处理任务异常

待补充

### 获取任务结果

- Pending：任务正在等待执行。
- Running：任务正在执行。
- Done：任务执行完成。
- Cancelled：任务被取消。


通过await获取结果

task.result()方法

处理任务异常


## Futrue

### 获取 Futrue 里的结果

future表示还没有完成的工作结果。事件循环可以通过监视一个future对象的状态来指示它已经完成。future对象有几个状态：

- Pending
- Running
- Done
- Cancelled

创建future的时候，task为pending，事件循环调用执行的时候当然就是running，调用完毕自然就是done，如果需要停止事件循环，就需要先把task取消，状态为cancel。

```python
import asyncio


def foo(future, result):
    print(f"此时future的状态:{future}")
    print(f"设置future的结果:{result}")
    future.set_result(result)  # 将Future对象的状态标记为已完成，并设置其结果为result。
    print(f"此时future的状态:{future}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        all_done = asyncio.Future()
        loop.call_soon(foo, all_done, "Future is done!")
        print("进入事件循环")
        result = loop.run_until_complete(all_done)
        print("返回结果", result)
    finally:
        print("关闭事件循环")
        loop.close()
    print("获取future的结果", all_done.result())  # future.result()来获取这个结果

```


### Future对象使用await

future和协程一样可以使用await关键字获取其结果。

```python
import asyncio


def foo(future, result):
    print("设置结果到future", result)
    future.set_result(result)


async def main(loop):
    all_done = asyncio.Future()
    print("调用函数获取future对象")
    loop.call_soon(foo, all_done, "the result")

    result = await all_done
    print("获取future里的结果", result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()

```


### Future回调

Future 在完成的时候可以执行一些回调函数，回调函数按注册时的顺序进行调用:

```python
import asyncio
import functools


def callback(future, n):
    print('{}: future done: {}'.format(n, future.result()))


async def register_callbacks(all_done):
    print('注册callback到future对象')
    all_done.add_done_callback(functools.partial(callback, n=1))
    all_done.add_done_callback(functools.partial(callback, n=2))


async def main(all_done):
    await register_callbacks(all_done)
    print('设置future的结果')
    all_done.set_result('the result')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        all_done = asyncio.Future()
        loop.run_until_complete(main(all_done))
    finally:
        loop.close()

```

通过add_done_callback方法给funtrue任务添加回调函数，当funture执行完成的时候,就会调用回调函数。并通过参数future获取协程执行的结果。
到此为止，我们就学会了如何在协程中调用一个普通函数并获取其结果。


## 回调

### 任务绑定回调

```python
import asyncio  # 导入asyncio模块，用于编写异步代码
import requests  # 导入requests模块，用于发送HTTP请求

async def request():  # 定义一个异步函数request
    url = 'https://www.baidu.com'  # 设置要请求的URL
    status = requests.get(url)  # 发送GET请求并获取响应
    return status  # 返回响应状态

def callback(task):  # 定义一个回调函数callback，用于处理任务完成后的结果
    print('Status:', task.result())  # 打印任务的结果

coroutine = request()  # 调用request函数创建一个协程对象
task = asyncio.ensure_future(coroutine)  # 将协程对象转换为一个任务对象
task.add_done_callback(callback)  # add_done_callback 方法 为任务对象添加一个回调函数，它是特定于任务的回调，只有在任务完成时才会触发
print('Task:', task)  # 打印任务对象

loop = asyncio.get_event_loop()  # get_event_loop() 获取当前线程的事件循环对象
loop.run_until_complete(task)  # 运行事件循环直到任务完成
print('Task:', task)  # 打印任务对象
loop.close()

"""输出
Task: <Task pending coro=<request() running at E:\liuweijie1234\Apitest\asyncio_test.py:4> cb=[callback() at E:\liuweijie1234\Apitest\asyncio_test.py:9]>
Status: <Response [200]>
Task: <Task finished coro=<request() done, defined at E:\liuweijie1234\Apitest\asyncio_test.py:4> result=<Response [200]>>
"""
```

### 事件循环回调

在协程中可以通过一些方法去调用普通的函数。可以使用的关键字有 call_soon, call_later，call_at。

#### call_soon

可以通过字面意思理解调用立即返回。

```python
loop.call_soon(callback, *args, context=None)
```

在下一个迭代的时间循环中立刻调用回调函数,大部分的回调函数支持位置参数，而不支持”关键字参数”，如果是想要使用关键字参数，则推荐使用functools.aprtial()对方法进一步包装.
可选关键字context允许指定要运行的回调的自定义contextvars.Context。当没有提供上下文时使用当前上下文。
在Python 3.7中， asyncio协程加入了对上下文的支持。使用上下文就可以在一些场景下隐式地传递变量，比如数据库连接session等，而不需要在所有方法调用显示地传递这些变量。

下面来看一下具体的使用例子。

```python
import asyncio
import functools


def callback(args, *, kwargs="defalut"):
    print(f"普通函数做为回调函数,获取参数:{args},{kwargs}")


async def main(loop):
    print("注册callback")
    loop.call_soon(callback, 1)
    wrapped = functools.partial(callback, kwargs="not defalut")  # 对callback函数进行包装,添加 kwargs 参数
    loop.call_soon(wrapped, 2)
    await asyncio.sleep(0.2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(loop))
finally:
    loop.close()
```
输出结果

```bash
注册callback
普通函数做为回调函数,获取参数:1,defalut
普通函数做为回调函数,获取参数:2,not defalut
```

通过输出结果我们可以发现我们在协程中成功调用了一个普通函数，顺序的打印了1和2。

有时候我们不想立即调用一个函数，此时我们就可以call_later延时去调用一个函数了。

#### call_later

```python
loop.call_later(delay, callback, *args, context=None)
```

首先简单的说一下它的含义，就是事件循环在delay多长时间之后才执行callback函数.

配合上面的call_soon让我们看一个小例子

```python
import asyncio


def callback(n):
    print(f"callback {n} invoked")


async def main(loop):
    print("注册callbacks")
    loop.call_later(0.2, callback, 1)
    loop.call_later(0.1, callback, 2)
    loop.call_soon(callback, 3)
    await asyncio.sleep(0.4)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()
```
输出
```bash
注册callbacks
callback 3 invoked
callback 2 invoked
callback 1 invoked
```

通过上面的输出可以得到如下结果：
1.call_soon会在call_later之前执行，和它的位置在哪无关
2.call_later的第一个参数越小，越先执行。

#### call_at

```python
loop.call_at(when, callback, *args, context=None)
```

call_at第一个参数的含义代表的是一个单调时间，它和我们平时说的系统时间有点差异，
这里的时间指的是事件循环内部时间，可以通过loop.time()获取，然后可以在此基础上进行操作。

后面的参数和前面的两个方法一样。
实际上call_later内部就是调用的call_at。

```python
import asyncio


def call_back(n, loop):
    print(f"callback {n} 运行时间点{loop.time()}")


async def main(loop):
    now = loop.time()
    print("当前的内部时间", now)
    print("循环时间", now)
    print("注册callback")
    loop.call_at(now + 0.1, call_back, 1, loop)
    loop.call_at(now + 0.2, call_back, 2, loop)
    loop.call_soon(call_back, 3, loop)
    await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        print("进入事件循环")
        loop.run_until_complete(main(loop))
    finally:
        print("关闭循环")
        loop.close()
```

输出
```bash
进入事件循环
当前的内部时间 4412.152849525
循环时间 4412.152849525
注册callback
callback 3 运行时间点4412.152942526
callback 1 运行时间点4412.253202825
callback 2 运行时间点4412.354262512
关闭循环
```

因为call_later内部实现就是通过call_at所以这里就不多说了。




## 并发执行模式

### 使用 gather 并发运行任务

```python
results = await asyncio.gather(
    task1(),
    task2(),
    task3(),
    return_exceptions=True
)
```

```python
import asyncio

async def task(name, delay):
    print(f"任务 {name} 开始")
    await asyncio.sleep(delay)
    print(f"任务 {name} 完成")
    return f"结果-{name}"

async def main():
    # 同时创建多个任务
    task1 = asyncio.create_task(task("A", 2))
    task2 = asyncio.create_task(task("B", 1))
    task3 = asyncio.create_task(task("C", 3))
    
    # 等待所有任务完成
    results = await asyncio.gather(task1, task2, task3)
    print("所有任务完成:", results)

asyncio.run(main())
```

#### gather的使用

gather的作用和wait类似不同的是。
1.gather任务无法取消。
2.返回值是一个结果列表
3.可以按照传入参数的顺序，顺序输出。

```python
import asyncio

async def num(n):
    try:
        await asyncio.sleep(n * 0.1)
        return n
    except asyncio.CancelledError:
        print(f"数字{n}被取消")
        raise


async def main():
    tasks = [num(i) for i in range(10)]
    complete = await asyncio.gather(*tasks)
    for i in complete:
        print("当前数字", i)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
```

输出

```bash
当前数字 0
当前数字 1
....中间部分省略
当前数字 9
```

gather通常被用来阶段性的一个操作，做完第一步才能做第二步，比如下面这样

```python
import asyncio
import time


async def step1(n, start):
    await asyncio.sleep(n)
    print("第一阶段完成")
    print("此时用时", time.time() - start)
    return n


async def step2(n, start):
    await asyncio.sleep(n)
    print("第二阶段完成")
    print("此时用时", time.time() - start)
    return n


async def main():
    now = time.time()
    result = await asyncio.gather(step1(5, now), step2(2, now))
    for i in result:
        print(i)
    print("总用时", time.time() - now)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
```

输出
```bash
第二阶段完成
此时用时 2.0014898777008057
第一阶段完成
此时用时 5.002960920333862
5
2
总用时 5.003103017807007
```

可以通过上面结果得到如下结论：
1.step1和step2是并行运行的。
2.gather会等待最耗时的那个完成之后才返回结果，耗时总时间取决于其中任务最长时间的那个。


### 使用 wait 管理任务组

```python
done, pending = await asyncio.wait(
    tasks,
    timeout=2.0,
    return_when=asyncio.FIRST_COMPLETED
)
```

```python
import asyncio  
import requests 

async def request():  # 定义一个异步函数request
    url = 'https://www.baidu.com'  # 设置要请求的URL
    status = requests.get(url)  # 发送GET请求并获取响应
    return status  # 返回响应状态

tasks = [asyncio.ensure_future(request()) for _ in range(5)]  # 创建包含5个任务的列表
print('Tasks:', tasks)  # 打印任务列表

loop = asyncio.get_event_loop()  # get_event_loop() 获取当前线程的事件循环对象
loop.run_until_complete(asyncio.wait(tasks))  # 运行事件循环直到所有任务完成 
# asyncio.wait(tasks)方法的作用是等待给定的一组协程任务完成。它会挂起当前协程直到所有任务都完成或者直到指定的超时时间到达。这个方法返回一个包含已完成任务和未完成任务的元组。

for task in tasks:  # 遍历所有任务
    print('Task Result:', task.result())  # 打印每个任务的结果

loop.close()  # 关闭事件循环
```
```python
import asyncio


async def num(n):
    try:
        await asyncio.sleep(n*0.1)
        return n
    except asyncio.CancelledError:
        print(f"数字{n}被取消")
        raise


async def main():
    tasks = [num(i) for i in range(10)]
    complete, pending = await asyncio.wait(tasks, timeout=0.5)
    for i in complete:
        print("当前数字",i.result())
    if pending:
        print("取消未完成的任务")
        for p in pending:
            p.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
```
可以发现我们的结果并没有按照数字的顺序显示，在内部wait()使用一个set保存它创建的Task实例。
因为set是无序的所以这也就是我们的任务不是顺序执行的原因。
wait的返回值是一个元组，包括两个集合，分别表示已完成和未完成的任务。wait第二个参数为一个超时值
达到这个超时时间后，未完成的任务状态变为pending，当程序退出时还有任务没有完成此时就会看到如下的错误提示。


### 使用 as_completed 处理任务完成顺序

```python
for coro in asyncio.as_completed(tasks):
    result = await coro
    # 处理结果
```


as_complete 是一个生成器，会管理指定的一个任务列表，并生成他们的结果。
每个协程结束运行时一次生成一个结果。
与wait一样，as_complete不能保证顺序，不过执行其他动作之前没有必要等待所以后台操作完成。

```python
import asyncio
import time


async def foo(n):
    print('Waiting: ', n)
    await asyncio.sleep(n)
    return n


async def main():
    coroutine1 = foo(1)
    coroutine2 = foo(2)
    coroutine3 = foo(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    for task in asyncio.as_completed(tasks):
        result = await task
        print('Task ret: {}'.format(result))


now = lambda : time.time()
start = now()

loop = asyncio.get_event_loop()
done = loop.run_until_complete(main())
print(now() - start)
```

输出
```bash
Waiting:  1
Waiting:  2
Waiting:  4
Task ret: 1
Task ret: 2
Task ret: 4
4.004292249679565
```
可以发现结果逐个输出。

### 使用 gather 和 wait 结合使用

待补充

### 结构化并发(python3.11+)

创建任务组后，在其上下文管理块内创建的任务都会被自动添加到该任务组中。它会自动等待所有子任务完成，不需要手动添加 await 语句来等待每个任务，简化了代码编写。
```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(task1())
    tg.create_task(task2())
# 自动等待所有子任务
```
#### 与传统并发方式对比

与 gather 对比 ：
gather 用于收集多个协程的结果，但不提供自动的任务管理功能，需要手动处理异常和资源管理等问题。
而 TaskGroup 则更侧重于任务的管理和异常处理，提供了更结构化和自动化的任务管理方式。

与 wait 对比 ：
wait 可以等待一组协程完成，但需要手动指定等待条件和处理异常，
而 TaskGroup 则提供了一种更简洁和直观的方式来管理任务组的执行和异常处理。


## 异步控制流

### 超时控制

```python
async def fetch_data():
    await asyncio.sleep(2)
    return "数据"

async def main():
    try:
        # 设置超时时间
        result = await asyncio.wait_for(fetch_data(), timeout=1.5)
        print(result)
    except asyncio.TimeoutError:
        print("请求超时")

asyncio.run(main())
```

### 任务取消

```python
task = asyncio.create_task(long_running_task())
await asyncio.sleep(0.5)
task.cancel()

try:
    await task
except asyncio.CancelledError:
    print("任务被取消")
```

### 同步原语

异步锁（Lock）

事件（Event）

信号量（Semaphore）

条件变量（Condition）



# 第三部分：实战应用

## 异步I/O操作

### 异步文件操作（aiofiles）

```python
import aiofiles

async with aiofiles.open('file.txt', mode='r') as f:
    contents = await f.read()
```


### 异步请求接口（aiohttp）

```python
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get('https://example.com') as response:
        html = await response.text()
```



```python
import asyncio  # 导入 asyncio 库，用于处理异步操作
import aiohttp  # 导入 aiohttp 库，用于发送异步 HTTP 请求
import time  # 导入 time 库，用于计算时间

start = time.time()  # 记录开始时间

async def get(url):  # 定义一个异步函数 get，用于发送 GET 请求
    session = aiohttp.ClientSession(trust_env=False)  # 创建一个 aiohttp 会话对象，trust_env=False 表示不使用系统代理
    response = await session.get(url)  # 发送 GET 请求，并使用 await 关键字等待响应
    await response.text()  # 读取响应内容（此处只是为了等待响应完成）
    await session.close()  # 关闭会话对象
    return response  # 返回响应对象

async def request():  # 定义一个异步函数 request，用于发起请求
    url = 'https://httpbin.org/delay/5'  # 设置请求 URL，该 URL 会延迟 5 秒返回响应
    print('Waiting for', url)  # 打印提示信息，表示正在等待响应
    response = await get(url)  # 调用 get 函数发送请求，并使用 await 关键字等待响应
    print('Get response from', url, 'response', response)  # 打印提示信息，表示已收到响应

tasks = [asyncio.ensure_future(request()) for _ in range(10)]  # 创建 10 个任务，每个任务都会调用 request 函数
loop = asyncio.get_event_loop()  # 获取事件循环对象
loop.run_until_complete(asyncio.wait(tasks))  # 运行事件循环，直到所有任务完成

end = time.time()  # 记录结束时间
print('Cost time:', end - start)  # 打印程序执行时间
loop.close()  # 关闭事件循环
```


```python
import asyncio
import aiohttp
import time


def test(number):
    start = time.time()

    async def get(url):
        session = aiohttp.ClientSession()
        response = await session.get(url)
        await response.text()
        await session.close()
        return response

    async def request():
        url = 'https://www.baidu.com/'
        await get(url)

    tasks = [asyncio.ensure_future(request()) for _ in range(number)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    print('Number:', number, 'Cost time:', end - start)
    loop.close()

for number in [1, 3, 5, 10, 15, 30, 50, 75, 100, 200, 500]:
    test(number)

```


```python
# python3.7
import time
import requests
import json
import aiohttp
import async_timeout
import asyncio


async def get_mexc_depth(session):
    with async_timeout.timeout(3):
        async with session.get('https://www.mexc.cc/open/api/v2/market/depth', params={
            "symbol": "BTC_USDT",
            "depth": "2"
        }) as response:
            if response.status == 200:
                text = await response.text()
                infos = json.loads(text).get("data")
                asks = infos.get("asks")
                return {asks[0].get('price')}, {asks[0].get('quantity')}


async def main():
    start_time = time.time()
    session = aiohttp.ClientSession(trust_env=False)
    for _ in range(100):
        _start_time = time.time()
        function = [get_mexc_depth(session)]
        result = await asyncio.gather(*function)
        print(f"{time.time() - _start_time} price:{result[0][0]} amount:{result[0][1]}")

    print(f"100次请求花费的时间: {time.time() - start_time}")


if __name__ == '__main__':
    asyncio.run(main())
```

### 异步数据库操作（asyncpg/aiomysql） 

```python
import asyncpg

conn = await asyncpg.connect(user='user', password='pass', database='db')
result = await conn.fetch('SELECT * FROM users')
```

## 设计异步应用架构

### 生产者-消费者模式

```python
async def producer(queue):
    while True:
        item = await generate_item()
        await queue.put(item)

async def consumer(queue):
    while True:
        item = await queue.get()
        await process_item(item)
```

### 异步 Web 框架（FastAPI/Quart）

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    await asyncio.sleep(0.1)
    return {"Hello": "Async World"}
```

### 微服务与分布式任务队列

使用Celery+asyncio

RQ异步任务队列

分布式任务调度

## 测试与调试异步代码

### 使用pytest-asyncio测试
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_func()
    assert result == expected
```

### 调试技巧

使用asyncio调试模式

日志记录异步操作

异常堆栈跟踪分析

### 性能分析工具

使用cProfile分析协程

可视化事件循环性能

识别性能瓶颈

# 第四部分：高级主题

## 高级模式与技巧

### 异步上下文管理器

```python
class AsyncResource:
    async def __aenter__(self):
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
```

### 异步迭代器

```python
class AsyncIterator:
    def __init__(self):
        self.data = [1, 2, 3]
    
    def __aiter__(self):
        return self
        
    async def __anext__(self):
        if not self.data:
            raise StopAsyncIteration
        return self.data.pop(0)
```


### 协程与线程池交互

```python
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(
    None,  # 使用默认线程池
    cpu_bound_function, arg1, arg2
)
```


## 内部原理剖析

### 事件循环实现机制

Selector事件循环

Proactor事件循环（Windows）

uvloop替代实现

### 协程底层原理

生成器与协程的关系

awaitable协议

协程状态机

### Future与Task实现解析

Future对象的作用

Task如何封装协程

回调链的执行机制

# 第五部分：实战项目

## 综合项目实战

### 异步Web爬虫

并发抓取页面

异步解析内容

限流与去重

### 实时数据处理管道

异步消息队列（Kafka/RabbitMQ）

流式处理

实时分析

### 高性能API服务

异步REST API

WebSocket实时通信

数据库连接池管理

# 第六部分：常见问题

协程不执行怎么办？

如何避免阻塞事件循环？

调试"Task was destroyed but it is pending"错误

处理"Event loop is closed"问题