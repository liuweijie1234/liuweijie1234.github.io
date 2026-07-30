---
title: 运维知识体系总览
date: 2026-07-30 10:00:00
tags:
- 运维
- 导航
- 知识树
categories:
- 运维
---

# 运维知识体系总览

本专栏系统梳理现代运维工程师所需的核心知识，从操作系统底层到容器编排、网关、监控、消息队列、CI/CD 与高可用架构，形成一套可检索、可扩展的知识树。

> 说明：本文档按主流运维知识树组织，各模块页面已基本完成正文补充与原有文档迁移。

## 知识模块导航

| 模块 | 说明 | 入口 |
| --- | --- | --- |
| 操作系统 | Linux / Windows / MacOS 命令、系统管理、权限、Shell 编程 | [readme](操作系统/readme.md) |
| 容器与编排 | Docker 与 Kubernetes 容器化与编排 | [readme](容器与编排/readme.md) |
| Web 网关与负载均衡 | Nginx / Apache 配置、反向代理、负载均衡、网关 | [readme](Web网关与负载均衡/readme.md) |
| 监控与可观测性 | Prometheus / Grafana / Zabbix / ELK 日志监控 | [readme](监控与可观测性/readme.md) |
| 消息队列 | Kafka / RabbitMQ 消息中间件 | [readme](消息队列/readme.md) |
| 进程守护与服务管理 | Supervisor / systemd 进程守护 | [readme](进程守护与服务管理/readme.md) |
| 性能压测 | ApacheBench / Siege / JMeter / wrk | [readme](性能压测/readme.md) |
| 网络与安全 | 防火墙 / TLS / OpenVPN / OpenSSL | [readme](网络与安全/readme.md) |
| CI 与 CD | Jenkins / GitLab CI 持续集成与交付 | [readme](CI与CD/readme.md) |
| 高可用与集群架构 | 负载均衡 / 集群 / 容灾 / 高并发 | [readme](高可用与集群架构/readme.md) |

## 面试专项

- [运维面试题汇总](面试题.md)：高负载高可用、计算机网络、操作系统等高频考点。

## 学习路径建议

1. 先打牢 **操作系统** 基础（命令、权限、Shell）。
2. 掌握 **容器与编排**，理解 Docker 与 K8s 是现代部署的基石。
3. 串联 **Web 网关 → 监控可观测 → 消息队列**，理解请求链路与观测手段。
4. 补齐 **CI/CD、网络与安全、高可用架构**，形成完整的生产级运维能力。
