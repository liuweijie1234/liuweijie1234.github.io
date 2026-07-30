

## 参数

**-A, --app**: 指定 Celery 应用名称。

示例：

```bash
celery -A app.core.celery_config.celery worker --loglevel=info
```

**-c, --concurrency**: 指定并发数。

示例：

```bash
celery -A app.core.celery_config.celery worker --concurrency=4 --loglevel=info
```

**-n, --hostname**：设置工作者名称

示例：

```bash
celery -A app.core.celery_config.celery worker --concurrency=4 --loglevel=info --hostname=worker1
```


**--pool**：设置任务池类型

--pool=prefork：默认的进程池类型。适用于CPU密集任务
--pool=eventlet：使用 eventlet 库的协程模型（需安装 eventlet）。pip install eventlet
--pool=gevent：使用 gevent 并发库（需安装 gevent）。  pip install gevent
--pool=solo：使用单个进程。
--pool=processes：使用进程池。
--pool=threads：使用线程池代替进程池。
--pool=custom：自定义 pool 类型。

```bash
celery -A app.core.celery worker --loglevel=info --pool=solo

celery -A app.core.celery worker --loglevel=info --pool=eventlet --concurrency=100

celery -A app.core.celery worker --loglevel=info --pool=gevent --concurrency=100

celery -A app.core.celery worker --loglevel=info --pool=solo --logfile=logs/worker.log
```


--time-limit：设置任务超时时间


示例：

```bash
celery -A app.core.celery_config.celery worker --time-limit=300 --loglevel=info
```

--soft-time-limit：设置任务软超时时间

指定每个任务的软超时时间（以秒为单位），超过该时间将触发超时警告，但不会终止任务。

示例：

```bash
celery -A app.core.celery_config.celery worker --soft-time-limit=240 --loglevel=info
```

--include：包含额外的任务模块

示例：

```bash
celery -A app.core.celery_config.celery worker --include=app.tasks.test --loglevel=info
```

--detach：以守护进程模式运行

让 Celery 工作者在后台以守护进程模式运行。

示例：

```bash
celery -A app.core.celery_config.celery worker --detach --loglevel=info
```

--purge：清除所有待处理的任务
在启动工作者前清除所有待处理的任务。

示例：

```bash
celery -A app.core.celery_config.celery worker --purge --loglevel=info
```

--scheduler：指定定时任务调度器
指定 Celery 定时任务的调度器类。

示例：

```bash
celery -A app.core.celery_config.celery beat --scheduler=cron_scheduler --loglevel=info
```

--max-tasks-per-child：设置每个工作进程的最大任务数
指定每个工作进程在被回收前可以处理的最大任务数。

示例：

```bash
celery -A app.core.celery_config.celery worker --max-tasks-per-child=100 --loglevel=info
```

--max-memory-per-child：设置每个工作进程的最大内存使用量
指定每个工作进程在被回收前可以使用的最大内存（以 MB 为单位）。

示例：

```bash
celery -A app.core.celery_config.celery worker --max-memory-per-child=512 --loglevel=info
```

**--without-gossip**：禁用工作者之间的闲聊
禁用工作者之间的闲聊协议，减少网络通信。

示例：

```bash
celery -A app.core.celery_config.celery worker --without-gossip --loglevel=info
```
**--without-mingle**：禁用工作者启动时的闲聊
禁用工作者启动时的闲聊协议，减少启动时间。

示例：

```bash
celery -A app.core.celery_config.celery worker --without-mingle --loglevel=info
```

**--without-heartbeat**：禁用心跳检测
禁用工作者之间的心跳检测，减少网络通信。

示例：

```bash
celery -A app.core.celery_config.celery worker --without-heartbeat --loglevel=info
```

--uid：指定运行进程的用户 ID
指定 Celery 工作者运行时的用户 ID。

示例：

```bash
celery -A app.core.celery_config.celery worker --uid=1000 --loglevel=info
```

--gid：指定运行进程的组 ID
指定 Celery 工作者运行时的组 ID。

示例：

```bash
celery -A app.core.celery_config.celery worker --gid=1000 --loglevel=info
```

--workdir：指定工作目录
指定 Celery 工作者的工作目录。

示例：

```bash
celery -A app.core.celery_config.celery worker --workdir=/home/user/celery --loglevel=info
```

--pidfile：指定 PID 文件路径
指定 Celery 工作者的 PID 文件路径。

示例：

```bash
celery -A app.core.celery_config.celery worker --pidfile=/var/run/celery.pid --loglevel=info
```