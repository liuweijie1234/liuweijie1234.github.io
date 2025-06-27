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


# 专用队列实现串行

## 1. 创建专用队列

```python
# celery_config.py

app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 定义专用队列
app.conf.task_queues = (
    Queue('persona_sync_queue', routing_key='persona.sync'),
)

# 任务路由配置
app.conf.task_routes = {
    'myapp.tasks.sync_persona_portrait_task': {
        'queue': 'persona_sync_queue',
        'routing_key': 'persona.sync',
    },
}
```

## 2. 启动专用 Worker

启动一个只处理 persona_sync_queue 队列且并发数为 1 的 Worker：

```bash
celery -A myapp worker -l info -Q persona_sync_queue --concurrency=1 -n worker.persona_sync
```

## 3. 修改任务调度
创建调度任务，将需要串行执行的任务放入专用队列：

```python
# tasks.py

@celery_app.task
def schedule_persona_sync():
    """调度所有traitor的画像同步任务到专用队列"""
    async def fetch_traitor_ids():
        async with AsyncSessionLocal() as db:
            result = await db.execute("SELECT id FROM traitors WHERE is_active = true")
            return [row[0] for row in result.fetchall()]
    
    # 获取ID列表
    loop = asyncio.get_event_loop()
    traitor_ids = loop.run_until_complete(fetch_traitor_ids())
    
    # 将每个任务放入专用队列
    for traitor_id in traitor_ids:
        sync_persona_portrait_task.apply_async(
            args=(traitor_id,),
            queue='persona_sync_queue'  # 指定专用队列
        )
    
    return f"Scheduled {len(traitor_ids)} tasks to persona_sync_queue"

# 保持原任务不变
@celery_app.task(time_limit=900)
def sync_persona_portrait_task(traitor_id):
    # 原有实现保持不变
    ...
```

## 4. 定时触发调度
配置 Celery Beat 定时任务：

```python
# celery_beat_schedule.py

app.conf.beat_schedule = {
    'nightly-persona-sync': {
        'task': 'myapp.tasks.schedule_persona_sync',
        'schedule': crontab(hour=3, minute=0),  # 每天凌晨3点执行
    },
}
```