深入讲解任务路由的高级用法

# 任务路由策略
## 基于任务优先级的路由

```python
app.conf.task_routes = {
    'my_app.tasks.high_priority_task': {'queue': 'high_priority'},
    'my_app.tasks.medium_priority_task': {'queue': 'medium_priority'},
    'my_app.tasks.low_priority_task': {'queue': 'low_priority'},
}
```

## 基于任务类型的路由

```python
def route_task(name, args, kwargs, options, task=None, **kw):
    if 'priority' in kwargs:
        if kwargs['priority'] == 'high':
            return {'queue': 'high_priority'}
        elif kwargs['priority'] == 'medium':
            return {'queue': 'medium_priority'}
        elif kwargs['priority'] == 'low':
            return {'queue': 'low_priority'}
    return {'queue': 'default'}

app.conf.task_router = route_task
```