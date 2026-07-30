讲解任务路由的原理和配置方法

# 任务路由

## 基于任务名称的路由

```python
from celery import Celery

app = Celery('my_app', broker='redis://localhost:6379/0')

app.conf.task_routes = {
    'my_app.tasks.high_priority_task': {'queue': 'high_priority'},
    'my_app.tasks.default_task': {'queue': 'default'},
}
```

```python
# 修改Celery配置，添加任务路由规则
celery_app.conf.update(
    task_routes={
        # 将请求第三方接口的任务分配到 'third_party' 队列
        "app.tasks.crawl_data.*": {"queue": "third_party"},
        "app.tasks.polling.*": {"queue": "third_party"},
        
        # 将处理数据库的任务分配到 'database' 队列
        "app.tasks.sync_client_robot.*": {"queue": "database"},
        "app.tasks.sync_log_data.*": {"queue": "database"},
    },
    
    # 可选：禁用默认的 'celery' 队列（避免任务误入默认队列）
    task_default_queue="third_party",  # 设置默认队列（如果必须保留默认队列则无需此配置）
)
```

## 动态路由

```python
def route_task(name, args, kwargs, options, task=None, **kw):
    if name == 'my_app.tasks.high_priority_task':
        return {'queue': 'high_priority'}
    return {'queue': 'default'}

app.conf.task_router = route_task
```