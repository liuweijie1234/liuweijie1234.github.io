---
title: MySQL 配置文件解读
date: 2024-01-15 10:00:00
tags:
- MySQL
categories:
- MySQL
---

Windows 配置文件是 .ini，Mac/linux 是 .cnf

```bash
[Windows]
MySQL\MySQL Server 5.7\my.ini

[Linux / Mac]
/etc/my.cnf
/etc/mysql/my.cnf 
```

## 客户端配置
```ini
[client]

port=3306  # 默认连接端口为 3306

# socket=MYSQL # 本地连接的 socket 套接字

# pipe=
```

[mysql]
```ini
no-beep

# default-character-set= utf8 # 设置字符集，通常使用 uft8 即可

# server_type=2
```

### 服务端配置

[mysqld]

```ini
# 接下来的三个选项与下面的 SERVER_PORT 是互斥的。
# skip-networking
# enable-named-pipe
# shared-memory

# shared-memory-base-name=MYSQL

# MySQL 服务器将使用的管道
# socket=MYSQL

# 在 MySQL 服务器创建的命名管道上授予客户端的访问控制。
# named-pipe-full-access-group=

# MySQL 服务器将侦听的 TCP/IP 端口
port=3306

# MySQL的安装目录路径。 所有路径通常都是相对于此进行解析的。
# basedir="C:/Program Files/MySQL/MySQL Server 5.7/"

# 数据库根路径
#datadir=C:/ProgramData/MySQL/MySQL Server 5.7/Data
datadir=D:/ProgramData/MySQL/Data

# 新模式或表创建时将使用的默认字符集 已创建且未定义字符集
# character-set-server=utf8

# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB

# 当前服务器SQL模式，可以动态设置。模式影响 MySQL 支持的 SQL 语法及其执行的数据验证检查。这可以更方便的在不同的环境下使用MySQL以及与其他的MySQL一起使用数据库服务器。
sql-mode="ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"

# 一般日志和慢速日志。
log-output=FILE

general-log=0

general_log_file="ATE-SERVER.log"

slow-query-log=1

slow_query_log_file="ATE-SERVER-slow.log"

long_query_time=10

# 错误日志
log-error="ATE-SERVER.err"

# ***** Group Replication Related *****
# 指定用于二进制日志文件的基本名称。 启用二进制日志记录后，服务器会将所有更改数据的语句记录到二进制日志中，用于备份和复制。
# log-bin

# ***** Group Replication Related *****
# 指定服务器ID。 对于复制拓扑中使用的服务器，必须为每个复制服务器指定唯一的服务器 ID，范围为 1 到 2^32 - 1。“唯一”意味着每个 ID 必须与使用的其他每个 ID 不同 由任何其他复制源或副本。
server-id=1

# ***** Group Replication Related *****
# 指示表和数据库名称如何存储在磁盘上以及如何在 MySQL 中使用。
# Value 0 = 表和数据库名称使用 CREATE TABLE 或 CREATE DATABASE 语句中指定的字母大小写存储在磁盘上。 名称比较区分大小写。 如果您在文件名不区分大小写的系统（例如 Windows 或 macOS）上运行 MySQL，则不应将此变量设置为 0。 如果在不区分大小写的文件系统上使用 --lower-case-table-names=0 强制此变量为 0，并使用不同的字母大小写访问 MyISAM 表名，则可能会导致索引损坏。

# Value 1 = 表名称以小写形式存储在磁盘上，名称比较不区分大小写。 MySQL 在存储和查找时将所有表名转换为小写。 此行为也适用于数据库名称和表别名。

# Value 2 = 表和数据库名称使用 CREATE TABLE 或 CREATE DATABASE 语句中指定的字母大小写存储在磁盘上，但 MySQL 在查找时将它们转换为小写。 名称比较不区分大小写。 这仅适用于不区分大小写的文件系统！ InnoDB表名和视图名以小写形式存储，如lower_case_table_names=1。
lower_case_table_names=1

# 该变量用于限制数据导入和导出操作的效果，例如由 LOAD DATA 和 SELECT ... INTO OUTFILE 语句以及 LOAD_FILE() 函数执行的操作。 这些操作仅允许具有 FILE 权限的用户执行。
secure-file-priv="C:/ProgramData/MySQL/MySQL Server 5.7/Uploads"

# MySQL 服务器允许的最大并发会话数。 这些连接之一将为具有 SUPER 权限的用户保留，以便即使已达到连接限制，也允许管理员登录。
max_connections=151

# 所有线程打开的表的数量。 增加该值会增加 mysqld 所需的文件描述符的数量。 因此，您必须确保在 [mysqld_safe] 部分的变量“open-files-limit”中将允许打开的文件数量设置为至少 4096
table_open_cache=2000

# 定义由 MEMORY 存储引擎以及从 MySQL 8.0.28 开始的 TempTable 存储引擎创建的内部内存临时表的最大大小。
# 如果内部内存临时表超过此大小，它将自动转换为磁盘内部临时表。【重点】
tmp_table_size=2G

#*** MyISAM Specific options
# 重新创建 MyISAM 索引时（在 REPAIR TABLE、ALTER TABLE 或 LOAD DATA 期间）允许 MySQL 使用的临时文件的最大大小。 如果文件大小大于此值，则会使用键缓存创建索引，但速度较慢。
# 该值以字节为单位给出。
myisam_max_sort_file_size=2146435072

# 在 REPAIR TABLE 期间对 MyISAM 索引进行排序或使用 CREATE INDEX 或 ALTER TABLE 创建索引时分配的缓冲区大小。
myisam_sort_buffer_size=4G

# Key Buffer 的大小，用于缓存 MyISAM 表的索引块。 不要将其设置为大于可用内存的 30%，因为操作系统也需要一些内存来缓存行。
# 即使您不使用 MyISAM 表，您仍然应该将其设置为 8-64M，因为它也将用于内部临时磁盘表。
key_buffer_size=8M

# 每个对 MyISAM 表进行顺序扫描的线程都会为其扫描的每个表分配一个此大小（以字节为单位）的缓冲区。
# 如果执行多次顺序扫描，您可能需要增加该值，默认为 131072。该变量的值应该是 4KB 的倍数。
# 如果它设置的值不是 4KB 的倍数，则其值将向下舍入到最接近的 4KB 倍数。
# MySQL 读入缓存的大小。如果对表对顺序请求比较频繁对话，可通过增加该变量值以提高性能。【重点】
read_buffer_size=128K

# 该变量用于从 MyISAM 表读取，并且对于任何存储引擎，用于多范围读取优化。
read_rnd_buffer_size=256K

#*** INNODB Specific options ***
# innodb_data_home_dir=

# 如果您有启用了 InnoDB 支持的 MySQL 服务器，但您不打算使用它，请使用此选项。 这将节省内存和磁盘空间并加快某些速度。
# skip-innodb

# 如果设置为 1，InnoDB 将在每次提交时将事务日志刷新（fsync）到磁盘，这提供了完整的 ACID 行为。
# 如果您愿意牺牲这种安全性，并且正在运行小型事务，则可以将其设置为 0 或 2 以减少日志的磁盘 I/O。
# 值 0 表示日志仅写入日志文件，并且日志文件大约每秒刷新一次到磁盘。
# 值 2 表示每次提交时都会将日志写入日志文件，但日志文件大约每秒仅刷新到磁盘一次。
innodb_flush_log_at_trx_commit=1

# InnoDB 用于写入日志文件的缓冲区大小（以字节为单位）磁盘。
# 默认值从 8MB 更改为 16MB，引入 32KB和 64KB innodb_page_size 值。
# 大的日志缓冲区支持大事务在事务提交之前无需将日志写入磁盘即可运行。
# 因此，如果您有更新、插入或删除许多行的事务，则日志缓冲区越大，可以节省磁盘 I/O。
innodb_log_buffer_size=16M

# 缓冲池的大小（以字节为单位），InnoDB 缓存表和索引数据的内存区域。
# 默认值为 134217728 字节 (128MB)。
# 最大值取决于CPU架构； 32 位系统上的最大值为 4294967295 (232-1)，64 位系统上的最大值为 18446744073709551615 (264-1)。在 32 位系统上，CPU 架构和操作系统可能会施加比规定的最大值更低的实际最大大小。
# 当缓冲池的大小大于1GB时，将innodb_buffer_pool_instances设置为大于1的值可以提高繁忙服务器上的可伸缩性。
# 影响 MySQL 性能的关键配置之一。它决定了 InnoDB 存储引擎可以使用的内存大小，用来缓存数据和索引。将其设置为物理内存的 60%-80% 通常可以获得最佳性能。
innodb_buffer_pool_size=128M

# 日志组中每个日志文件的大小。
# 您应该将日志文件的组合大小设置为缓冲池大小的大约 25%-100%，以避免日志文件覆盖时出现不必要的缓冲池刷新活动。
# 但请注意，较大的日志文件大小将增加恢复过程所需的时间。
innodb_log_file_size=48M

# 定义 InnoDB 内部允许的最大线程数。
# 值 0（默认值）被解释为无限并发（无限制）。 该变量旨在用于高并发系统上的性能调优。
# InnoDB 尝试保持 InnoDB 内部的线程数小于或等于 innodb_thread_concurrency 限制。
# 一旦达到限制，额外的线程就会被放入“先进先出”(FIFO) 队列中等待线程。 等待锁的线程不计入并发执行线程数。
innodb_thread_concurrency=33

# 当自动扩展 InnoDB 系统表空间文件变满时，用于扩展其大小的增量大小（以 MB 为单位）。
innodb_autoextend_increment=64

# InnoDB缓冲池划分的区域数。
# 对于缓冲池在数 GB 范围内的系统，将缓冲池划分为单独的实例可以通过减少不同线程读取和写入缓存页面时的争用来提高并发性。
innodb_buffer_pool_instances=8

# 确定可以同时进入 InnoDB 的线程数。
innodb_concurrency_tickets=5000

# 指定插入到旧子列表中的块在首次访问后必须保留多长时间（以毫秒 (ms) 为单位）
# 它可以移动到新的子列表中。
innodb_old_blocks_time=1000

# 启用此变量后，InnoDB 在元数据语句期间更新统计信息。
innodb_stats_on_metadata=0

# 当启用 innodb_file_per_table 时（5.6.6 及更高版本中的默认值），InnoDB 将每个新创建的表的数据和索引存储在单独的 .ibd 文件中，而不是存储在系统表空间中。
innodb_file_per_table=1

# 使用以下值列表：0 表示 crc32、1 表示 strict_crc32、2 表示 innodb、3 表示 strict_innodb、4 表示 none、5 表示 strict_none。
innodb_checksum_algorithm=0

# 如果将其设置为非零值，则每隔flush_time秒关闭所有表以释放资源并将未刷新的数据同步到磁盘。
# 此选项最好仅在资源最少的系统上使用。
flush_time=0

# 用于普通索引扫描、范围索引扫描以及不使用索引并因此执行全表扫描的联接的缓冲区的最小大小。
join_buffer_size=256K

# 允许最大数据包的大小，防止服务器发送过大的数据包
# 或由 mysql_stmt_send_long_data() C API 函数发送的任何参数。
max_allowed_packet=4M

# 如果来自主机的连续连接请求超过此数量而没有成功连接，则服务器会阻止该主机执行进一步的连接。
max_connect_errors=100

# 更改 mysqld 可用的文件描述符的数量。
# 如果 mysqld 给你错误“打开文件太多”，你应该尝试增加这个选项的值。
open_files_limit=4161

# 如果您在 SHOW GLOBAL STATUS 输出中看到每秒有许多 sort_merge_passes，则可以考虑增加 sort_buffer_size 值以加速 ORDER BY 或 GROUP BY 操作，而这些操作无法通过查询优化或改进索引来改进。
# MySQL 执行排序时，使用的缓存大小。增大这个缓存，提高 group by，order by 的执行速度。【重点】
sort_buffer_size=256K

# 指定基于行的二进制日志事件的最大大小（以字节为单位）。
# 如果可能，行将被分组为小于此大小的事件。 该值应该是 256 的倍数。
binlog_row_event_max_size=8K

# If the value of this variable is greater than 0, a replica synchronizes its master.info file to disk.
# (using fdatasync()) after every sync_master_info events.
sync_master_info=10000

# If the value of this variable is greater than 0, the MySQL server synchronizes its relay log to disk.
# (using fdatasync()) after every sync_relay_log writes to the relay log.
sync_relay_log=10000

# 如果此变量的值大于 0，副本会将其 master.info 文件同步到磁盘。
# （使用 fdatasync()）在每个sync_master_info事件之后。
sync_relay_log_info=10000

# 在开始时加载mysql插件。“plugin_x;plugin_y”。
# plugin_load

# MySQL Server X 协议将侦听的 TCP/IP 端口。
# loose_mysqlx_port=33060

```
修改前请备份配置文件，检查是否存在该配置项
SHOW VARIABLES LIKE '%thread_cache_size%';

max_connections=300
max_allowed_packet=500M
innodb_thread_concurrency=64
key_buffer_size=256M

innodb_buffer_pool_size=4G

innodb_log_buffer_size=20M
read_buffer_size=4M
sort_buffer_size=4M
read_rnd_buffer_size=8M

> 如果你的 MySQL 版本使用查询缓存（MySQL 8.0 及之后的版本已移除该功能），确保它的大小和类型设置合理：
query_cache_size=128M
query_cache_type=1

thread_cache_size=64



[mysql配置文件优化](https://blog.csdn.net/qq_33932782/article/details/110533931)