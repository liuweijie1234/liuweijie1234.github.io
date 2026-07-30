介绍 Celery 的队列机制，包括如何创建和使用队列


# 队列机制

## 创建队列

队列在消息中间件（如 Redis、RabbitMQ）中创建。以下是一个 Redis 队列示例：

```python
from celery import Celery

app = Celery('my_app', broker='redis://localhost:6379/0')

app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
    },
    'high_priority': {
        'exchange': 'high_priority',
        'routing_key': 'high_priority',
    },
}
```

## 使用队列

在任务定义时，可以指定任务的队列。以下是一个示例：

```python

@app.task(bind=True)
def my_task(self):
    # 任务逻辑
    pass

# 将任务发送到指定队列
my_task.apply_async(queue='high_priority')
```


## 队列优先级

Celery 支持队列优先级，通过设置任务的 `priority` 参数来控制任务的执行顺序。

```python
@app.task(bind=True)
def my_task(self):
    # 任务逻辑
    pass

# 将任务发送到指定队列并设置优先级
my_task.apply_async(queue='high_priority', priority=10)

# 优先级范围：0-9，数字越大优先级越高
``` 

```python
app.conf.task_queues = {
    'high_priority': {
        'exchange': 'priority',
        'routing_key': 'high',
    },
    'low_priority': {
        'exchange': 'priority',
        'routing_key': 'low',
    }
}
```

```bash
# 专用 Worker 处理高优先级任务
celery -A proj worker -Q high_priority --concurrency=4
```
