---
title: Windows MySQL 主主复制
date: 2022-08-15 11:42:00
tags:
- MySQL
categories:
- MySQL
---


## 一、架构区别

### 主主架构

本质：互为主从复制

两个或者多个主库同时提供服务，负载均衡

第一，数据一致性问题，一致性解决方案可解决问题。
第二，主键冲突问题，ID统一地由分布式ID生成服务来生成可解决问题。

![](./images/31065741_61ce3965e769335026.webp)

### 主从架构

在一主多从的数据库体系中，多个从服务器采用异步的方式更新主数据库的变化，业务服务器在执行写或者相关修改数据库的操作是在主服务器上进行的，读操作则是在各从服务器上进行。

- 优点：

1、读写分离：解决 SQL命令导致锁表的问题，提高系统流畅性
3、数据备份：多个数据备份，故障节点方便替换
3、高可用HA
1、一主多从：提高业务可用性，提升数据库负载性能

- 缺点：

1、主库单点：若业务量越来越大，I/O访问频率高，单机性能无法满足，需要改造成 多主 或者 多库，来降低I/O访问频率

#### 架构图

![](./images/31065742_61ce39662f2d761018.webp)

![](./images/v2-cfdff80703dc1a7d6da6ec5fbcd4fc13_r.jpg)

#### 工作流程

![](./images/v2-1411625068bcd9b7a0dca872efc1b8a4_720w.webp)

1、主库db的更新事件(update、insert、delete)被写到binlog
2、从库启动并发起连接，连接到主库
3、主库创建一个binlog dump thread，把binlog的内容发送到从库
4、从库启动之后，创建一个I/O线程，读取主库传过来的binlog内容并写入到relay log
5、从库启动之后，创建一个SQL线程，从relay log里面读取内容，从Exec_Master_Log_Pos位置开始执行读取到的更新事件，将更新内容写入到slave的db

注：上述流程为相对流程，并非绝对流程

#### 主从形式

1、一主一从

2、一主多从

3、多主一丛

4、双主复制

5、联级复制

参考 ：[MySQL主从同步详解与配置](https://zhuanlan.zhihu.com/p/335142300)

### 主备架构

只有主库提供读写服务，备库冗余作故障转移用。

第一，性能一般，这点可以通过建立高效的索引和引入缓存来增加读性能，进而提高性能。这也是通用的方案。
第二，扩展性差，这点可以通过分库分表来扩展。

![](./images/31065742_61ce3966440ea26098.webp)


参考：[主主、主从和主备区别](https://blog.51cto.com/u_11440114/5099110)

## 二、配置

本文主要讲解 主主架构，没有使用GTID模式

MySQL 主主复制（Master-Master Replication）指的是两个或多个 MySQL 服务器之间相互复制数据，并且每个服务器都可以处理来自客户端的读写请求。

### 2.1 主从配置

#### i 配置流程

参考：

[mysql主从复制配置](https://blog.csdn.net/qq_48721706/article/details/122520672)

[MySQL主从数据库配置](https://blog.csdn.net/weixin_44454512/article/details/124278646)

[windows mysql 主从配置](https://cloud.tencent.com/developer/article/1947879)

#### ii 主从问题

[mysql主从的一些问题](https://blog.csdn.net/guo_3472428370/article/details/125060909)

问题一：主从，那如果主服务器突然挂了怎么办？

答：手动切换从机器为主机器，待操作

问题二：怎样将正在使用的数据库变成主 或者从

[Linux下Mysql主从同步配置，以及如何同步主库已有数据到从库](https://blog.csdn.net/zlf_php/article/details/88937531)
[mysql主从复制-主库已有数据](https://blog.csdn.net/Xumuyang_/article/details/103348617)
[【MySQL】一文解决主库已有数据的主从复制](https://blog.csdn.net/fangkang7/article/details/105404787)

问题三：
如果主从，数据同步失败，怎么发现和处理

答：手动处理

问题四：
主从复制，从在写入是特别慢，有什么好的解决方案吗？
[mysql主从的一些问题](https://blog.csdn.net/guo_3472428370/article/details/125060909)

### 2.2 配置步骤

配置前提：

- MySQL软件 版本一致
- 数据库 数据一致 或 为空(若存在数据，应停止写入 、进行数据备份，保持两台MySQL数据一致)
- 数据库 编码一致 (不然会报错)

参考:

[Mysql 数据库 主从数据库 (主从)(主主)](https://blog.csdn.net/qq_53840970/article/details/124736793)
[Mysql（双主）主主架构配置](https://cloud.tencent.com/developer/article/1119242)


主主 其实就是互为主从关系

服务器A，IP: 172.16.2.227
服务器B，IP: 172.16.2.228

#### i 配置流程


##### 1. 停止MySQL服务

Windows
方法一：`net stop mysql`
方法二：`Win+R`，输入 `services.msc` 进入服务，页面操作，停止 MySQL 服务

Linux
命令：`systemctl stop mysqld`

##### 2. 配置文件修改

默认路径
Windows C:\ProgramData\MySQL\MySQL Server 5.7\my.ini 
Linux /etc/my.cnf

> 注意： 记得备份配置文件

服务器 A (172.16.2.227) 配置，建议手动配置

```ini
[mysqld]

# 开启二进制日志
log-bin="WIN-2-227-bin.log"
#log_bin_index="WIN-2-227.bin.index"
# 需要同步的数据库名，如果有多个数据库，可重复此参数，每个数据库一行（和下面binlog-ignore-db二选一）,与gtid冲突
binlog-do-db=test
# 不同步mysql系统数据库
# binlog-ignore-db=mysql
# 使binlog在每N次binlog写入后与硬盘同步
sync-binlog=1
# 二进制日志记录格式
binlog_format=ROW
# 7天时间自动清理二进制日志
expire_logs_days=7

relay_log="WIN-2-227.relay"
# 设置服务器id
server-id=1
# 自增主键配置
auto_increment_increment=2
auto_increment_offset=1

# 目前暂未配置下面参数
# 配置gtid
gtid_mode=ON
enforce_gtid_consistency=ON
log_slave_updates = ON
# 控制innodb是否对gap加锁，提高性能
innodb_locks_unsafe_for_binlog=1
```

服务器B (172.16.2.228) 配置，建议手动配置

```ini
[mysqld]
log-bin="WIN-2-228-bin.log"
#log_bin_index="WIN-2-228.bin.index"
binlog-do-db=test
#binlog_ignore_db
sync-binlog=1
binlog_format = ROW
expire_logs_days=7
relay_log="WIN-2-228.relay"
server-id=2
auto_increment_increment=2
auto_increment_offset=2

#gtid_mode=ON
#enforce_gtid_consistency=ON
#log_slave_updates = ON
```

- auto_increment_increment : 表示自增长字段每次递增的量，其默认值是1，取值范围是1 .. 65535
- auto_increment_offset : 表示自增长字段从那个数开始，他的取值范围是1 .. 65535

参考：[Mysql设置auto_increment_increment和auto_increment_offset](https://blog.csdn.net/xinyuan_java/article/details/93874555)

[Mysql数据库之Binlog日志使用总结(必看篇)](https://zhuanlan.zhihu.com/p/106766282)

- gtid_mode：指定GTID模式是否启用，可以设置为ON或OFF，默认为OFF。

- enforce_gtid_consistency：在事务提交之前检查GTID，以确保从属服务器上没有重复或丢失的事务。可以设置为ON或OFF，默认为OFF。
- log_slave_updates：指定从属服务器是否记录复制事件到二进制日志中。如果设置为ON，则会自动记录所有读取的事务，包括主库执行的事务和从属服务器上重新执行的事务。如果设置为OFF，则不会将从属服务器上的事务记录到二进制日志中。

##### 3. 重启MySQL

Windows
方法一：`net start mysql`
方法二：`Win+R`，输入 `services.msc` 进入服务，页面操作，启动 MySQL 服务

Linux
命令：`systemctl restart mysqld`

##### 4. 建立读取账户

<font color=red>注意：专门用给从库连接的，注意这是在主库里面建立的</font>

在 172.16.2.227 创建
```sql
# 1. 创建账户
CREATE USER 'MySlave228'@'172.16.2.228' IDENTIFIED BY '123456';
# 2. 授权
GRANT REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'MySlave228'@'172.16.2.228';
# 3. 刷新权限
FLUSH PRIVILEGES;
# 4. 检查权限，显示账户权限
SHOW GRANTS FOR 'MySlave228'@'172.16.2.228';
```

在 172.16.2.228 创建
```sql
# 1. 创建账户
CREATE USER 'MySlave227'@'172.16.2.227' IDENTIFIED BY '123456';
# 2. 授权
GRANT REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'MySlave227'@'172.16.2.227';
# 3. 刷新权限
FLUSH PRIVILEGES;
# 4. 检查权限，显示账户权限
SHOW GRANTS FOR 'MySlave227'@'172.16.2.227';
```

测试:
在 172.16.2.227 机器上测试账号远程连通性, 
```bash
mysql -h 172.16.2.228 -u MySlave227 -p
```


在 172.16.2.228 机器上测试账号远程连通性, 
```bash
mysql -h 172.16.2.227 -u MySlave228 -p
```

小知识：
REPLICATION CLIENT：授予此权限，复制用户可以使用 `SHOW MASTER STATUS`, `SHOW SLAVE STATUS`和 `SHOW BINARY LOGS`来确定复制状态。

REPLICATION SLAVE：授予此权限，复制才能真正工作。使帐户能够使用 `SHOW SLAVE HOSTS` , `SHOW RELAYLOG EVENTS` 和 `SHOW BINLOG EVENTS` 

##### 5. 获取主库基本信息

（二次确认）用于从库服务器的配置

```sql
# 查看主服务器状态（得到File和Position）
show master status\G

SELECT @@GLOBAL.GTID_EXECUTED;
```

- 其他查看命令

```sql
# 查看服务器id
show global variables like 'server_id';
# 查看端口号
show global variables like 'port';
# 查看配置自增长字段（全局变量）
show global variables like '%auto_increment%';
show global variables like 'binlog_format';


# 查看配置自增长字段（会话变量）
show variables like '%auto_inc%';
# 查看地址
show variables like 'datadir';
# 查看binlog 事件
show binlog events\G

show global variables like 'gtid_mode';
show global variables like 'enforce_gtid_consistency';


show global variables like 'innodb_locks_unsafe_for_binlog';

```


##### 6. 配置从服务器

服务器 A (172.16.2.227) 查询得到需要的数据
```sql
mysql> show master status\G;
*************************** 1. row ***************************
             File: WIN-2-227.000001
         Position: 154
     Binlog_Do_DB: test
 Binlog_Ignore_DB:
Executed_Gtid_Set:
1 row in set (0.00 sec)
```
服务器 B (172.16.2.228) 操作
```sql
# 停止复制线程
stop slave;

CHANGE MASTER TO MASTER_HOST='172.16.2.227',MASTER_PORT=3306,MASTER_USER='MySlave228',MASTER_PASSWORD='123456',MASTER_LOG_FILE='WIN-2-227.000001',MASTER_LOG_POS=154;

# 启动复制线程
start slave;

# 检查从服务器的状态，确保它已经成功连接到主库并开始复制数据：
show slave status\G
```

-----------------------------------------分割线-----------------------------------------

服务器 B (172.16.2.228) 查询得到需要的数据
```sql
mysql> show master status\G;
*************************** 1. row ***************************
             File: WIN-2-228.000001
         Position: 154
     Binlog_Do_DB: test
 Binlog_Ignore_DB:
Executed_Gtid_Set:
1 row in set (0.00 sec)
```
服务器 A (172.16.2.227) 操作

```sql
stop slave;
CHANGE MASTER TO MASTER_HOST='172.16.2.228',MASTER_PORT=3306,MASTER_USER='MySlave227',MASTER_PASSWORD='123456',MASTER_LOG_FILE='WIN-2-228.000001',MASTER_LOG_POS=154;
start slave;

# 查看从服务器状态
show slave status\G
```

参数解释：

- MASTER_HOST : 设置要连接的主数据库的IP地址

- MASTER_PORT : 设置要连接的主服务器的端口

- MASTER_USER : 设置要连接的主数据库的用户名

- MASTER_PASSWORD : 设置要连接的主数据库的密码

- MASTER_AUTO_POSITION : 用于自动选择新的复制位置。在 MySQL 5.6.5 之后的版本中，可以使用该参数代替 MASTER_LOG_FILE 和 MASTER_LOG_POS 参数，从而简化主主复制的配置。

当 MASTER_AUTO_POSITION=1 时，MySQL 将自动检测并记录每个服务器上的二进制日志文件和位置信息，并根据最近的可用数据进行复制。这样可以避免手动指定位置信息的错误或不一致，从而提高主主复制的可靠性和稳定性。

-MASTER_LOG_FILE : 设置要连接的主数据库的bin日志的日志名称（show master status）;

-MASTER_LOG_POS : 设置要连接的主数据库的bin日志的记录位置（show master status）(这里注意，最后项不需要加引号。否则配置失败)




需要注意的是，使用 MASTER_AUTO_POSITION 并不意味着自动发现服务器故障或网络问题。因此，在实际的主主复制部署中，还需要定期备份数据、监控主从状态和测试故障转移过程，以确保系统的可靠性和稳定性。

对于MASTER_AUTO_POSITION参数，只能填写数字1或默认值0。当设置为1时，表示从属服务器会自动更新复制的主库位置信息。这种情况下，您需要使用GTID（Global Transaction Identifier，全局事务标识符）来确保正确性和高可用性。

在MySQL 5.6及更高版本中，可以通过执行以下命令来启用gtid模式并获取当前复制状态的信息：

SET @@GLOBAL.GTID_MODE = ON;

SELECT @@GLOBAL.GTID_MODE;
SELECT @@GLOBAL.GTID_EXECUTED;

在MySQL 5.7及更高版本中，您还可以运行以下命令来查看当前主库上所有的GTID：

SELECT @@GLOBAL.GTID_PURGED;

根据这些信息，您可以配置从属服务器以开始复制数据。请注意，在使用GTID模式时，必须禁用 binlog_do_db 和 binlog_ignore_db 选项。





报错

```log
执行 CHANGE MASTER TO MASTER_HOST='192.168.0.110',MASTER_PORT=3306,MASTER_USER='MySlave110',MASTER_PASSWORD='123456',MASTER_AUTO_POSITION=1; 
这个命令报错
CHANGE MASTER TO MASTER_HOST='192.168.0.110',MASTER_PORT=3306,MASTER_USER='MySlave110',MASTER_PASSWORD='123456',MASTER_AUTO_POSITION=1;
```

如果执行该命令时出现错误，可能是由于以下原因之一：

无法连接到主库。请检查主库的IP地址、端口号、用户名和密码是否正确，并确保从属服务器可以访问该主库。

主库没有启用GTID模式。在使用MASTER_AUTO_POSITION参数时，需要使用GTID模式来确保正确性和高可用性。

您没有足够的权限来执行CHANGE MASTER命令。请确保您的用户有REPLICATION SLAVE权限，并且已经配置了正确的权限和角色分配。

该从属服务器已经存在一个复制通道。在启动新的复制通道之前，请确保删除旧的通道并清除相关的状态信息。

您的MySQL版本不支持MASTER_AUTO_POSITION参数。请检查您的MySQL版本是否符合要求。

在更改主库配置之前，请确保所有当前正在进行的事务都已经提交或回滚。否则，可能会导致数据不一致和数据丢失。

当出现问题时，请仔细阅读错误消息，并尝试修复问题。在解决问题之前，建议备份所有重要数据以避免数据丢失。


```log
ERROR 1598 (HY000): Binary logging not possible. Message: MySQL server failed to update the binlog.index file's content properly. It might not be in sync with available binlogs and the binlog.index file state is in unrecoverable state. Aborting the server.
```
这个错误提示说明MySQL服务器无法更新二进制日志索引文件(binlog.index)，导致其与可用的二进制日志文件不同步，并且该状态无法恢复。因此，MySQL服务器无法继续进行二进制日志记录或复制操作，并中止了服务。

要解决这个问题，可以尝试执行以下步骤：

首先，备份所有二进制日志和索引文件，以免丢失任何重要数据。

停止MySQL服务器并检查二进制日志目录(binlog_dir)及其下面的所有文件和子目录的权限和所有权设置是否正确。确保MySQL用户具有读写权限，并且所有者是正确的。

在安全模式下重新启动MySQL服务器，并检查错误日志文件以获取可能有关该问题的详细信息。

如果您发现binlog.index文件已损坏，则可以尝试手动删除该文件，并使用FLUSH LOGS命令重新生成新的二进制日志索引文件。请注意，这将删除所有旧的二进制日志文件并创建一个新的文件，因此在执行此操作之前应该备份所有的二进制日志文件：

mysql> FLUSH LOGS;

如果上述方法都不能解决问题，则需要考虑恢复备份数据并重新创建二进制日志文件。

请注意，在修复问题后，建议定期备份所有的二进制日志和索引文件，并监控系统以确保它们一直保持同步。

```log
[ERROR] While rebuilding index file .\WIN-6FD6Q015AUJ.index: Failed to rename the new index file to the existing index file.
```

这个错误通常出现在MySQL或MariaDB使用MyISAM存储引擎并尝试重建索引文件时。它表示无法将新的索引文件重命名为现有的索引文件，可能是因为该文件正在被其他进程占用。

要解决这个问题，可以尝试以下步骤：

检查磁盘空间：确保磁盘上还有足够的空间来创建新的索引文件。

关闭MySQL服务：通过关闭MySQL服务来确保没有其他进程正在访问索引文件。在关闭MySQL服务之前，可以使用SHOW FULL PROCESSLIST命令检查是否有其他进程正在运行。

删除现有的索引文件：手动删除现有的索引文件以便系统能够重新创建。

重启MySQL服务：启动MySQL服务，它会自动创建新的索引文件。如果MySQL仍然无法创建新文件，请确保MySQL用户具有足够的权限来写入该目录，或者尝试将索引文件移动到另一个位置并在my.cnf中更新索引文件路径。

如果上述步骤都无法解决问题，则可能需要考虑使用数据恢复工具尝试修复索引文件，或者备份数据并重新构建数据库。

请注意，在重建索引文件之前，应该定期备份所有的数据以避免意外数据损失。


```log
Slave_IO_Running: Connecting
Slave_SQL_Running: Yes
Last_IO_Errno: 1130
Last_IO_Error: error connecting to master 'MySlave109@192.168.0.110:3306' - retry-time: 60  retries: 4
```



#### ii 报错及解决方法

##### Slave_IO_Running 问题


- **问题 : `Slave_IO_Running: No`**

问题状态码及描述:

```log
Slave_IO_Running: No
Slave_SQL_Running: Yes
Last_IO_Errno: 1236
Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'Could not find first log file name in binary log index file'
```

`Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'Could not open log file'`

解决方法：
```sql
# 主服务器生成新的bin logs文件
flush logs;
# 查看主服务器状态（得到File和Position）
show master status\G

*************************** 1. row ***************************
             File: WIN-2-228.000003
         Position: 154
     Binlog_Do_DB: test
 Binlog_Ignore_DB:
Executed_Gtid_Set:
1 row in set (0.00 sec)
-----------------分割线-----------------------------
# 从服务器配置
stop slave;
CHANGE MASTER TO MASTER_HOST='172.16.2.228',MASTER_PORT=3306,MASTER_USER='MySlave227',MASTER_PASSWORD='123456',MASTER_LOG_FILE='WIN-2-228.000003',MASTER_LOG_POS=154;
start slave;

# 查看从服务器状态
show slave status\G
``` 

[mysql主从同步出现Slave_IO_Running:NO的解决办法](https://blog.csdn.net/shangdi1988/article/details/94639778)


- **问题: `Slave_IO_Running: Connecting`**

解决方法:
一般是网络问题,等一会再check。

[Mysql主从同步时Slave_IO_Running：Connecting 问题排查](https://blog.csdn.net/panrenjun/article/details/114219097)

##### Slave_SQL_Running 问题

- **问题: `Slave_SQL_Running: No`**

解决方法:
```sal
mysql> stop slave;
mysql> SET GLOBAL sql_slave_skip_counter=1;
mysql> start slave;
# 查看从服务器状态
mysql> show slave status\G
mysql> show global variables like 'SQL_SLAVE_SKIP_COUNTER';
```
查看从库状态后，两Yes状态，即表示成功了。


sql_slave_skip_counter 是 MySQL 主从复制中的一个参数，可以用于跳过执行指定数量的 SQL 语句。

当在主服务器上执行某些写入操作时，MySQL 将这些操作复制到从服务器以保持主从一致。但有时由于数据或网络问题等原因，导致从服务器出现错误或延迟，从而导致主从不一致。如果出现这种情况，可以使用 sql_slave_skip_counter 参数来跳过执行指定数量的 SQL 语句，以重新与主服务器保持一致。

具体来说，当从服务器出现错误时，可以通过将该参数设置为要跳过的 SQL 语句数量来告诉 MySQL 跳过这些语句并继续执行后面的语句。例如，如果要跳过前三个 SQL 语句，则可以使用以下命令：

STOP SLAVE;
SET GLOBAL sql_slave_skip_counter = 3;
START SLAVE;

需要注意的是，跳过 SQL 语句可能会导致从服务器数据不一致，因此必须确保跳过的语句不重要或已经在其他方式下被执行。

- **问题 : `ERROR 1872 (HY000): Slave failed to initialize relay log info structure from the repository`**

解决方法:

```sal
mysql> show master logs; //查看master的binlog日志列表
mysql> reset master; //删除master的binlog，即手动删除所有的binlog日志
mysql> show master status\G

mysql> stop slave;
mysql> reset slave; //删除slave的中继日志
mysql> reset slave all; //(彻底清理)
mysql> show slave status\G
然后重新配置主从
```

问题 :
```sql
Last_SQL_Errno: 1050 
Last_SQL_Error: Error 'Table 'events' already exists' on query. Default database: 'eygle'. Query: 'create table events`
```

解决方法:
https://www.cnblogs.com/tingxin/p/14289991.html


问题：
```sql
Slave_SQL_Running: No

Last_Errno: 1032
Last_Error: Could not execute Update_rows event on table ate_2022.services_bluetooth; Can't find record in 'services_bluetooth', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log WIN-0-12.000004, end_log_pos 2792

Last_Errno: 1032
Last_Error: Could not execute Update_rows event on table ate.celery_taskmeta; Can't find record in 'celery_taskmeta', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log WIN-6FD6Q015AUJ-bin.000001, end_log_pos 25096363

Last_Errno: 1032
Last_Error: Could not execute Delete_rows event on table ate.authtoken_token; Can't find record in 'authtoken_token', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log WIN-BLVULVB0JU7-bin.000001, end_log_pos 467



```
MySQL复制副本（从）服务器发生数据损坏后，需要再次完全同步数据库。为此，需要执行以下步骤：

1、锁定源（主）数据库服务器（写入此 MySQL 服务器的应用程序将在锁定期间失败）
2、检索当前源（主）状态信息
3、在（主）数据库服务器上转储数据库
4、解锁源（主）数据库服务器
5、将转储传输到副本（从属）服务器
6、停止副本（从属）服务器上的从属进程
7、在副本（从属）服务器上导入数据库转储
8、使用在副本（从属）服务器上的步骤 2 中检索到的信息更改复制设置
9、在副本（从）服务器上启动从属进程

参考[MySQL 复制不同步：如何进行完整数据库还原并解决错误 1032（无法执行 update_rows）](https://www.claudiokuenzler.com/blog/1075/mysql-replication-out-of-sync-full-database-restore-solve-error-1032-could-not-update)

问题：

```sql
Slave_IO_Running: Yes
Slave_SQL_Running: No
Last_Errno: 1677
Last_Error: Column 1 of table 'ate.django_migrations' cannot be converted from type 'varchar(1020(bytes))' to type 'varchar(765(bytes) utf8)'
```

这个错误提示表明 MySQL 在执行主从复制时遇到了问题。更具体地说，MySQL 尝试将原始服务器上的数据复制到从服务器上，但出现了类型转换错误。

在这种情况下，您可以尝试以下步骤来解决问题：

1、确认源和目标数据库的字符集和排序规则设置相同。在 MySQL 中，可以使用 `SHOW VARIABLES LIKE 'character_set_%';` 和 `SHOW VARIABLES LIKE 'collation_%';` 命令检查当前字符集和排序规则设置。

2、如果目标数据库的字符集或排序规则与源不同，则可以在执行 SQL 语句之前修改目标数据库的字符集和排序规则。在 MySQL 中，可以使用以下命令更改字符集和排序规则：

ALTER DATABASE dbname CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

3、如果更改字符集和排序规则无法解决问题，则可能需要手动修复受影响的表。在这种情况下，具体操作取决于表的结构和数据。您可以尝试使用 ALTER TABLE 命令更改列的类型，然后使用 UPDATE 命令更新数据。

例如，如果要将 django_migrations 表中的第一列从 varchar(1020) 更改为 varchar(765)，可以使用以下命令：

ALTER TABLE django_migrations MODIFY COLUMN <column_name> VARCHAR(765);
UPDATE django_migrations SET <column_name> = LEFT(<column_name>, 765);

需要注意的是，手动修改表结构和数据可能会对应用程序产生不利影响。因此，您应该在执行这些操作之前备份数据库，并在测试环境中测试它们。


小知识：
utf8mb4 和 utf8_general_ci 都是 MySQL 数据库中的字符集和排序规则。

utf8mb4 是一种全新的字符集，它支持存储更广泛的 Unicode 字符，包括大部分 emoji 表情。而 utf8_general_ci 则只支持 Unicode 的基本多语言平面（BMP），无法存储某些特殊字符，例如超出 BMP 范围的 emoji。

另外，排序规则也不同。utf8_general_ci 使用一种基于字符编码的简单排序算法，而 utf8mb4_general_ci 则使用一种更复杂的排序算法，以便正确地对待不同语言的区别处理。

因此，如果需要在 MySQL 中存储包含 emoji 等特殊字符的数据，并且需要正确地对待不同语言的排序，应该选择 utf8mb4 作为字符集，并使用相应的排序规则。


```sql
Slave_IO_Running: Yes
Slave_SQL_Running: No
Last_SQL_Errno: 1062
Last_SQL_Error: Could not execute Write_rows event on table ate.services_bluetooth; Duplicate entry 'K2A0231610001' for key 'sn', Error_code: 1062; handler error HA_ERR_FOUND_DUPP_KEY; the event's master log WIN-BLVULVB0JU7-bin.000001, end_log_pos 14480

```



##### 其他问题参考

[Mysql主从异常及常见问题处理](https://blog.csdn.net/m0_47116305/article/details/120368548)

[MySQL复制跳过错误](https://blog.csdn.net/coco3600/article/details/100232783)

一些error code代表的错误如下：

1007：数据库已存在，创建数据库失败

1008：数据库不存在，删除数据库失败

1050：数据表已存在，创建数据表失败

1051：数据表不存在，删除数据表失败

1054：字段不存在，或程序文件跟数据库有冲突

1060：字段重复，导致无法插入

1061：重复键名

1068：定义了多个主键

1094：位置线程ID

1146：数据表缺失，请恢复数据库

1053：复制过程中主服务器宕机

1062：主键冲突 Duplicate entry '%s' for key %d



问题：在 MySQL 主主复制中，如果两个服务器的自增长 ID 范围重叠，则可能会出现 ID 冲突。

为避免这种情况，可以采用以下几种方法：

1、手动指定 ID 范围：在每个服务器上，可以手动指定自增长 ID 的范围，以确保不会重叠。例如，在第一个服务器上将自增长 ID 设置为 1 到 1000000，在第二个服务器上将自增长 ID 设置为 1000001 到 2000000。

2、使用 UUID：UUID（Universally Unique Identifier）是一种全局唯一的标识符，可以用于代替自增长 ID。在主主复制中，可以使用 UUID 作为主键，从而避免 ID 冲突。

3、使用分布式 ID 生成器：分布式 ID 生成器可以在多台服务器之间生成唯一的 ID，例如 Twitter 的 Snowflake、百度的 UidGenerator 等。在主主复制中，可以使用分布式 ID 生成器生成唯一的 ID，从而避免 ID 冲突。

3、若只是双主，可以使用奇偶自增

auto_increment_increment=2
auto_increment_offset=1

[MySQL系统变量auto_increment_increment与auto_increment_offset学习总结](https://www.cnblogs.com/kerrycode/p/11150782.html)

需要注意的是，如果已经存在 ID 冲突，则需要手动解决冲突，并修改数据以使其唯一。同时，也需要对数据库的设计和应用程序进行重新评估，以避免类似的问题发生。








问题：配置报错，服务停止
`ERROR 1598 (HY000): Binary logging not possible. Message: MySQL server failed to update the binlog.index file's content properly. It might not be in sync with available binlogs and the binlog.index file state is in unrecoverable state. Ahorting the server`
![](/images/微信图片_20230113153312.png)
日志

[ERROR] While rebuilding index file .\WIN-0-12.index: Failed to rename the new index file to the existing index file.
[ERROR] D:\mysql-5.7\bin\mysqld: Binary logging not possible. Message: MySQL server failed to update the binlog.index file's content properly. It might not be in sync with available binlogs and the binlog.index file state is in unrecoverable state. Aborting the server.


参考 https://blog.csdn.net/u014735239/article/details/40746683


##### 7. 测试


| 测试任务 | 测试结果 |
| -- | -- |
| A机器创建表 | B机器创建该表 |
| A机器的表插入一条/多条数据 | B机器新增相同数据 |
| A机器的表更新一条数据 | B机器修改同一条数据 |
| A机器的表删除一条数据(B机器存在这个数据) | B机器删除同一条数据 |
| A机器的表清空所有数据(B机器表数据一致)   | B机器删除所有数据 |
| A机器删除表(B机器存在这个表，表数据一致)  | B机器删除该表 |
| A机器删除表(B机器存在这个表，表数据不一致) | B机器删除该表 |
| A机器删除B机器不存在的表 | 不存在表的机器slave异常 |

结论：操作不存在其中一台机器的数据，必定导致 另外一台 slave 异常报错。

##### 8. 测试命令操作

1、创建数据库

```sql
CREATE DATABASE `test` default charset utf8 COLLATE utf8_general_ci;
```

2、选择数据库

```sql
use `test`;
```

3、创建表

```sql
CREATE TABLE IF NOT EXISTS `tbl`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `title` VARCHAR(100) NOT NULL,
   `author` VARCHAR(40) NOT NULL,
   PRIMARY KEY ( `id` )
)DEFAULT CHARSET=utf8;
```

4、查看表

```sql
show tables;

desc `tbl`;
```

6、插入假数据 （从服务器不用）

```sql
INSERT INTO `tbl` ( title,author) VALUES ("python","小明");
INSERT INTO `tbl` ( title,author) VALUES ("java","小红");
INSERT INTO `tbl` ( title,author) VALUES ("PHP","小张");
INSERT INTO `tbl` ( title,author) VALUES ("C","小刘");
INSERT INTO `tbl` ( title,author) VALUES ("Golang","小赵");
INSERT INTO `tbl` ( title,author) VALUES ("C++","小洪");

UPDATE `tbl` SET author='小明白' WHERE id=1;

DELETE FROM tbl WHERE id=1;

INSERT INTO `tbl` ( title,author) VALUES ("IOS","小陈");
INSERT INTO `tbl` ( title,author) VALUES ("安卓","小陈");
```

7、查看表数据

```sql
mysql> select * from `tbl`;
+----+--------+--------+
| id | title  | author |
+----+--------+--------+
|  1 | python | 小明   |
|  2 | java   | 小红   |
|  3 | PHP    | 小张   |
|  4 | C      | 小刘   |
|  5 | Golang | 小赵   |
+----+--------+--------+
5 rows in set (0.00 sec)
```




[Win10如何开启远程桌面](https://jingyan.baidu.com/article/a948d651dc7b060a2dcd2e22.html)

[公司电脑上怎么固定内网IP地址，不让IP变动](https://blog.csdn.net/qq_41936224/article/details/106860155)

