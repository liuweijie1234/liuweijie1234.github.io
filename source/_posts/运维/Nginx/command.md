

## Nginx常用命令

```bash
nginx -t	    # 测试配置文件语法（检查是否有错误，不重启服务）。
nginx -s reload	# 平滑重启（重新加载配置，不影响已建立的连接）。
nginx -s stop	# 立即停止服务（强制终止所有连接）。
nginx -s quit	# 优雅停止服务（等待现有请求完成后再退出）。
nginx -v	    # 查看 Nginx 版本（简略信息）。
nginx -V	    # 查看详细版本及编译参数（显示安装的模块，如 --with-http_ssl_module）。
nginx -c /path/to/nginx.conf	# 指定配置文件启动（默认从 /etc/nginx/nginx.conf 加载）。
ps aux | grep nginx	            # 查看 Nginx 进程（确认 Master/Worker 进程是否运行）。
journalctl -u nginx --no-pager	# 查看 Nginx 日志（Systemd 系统）。
```

## Nginx 配置文件查看与结构

### 1. 默认配置文件路径

```bash
/etc/nginx/nginx.conf	# 主配置文件（全局配置，如 Worker 进程数、日志格式）。
/etc/nginx/conf.d/	    # 子配置目录（推荐存放自定义配置，如 app.conf）。
/etc/nginx/sites-enabled/	# 虚拟主机配置（符号链接到 sites-available/ 中的文件，Ubuntu 常用）。
/var/log/nginx/	        # 日志目录（access.log 记录请求，error.log 记录错误）。
访问日志 → /var/log/nginx/access.log
错误日志 → /var/log/nginx/error.log
```

### 2. 配置文件核心结构

```conf
# 全局块（影响整个服务的配置）
user  nginx;                     # Worker 进程运行用户
worker_processes  auto;          # Worker 进程数（通常设为 CPU 核心数）
error_log  /var/log/nginx/error.log warn;  # 错误日志路径和级别

# 事件块（连接处理参数）
events {
    worker_connections  1024;    # 每个 Worker 的最大连接数
}

# HTTP 块（Web 相关配置）
http {
    include       /etc/nginx/mime.types;    # 文件类型映射
    default_type  application/octet-stream; # 默认 MIME 类型

    # 日志格式定义
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;  # 访问日志路径

    # 服务器块（虚拟主机配置）
    server {
        listen       80;          # 监听端口
        server_name  example.com; # 域名

        # 路径匹配规则
        location / {
            root   /var/www/html; # 静态文件根目录
            index  index.html;
        }

        # 反向代理示例
        location /api/ {
            proxy_pass http://localhost:3000/; # 转发到后端服务
        }
    }
}
```

## 快速调试技巧

### 1. 检查配置语法
```bash
nginx -t
```
输出示例：

```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 2. 查看加载的配置文件

```bash
# 列出所有加载的配置文件路径
nginx -T 2>&1 | grep "conf"  
```

### 3. 实时查看访问日志
```bash
tail -f /var/log/nginx/access.log
```
### 4. 查找错误日志中的关键问题

```bash
grep -E "error|warn" /var/log/nginx/error.log
```

## 常见问题排查

端口冲突	
netstat -tulnp | grep 80 检查占用端口的进程，修改 Nginx 的 listen 端口。

权限不足	
确保 Nginx 用户（如 nginx 或 www-data）对静态文件目录有读取权限。

502 Bad Gateway	
检查后端服务是否运行（curl http://backend:port），确认 proxy_pass 地址正确。

404 Not Found	
检查 root 或 alias 路径是否存在文件。

SSL 证书错误	
确保证书路径和私钥权限正确（chmod 600 cert.key）。