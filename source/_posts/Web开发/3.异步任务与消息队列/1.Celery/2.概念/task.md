---
title: django celery Periodic Task
date: 2022-08-15 15:52:00
tags:
- Django
categories:
- Django
---

# 任务定义和管理

## 定义任务

```python
from celery import Celery

app = Celery('my_app', broker='redis://localhost:6379/0')

@app.task
def my_task():
    # 任务逻辑
    pass
```
```python
from celery import shared_task
import time

# 全局配置
app.conf.task_time_limit = 300  # 硬超时时间
app.conf.task_soft_time_limit = 250  # 软超时时间  

> 注意：软超时是指当任务执行时间超过设定的时间后，会引发一个 SoftTimeLimitExceeded 异常，你可以捕获这个异常并进行自定义的处理逻辑。

@shared_task(time_limit=1800, soft_time_limit=1700)  # 任务定义时设置超时时间
def my_long_task():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(fetch_keyword_data())
        return result
    except SoftTimeLimitExceeded:
        logger.warning("Task exceeded soft time limit")
    except Exception as e:
        logger.error(f"Error in sync_keyword_task: {e}", exc_info=True)
        raise

# 调用任务时设置超时时间
my_long_task.apply_async(args=[], kwargs={}, time_limit=900, soft_time_limit=800)
```
### 执行任务

```python
# 手动触发任务
result = my_task.delay()

# 获取任务结果
print(result.get())
```

## 异步执行任务

### delay() —— 快速异步调用

作用
- 是 apply_async 的简化版，适用于不需要额外配置（如定时、重试策略）的简单任务。
- 直接传递任务参数，不支持高级参数（如 countdown、queue）。


```python
from celery import Celery

app = Celery()

@app.task
def add(x, y):
    return x + y

# 异步调用任务（等效于 apply_async(args=(2, 3))）
result = add.delay(2, 3)  # 返回 AsyncResult 对象
print(result.get())       # 阻塞获取结果（慎用，会破坏异步性）
```

适用场景
- 快速测试或简单任务。
- 不需要定制化参数（如定时、优先级）。


### apply_async() —— 高级异步调用(生产环境推荐)

作用

是 Celery 的底层异步调用方法，支持所有高级功能：

- 定时任务（countdown/eta）
- 指定队列（queue）
- 重试策略（retry）
- 任务路由（routing_key）
- 序列化方式（serializer）

参数
eta ：指定任务的预定执行时间（datetime 对象），任务会在该时间到达时执行。
countdown ：与 eta 类似，但更简单，表示任务在多少秒后执行。
expires ：指定任务的过期时间，如果任务在该时间内未被处理，则会被丢弃。
queue ：指定任务应该发送到的队列名称，用于任务的路由。

```python
result = add.apply_async(args=(2, 3))  # 等效于 delay(2, 3)
```

```python
from datetime import datetime, timedelta

# 10 秒后执行
result = add.apply_async(
    args=(2, 3),
    countdown=10,  # 延迟秒数
)

# 指定时间执行（UTC 时间）
eta = datetime.utcnow() + timedelta(minutes=5)
result = add.apply_async(
    args=(2, 3),
    eta=eta,       # 精确执行时间
)

# 指定队列和优先级
result = add.apply_async(
    args=(2, 3),
    queue='high_priority',
    priority=10,   # 数字越大优先级越高
)

add.apply_async(args=[], kwargs={}, time_limit=900, soft_time_limit=800) # 调用任务时设置超时时间
```

适用场景
- 需要定时、优先级、自定义队列等高级功能。
- 生产环境推荐使用。

### signature() —— 任务签名

用于创建任务签名（部分参数预绑定），便于复用：

```python
from celery import signature

# 创建任务签名（部分参数预绑定）
task_s = add.s(2, 3)  # 等效于 signature('add', args=(2, 3))

# 异步执行签名任务
result = task_s.delay()          # 等效于 add.delay(2, 3)
result = task_s.apply_async()    # 等效于 add.apply_async(args=(2, 3))
```


### send_task() —— 动态调用

直接通过任务名称调用（无需导入任务函数）：

```python
# 通过名称调用任务（适用于动态任务或跨模块调用）
result = app.send_task('tasks.add', args=(2, 3))
```


## 注意

不要滥用 .get()
```python
result.get()  # 阻塞调用，破坏异步性！仅在测试或特殊场景使用。
```

任务结果需配置后端
若需获取结果，需配置 result_backend（如 Redis/RabbitMQ）。