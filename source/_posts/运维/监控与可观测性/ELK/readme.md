---
title: 运维 · ELK 日志栈
date: 2026-07-30 10:00:00
tags:
- 运维
- ELK
- Elasticsearch
- 日志
- 导航
categories:
- 运维
- 监控与可观测性
- ELK
---

# ELK 日志栈

ELK（Elasticsearch + Logstash + Kibana）是日志收集、检索与可视化的一站式方案（现常称 Elastic Stack，Beats 为轻量采集端）。

## 子页面

- [Elasticsearch 安装部署](Elasticsearch/安装部署.md)
- [Elasticsearch 常用命令](Elasticsearch/常用命令.md)
- [Kibana 常用命令](Kibana/常用命令.md)
- [Logstash 与 Beats](Logstash与Beats.md)

## 数据流

Beats/Logstash 采集 → 过滤转换 → Elasticsearch 存储 → Kibana 可视化。
