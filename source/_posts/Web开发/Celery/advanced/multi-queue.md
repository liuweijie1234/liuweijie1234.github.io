提供多队列的实践指南，包括如何创建和使用多个队列

# 多队列实践
## 创建多个队列

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
    'low_priority': {
        'exchange': 'low_priority',
        'routing_key': 'low_priority',
    },
}
```

## 将任务发送到指定队列
```python
@app.task
def my_task():
    pass

my_task.apply_async(queue='high_priority')
```