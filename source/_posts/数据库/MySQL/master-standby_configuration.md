---
title: Windows MySQL 主备复制
date: 2023-05-15 09:00:00
tags:
- MySQL
categories:
- MySQL
---

与主从复制的 技术是一致的，只是对数据的读取不一样，导致称呼不一样

### 具体步骤说明

配置 Django 使用 MySQL 主备复制，需要进行以下步骤：

1、首先，在主库和备库上都安装 MySQL，并按照官方文档的说明启用主备复制功能。

2、在 Django 的 settings.py 文件中，配置数据库连接信息，将主库和备库的连接信息都填写进去。具体可以参考 Django 官方文档中的示例代码。

3、针对数据同步这个问题，可以使用 MySQL 自带的主备复制功能来实现。在主库上，每次有新的数据插入、更新或删除时，MySQL 会将相应的 binlog 记录发送到备库。备库会根据这些 binlog 记录来同步数据。

4、如果主库服务器挂了，备库如何快速切换成主库，需要手动进行操作。具体步骤是：将备库上的 MySQL 实例停止，然后将其配置成主库并启动 MySQL 实例。此时，原来的主库恢复后也必须重新进行配置，并启动 MySQL 实例。为了保证数据的一致性，可以考虑使用一些工具来协助完成主备切换的过程。

需要注意的是，在进行主备复制配置时，应该确保主库和备库的版本一致，否则可能会出现兼容性问题。此外，还应该定期进行备份和恢复测试，以确保备库能够正常工作，并且数据可以正确地同步到备库中。


### 主备复制详细步骤

主IP: 192.168.0.109
备IP: 192.168.0.110

#### 修改 MySQL 配置文件

停止 MySQL 服务

Windows
方法一：`net stop mysql`
方法二：`Win+R`，输入 `services.msc` 进入服务，页面操作，停止 MySQL 服务


备份 my.cnf 配置文件
Windows 配置文件 my.cnf 默认路径 
C:\ProgramData\MySQL\MySQL Server 5.7\my.ini 


修改 my.cnf 配置文件

编辑MySQL的配置文件my.cnf，在[mysqld]下添加如下内容：

主服务器: 192.168.0.109
```ini
[mysqld]
log-bin="WIN-6FD6Q015AUJ-bin.log"
binlog-do-db=ate
sync-binlog=1
binlog_format=ROW
expire_logs_days=7
server-id=1
```

从服务器: 192.168.0.110 （注释是用于备切主）
```ini
[mysqld]
#log-bin="WIN-BLVULVB0JU7-bin.log"
#binlog-do-db=ate
#sync-binlog=1
#binlog_format=ROW
#expire_logs_days=7
server-id=2
```

重启MySQL服务

Windows
方法一：net start mysql
方法二：Win+R，输入 services.msc 进入服务，页面操作，启动 MySQL 服务

#### 建立读取账户

<font color=red>注意：专门用给从库连接的，注意这是在主库里面建立的</font>

在 两个服务器都创建 同名的账户 

```sql
CREATE USER 'MySlave'@'%' IDENTIFIED BY '123456';
GRANT REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'MySlave'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'MySlave'@'%';
```


测试账号远程连通性:

在 从服务器: 192.168.0.110 机器上测试, 
```bash
mysql -h 192.168.0.109 -u MySlave -p
```

#### 获取主库基本信息

主服务器：192.168.0.109 
查询信息（得到File和Position）

```sql
show master status\G

*************************** 1. row ***************************
             File: WIN-6FD6Q015AUJ-bin.000001
         Position: 154
     Binlog_Do_DB: ate
 Binlog_Ignore_DB:
Executed_Gtid_Set:
1 row in set (0.00 sec)
```

##### 6. 配置从服务器

从服务器: 192.168.0.110

```sql
# 停止复制线程
stop slave;

# 配置复制
CHANGE MASTER TO 
MASTER_HOST='192.168.0.109',
MASTER_PORT=3306,
MASTER_USER='MySlave',
MASTER_PASSWORD='123456',
MASTER_LOG_FILE='WIN-6FD6Q015AUJ-bin.000001',
MASTER_LOG_POS=154;


# 启动复制线程
start slave;

# 查看从服务器状态
show slave status\G

```

暂不支持
MASTER_AUTO_POSITION=1;

ERROR 1777 (HY000): CHANGE MASTER TO MASTER_AUTO_POSITION = 1 cannot be executed because @@GLOBAL.GTID_MODE = OFF.


*************************** 1. row ***************************
             File: WIN-BLVULVB0JU7-bin.000001
         Position: 154
     Binlog_Do_DB: ate
 Binlog_Ignore_DB:
Executed_Gtid_Set:
1 row in set (0.00 sec)


CHANGE MASTER TO 
MASTER_HOST='192.168.0.109',
MASTER_PORT=3306,
MASTER_USER='MySlave',
MASTER_PASSWORD='123456',
MASTER_LOG_FILE='WIN-BLVULVB0JU7-bin.000001',
MASTER_LOG_POS=154;

### 备切主详细步骤

1、了解主服务器的IP信息

方法一：可以通过 进入 cmd 输入`ipconfig /all` 获取，
方法二：“控制面板” -> “网络和 Internet” -> “网络和共享中心” -> “更改适配器设置” -> "选择以太网-右键属性"  -> “Internet 协议版本 4 (TCP/IPv4)”

```bash
Windows IP 配置

   主机名  . . . . . . . . . . . . . : WIN-6FD6Q015AUJ
   主 DNS 后缀 . . . . . . . . . . . :
   节点类型  . . . . . . . . . . . . : 混合
   IP 路由已启用 . . . . . . . . . . : 否
   WINS 代理已启用 . . . . . . . . . : 否

以太网适配器 以太网 2:

   连接特定的 DNS 后缀 . . . . . . . :
   描述. . . . . . . . . . . . . . . : Intel(R) I211 Gigabit Network Connection
   物理地址. . . . . . . . . . . . . : C8-7F-54-50-69-1C
   DHCP 已启用 . . . . . . . . . . . : 否
   自动配置已启用. . . . . . . . . . : 是
   本地链接 IPv6 地址. . . . . . . . : fe80::1189:ba54:4e1b:51e8%4(首选)
   IPv4 地址 . . . . . . . . . . . . : 192.168.0.109(首选)
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : 192.168.0.1
   DHCPv6 IAID . . . . . . . . . . . : 63471444
   DHCPv6 客户端 DUID  . . . . . . . : 00-01-00-01-2B-A0-BD-5E-F8-E4-3B-90-F5-17
   DNS 服务器  . . . . . . . . . . . : 202.96.128.166
   TCPIP 上的 NetBIOS  . . . . . . . : 已启用
```

2、确保备用服务器与主服务器在同一个局域网中，并拥有相同的IP地址

如果备用服务器的IP地址与主服务器不同，您需要更改备用服务器的IP地址为主服务器的IP地址。

3、切换备用机器IP

打开“控制面板”并选择“网络和 Internet”- “网络和共享中心”。

在左侧菜单中点击“更改适配器设置”。

选择需要修改 IP 地址的网络连接，并右键点击它。

选择“属性”，然后在列表中找到“Internet 协议版本 4 (TCP/IPv4)”。

点击“属性”，然后在弹出窗口中选择“使用下面的 IP 地址”。

输入要更改的 IP 地址、子网掩码和默认网关。

点击“确定”保存更改


进入 cmd 输入`ipconfig /all` 查看是否一致，

4、停止MySQL复制线程并删除配置

```sql
# 停止复制线程
stop slave;

# 删除slave的所有中继日志
reset slave all;

# 查看从服务器状态
show slave status\G
```

5、拉起备用机器服务

在备用服务器上安装并配置需要使用的服务或应用程序，以保证它能够执行主服务器的工作。
这包括确保备用服务器与主服务器的数据和配置文件是同步的

按照部署系统的维护文档操作即可

6、验证基本服务状态

登录网页，调用查询API，让用户进行生产联调检验功能可用性

<font color="red">注意：主服务器的IP被占用，此时主服务器开机那么网络应该是不通的，所以远程软件是无法连接的，只能去机房(工厂网管)手动改网络配置</font>

7、登录前住服务器的机器停止服务（因为网络不通，所以一定抛数据抛不出去）

方法一：搜索 -> 服务

方法二：`Win+R`，输入 `services.msc` 进入服务

关闭 Apache24,celery_beat, celery_worker 服务 防止数据重复上抛

8、将主服务器的IP地址更改为备用服务器的IP地址。（若机房或者工厂操作完成IP更改后，可以让ATE开发来操作后续操作）

打开“控制面板”并选择“网络和 Internet”- “网络和共享中心”。

在左侧菜单中点击“更改适配器设置”。

选择需要修改 IP 地址的网络连接，并右键点击它。

选择“属性”，然后在列表中找到“Internet 协议版本 4 (TCP/IPv4)”。

点击“属性”，然后在弹出窗口中选择“使用下面的 IP 地址”。

输入要更改的 IP 地址、子网掩码和默认网关。

点击“确定”保存更改


进入 cmd 输入`ipconfig /all` 查看是否一致，



9、删除前主服务器的MySQL配置

```sql
mysql> show master logs; //查看master的binlog日志列表
mysql> reset master; //删除master的binlog，即手动删除所有的binlog日志
mysql> show master status\G

mysql> stop slave;
mysql> reset slave all; //(彻底清理)
mysql> show slave status\G
```


请注意，在进行任何更改之前，请务必备份所有重要数据和配置文件，并测试备用服务器是否能够成功替代主服务器。


### 数据同步

#### 使用 脚本进行数据同步

待补充



#### 使用第三方工具进行同步

使用SQLyog进行数据同步的详细步骤：

1、打开SQLyog软件，并连接到源数据库和目标数据库。

2、在SQLyog界面左侧的“Object Browser”中，选择要同步的数据库。

3、点击“Tools”菜单，选择“Data Sync Manager”。

4、在“Data Sync Manager”窗口中，点击“New Job”按钮，开始创建新的同步任务。

5、在“New Job Wizard”中，按照提示，依次选择源数据库和目标数据库，以及需要同步的表和字段。

6、配置同步选项，包括同步方式（增量同步或全量同步）、同步方向（双向同步或单向同步）、同步频率等。

7、完成配置后，点击“Finish”按钮，保存同步任务，并返回“Data Sync Manager”窗口。

8、在“Data Sync Manager”窗口中，选择刚刚创建的任务，并点击“Start”按钮，开始执行同步操作。

9、等待同步任务执行完成后，可以在目标数据库中查看同步结果。

注意事项：

1、在执行同步任务前，请先备份好源数据库和目标数据库。

2、在同步过程中，可能会出现数据冲突、网络异常等问题，需要及时处理。

3、请不要在同步任务执行期间对源数据库和目标数据库进行修改操作，以免影响同步结果。




### 定期备份

在 Windows 机器上定期备份 MySQL 数据库，可以使用多种方案。以下是其中几种常用的方案和配置方式：

#### 使用 MySQL 自带的 mysqldump 工具进行备份

配置步骤：

- 打开命令行窗口（cmd）。

- 进入 MySQL 安装目录下的 bin 目录，例如：cd C:\Program Files\MySQL\MySQL Server 8.0\bin。

- 使用以下命令备份指定数据库：

```bash
mysqldump -u 用户名 -p 密码 数据库名 > 备份文件名.sql
```

其中，用户名 和 密码 分别为 MySQL 的登录用户名和密码，数据库名 为要备份的数据库名称，备份文件名.sql 为备份输出的文件名，可自定义指定路径。

可以将该命令添加到 Windows 计划任务中，定期执行备份操作。

在 Windows 中，您可以使用“任务计划程序”来配置定时计划任务。

以下是配置定时计划任务的步骤：

1、打开“任务计划程序”：按下“Win + R”键，输入**taskschd.msc**，然后点击“确定”。

2、在左侧面板中，展开“任务计划程序库”，然后右键单击“任务计划程序库”，选择“创建任务”。

3、在“常规”选项卡中，输入任务名称并选择适当的描述信息。

4、在“触发器”选项卡中，单击“新建”按钮，选择要运行任务的计划，如每天、每周或每月等，并设置开始日期和时间。

5、在“操作”选项卡中，单击“新建”按钮，选择您要运行的程序或脚本，或者指定一个特定的命令。

6、在“条件”选项卡中，您可以根据需要指定额外的条件，例如只有当计算机处于空闲状态时才运行该任务。

7、在“设置”选项卡中，您可以指定任务是否在计算机电源供应状态改变时启动，以及任务执行期间何时停止。

8、单击“确定”按钮保存任务。现在，您的计划任务已经成功设置。

请注意，对于某些计划任务，您可能需要提供管理员凭据。如果您没有管理员权限，则需要请求管理员授权进行此操作。

#### 使用第三方工具进行备份

##### 常用工具

- Navicat for MySQL

- 海蒂SQL

- SQLyog

##### 配置步骤

- 下载并安装所选的备份工具。

- 连接到需要备份的 MySQL 数据库。

- 在工具界面上选择备份数据库的选项。

- 配置备份文件的保存位置及其他相关设置。

- 可以将备份操作添加到 Windows 计划任务中，定期执行备份操作。

无论使用哪种备份方案，都需要确保备份文件的安全性，建议将备份文件保存在其他磁盘或远程服务器上，并进行加密或其他安全措施。


##### SQLyog 详细配置

SQLyog是一种流行的MySQL数据库管理工具，它提供了许多备份和还原数据库的功能。要定时备份数据库，可以按照以下步骤操作：

1、打开SQLyog并连接到您的MySQL服务器。
2、选择要备份的数据库，并单击“高级工具 - 计划备份(以批处理脚本向导导出数据)”按钮。
3、在打开的“计划备份”窗口中，选择“开始新工作”选项。
4、选择本地 或者 远程服务器，填写好相关配置，指定好数据库
5、根据需要，导出所有对象 或者 导出选择的项目
6、勾选压缩备份文件，选择每个目标使用单独的文件，填上备份文件的名字，勾选使用时间戳生成子文件夹
7、输出 结构和数据，DDL选项和DML选项默认即可
8、生成什么，按照默认即可
9、错误处理，邮件提醒（需要配置邮件服务器）
10、勾选 立即运行 + 保存计划
11、测试脚本，若遇到问题请检查日志
12、指定任务文件路径及文件名 + 指定时间表名称
13、配置定时任务计划，点击计划-新建任务-指定时间-设置账户信息
14、配置完成后 可以在 【高级工具-计划的作业】查看任务


注意： 在MySQL中，

DDL代表数据定义语言，用于管理数据库结构。

DML代表数据操作语言，用于管理数据库中的数据。

DDL是用于创建和修改数据库对象的语言。这些对象包括数据库、表、索引、触发器、视图等。常用的DDL语句包括CREATE、ALTER、DROP等。

DML则是用于对数据库中的数据进行操作的语言。这些操作包括插入、更新、删除数据等。常用的DML语句包括SELECT、INSERT、UPDATE、DELETE等。


### 恢复测试