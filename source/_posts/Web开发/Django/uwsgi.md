---
title: uWSGI 服务
date: 2022-12-28 15:52:00
tags:
- uWSGI
categories:
- Django
---


[linux安装uwsgi](https://blog.csdn.net/SiShen654/article/details/109103116)

[uwsgi服务启动、关闭、重启操作](https://www.cnblogs.com/mengrennwpu/p/9727100.html)
uwsgi --stop uwsgi/uwsgi.pid


[uwsgi 常用参数](https://www.cnblogs.com/JIM-FAN/p/14680520.html)

### 示例 uwsgi配置
```ini
[uwsgi]
#监听的地址 必须和nginx中的一致
socket = 127.0.0.1:8000

#wsgi文件，在你的项目配置目录下可以找到 注意：最后输入绝对地址
wsgi-file = /home/aeasringnar/my_Project/jwt-test/my_jwt_test/wsgi.py

# 你的项目的根目录 绝对地址
chdir = /home/aeasringnar/my_Project/jwt-test

# 你项目使用的虚拟环境的根目录 绝对地址
home = /home/aeasringnar/.envs/jwt-test

# 你的日志目录，注意的是，你的django控制台输出的日志都会在这里输出，uwsgi的相关日志也在这里
daemonize = /home/aeasringnar/my_Project/jwt-test/test.log

#### 下面的配置可以有 也可以没有，看个人需求，不建议配置
# 主进程
master = true 

# 多站模式  
vhost = true 

# 多站模式时不设置入口模块和文件   
no-site = true 

# 子进程数  
workers = 2

# 退出、重启时清理文件 
vacuum = true
```

要在Linux上部署Django和uWSGI，您需要创建一个uWSGI配置文件。以下是一个示例配置文件：
```ini
[uwsgi]
socket = /tmp/%n.sock
chdir = /path/to/your/project/
module = your_project_name.wsgi:application
home = /path/to/your/virtualenv/
processes = 4
threads = 2
harakiri = 60
master = true
vacuum = true
die-on-term = true
```
其中，socket 是 uWSGI 与 Nginx（或其他 Web 服务器）通信的套接字路径；chdir 是你的 Django 项目路径；module 是指向 Python 应用程序的 WSGI 入口点；home 是虚拟环境的路径；processes 和 threads 分别是 uWSGI 启动的进程和线程数量；harakiri 是设置请求执行时间的最大秒数；master 表示是否开启 master 进程；vacuum 会在关闭 uwsgi 进程时清理相关文件；die-on-term 会在接收到 SIGTERM 信号时直接退出。

您可以将此配置文件保存为 your_project_name.ini 文件并通过命令行运行 uWSGI：
```bash
uwsgi --ini /path/to/your_project_name.ini
```
这样就可以启动 uWSGI 服务器，然后将其与 Web 服务器（如 Nginx）结合使用，从而处理 Django 应用程序的请求。

在 uWSGI 的配置文件 uwsgi.ini 中，processes 和 process 都是用于设置 uWSGI 进程数量的参数，但它们具有不同的含义。

- processes: 用于设置 uWSGI 进程的数量。例如，如果将 processes = 4，则会启动 4 个 uWSGI 进程来处理请求。每个进程都独立运行，可以在多个 CPU 核心上同时处理请求。这也是 uWSGI 的默认设置。
- process: 用于设置 uWSGI 进程（worker）中线程的数量。例如，如果将 process = 2，则会启动每个 uWSGI 进程内部，2 个线程来同时处理请求。这有助于提高性能，并减少响应时间。

因此，processes 和 process 参数主要区别在于它们控制的是不同层次的并发性：

- processes 控制的是整个应用程序级别的并发性，它定义了启动的独立进程数，可通过多个 CPU 核心来并行处理请求，从而提高吞吐量。
- process 控制的是进程内部的线程数，它定义了每个单独进程内并发处理请求的最大数量，从而更好地利用系统资源，减少响应时间。

需要注意的是，增加进程和线程数量可能会增加服务器负载，并可能导致内存和 CPU 占用率的增加。因此，应该根据具体的服务器硬件配置和应用程序需求来设置这些参数，以达到最佳性能和稳定性。


### 示例 Supervisor配置

Supervisor 是一种进程管理工具，可以用来持续监控并自动重启 uWSGI 进程。下面是一个示例 Supervisor 配置文件：
```conf
[program:your_project_name]
command=/path/to/your/virtualenv/bin/uwsgi --ini /path/to/your_project_name.ini
directory=/path/to/your/project/
user=your_username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/%(program_name)s.log
```
在上述配置中，我们创建了一个名为 your_project_name 的进程，指定了 uwsgi 命令和其配置文件的路径。
directory 是 Django 项目的目录位置，
user 是运行该进程的用户。
autostart 和 autorestart 分别指定是否自动启动和自动重启 uwsgi 进程。
redirect_stderr 将标准错误输出重定向到日志文件。
stdout_logfile 指定了标准输出日志文件的位置。

将此配置文件保存为 your_project_name.conf 并将其放置在 Supervisor 的配置目录下（通常是 /etc/supervisor/conf.d/）。接下来，重新加载 Supervisor 配置文件：

```bash
sudo supervisorctl reread
sudo supervisorctl update
```
现在，您可以使用以下命令来启动、停止和重启 uWSGI 进程：
```bash
sudo supervisorctl start your_project_name
sudo supervisorctl stop your_project_name
sudo supervisorctl restart your_project_name
```

### linux 如何查看uwsgi部署的具体路径

要查看 uwsgi 部署的具体路径，您可以执行以下命令：
```bash
ps aux | grep uwsgi
```
这将显示所有正在运行的 uwsgi 进程及其参数。在输出中，可以找到 --ini 参数，后面跟着 uwsgi 配置文件的路径。例如：
```bash
uwsgi --ini /path/to/your_project_name.ini
```
另外，uWSGI 默认情况下将创建一个套接字文件用于与 Web 服务器通信，通常位于 /tmp 目录下。您可以使用以下命令来查找 uwsgi 套接字文件的位置：
```bash
ls -la /tmp/*.sock
```
这将列出 /tmp 目录下所有 .sock 结尾的文件，并且它们的拥有者应该是启动 uwsgi 进程的用户。在输出中，您可能会看到 uwsgi 的套接字文件名，类似于 your_project_name.sock。








supervisorctl 拉起uwsgi失败 FATAL     Exited too quickly (process log may have details)
```log
*** Starting uWSGI 2.0.18 (64bit) on [Tue Mar 21 10:04:31 2023] ***
compiled with version: 7.4.0 on 07 August 2019 03:05:01
os: Linux-4.15.0-55-generic #60-Ubuntu SMP Tue Jul 2 18:22:20 UTC 2019
nodename: iZwz9bzvz55uz1c6su15gwZ
machine: x86_64
clock source: unix
detected number of CPU cores: 2
current working directory: /home/ate/projects/ATECenter
detected binary path: /usr/local/bin/uwsgi
!!! no internal routing support, rebuild with pcre support !!!
uWSGI running as root, you can use --uid/--gid/--chroot options
*** WARNING: you are running uWSGI as root !!! (use the --uid flag) *** 
chdir() to /home/ate/projects/ATECenter
your processes number limit is 31733
your memory page size is 4096 bytes
 *** WARNING: you have enabled harakiri without post buffering. Slow upload could be rejected on post-unbuffered webservers *** 
detected max file descriptor number: 65535
lock engine: pthread robust mutexes
thunder lock: disabled (you can enable it with --thunder-lock)
probably another instance of uWSGI is running on the same address (0.0.0.0:8000).
bind(): Address already in use [core/socket.c line 769]
```
根据日志，可以看出以下错误信息：

- FATAL Exited too quickly: 进程启动后很快就退出了。
- probably another instance of uWSGI is running on the same address (0.0.0.0:8000): 可能已经有一个 uwsgi 进程在使用指定的地址（0.0.0.0:8000）。

因此，问题可能是由于端口冲突导致的。您可以执行以下步骤来解决问题：

1、确认是否正在运行另一个 uwsgi 进程，并且它正在使用相同的端口号。可以使用 ps aux | grep uwsgi 命令检查是否存在其他 uwsgi 进程。
2、如果确实存在另一个 uwsgi 进程，请停止该进程，然后再尝试重新启动uwsgi。
3、如果没有其他 uwsgi 进程正在运行，请检查您的配置文件，并确保端口号未被占用或已正确设置。

此外，还需要注意以下提示：

- `!!! no internal routing support, rebuild with pcre support !!!` 提示缺少内部路由支持，请重新编译 uwsgi 并添加 pcre 支持。
- `*** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***` 建议不要以 root 用户身份运行 uwsgi。应该使用非特权用户来运行 uwsgi 进程，以提高安全性。
- `*** WARNING: you have enabled harakiri without post buffering. Slow upload could be rejected on post-unbuffered webservers ***` 建议开启 post buffering 来避免上传速度慢时被拒绝等情况。

[unix:///var/run/supervisor.sock no such file 报错](https://www.cnblogs.com/aiyablog/p/16794403.html)


[supervisor 启动报错的解决方法 Error: Another program is already listening on a port that one of our HTTP servers is configured to use. Shut this program down first before starting supervisord.](https://blog.csdn.net/hello_world_wbg/article/details/85252160)