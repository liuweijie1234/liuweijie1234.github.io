
## Celery Beat（哨兵）

### 简介

哨兵模式（Celery Beat）是 Celery 的一个重要组件，主要用于处理定时任务。

Celery Beat（哨兵）的主要作用：

1、定时任务调度

按照预定的时间表自动触发任务
类似于 Linux 的 crontab 功能
可以设置周期性任务执行

2、使用场景

定期数据备份
定时数据统计
周期性清理任务
定时发送报告邮件

在你的项目中添加 Beat 的示例：
```bash
// ... existing code ...

启动 Worker 服务
celery -A app.celery worker -P gevent -c 1 -Q dataset,generation,mail,ops_trace --loglevel INFO

启动 Beat 服务（定时任务调度器）
celery -A app.celery beat --loglevel INFO

Windows 系统启动 Beat：
celery -A app.celery beat --loglevel INFO

// ... existing code ...
```

配置示例：
```python
# celery配置文件
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    '每天凌晨备份数据': {
        'task': 'tasks.backup_database',
        'schedule': crontab(hour=0, minute=0),
    },
    '每周日统计报告': {
        'task': 'tasks.generate_weekly_report',
        'schedule': crontab(day_of_week='sunday'),
    }
}
```

注意事项：
Beat 进程只需要启动一个，多个 Beat 会导致重复执行
Beat 进程要和 Worker 进程配合使用
Beat 只负责任务的调度，具体任务的执行还是由 Worker 完成

### crontab 参数说明：

参数说明

minute：分钟（0-59）
hour：小时（0-23）
day_of_week：一周中的某一天（0-6，0 表示周一，6 表示周日）
day_of_month：一个月中的某一天（1-31）
month_of_year：一年中的某个月（1-12）


常见用法

crontab(minute=0, hour=0)：每天午夜（00:00）执行
crontab(minute=30)：每小时的第 30 分钟执行
crontab(minute=0, hour='*/2')：每 2 小时执行一次
crontab(minute=0, hour=0, day_of_week=0)：每周一的午夜执行
crontab(minute=0, hour=0, day_of_month=1)：每月第一天的午夜执行


## 周期任务调度策略

- crontab：通过 crontab 表达式定义的调度策略
- solar：根据不同地区的日常，日落，黎明，或黄昏时间来执行调度策略

elery.schedules模块提供了crontab类，用于指定基于Cron表达式的定时任务。

crontab对象的构造函数接受一系列参数来定义定时任务的执行时间。

下面是这些参数的详细说明：

- minute（可选）：表示分钟字段。可以是一个整数（0-59），一个字符串（用逗号分隔多个值），一个range对象或者一个Cron表达式。默认值为'*'，表示每分钟。
- hour（可选）：表示小时字段。可以是一个整数（0-23），一个字符串（用逗号分隔多个值），一个range对象或者一个Cron表达式。默认值为'*'，表示每小时。
- day_of_week（可选）：表示星期几字段。可以是一个整数（0-6，其中0表示星期一），一个字符串（用逗号分隔多个值），一个range对象或者一个Cron表达式。默认值为'*'，表示每天。
- day_of_month（可选）：表示月份中的日期字段。可以是一个整数（1-31），一个字符串（用逗号分隔多个值），一个range对象或者一个Cron表达式。默认值为'*'，表示每天。
- month_of_year（可选）：表示年份中的月份字段。可以是一个整数（1-12），一个字符串（用逗号分隔多个值），一个range对象或者一个Cron表达式。默认值为'*'，表示每月。
- timezone（可选）：指定时区信息。可以是一个字符串，表示时区的名称；也可以是一个pytz.timezone对象；如果未指定，则使用系统的本地时区。
- nowfun（可选）：指定获取当前时间的函数。默认情况下，会使用Python标准库中的datetime.datetime.now函数获取当前时间。

下面是一个示例，展示如何使用crontab创建一个定时任务：

```python
from celery.schedules import crontab

task_schedule = {
    'task': 'my_task',
    'schedule': crontab(minute=0, hour='*/2', day_of_week='mon-fri'),
}
```
以上代码定义了一个定时任务，将在每天周一到周五的每两个小时（整点和半点）触发一次名为my_task的任务。

## 周期调度进程：beat

https://www.cnblogs.com/yzm1017/p/15357165.html
