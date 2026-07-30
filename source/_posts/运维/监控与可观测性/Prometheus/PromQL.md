---
title: PromQL 查询
date: 2026-07-30 10:00:00
tags:
- 运维
- Prometheus
- PromQL
categories:
- 运维
- 监控与可观测性
- Prometheus
---

# PromQL 查询

PromQL 是 Prometheus 的查询语言，用于实时与历史指标计算、告警规则与 Grafana 面板。

## 数据类型

- **Instant vector（瞬时向量）**：同一时刻的一组时间序列（如 `node_cpu_seconds_total`）。
- **Range vector（区间向量）**：一段时间内的序列（如 `[5m]`）。
- **Scalar**：单个数值；**String**：字符串（极少用）。

## 选择器与标签匹配

```promql
# 精确指标名
node_cpu_seconds_total

# 标签过滤（= 等, != 不等, =~ 正则, !~ 反则）
node_cpu_seconds_total{mode="idle"}
node_cpu_seconds_total{instance=~"10.0.0.*", mode!="idle"}

# 区间向量
node_cpu_seconds_total[5m]
```

## 常用函数

| 函数 | 用途 |
| --- | --- |
| `rate()` | 计数器每秒平均增量（自动处理重置） |
| `irate()` | 基于最近两个点计算速率，更灵敏 |
| `increase()` | 区间内的总增量 |
| `sum()` / `avg()` / `max()` / `min()` | 聚合 |
| `by (label)` / `without (label)` | 聚合维度 |
| `count()` | 计数 |
| `histogram_quantile()` | 计算分位数（P99 等） |
| `topk()` / `bottomk()` | 取前/后 N |
| `absent()` | 指标缺失返回 1（用于"不存在"告警） |

## 实战查询

```promql
# CPU 使用率（非 idle 占比）
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)

# 磁盘使用率
100 * (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes)

# 节点 5 分钟内平均 Load
avg(node_load5) by (instance)

# QPS（请求速率）
sum(rate(http_requests_total[5m]))

# P99 响应时间（基于 histogram）
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

## 聚合与运算

```promql
sum(rate(node_network_receive_bytes_total[5m])) by (instance)   # 流量/实例
sum without (cpu, mode) (rate(node_cpu_seconds_total[5m]))      # 忽略某些标签
node_memory_MemTotal_bytes / 1024 / 1024 / 1024                 # 标量运算，得 GB
```

## 告警规则示例

```yaml
groups:
  - name: node-alert
    rules:
      - alert: HighCpuUsage
        expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "实例 {{ $labels.instance }} CPU 持续 >85%"
```

## 在 Grafana 中使用

- 添加 Prometheus 数据源后，面板查询直接写 PromQL。
- 变量（Variables）结合 `label_values(node_cpu_seconds_total, instance)` 实现下拉联动。
- 速查参考：https://prometheus.io/docs/prometheus/latest/querying/functions/

服务端部署见 [服务端部署](服务端部署.md)；告警分发见 [Alertmanager](Alertmanager.md)。
