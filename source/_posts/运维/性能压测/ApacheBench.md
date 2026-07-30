---
title: ApacheBench
date: 2026-07-30 10:00:00
tags:
- 性能压测
categories:
- 运维
- 性能压测
---

# ApacheBench

ApacheBench（`ab`）是 Apache 自带的一款轻量级 HTTP 基准测试工具，适合对单一 URL 做快速的压力与并发测试，验证服务端在大并发下的吞吐与稳定性。

## 安装

```bash
# Debian/Ubuntu
apt-get install -y apache2-utils

# RHEL/CentOS
yum install -y httpd-tools

# 验证
ab -V
```

## 核心参数

| 参数 | 含义 |
| --- | --- |
| `-n <requests>` | 总请求数 |
| `-c <concurrency>` | 并发数（同时发起的请求数） |
| `-t <seconds>` | 测试最大时长，到时即停 |
| `-k` | 启用 HTTP KeepAlive |
| `-p <file>` | POST 请求体文件 |
| `-T <type>` | POST 的 Content-Type |
| `-H <header>` | 自定义请求头 |
| `-r` | 遇到 socket 错误不退出（默认中断并报错） |

## 常用命令

```bash
# 100 并发、共 10000 次请求
ab -c 100 -n 10000 http://localhost:8080/

# 带请求头与 POST 数据
ab -c 50 -n 5000 -T 'application/json' \
   -p data.json -H 'Authorization: Bearer xxx' http://api.example.com/login

# 限时 60 秒、开启 KeepAlive
ab -k -c 200 -t 60 http://localhost/
```

## 结果解读

关注以下关键指标：

- **Requests per second**：每秒完成的请求数，即吞吐量，越高越好。
- **Time per request（mean）**：平均每个请求的耗时（含并发等待）。
- **Time per request（across all）**：单个请求实际处理时间 = 总耗时 / 总请求。
- **Transfer rate**：传输速率（KB/s）。
- **Percentage of requests served within a certain time**：如 `50% 12ms`、`90% 45ms`、`99% 200ms`，用于观察长尾延迟。

示例输出：

```
Concurrency Level:      100
Time taken for tests:   12.345 seconds
Complete requests:      10000
Failed requests:        0
Requests per second:    810.44 [#/sec] (mean)
Time per request:       123.450 [ms] (mean)
Time per request:       1.235 [ms] (mean, across all concurrent requests)
Percentage of the requests served within a certain time (ms)
  50%    110
  90%    180
  99%    320
 100%    450 (longest request)
```

## 注意事项

- `ab` 默认单进程单线程，受自身 CPU 与本地端口（`TIME_WAIT`）限制，单机压测上限有限，不建议用来做超大规模压测。
- 压测目标为 `localhost` 时需排除网络开销；跨机压测才能反映真实链路。
- 大量短连接会产生大量 `TIME_WAIT`，可通过 `ulimit -n` 提升文件描述符上限，或调大本地端口范围。
- 仅支持 HTTP/1.0、1.1，不支持 HTTP/2，需要测 HTTP/2 请改用 `wrk` 或 `hey`。

## 参考资料

- 官方文档：https://httpd.apache.org/docs/current/programs/ab.html
