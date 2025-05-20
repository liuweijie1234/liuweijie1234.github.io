---
title: Python3 备份数据库
date: 2023-08-15 10:14:00
tags:
- Python
categories:
- Python
---

在 Python 中，有几个常用的库可用于操作 MySQL 数据库。以下是其中几个主要的库以及它们的优点和支持的 Python 版本：

**mysql-connector-python**:

优点：mysql-connector-python 是官方 MySQL Connector/Python 库，提供了与 MySQL 服务器的稳定连接和交互。它具有良好的文档和活跃的社区支持。
缺点：相对于其他库，有一些功能和操作可能较为繁琐。
Python 版本支持：支持 Python 2.7 和 Python 3.4 及更高版本。

**PyMySQL**:

优点：PyMySQL 是一个纯 Python 实现的库，具有性能良好和易于使用的特点。在与 MySQL 服务器的连接和操作方面提供了简洁的 API。
缺点：由于 PyMySQL 是纯 Python 实现的，与 C 语言的 MySQL 客户端相比，可能在某些复杂场景下略有性能不足。
Python 版本支持：支持 Python 2.7 和 Python 3.x 版本。

**mysqlclient**:

优点：mysqlclient 库是 Python DB API 规范的 MySQL 驱动程序，与 C 扩展的 MySQL 客户端库兼容，速度较快。
缺点：在安装和配置方面相对较复杂，对操作系统环境有一定要求。
Python 版本支持：支持 Python 2.7 和 Python 3.x 版本。


1、安装mysql-connector-python库。

```bash
pip install mysql-connector-python
```

2、执行脚本

```python
import mysql.connector
import os
import time

# MySQL数据库连接配置
config = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'database': 'database_name'
}

# 备份目录
backup_dir = '/path/to/backup/directory'

# 备份文件名
backup_file_name = 'backup-' + time.strftime('%Y-%m-%d') + '.sql'

# 创建备份目录（如果不存在）
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# 连接到MySQL数据库
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# 执行备份命令
dump_cmd = 'mysqldump --user={0} --password={1} --host={2} {3} > {4}/{5}'.format(config['user'], config['password'], config['host'], config['database'], backup_dir, backup_file_name)
os.system(dump_cmd)

# 关闭MySQL连接
cursor.close()
cnx.close()

# 输出备份文件路径
print('Backup saved to', backup_dir + '/' + backup_file_name)
```


3、定期运行该脚本。

您可以使用操作系统的定时任务功能，在适当的时间间隔内运行备份脚本，以确保数据库始终得到备份。