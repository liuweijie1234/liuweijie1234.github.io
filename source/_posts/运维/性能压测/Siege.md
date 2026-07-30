---
title: Siege
date: 2026-07-30 10:00:00
tags:
- 性能压测
categories:
- 运维
- 性能压测
---

# Siege

Siege 是一款开源的 HTTP/FTP 负载测试工具，支持多用户并发、随机 URL 列表（regression 模式）以及可调的并发与持续时间，适合对站点做持续压力测试与回归测试。

## 安装

```bash
# Debian/Ubuntu
apt-get install -y siege

# RHEL/CentOS
yum install -y siege

# 源码编译
wget http://download.joedog.org/siege/siege-latest.tar.gz
tar -xzf siege-latest.tar.gz && cd siege-*/
./configure && make && make install
```

## 核心参数

| 参数 | 含义 |
| --- | --- |
| `-c, --concurrent` | 并发用户数 |
| `-r, --reps` | 每个用户的请求次数（与 `-t` 二选一） |
| `-t, --time` | 持续时间，如 `1M`（1分钟）、`1H` |
| `-f, --file` | URL 列表文件（一行一个） |
| `-b, --benchmark` | 基准模式，无延迟（尽快发送） |
| `-d, --delay` | 用户间随机延迟（秒），模拟真实思考时间 |
| `-H, --header` | 自定义请求头 |
| `-g, --get` | 仅抓取一个 URL 并打印请求过程（调试用） |
| `-i, --internet` | 随机选取 URL 列表中的地址 |

## 常用命令

```bash
# 200 并发、持续 1 分钟
siege -c 200 -t 1M http://localhost:8080/

# 使用 URL 列表文件，随机访问
siege -c 50 -r 10 -f urls.txt -i

# 带自定义请求头与 POST 数据
siege -c 100 -t 30S -H 'Authorization: Bearer xxx' \
   'http://api.example.com/login POST {"user":"a","pwd":"b"}'
```

`urls.txt` 示例：

```
http://localhost:8080/
http://localhost:8080/api/list
http://localhost:8080/api/detail?id=1
```

## 结果解读

```
Transactions:                   12000 hits
Availability:                  99.83 %
Elapsed time:                  59.12 secs
Data transferred:             234.50 MB
Response time:                  0.98 secs
Transaction rate:             202.98 trans/sec
Throughput:                     3.97 MB/sec
Concurrency:                  198.55
Successful transactions:      11980
Failed transactions:             20
Longest transaction:            4.32
Shortest transaction:           0.05
```

- **Availability**：请求成功率，生产压测要求 ≥ 99.9%。
- **Transaction rate**：每秒事务数。
- **Concurrency**：平均并发连接数。
- **Failed transactions**：失败数（含超时、连接拒绝、5xx）。

## 配置文件

默认配置文件位于 `~/.siegerc`，可设置并发上限、日志路径等：

```
verbose = false
concurrent = 50
time = 1M
file = /path/to/urls.txt
```

## 与 ab/wrk 对比

- `ab` 仅支持单一 URL、`siege` 支持 URL 列表与随机访问，更接近真实流量。
- `wrk` 基于事件驱动、性能更强，但需 Lua 脚本定制；`siege` 开箱即用更简单。
- 三者均不支持 HTTP/2。
