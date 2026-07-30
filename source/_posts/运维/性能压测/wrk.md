---
title: wrk 性能压测
date: 2026-07-30 10:00:00
tags:
- 运维
- 压测
- wrk
categories:
- 运维
- 性能压测
---

# wrk 性能压测

wrk 是一款现代 HTTP 基准测试工具，基于事件驱动（多线程 + 多路复用），单机即可产生极高的并发，同时支持 Lua 脚本定制请求与统计。缺点是不支持 HTTP/2。

## 安装

```bash
# Ubuntu
apt-get install -y wrk

# 源码编译（推荐，获取最新版）
git clone https://github.com/wg/wrk.git && cd wrk
make && cp wrk /usr/local/bin/
```

## 核心参数

| 参数 | 含义 |
| --- | --- |
| `-t <threads>` | 线程数（建议等于 CPU 核数） |
| `-c <connections>` | 总连接数（并发） |
| `-d <duration>` | 持续时间，如 `30s`、`2m` |
| `-s <script>` | 指定 Lua 脚本 |
| `-H <header>` | 自定义请求头 |
| `--latency` | 打印详细的延迟分布 |
| `--timeout` | 请求超时时间 |

## 基本用法

```bash
# 12 线程、400 并发、持续 30 秒
wrk -t12 -c400 -d30s http://localhost:8080/

# 打印延迟分布并带请求头
wrk -t8 -c200 -d30s --latency -H 'Accept: application/json' http://api.local/v1/list
```

## Lua 脚本定制

通过 `-s` 可定义请求构造、响应处理与自定义统计。常用三个钩子：

- `setup(thread)`：线程启动时调用。
- `request()`：返回要发送的请求（可动态拼接路径、参数）。
- `response(status, headers, body)`：处理响应。

示例 `post.lua`：

```lua
wrk.method = "POST"
wrk.body   = '{"user":"test","pwd":"123456"}'
wrk.headers["Content-Type"] = "application/json"

request = function()
  return wrk.format(nil, "/login")
end
```

运行：

```bash
wrk -t4 -c100 -d30s -s post.lua --latency http://api.local
```

## 结果解读

```
Running 30s test @ http://localhost:8080/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    12.34ms    3.21ms  89.10ms   88.42%
    Req/Sec    32.10k     1.21k   35.00k    72.00%
  11456789 requests in 30.01s, 1.83GB read
Requests/sec: 381738.55
Transfer/sec:     62.43MB
```

- **Latency**：请求延迟（均值、标准差、最大、分布占比）。
- **Req/Sec**：单线程每秒请求数。
- **Requests/sec**：整体吞吐，wrk 的核心指标。
- 加 `--latency` 后还会输出 50/75/90/99 分位延迟。

## 与 ab/Siege 对比

| 工具 | 性能 | 脚本能力 | HTTP/2 | 场景 |
| --- | --- | --- | --- | --- |
| ab | 中 | 无 | 否 | 单 URL 快速验证 |
| Siege | 中 | URL 列表 | 否 | 多 URL 回归 |
| wrk | 高 | Lua 强 | 否 | 高并发、复杂场景 |

需要 HTTP/2 压测可改用 `wrk2`（恒定吞吐）或 `hey`、`k6`。
