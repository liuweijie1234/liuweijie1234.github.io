---
title: 运维 · Apache
date: 2026-07-30 10:00:00
tags:
- 运维
- Apache
- 导航
categories:
- 运维
- Web网关与负载均衡
- Apache
---

# Apache

Apache HTTP Server 是老牌 Web 服务器，配置稳定、模块丰富。

## 子页面

- [安装部署](安装部署.md)
- [配置详解](配置详解.md)
- [日志分析](日志分析.md)
- [性能优化](性能优化.md)

## 说明

- 与 Nginx 对比：Apache 的 `.htaccess` 目录级配置、prefork/worker/event MPM 模型。
- 高并发场景通常选择 Nginx 做前端、Apache 做后端动态处理（反向代理）。
