---
title: Exporter
date: 2026-07-30 10:00:00
tags:
- 监控与可观测性
- Prometheus
- Exporter
categories:
- 运维
- 监控与可观测性
- Prometheus
---

# Prometheus Exporter

Exporter 是 Prometheus 采集指标的"探针"，把被监控对象的内部状态转换为 Prometheus 能拉取的 `/metrics` 格式（文本、键值对、带 HELP/TYPE）。

## 工作原理

- Prometheus Server 周期性（由 `scrape_interval` 控制）**主动拉取（pull）** Exporter 暴露的 HTTP 端点。
- 指标格式示例：

```
# HELP node_cpu_seconds_total Seconds the CPUs spent in each mode.
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 12345.6
```

- Exporter 通常为独立进程，监听端口并暴露 `/metrics`；部分应用（如 Kubernetes、etcd）内置暴露。

## 常用 Exporter

| Exporter | 监控对象 |
| --- | --- |
| `node_exporter` | 节点（CPU/内存/磁盘/网络） |
| `mysqld_exporter` | MySQL |
| `redis_exporter` | Redis |
| `postgres_exporter` | PostgreSQL |
| `nginx-prometheus-exporter` | Nginx（需 `stub_status`） |
| `blackbox_exporter` | HTTP/TCP/DNS 探测 |
| `cadvisor` | 容器（Docker/K8s） |
| `kube-state-metrics` | K8s 对象状态 |

## node_exporter 部署示例

```bash
# 下载解压后
./node_exporter --web.listen-address=:9100

# docker 方式
docker run -d --name node-exporter -p 9100:9100 \
  --net=host prom/node-exporter
```

在 `prometheus.yml` 中配置抓取：

```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['10.0.0.1:9100', '10.0.0.2:9100']
```

## 自定义 Exporter

用官方客户端库编写（Go/Python/Java）：

- 定义 `Counter`/`Gauge`/`Histogram`/`Summary` 指标。
- 注册到 `/metrics` 处理器。
- 暴露 HTTP 端口供 Prometheus 拉取。

也可直接用 `textfile` 收集器让脚本写入指标文件，由 node_exporter 读取。

## 注意事项

- Exporter 与被监控对象**同机或网络可达**；跨网络可用 `relabel`/服务发现。
- 指标基数（cardinality）过大会拖垮 Prometheus，避免高基数标签（如 user_id）。
- 短生命周期任务无法被拉取，改用 [PushGateway](PushGateway.md)。
- 安全：Exporter 默认无鉴权，建议仅在内网或经反向代理加认证。

相关：服务端部署见 [服务端部署](服务端部署.md)；查询见 [PromQL](PromQL.md)。
