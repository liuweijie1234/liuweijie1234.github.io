---
title: docker 常用命令
date: 2025-01-07 10:00:00
tags:
- docker
categories:
- 运维工具
---


## 常用命令

参考 https://www.runoob.com/docker/docker-command-manual.html

### 镜像仓库

docker login  登录docker hub
docker logout  退出docker hub
docker search <镜像名>  搜索可用的镜像
docker pull <镜像名>  下载镜像
$ docker pull ubuntu:latest
docker push <镜像名>  上传镜像


### 本地镜像管理

docker images  查看本地镜像
docker rmi <镜像名>  删除镜像
docker tag <镜像名> <新镜像名>  重命名镜像别名
docker build -t <镜像名> .  构建镜像
docker history <镜像名>  查看镜像历史
docker save -o <镜像名>.tar <镜像名>  保存镜像为tar文件
docker load -i <镜像名>.tar  加载镜像
docker import <镜像名>.tar - <镜像名>  导入镜像


### 容器生命周期管理

docker run <镜像名>  运行镜像

例子：
$ docker run learn/tutorial apt-get install -y ping  # 在learn/tutorial镜像里面安装ping程序

docker start <容器名>  启动容器
docker stop <容器名>  停止容器
docker restart <容器名>  重启容器
docker kill <容器名>  杀死容器
docker rm <容器名>  删除容器
docker pause <容器名>  暂停容器
docker unpause <容器名>  恢复容器
docker create <镜像名>  创建容器
docker exec -it <容器名> /bin/bash  进入容器
docker rename <旧容器名> <新容器名>  重命名容器


### 容器操作

docker ps  查看所有Docker容器（包括单独运行的和compose创建的）
docker ps -a  查看所有容器（包括已停止的）
docker inspect <容器名>  查看容器详细信息
docker top <容器名>  查看容器进程
docker attach <容器名>  连接到正在运行的容器
docker events  查看容器事件
docker logs <容器名>  查看容器日志
docker wait <容器名>  等待容器停止
docker export <容器名> -o <文件名>.tar  导出容器为tar文件
docker port <容器名>  查看容器端口映射
docker stats <容器名>  查看容器资源使用情况
docker update <容器名>  更新容器配置


### 容器的root文件系统命令

docker commit <容器名> <镜像名>  将容器提交为镜像
$ docker commit 698 learn/ping  # 将容器698提交为镜像learn/ping

docker cp <容器名>:<文件路径> <本地路径>  将容器文件复制到本地
docker diff <容器名>  查看容器文件变化


### docker compose 

docker compose pull  下载镜像
docker compose run <服务名>  启动服务
docker compose rm <服务名>  删除服务
docker compose ps  仅查看当前docker-compose.yml中定义的容器状态
docker compose build  构建镜像
docker compose up -d  启动容器
docker compose ls  列出所有服务
docker compose start <服务名>  启动服务
docker compose restart <服务名>  重启服务
docker compose down  停止容器




docker run --hostname=7ddcdfc6b6c1 --mac-address=de:af:25:d2:26:66 --env=MYSQL_ROOT_PASSWORD=zfx@2021 --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=GOSU_VERSION=1.17 --env=MYSQL_MAJOR=8.0 --env=MYSQL_VERSION=8.0.39-1.el9 --env=MYSQL_SHELL_VERSION=8.0.38-1.el9 --volume=/var/lib/mysql --network=bridge -p 13336:3306 -p 33060 --restart=no --runtime=runc -d mysql:8.0

docker run --hostname=47c4a89e9395 --mac-address=0a:aa:7f:8b:c3:f4 --env=requirepass=zfx@2021wxcm11taofx --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=GOSU_VERSION=1.17 --env=REDIS_VERSION=7.4.0 --env=REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-7.4.0.tar.gz --env=REDIS_DOWNLOAD_SHA=57b47c2c6682636d697dbf5d66d8d495b4e653afc9cd32b7adf9da3e433b8aaf --volume=/data --network=bridge --workdir=/data -p 16379:6379 --restart=no --runtime=runc -d redis:latest