---
title: Windows MySQL 升级
date: 2023-01-11 11:00:00
tags:
- MySQL
categories:
- 数据库
---

## 背景

windows MySQL 版本不一致，导致不能配置主从

参考：https://blog.51cto.com/u_15437298/4695308

## 小版本升级：5.7.30 升级至 5.7.40

### 原地升级：推荐

#### 0、zip下载

下载 MySQL 5.7.40 的zip包文件，下载地址：https://dev.mysql.com/downloads/mysql/

#### 1、关闭删除mysql服务

本文 mysql 服务名为 **MySQL57**

```sql
//查看mysql安装路径
select @@basedir as basePath from dual;
//查看mysql data数据存放路径
show global variables like '%datadir%';
```

![](/images/微信截图_20230111163633.png)

- 停止服务

方法一：`Win+R` 进入 `services.msc` ，找到 mysql ,停止服务

方法二：`Win+R` 进入 `cmd` (使用管理员权限)，停止服务 

```sql
net stop MySQL57
```

- 删除服务

方法一：`Win+R` 进入 `cmd` (使用管理员权限)，删除服务

```sql
sc delete MySQL57
```

方法二：`Win+R` 进入 `cmd` (使用管理员权限)，使用 mysqld.exe 删除服务

在默认路径下

```sql
cd C:\Program Files\MySQL\MySQL Server 5.7\bin
mysqld --remove MySQL57
```

#### 2、文件备份

`C:\Program Files\MySQL\MySQL Server 5.7` 改名 `C:\Program Files\MySQL\MySQL Server 5.7bak`

#### 3、新版zip解压

`C:\Program Files\MySQL\mysql-5.7.40-winx64.zip` 解压并改名为 `C:\Program Files\MySQL\MySQL Server 5.7`

注意：若配置文件和data目录在同一个目录，将原来的my.ini和data目录拷贝到 MySQL Server 5.7 文件夹中
 
#### 4、初始化数据文件

在 `C:\Program Files\MySQL\MySQL Server 5.7\bin> `下操作

```sql
mysqld --initialize-insecure --user=mysql
```

[无法启动此程序 因为计算机中丢失 vcruntime140_1 .dll](https://blog.csdn.net/wsjzzcbq/article/details/106146413)

[VC_redist.x64.exe下载地址](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)

#### 5、安装服务

根据需要修改配置文件路径

```sql
mysqld --install "MySQL57" --defaults-file="C:/ProgramData/MySQL/MySQL Server 5.7/my.ini"
```
mysqld --install "MySQL57" --defaults-file="D:\mysql-5.7\my.ini"


mysqld --install "MySQL57" --defaults-file="D:\ProgramData\MySQL\MySQL Server 5.7\my.ini"


#### 6、启动服务
```sql
net start MySQL57
```



#### 7、升级mysql：

```sql
mysql_upgrade -uroot -p
```



若遇到报错
```sql
mysql_upgrade: Got error: 1045: Access denied for user ‘root’@localhost <using password: YES> while connecting to the MySqL server Upgrade process encountered error and will not continue
```
配置文件添加免认证登录`skip-grant-tables`,添加后重启


UPDATE user 
SET authentication_string = PASSWORD('abcdefg@com')
WHERE user = 'root' AND 
      host = 'localhost';


GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'abcdefg@com' WITH GRANT OPTION;
GRANT PROXY ON ''@'' TO 'root'@'localhost' IDENTIFIED BY 'abcdefg@com' WITH GRANT OPTION;
flush privileges;


测试账号连通性

#### 8、重启mysql

```sql
net stop MySQL57
net start MySQL57
```

#### 9、检查版本

```sql
status;

或者

select version();
```

#### 10、测试基本功能

创建、插入、查看、修改、删除


## 5.7.26 升级至 5.7.40

### 逻辑升级:不推荐

逻辑升级对数据文件的处理方式是
通过逻辑导出导入，需要用到mysqldump。

这种方式在数据量比较大的情况下花费时间比较长。


#### 1、备份数据库

<a href="{% post_path 'sql/command' %}#导出">导出数据库数据-文档</a>

#### 2、卸载mysql

#### 3、安装mysql

#### 4、创建数据库

#### 5、导入数据

#### 6、测试基本功能

