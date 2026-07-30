---
title: django celery Worker
date: 2022-08-15 15:52:00
tags:
- Django
categories:
- Django
---


## Worker 进程

Worker 的职责：
- 执行任务
- 监听 Broker 中是否有待处理的消息

### 启动 Worker

```bash
# 启动 worker
celery -A my_app worker --loglevel=info

# 启动定时任务
celery -A app.celery beat

# 查看当前 worker 状态
celery -A app.celery status

# 查看队列情况
celery -A your_celery_app inspect registered  # 查看注册的任务
celery -A your_celery_app inspect active  # 查看正在执行的任务
celery -A your_celery_app inspect reserved  # 查看已保留的任务
celery -A your_celery_app inspect stats  # 查看 Worker 统计信息
```


### Worker 参数

- `-A`：celery app 声明的模块，worker 通过来路径定位到 celery app 并是否有其中的配置来完成初始化
- `-c` 或 `--concurrency=4`：并发数，决定了 worker 进程能够同时处理的任务数量，例子 `-c 4` 表示 worker 进程能够同时处理 4 个任务
- `-n` 或 `--hostname`：设置 worker 名称。
- `-Q` 或 `--queues`：指定 worker 消费的队列。例子 `-Q queueA,queueB` 表示 worker 进程会消费 queueA 和 queueB 两个队列的任务
- `-P`：worker pool 的类型
- `-l`:--loglevel=info 日志等级

实例命令：

```bash
celery worker -l info -P threads

celery worker -l info -P eventlet

celery worker -A proj -l info -P eventlet -c 4 -Q queueA,queueB
```

--pool=solo：单线程。调试使用
--pool=prefork ：多进程池，CPU密集型任务  推荐linux使用
--pool=processes：进程池。等于 --pool=prefork。弃用
--pool=threads：多线程池
--pool=custom：自定义池 
--pool=eventlet：协程池， IO密集型任务  注意： 协程池与 asyncio 可能冲突。注意：需安装 eventlet。pip install eventlet
--pool=asyncio：使用 asyncio 库的协程模型（需安装 asyncio）。 pip install asyncio

--loglevel=info：设置日志级别为 info。

--logfile=logs/worker.log：将日志输出到指定文件。
--logfile=logs/beat.log


windows 推荐使用 eventlet 或者 solo 测试接口，最好别windows使用多进程池。



```python
from eventlet import monkey_patch
monkey_patch()
```
--pool=gevent：协程池 注意：需安装 gevent。pip install gevent
```python
from gevent import monkey
monkey.patch_all()
```


```bash

celery -A app.core.celery:celery_app worker -Q celery --concurrency=100 --loglevel=info --hostname=worker1@%h

celery -A app.core.celery:celery_app worker -Q file_generation --concurrency=1  --loglevel=info --hostname=file_generator@%h


celery -A app.core.celery worker --loglevel=info --pool=threads --concurrency=10

celery -A app.core.celery worker --loglevel=info --pool=gevent --concurrency=100 --without-gossip --without-mingle --without-heartbeat

celery -A app.core.celery worker --loglevel=info --pool=eventlet --concurrency=100 --without-gossip --without-mingle --without-heartbeat

celery -A app.core.celery worker --loglevel=info --pool=solo --without-gossip --without-mingle --without-heartbeat

# 消息队列+并发为1
celery -A app.core.celery:celery_app worker \
  -Q file_generation \         # 只消费指定队列
  --concurrency=1 \            # 并发工作进程数
  --loglevel=info \            # 日志级别
  --hostname=file_generator@%h \ # 自定义主机标识
  --without-gossip \           # 禁用集群协议
  --without-mingle \           # 禁用启动同步
  --without-heartbeat          # 禁用心跳事件
```


### 停止worker

```bash
# 优雅停止所有 worker
celery -A app.core.celery control shutdown

# 强制终止残留进程（如果优雅停止无效）
pkill -f "celery -A app.core.celery worker"
```

### 启动定时任务


```bash
celery -A app.core.celery:celery_app beat --scheduler=sqlalchemy_celery_beat.schedulers:DatabaseScheduler --loglevel=debug
celery -A app.core.celery:celery_app beat --loglevel=info --pidfile=./celerybeat.pid --schedule=./celerybeat-schedule
celery -A app.core.celery beat --loglevel=info
celery -A app.core.celery beat --loglevel=debug 
celery -A app.core.celery beat --loglevel=info --logfile=logs/beat.log
```



### 清空队列
```bash
# 强制清空默认队列（最直接的方法）
celery -A app.core.celery purge --force
```

### 清空消息中间件的 Celery 数据
```bash
# Redis 清空 Celery 数据
# 清空 Redis 中的 Celery 数据（假设使用默认数据库）
redis-cli FLUSHDB

# 或者更精确地删除所有 Celery 相关键
redis-cli KEYS "celery*" | xargs redis-cli DEL


# RabbitMQ 清空 Celery 数据
# 清空默认队列（通常名为 celery）
sudo rabbitmqctl purge_queue celery

# 删除并重建队列（更彻底）
sudo rabbitmqctl delete_queue celery
sudo rabbitmqctl declare_queue celery durable=true
```

### 查看队列

```bash
# 查看队列
celery -A app.core.celery inspect registered  # 查看注册的任务
celery -A app.core.celery inspect active  # 查看正在执行的任务
celery -A app.core.celery inspect reserved  # 查看已保留的任务
celery -A app.core.celery inspect stats  # 查看 Worker 统计信息
```