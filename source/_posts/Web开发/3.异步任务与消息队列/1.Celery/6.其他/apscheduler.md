---
title: Python 定时任务之 APScheduler
date: 2022-08-15 15:52:00
tags:
- apscheduler
categories:
- [Python]
- [定时任务]
---

# apscheduler 使用说明

## 介绍

APScheduler 是 Python 定时任务框架，它可以帮助你轻松实现定时任务，支持多种定时触发器，如 date、interval、cron 等，并且支持多种 jobstores 存储方式，如内存、MongoDB、Redis、SQLAlchemy、ZooKeeper 等。

## 安装

```bash
pip install apscheduler

# requirements.txt 添加
apscheduler==3.8.1
```

## 基本使用

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def Time_task():
    print("The time is ： %s"%datetime.now())


if __name__ == '__main__':
    scheduler  = BlockingScheduler()
    # 每天10.30执行该定时任务
    # scheduler.add_job(Time_task, 'cron', day='*', hour=10, minute=30)
    scheduler.add_job(Time_task, 'interval', seconds=3)
    scheduler.start()
```

## 触发器（triggers）

触发器管理着 job 的调度方式。

- apscheduler.triggers.date：在某个特定时间仅运行一次 job 时使用
- apscheduler.triggers.interval：当以固定的时间间隔运行 job 时使用
- apscheduler.triggers.cron：当在特定时间定期运行 job 时使用

### 1、date 触发器（单次触发）

- 代码示例

```python
from datetime import date

from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

def my_job(text):
    print(text)

# 单次定时
sched.add_job(my_job, 'date', run_date=date(2022, 11, 6), args=['text'])
# sched.add_job(my_job, 'date', run_date=datetime(2022, 11, 6, 16, 30, 5), args=['text'])
# sched.add_job(my_job, 'date', run_date='2022-11-06 16:30:05', args=['text'])

# 立即执行
# sched.add_job(my_job, args=['text'])

sched.start()
```

- 参考

https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html

### 2、interval 触发器（间隔/固定触发）

- 代码示例

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

app = FastAPI()
scheduler = AsyncIOScheduler()

async def poll_third_party_api():
    # 轮询第三方API并处理数据
    pass

@app.on_event("startup")
async def startup():
    scheduler.add_job(poll_third_party_api, "interval", minutes=5)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
```

- 参考

https://apscheduler.readthedocs.io/en/stable/modules/triggers/interval.html

### 3、crontab 触发器（定时/周期触发）

## job stores （job 存储）

用于 job 数据的持久化。默认 job 存储在内存中，还可以存储在各种数据库中。除了内存方式不需要序列化之外（一个例外是使用 ProcessPoolExecutor），其余都需要 job 函数参数可序列化。另外多个调度器之间绝对不能共享 job 存储（APScheduler 原作者的意思是不支持分布式，但是我们可以通过重写部分函数实现，具体方法后面再介绍）。

## executors （执行器）


负责处理 job。通常使用线程池（默认）或者进程池来运行 job。当 job 完成时，会通知调度器并发出合适的事件。

执行器使用默认的 ThreadPoolExecutor


## schedulers （调度器）

将 job 与以上组件绑定在一起。通常在程序中仅运行一个调度器，并且不直接处理 jobstores ，executors 或 triggers，而是通过调度器提供的接口，比如添加，修改和删除 job。

- [apscheduler.schedulers.blocking.BlockingScheduler](https://apscheduler.readthedocs.io/en/stable/modules/schedulers/blocking.html) ：当调度器是程序中唯一运行的东西时使用，阻塞式。
- [apscheduler.schedulers.background.BackgroundScheduler](https://apscheduler.readthedocs.io/en/stable/modules/schedulers/background.html)：当调度器需要后台运行时使用。
- [apscheduler.jobstores.memory.MemoryJobStore](https://apscheduler.readthedocs.io/en/stable/modules/jobstores/memory.html)：将作业使用内存存储
- [apscheduler.jobstores.mongodb.MongoDBJobStore](https://apscheduler.readthedocs.io/en/stable/modules/jobstores/mongodb.html) ：使用 MongoDB 存储
- [apscheduler.jobstores.redis.RedisJobStore](https://apscheduler.readthedocs.io/en/stable/modules/jobstores/redis.html) ：使用 redis 存储
- [apscheduler.jobstores.sqlalchemy.SQLAlchemyJobStore](https://apscheduler.readthedocs.io/en/stable/modules/jobstores/sqlalchemy.html) ：使用 ORM 框架 SQLAlchemy，后端可以是 sqlite、mysql、PoatgreSQL 等数据库
- [apscheduler.jobstores.zookeeper.ZooKeeperJobStore](https://apscheduler.readthedocs.io/en/stable/modules/jobstores/zookeeper.html) ：使用 zookeeper 存储


```python
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()
@sched.scheduled_job('cron', hour=8, minute='59')
```

```python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from tasks import fetch_and_process_data

def fetch_data_from_api():
    # 调用第三方接口，获取数据
    print(f"Fetching data at {datetime.now()}")
    fetch_and_process_data.delay()  # fetch_and_process_data 为 task任务

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_data_from_api, 'interval', minutes=5)  # 每5分钟拉取一次数据
scheduler.start()
```


## 参考

https://apscheduler.readthedocs.io/en/stable/userguide.html

[Python 定时任务框架 APScheduler 详解](https://www.cnblogs.com/leffss/p/11912364.html)

[python 定时任务最强框架 APScheduler 详细教程](https://zhuanlan.zhihu.com/p/144506204)

[django 中的定时任务方式](https://blog.csdn.net/haeasringnar/article/details/106129392)