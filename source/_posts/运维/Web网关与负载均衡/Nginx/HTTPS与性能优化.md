---
title: Nginx HTTPS 与性能优化
date: 2026-07-30 10:00:00
tags:
- 运维
- Nginx
- HTTPS
- 性能优化
categories:
- 运维
- Web网关与负载均衡
- Nginx
---

# Nginx HTTPS 与性能优化

本章涵盖 Nginx 的 TLS 配置、强制 HTTPS 跳转以及常见性能与安全调优项。证书申请与续期见 [TLS 与 HTTPS](../../网络与安全/TLS与HTTPS.md)。

## TLS/SSL 配置

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;

    # 协议与加密套件（前向安全优先）
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # 会话复用，降低握手开销
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets on;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 valid=60s;
}
```

## HTTP 强制跳转 HTTPS

```nginx
server {
    listen 80;
    server_name example.com;
    # 301 永久跳转
    return 301 https://$host$request_uri;
}
```

## 开启 HTTP/2

在 `listen 443 ssl` 后加 `http2;` 即可（Nginx 1.25+ 默认开启，旧版需显式声明）。HTTP/2 多路复用可显著降低延迟。

## 压缩（gzip / brotli）

```nginx
http {
    gzip on;
    gzip_comp_level 6;
    gzip_min_length 1k;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;
    gzip_vary on;
}
# brotli（需 ngx_brotli 模块）效果更好，配置类似
```

## 静态资源缓存与 expires

```nginx
location ~* \.(js|css|png|jpg|gif|ico|svg|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

## worker 进程与连接数调优

```nginx
worker_processes auto;            # 等于 CPU 核数
worker_rlimit_nofile 65535;       # 进程文件描述符上限

events {
    worker_connections 10240;     # 单 worker 最大连接
    use epoll;                     # Linux 高效事件模型
    multi_accept on;
}
```

配套系统参数（`/etc/sysctl.conf`）：

```bash
net.core.somaxconn = 65535
net.ipv4.tcp_tw_reuse = 1
fs.file-max = 1000000
```

并提升用户文件描述符（`/etc/security/limits.conf`）：

```
* soft nofile 65535
* hard nofile 65535
```

## 安全加固

```nginx
# 开启 HSTS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# 隐藏版本号
server_tokens off;

# 限制请求体大小，防大文件攻击
client_max_body_size 20m;
```

## 证书自动续期（certbot）

```bash
certbot --nginx -d example.com
# 续期脚本加入 crontab 每日执行：certbot renew --quiet
```

续期后 `certbot` 会自动 reload Nginx，无需手动干预。
