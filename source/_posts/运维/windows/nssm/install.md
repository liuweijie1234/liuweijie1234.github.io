---
title: nssm 安装
date: 2024-03-19 09:00:00
tags:
- nssm
categories:
- nssm
---

Windows 上，可以使用 nssm（Non-Sucking Service Manager）工具创建 Celery Worker 服务。

### 下载 nssm 

https://nssm.cc/download

解压到指定目录，例如：`D:\nssm`

> 推荐：将 nssm 路径添加到环境变量中，方便使用。

### nssm 常用命令

1、安装服务
nssm install 

2、卸载服务
nssm remove 自定义的服务名称 

3、启动服务
nssm start 自定义的服务名称 

4、停止服务
nssm stop 自定义的服务名称 

5、重启服务
nssm restart 自定义的服务名称

6、修改服务
nssm edit 服务名称

7、查看服务状态
nssm status 自定义的服务名称

8、查看服务列表
nssm list

9、设置服务描述
nssm set 服务名称 Description "自定义描述"

10、设置服务显示名称
nssm set 服务名称 DisplayName "自定义显示名称"




配置参数

Application path：就是选择你  exe文件的路径

Startup directory：会自动加载exe所对应目录，不需改动

Service name ：自定义服务名称，可在服务列表找到。 

