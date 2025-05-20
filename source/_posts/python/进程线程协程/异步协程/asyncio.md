---
title: Python3 协程/异步 asyncio
date: 2022-08-15 10:22:00
tags:
- Python
- asyncio
categories:
- Python
---

## 概念

**event_loop**: 事件循环，相当于一个无线循环，我们可以把一些函数注册到这个事件循环上，当满足发生条件的时候，就调用对应的处理方法。

**coroutine**: 协程，在 Python 中常指代协程对象类型，我们可以将协程对象注册到事件循环中，它会被事件循环调用。我们可以使用 async 关键字来定义一个方法，这个方法在调用时不会立即被执行，而是会返回一个协程对象

**task**： 任务，这是对协程对象的进一步封装，包含协程对象的各个状态。

**future**: 未来，它是对任务对象的进一步封装，它代表着协程的执行结果。

**async**: 关键字，用于定义一个协程函数。

**await**: 关键字，用于等待协程的执行结果。用来挂起阻塞方法的执行。

## 参考

https://cuiqingcai.com/202271.html

https://zhuanlan.zhihu.com/p/59671241

## 定义协程

```python
import asyncio  # 导入 asyncio 库，用于处理异步操作

async def execute(x):  # 定义一个异步函数 execute，接收一个参数 x
    print('Number:', x)

coroutine = execute(1)  # 调用异步函数 execute(1)，并将返回的协程对象赋值给 coroutine 变量
print('Coroutine:', coroutine)
print('After calling execute')

loop = asyncio.get_event_loop()  # get_event_loop() 获取当前线程的事件循环对象
# loop.run_until_complete(coroutine)  也可以直接传递 coroutine 到 run_until_complete 方法中,不用 create_task
task = loop.create_task(coroutine)  # create_task 方法将 coroutine 对象转化为 task 对象
print('Task:', task)
loop.run_until_complete(task)  # 调用了 loop 对象的 run_until_complete 方法将协程注册到事件循环 loop 中，然后启动
print('Task:', task)
print('After calling loop')
loop.close()

"""输出
Coroutine: <coroutine object execute at 0x000001F697581780>
After calling execute
Task: <Task pending coro=<execute() running at E:\liuweijie1234\Apitest\xpath_test.py:3>>
Number: 1
Task: <Task finished coro=<execute() done, defined at E:\liuweijie1234\Apitest\xpath_test.py:3> result=1>
After calling loop
"""
```

```python
import asyncio  # 导入 asyncio 库，用于处理异步操作

async def execute(x):  # 定义一个异步函数 execute，接收一个参数 x
    print('Number:', x)  # 打印传入的参数 x
    return x  # 返回参数 x

coroutine = execute(1)  # 调用异步函数 execute(1)，并将返回的协程对象赋值给 coroutine 变量
print('Coroutine:', coroutine)  # 打印协程对象 coroutine，此时协程还未运行
print('After calling execute')  # 打印提示信息

task = asyncio.ensure_future(coroutine)  # 将协程对象 coroutine 封装成一个 Task 对象，并赋值给 task 变量
print('Task:', task)  # 打印 Task 对象 task，此时 Task 对象还未运行
loop = asyncio.get_event_loop()  # 获取事件循环
loop.run_until_complete(task)  # 运行事件循环，直到 Task 对象 task 执行完毕
print('Task:', task)  # 打印 Task 对象 task，此时 Task 对象已经执行完毕
print('After calling loop')  # 打印提示信息
loop.close()  # 关闭事件循环
```

## 协程调用协程

```python
import asyncio


async def main():
    print("主协程")
    print("等待result1协程运行")
    res1 = await result1()
    print("等待result2协程运行")
    res2 = await result2(res1)
    return (res1,res2)


async def result1():
    print("这是result1协程")
    return "result1"


async def result2(arg):
    print("这是result2协程")
    return f"result2接收了一个参数,{arg}"


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(main())
        print(f"获取返回值:{result}")
    finally:
        print("关闭事件循环")
        loop.close()
'''
输出：
主协程
等待result1协程运行
这是result1协程
等待result2协程运行
这是result2协程
获取返回值:('result1', 'result2接收了一个参数,result1')
关闭事件循环
'''
```


## 任务绑定回调

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

## 事件循环回调

在协程中可以通过一些方法去调用普通的函数。可以使用的关键字有call_soon,call_later，call_at。

### call_soon

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

### call_later

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

### call_at

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


## 多任务协程


```python
import asyncio  # 导入asyncio模块，用于编写异步代码
import requests  # 导入requests模块，用于发送HTTP请求

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

## 协程实现


await 后面的对象必须是如下格式之一（具体可以参见 https://www.python.org/dev/peps/pep-0492/#await-expression）：

- 一个原生 coroutine 对象；
- 一个由 types.coroutine 修饰的生成器，这个生成器可以返回 coroutine 对象；
- 一个包含 `__await__` 方法的对象返回的一个迭代器。


异步请求需要使用 aiohttp 库


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



## 并发的执行任务

任务（Task）是与事件循环交互的主要途径之一。任务可以包装协程，可以跟踪协程何时完成。

任务是Future的子类，所以使用方法和future一样。
协程可以等待任务，每个任务都有一个结果，在它完成之后可以获取这个结果。
因为协程是没有状态的，我们通过使用create_task方法可以将协程包装成有状态的任务。

还可以在任务运行的过程中取消任务。

```python
import asyncio


async def child():
    print("进入子协程")
    return "the result"


async def main(loop):
    print("将协程child包装成任务")
    task = loop.create_task(child())
    print("通过cancel方法可以取消任务")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("取消任务抛出CancelledError异常")
    else:
        print("获取任务的结果", task.result())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()
```
输出
```bash
将协程child包装成任务
通过cancel方法可以取消任务
取消任务抛出CancelledError异常
```

如果把上面的task.cancel()注释了我们可以得到正常情况下的结果，如下。
```bash
将协程child包装成任务
通过cancel方法可以取消任务
进入子协程
获取任务的结果 the result
```

另外出了使用 loop.create_task 将协程包装为任务外还可以使用 asyncio.ensure_future(coroutine) 建一个task。
在python3.7中可以使用 asyncio.create_task 创建任务。


## gather的使用

gather的作用和wait类似不同的是。
1.gather任务无法取消。
2.返回值是一个结果列表
3.可以按照传入参数的顺序，顺序输出。
我们将上面的代码改为gather的方式

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


## 任务完成时进行处理

as_complete是一个生成器，会管理指定的一个任务列表，并生成他们的结果。
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

