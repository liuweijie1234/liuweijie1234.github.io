---
title: windows 安装 MySQL 5.7
date: 2022-12-25 11:42:00
tags:
- MySQL
categories:
- MySQL
---


推荐使用 DataGrip、SQLyog 作为 MySQL 数据库管理工具，可以方便地管理数据库，并且有强大的 SQL 编辑器。

## 安装 MySQL
下载
https://dev.mysql.com/downloads/mysql/



## 卸载 MySQL

彻底的卸载掉MySQL，并把有关MySQL的记录全部清除，有以下步骤

（1）到控制面板—>程序和功能—>把有关MySQL的程序全部右键卸载

（2）把所有没有清理干净的文件夹删除，主要集中在以下文件夹中：
C:\Users*你的用户名*\AppData\Roaming下的MySQL文件夹
C:\Users*你的用户名*\AppData\Roaming\Oracle下的MySQL文件夹
C:\Program Files下的MySQL文件夹
C:\Program Files (x86)下的MySQL文件夹
C:\ProgramData下的MySQL文件夹

（3）把MySQL的注册表删除，打开“运行”—>输入regedit，在HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\Eventlog\Application\MySQL，把MySQL这个文件夹删除

## 查看

查看MySQL的安装目录和数据存放目录

```sql
mysql> select @@basedir;
+------------------------------------------+
| @@basedir                                |
+------------------------------------------+
| C:\Program Files\MySQL\MySQL Server 5.7\ |
+------------------------------------------+
1 row in set (0.00 sec)

mysql> select @@datadir;
+---------------------------------------------+
| @@datadir                                   |
+---------------------------------------------+
| C:\ProgramData\MySQL\MySQL Server 5.7\Data\ |
+---------------------------------------------+
1 row in set (0.00 sec)
```


## 报错

```bash
mysqld: Can't create directory 'E:\mysql\mysql_data\Data\' (Errcode: 2 - No such file or directory)
```

[mysqld: Can't create directory 解决方法](https://blog.csdn.net/weixin_41851906/article/details/103459381)



```bash
2022-12-16T02:12:25.257069Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2022-12-16T02:12:25.257250Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2022-12-16T02:12:25.257250Z 0 [ERROR] --initialize specified but the data directory has files in it. Aborting.
2022-12-16T02:12:25.268289Z 0 [ERROR] Abortin
```


### windows 安装报错

安装 MySQL For Excel 1.3.8失败
Microsoft Excel 2007 or higher is not installed

安装 MySQL for Visual Studio 1.2.9
Visual Studio version 2015 , 2017 or 2019 must be installed


