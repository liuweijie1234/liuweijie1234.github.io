---
title: Scrapy 爬虫框架笔记索引
date: 2026-07-30 10:00:00
tags:
- Python
- 爬虫
- Scrapy
categories:
- Python
---

## 简介

Scrapy 是基于 **Twisted 异步网络引擎**的爬虫框架，内置调度、去重、下载、解析、存储管道等完整组件。

```bash
pip install scrapy
scrapy startproject myspider      # 创建项目
scrapy genspider demo example.com # 创建爬虫
scrapy crawl demo                 # 运行
```

核心组件与数据流：

```
Spider -> Engine -> Scheduler（调度+去重）
                 -> Downloader（经下载中间件发请求）
Response -> Spider 解析 -> Item -> Item Pipeline（清洗/存储）
                        -> 新 Request 回到 Scheduler
```

## 专题笔记

- 代理池：{% post_link Python/13.爬虫/爬虫框架/Scrapy/代理池 %}

## 待整理专题（原占位目录，要点先记录于此）

### Twisted 异步 IO

Scrapy 的并发能力来自 Twisted 的事件循环（Reactor 模式），单线程内通过回调/Deferred 处理大量并发请求。并发相关配置：`CONCURRENT_REQUESTS`、`CONCURRENT_REQUESTS_PER_DOMAIN`、`DOWNLOAD_DELAY`。

### 分布式（scrapy-redis）

`scrapy-redis` 把调度队列和去重集合放到 Redis，实现多机共享任务：

```python
# settings.py
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = "redis://127.0.0.1:6379/0"
SCHEDULER_PERSIST = True   # 停止后保留队列，支持断点续爬
```

### 增量爬虫

核心是**去重与状态记录**：利用 scrapy-redis 的持久化去重指纹，或自行把已抓 URL/数据指纹（如 MD5）存入 Redis，入库前比对，只抓新增内容。

### 反爬应对

| 手段 | Scrapy 中的做法 |
| --- | --- |
| headers | 在 `DEFAULT_REQUEST_HEADERS` 或下载中间件中随机 User-Agent |
| cookie | `COOKIES_ENABLED` 控制；登录态可在中间件注入 Cookie |
| 延迟 | `DOWNLOAD_DELAY` + `RANDOMIZE_DOWNLOAD_DELAY`，或 `AUTOTHROTTLE_ENABLED = True` 自动限速 |
| 动态内容 | 接入渲染服务（scrapy-playwright / scrapy-splash），或直接分析 XHR 接口 |
| IP 封禁 | 代理中间件 + 代理池（见上方专题） |

### 抓包

- App 抓取：Charles / mitmproxy 抓 HTTPS（需装证书），高版本 Android 需处理 SSL Pinning（Frida 等），定位接口后用 Scrapy 直接请求 API。
- 视频抓取：开发者工具 Network 筛选 media/m3u8，m3u8 需下载分片合并（ffmpeg）。
