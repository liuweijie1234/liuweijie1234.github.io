---
title: django+celery 的使用介绍
date: 2022-08-15 15:52:00
tags:
- Django
categories:
- Django
---


Celery 是一个强大的分布式任务队列，用于异步任务处理。

这份笔记涵盖了从基础安装到高级特性的各个方面，旨在帮助开发者在生产环境中高效使用 Celery。

## 目录结构

- [基础](./basics)
- [核心概念](./concepts)
- [配置](./configuration)
- [高级特性](./advanced)
- [生产环境实践](./production)
- [其他](./other)


## 工作流程：

1. Client 发送任务到 Broker
2. Broker 将任务存入队列
3. Worker 从 Broker 获取任务
4. Worker 执行任务
5. Worker 将结果存入 Backend
6. Client 可以从 Backend 查询任务结果


## 组成

Celery 主要由以下几个核心组件组成：

1. Worker（工作进程）

执行具体任务的进程。可以启动多个 worker 来并行处理任务

celery -A app.celery worker -P gevent -c 4  # 启动4个协程

2. Beat（定时调度器）

负责定时任务的调度。类似 crontab 的功能

celery -A app.celery beat

3. Broker（消息中间件）

任务队列，存储待执行的任务。常用的有 Redis、RabbitMQ

CELERY_BROKER_URL = 'redis://localhost:6379/0'

4. Backend（结果存储）

存储任务执行结果
也常用 Redis 或 MySQL 等

CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

5. Task（任务）

具体要执行的任务代码

```python
@celery.task
def my_task():
    return "task completed"
```


完整配置示例：
```python
from celery import Celery

# 创建 Celery 实例
celery = Celery('myapp',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/1')

# 任务配置
celery.conf.update(
    # 任务队列配置
    task_queues = {
        'default': {'exchange': 'default'},
        'high_priority': {'exchange': 'high_priority'},
    },
    # 任务序列化方式
    task_serializer='json',
    # 结果序列化方式
    result_serializer='json',
    # 接受的内容类型
    accept_content=['json']
)

# 定时任务配置
celery.conf.beat_schedule = {
        'daily-task': {
            'task': 'tasks.daily_task',
            'schedule': 3600.0,  # 每小时执行
        }
    },
```





一、普通后台任务

后台任务通过将同步请求异步化，可以有效地解决请求超时的问题。
示例场景：app有一个执行任务的请求，该任务执行比较耗时。

Example：

```python
import json
from celery import task
from django.http import HttpResponse

@task(ignore_result=True)
def custom_task(paraml, param2):
    #定义自己的任务逻辑(比如做大数据的计算等
    pass

def exe_task(request):
    param1 = request.GET.get('param1')
    param2 = request.GET.get('param2')
    custom_task.apply async(args=[param1, param2])
    return HttpResponse(json.dumps({'result': True}))
```


调用custom_task.apply_async(args=[param1, param2])时，不会立即执行custom_task函数，而是向消息队列中插入一条相关的任务元数据，接着程序会立即执行return操作。

同时，celery服务端会从消息队列中取出这条元数据并执行custom_task。这样就实现了耗时任务的异步化，空闲出了uwsgi的worker资源。

本地开发时celery的启动方法：

```bash
python  manage.py  celery  worker  --settings=settings
```

二、周期性任务

周期性任务是较为常见的后台任务，例如周期地推送消息，周期地清理日志等。

celery的周期性任务用法类似于linux的crontab任务。由于它是应用层面的，可用性更灵活，用户可以通过简单的配置数据库，就可以管理周期性任务了。

示例场景：定期清理日志文件。

Example:

```python
from celery import task
from celery.task import periodic_task
from celery.schedules import crontab

@periodic_task(run_every=crontab(day_of_week='sunday'))
def clean_log1():
    #日志文件的清理代码
    pass

@task(ignore_result=True)
def clean_log2():
    #日志文件的清理代码
    pass
```


如图2.1中的代码片段，clean_log1会在celery beat启动后，自动注册到数据库中(CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler")。

clean_log2则需要手动配置到库中(开发框架中提供了api接口来直接操作数据库)。

区别在于两个装饰器的作用不同，@task是通用的，而@periodic_task是针对周期性任务的，参数run_every设置了周期crontab。

crontab设置规则类似于linux系统的crontab，如图2.2所示。

具体的配置可以参考http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html 。

![](/images/celery_3.png)

图2.2 crontab配置示例

*配置出周期性任务：

celery执行周期性任务的一大优势是可配置性，即不修改原有代码，就可以方便的调整任务的调度规则和关闭任务等。
和app的自定义model管理方式一样，Djcelery库也可以通过admin页面管理，如图2.3，它是Djcelery的库，其中Crontabs和Interval是配置调度规则的，
Periodic tasks是配置任务的。

强调一点，这里的任务都需要在代码中用装饰器@task或者@periodic_task包装，否则是无效的。

点击Periodic tasks后，如图2.4，celery beat启动后，自动注册了clean_log1任务。如果需要将clean_log2配置成周期性任务，可以通过配置Crontabs


![](/images/celery_4.png)
图2.3 Djcelery管理


![](/images/celery_5.png)
图2.4 periodic task子表

和Periodic tasks实现。同时，平台也提供了对应的api方便开发者使用。

图2.5是一个配置示例，其中Task是注册上clean_log2,  Crontab选择的是每3分钟执行一次。

![](/images/celery_6.png)
图2.5 clean_log2的配置示例

本地开发时celery的启动方法：

```bash
python manage.py celery worker --settings=settings
python manage.py celery beat --settings=settings
```


三、定时任务

指定定时的时间点，执行某个任务。
示例场景：定时发送邮件。
Example：


![](/images/celery_7.png)

图3.1 定时任务示例

图3.1中给出了调用定时任务的两种例子，countdown=60和eta=datetime.now()+timedelta(seconds=60)都是设置send_email_task在60s后执行。

本地开发时celery的启动方法:

```bash
python  manage.py  celery  worker  --settings=settings
```

https://blog.csdn.net/weixin_33127753/article/details/84872322

https://cloud.tencent.com/developer/article/1805994

https://www.jianshu.com/p/181074514567

https://www.jianshu.com/p/181074514567

https://blog.csdn.net/Tony_20/article/details/105035942

https://cloud.tencent.com/developer/article/2218981


https://blog.csdn.net/qq_37837134/article/details/90904669


celery -A app.core.celery inspect registered






