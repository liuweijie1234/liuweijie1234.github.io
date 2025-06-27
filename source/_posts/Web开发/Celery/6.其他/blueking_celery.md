---
title: 蓝鲸开发框架 Celery 使用
date: 2022-08-15 15:52:00
tags:
- Django
categories:
- Django
---


[Celery 官方文档](https://docs.celeryq.dev/en/master/)

## 本地 安装 celery

## 安装消息中间件

目前 celery 支持 redis、rabbitmq 作为任务的消息队列，推荐使用 redis。

mac 系统 redis 使用指南：
- 安装指令 `brew install redis`；
- 启动指令 `redis-server`；
- 打开客户端 `./bin/redis-cli` 。

windows 系统 redis 使用指南：

下载安装地址： https://github.com/MicrosoftArchive/redis/releases。 

点击安装目录下的 redis-server.exe 启动 redis 服务。

[使用 redis](https://www.celerycn.io/ru-men/zhong-jian-ren-brokers/shi-yong-redis)

- window 中间件路径（参考）

C:\Program Files (x86)\RabbitMQ Server\rabbitmq_server-3.2.4\sbin

D:\Program Files\Redis

## 开发框架 celery 依赖

- requirements.txt 添加依赖（默认已添加）
```txt
celery==4.4.0
redis==3.5.3
django-celery-beat==2.2.0
django-celery-results==2.0.1
```

## config 配置项

### 在 config/default.py 中修改配置

- CELERY 开关

```python
# CELERY 开关，使用时请改为 True，修改项目目录下的 Procfile 文件，添加以下两行命令：
# worker: python manage.py celery worker -l info
# beat: python manage.py celery beat -l info
# 不使用时，请修改为 False，并删除项目目录下的 Procfile 文件中 celery 配置
IS_USE_CELERY = True
```

- celery 配置任务文件

```python
# CELERY 配置，申明任务的文件路径，即包含有 @task 装饰器的函数文件
CELERY_IMPORTS = (
    'home_application.tasks'
)
```

- celery 并发数

```python
# CELERY 并发数，默认为 2，可以通过环境变量或者 Procfile 设置
CELERYD_CONCURRENCY = os.getenv('BK_CELERYD_CONCURRENCY', 2)
```

### 在 config/dev.py 文件中修改消息队列配置

- 开发框架默认

```python
# Celery 消息队列设置 RabbitMQ
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Celery 消息队列设置 Redis
BROKER_URL = 'redis://localhost:6379/0'
```

- 自定义

```bash
redis://:password@hostname:port/db_number
```

## 添加 Celery 任务

在 app 底下创建 tasks.py 文件，添加 @task 任务：

```python
from celery import task

@task
def mul(x, y):
    return x * y
```

## 调用 Celery 任务

在 app 的 view.py 调用
```python
from celery.schedules import crontab
from tasks import *

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}
```

## celery 日志

```python
import logging

logger_celery = logging.getLogger('celery')
logger_celery.error("test error")
```


## 启动异步 worker

- 启动异步任务服务 celery worker

在根目录执行：
```bash
python manage.py celery worker -l info
```

https://blog.csdn.net/haeasringnar/article/details/105232966

## 启动定时 beat

- 启动周期性任务服务 celery beat

在根目录执行：
```bash
python manage.py celery beat -l info 
```
添加周期任务

进入 admin，在 DJCELERY -> Periodic_tasks 表中添加一条记录。

- 常见问题



### 如何在 PaaS 平台部署时，自动启动 celery 进程

项目目录下的 app_desc.yaml 文件，添加以下两行配置：

```txt
    celerywork:
      command: celery -A blueapps.core.celery worker -l info --concurrency 4
    celerybeat:
      command: celery -A blueapps.core.celery beat -l info
```

## 关闭 celery

请根据以下步骤操作：

- 将配置文件 config/default.py 中的 IS_USE_CELERY 改为 False
- 删除 Procfile 文件中 worker 与 beat 进程
- 提交代码改动后重新部署应用


【基础】Django中使用Celery完成异步轮询任务实践

https://bk.tencent.com/s-mart/community/question/1070?type=answer

【进阶】从一个问题现象追查Celery内幕

https://bk.tencent.com/s-mart/community/question/1065?type=answer