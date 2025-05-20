---
title: supervisor 安装
date: 2023-02-27 17:42:00
tags:
- supervisor
categories:
- supervisor
---


[Centos7 使用 Supervisor 守护进程 Celery](https://cloud.tencent.com/developer/article/2218981)
[supervisor djcelery（django、celery）在linux上的部署](https://blog.csdn.net/weixin_33127753/article/details/84872322)

[supervisor 安装配置以及常见的错误](https://blog.csdn.net/qq_38234594/article/details/89923583)


Error: %(process_num) must be present within process_name when numprocs > 1 in section 'program:celerywork'

[supervisor 同时开启多个进程 numprocs > 1](https://blog.csdn.net/qq_37837134/article/details/90904669)


supervisorctl update 命令用于将新的或修改过的 Supervisor 配置文件加载到 Supervisor 进程中并重新启动相关进程。执行该命令后，Supervisor 会比较当前的配置和之前的配置，并将更改应用于正在运行的进程。

具体来说，supervisorctl update 命令会做以下事情：

1、检查 /etc/supervisor/conf.d/ 目录下所有以 .conf 或 .ini 结尾的文件。
2、对于每个配置文件，如果该进程不存在，则创建该进程并启动；如果已经存在，检查该进程是否需要重启。
3、如果有任何更改，则重新启动进程。

因此，当您更改了 Supervisor 配置文件（例如添加、删除、修改了一个进程），您需要通过 supervisorctl update 命令来通知 Supervisor 加载这些更改并重新启动进程。

注意，supervisorctl update 只会重新加载配置文件，而不会重新启动 Supervisor 进程本身。如果您修改了 Supervisor 自身的配置（例如 /etc/supervisord.conf 文件），则需要使用 supervisorctl reread 和 supervisorctl reload 命令来重新加载和重启 Supervisor 进程。


### 面试题

Supervisor和Fastdfs
守护进程，如何配置，supervisor+tornado,文件指纹，分布式文件存储方案（引申阿里云oss），文件hash（hash一致性算法）

https://v3u.cn/a_id_102

https://v3u.cn/Index_a_id_76