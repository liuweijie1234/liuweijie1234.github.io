---
title: windows 安装 MySQL 5.7
date: 2022-12-25 11:42:00
tags:
- MySQL
categories:
- MySQL
---


推荐使用 DataGrip、SQLyog、Navicat Premium 作为 MySQL 数据库管理工具，可以方便地管理数据库，并且有强大的 SQL 编辑器。

## 安装 MySQL

### windows安装

https://dev.mysql.com/downloads/mysql/


### macOS安装

```bash
brew install mysql
```

启动 MySQL

临时启动：
```bash
mysql.server start
```

后台服务（推荐）：
```bash
brew services start mysql
```

初始化 MySQL（首次安装后）
```bash
mysql_secure_installation
```

按提示设置：
输入 root 密码（默认可能为空，直接回车）。
是否设置 root 密码？Y，然后输入新密码。
是否移除匿名用户？Y（增强安全）。
是否禁止远程 root 登录？Y（推荐）。
是否移除测试数据库？Y（可选）。
是否立即生效？Y。


验证 MySQL 是否运行
```bash
mysql -u root -p
```
```bash
brew services list | grep mysql
```

### docker安装

启动 MySQL
```bash
docker run --name my-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=yourpassword -d mysql:latest
```

验证 MySQL
```bash
docker exec -it my-mysql mysql -u root -p
```





## 卸载 MySQL

### windows 卸载

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


### MySQL 连接问题
错误：Can't connect to local MySQL server

确保 MySQL 服务已启动：

```bash
# macOS
brew services list | grep mysql
```
检查端口是否占用：

```bash
lsof -i :3306
```
