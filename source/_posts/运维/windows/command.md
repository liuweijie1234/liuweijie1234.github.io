---
title: windows 常用命令
date: 2022-10-14 17:42:00
tags:
- windows
categories:
- windows
---

## 命令

mstsc 远程服务器

### 查看端口

netstat -aon

netstat -aon|findstr "8080"

netstat -nao | findstr "8080" | find /c ":8080"

netstat -n | find /c "ESTABLISHED"  # 查看当前连接数


netstat -nao | findstr "80" | find /c ":80"

## exe日志输出
LD-RPA.exe >> log.txt 2>&1

## 查看端口转发
netsh interface portproxy show all

## 配置端口转发

netsh interface portproxy add v4tov4 listenport=8000 listenaddress=192.168.5.102 connectport=8000 connectaddress=172.22.151.72
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8000 connectaddress=172.22.151.72 connectport=8000

## 删除端口转发

netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8000

命令解释
netsh interface portproxy delete v4tov4：删除 IPv4 到 IPv4 的端口转发规则。
listenaddress=0.0.0.0：指定要删除的规则的监听地址。
listenport=8000：指定要删除的规则的监听端口。


## 防火墙

New-NetFirewallRule -DisplayName "WSL2 API Port" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow -InterfaceAlias "WLAN"

### 查看进程名

tasklist | findstr 9268

### 杀死进程

taskkill -PID 9268 -F

### 查看windows已经建立的连接数

netstat -n | find /C /I "established"

### 查看端口是否被监听

netstat -ano | findstr :8000

### 创建服务

sc create 服务名 binpath= "服务路径" start= "自动或手动"

如：    

sc create myservice binpath= "C:\myservice.exe" start= "auto"

例如： 创建windows_exporter服务
sc create windows_exporter binpath= "D:\windows_exporter\windows_exporter-0.25.1-amd64.exe" type= own start= auto displayname= windows_exporter

### 停止服务

sc stop 服务名

如：

sc stop myservice

### 启动服务

sc start 服务名


如：

sc start myservice

### 删除服务

sc delete 服务名

如：

sc delete myservice

### 查看服务状态

sc query 服务名

如：

sc query myservice

### 查看所有服务

sc queryex type= service

如：

## 注册表


win+r，打开运行框，输入 regedit 进入注册表页面

### 修改Windows服务器最大的Tcp连接数

https://www.jianshu.com/p/00136a97d2d8

https://www.jianshu.com/p/c168f1fdf915


[【Windows &MTU】Windows上最大传输单元MTU值的查看和设置](https://blog.csdn.net/michaelwoshi/article/details/126924526)

[Win10如何修改/取值mtu值](https://jingyan.baidu.com/article/0a52e3f46824deff63ed7205.html)


[阿里云ssh远程连接短时间就会断掉的解决方案](https://blog.csdn.net/xinshuzhan/article/details/107273525)


[如何修改windows系统的盘符名称比如C盘的C、D盘的D](https://www.yisu.com/zixun/438708.html)


查看主板型号

1. 在键盘上按下“win”+“R”按键调出运行窗口，在运行窗口中输入命令“dxdiag”，点击“确定”或回车。 2. 弹出诊断工具窗口，点击“是”进行下一步操作。 3.这时候诊断工具会弹出详细的电脑品牌型号等信息。


查看网卡型号


### win10如何设置通电自动开机 

1、电源也需要配置，充电自动启动
2、[win10如何设置通电自动开机 ](https://www.sohu.com/a/460751175_120464892)


### window开启远程桌面连接

右键我的电脑，选择【属性】
点击【远程设置】
在【远程】桌面处，勾选 允许远程连接到此计算机。
点击远程用户，可以添加允许远程连接的用户。

确定，完成设置，查看这台机器ip地址。

alt+r输入cmd

然后输入ipconfig

然后在另外一台电脑，atl+r

输入mstsc，回车

然后输入那台电脑的ip地址。


点击【连接】，再点击【连接】

输入用户名和密码，确定登录。

点击【更多选项】切换用户。


### Windows服务器系统如何开启PING功能

https://www.ahaoyw.com/article/464.html


### Win10用户账户控制怎么取消？两种Win10取消用户账户控制的方法

https://cloud.tencent.com/developer/news/452007


### windwos修改主机名称

https://cloud.tencent.com/developer/article/2026281?from=15425



### 打开服务（Services）

1、使用搜索功能打开服务

在Windows 10中，按下键盘上的Windows键或点击搜索框，输入“services”，然后按Enter键或点击搜索结果中的“Services”。
在Windows 11中，点击任务栏上的搜索图标，输入“services”，或按下Windows键，输入“services”，然后按Enter键或点击搜索结果。

2、通过运行窗口打开服务

同时按下Windows键 + R键打开运行窗口，输入“services.msc”并按Enter键或点击确定按钮。
3、从CMD、PowerShell或Windows终端打开服务

打开命令提示符、PowerShell或Windows终端，输入命令“services.msc”并按Enter键。

4、从文件资源管理器启动服务

打开文件资源管理器（快捷键Windows + E），导航到C:\Windows\System32目录，找到并双击“services.msc”文件。

5、在Windows中创建服务的快捷方式

在桌面的空白处右键点击，选择“新建”>“快捷方式”，在创建快捷方式向导中输入“services.msc”，点击“下一步”，输入快捷方式的名称，然后点击“完成”。

6、从开始菜单打开服务

在Windows 10中，点击任务栏上的Windows图标，滚动程序列表直到看到“Windows Administrative Tools”，点击展开，然后点击“Services”。
在Windows 11中，点击Windows图标，然后点击开始菜单右上角的“所有应用”按钮，滚动直到找到“Windows Tools”，点击打开，找到并双击“Services”。

7、通过控制面板访问服务

打开控制面板，进入“系统和安全”，在底部，你会看到“Windows Tools”（如果你使用的是Windows 11）或“Administrative Tools”（如果你使用的是Windows 10），在新窗口中找到并双击“Services”。

8、从计算机管理查看Windows服务

右键点击任务栏上的Windows图标或按Windows键 + X键，选择“计算机管理”，在左侧面板中点击“服务和应用程序”，然后在中间面板双击“服务”。

9、使用任务管理器打开服务

在Windows 10中，打开任务管理器，点击“文件”>“运行新任务”，在打开字段中输入“services.msc”，然后点击确定。
在Windows 11中，打开任务管理器，点击进程标签下的“运行新任务”按钮，输入“services.msc”，然后点击确定。