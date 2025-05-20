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