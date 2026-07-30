---
title: PushGateway
date: 2026-07-30 10:00:00
tags:
- 监控与可观测性
- Prometheus
- PushGateway
categories:
- 运维
- 监控与可观测性
- Prometheus
---

# Prometheus PushGateway

PushGateway 用于接收**短时任务（批处理、定时脚本）**主动推送（push）的指标，解决 Prometheus 拉模型（pull）无法抓取到短生命周期任务的问题。

## 适用场景

- 定时脚本（cron job）、一次性任务、CI 构建等执行几秒到几分钟即退出的作业。
- 这类任务的指标在 Prometheus 来拉取时往往已经退出，必须在退出前把指标推送给 PushGateway。
- 不适合长期运行的服务（它们应直接用 Exporter 被 pull）。

## 部署

```bash
# docker
docker run -d -p 9091:9091 prom/pushgateway

# 二进制
./pushgateway --web.listen-address=:9091
```

Prometheus 仍需配置抓取 PushGateway 本身：

```yaml
scrape_configs:
  - job_name: 'pushgateway'
    honor_labels: true
    static_configs:
      - targets: ['pushgateway:9091']
```

> `honor_labels: true` 很重要，否则 PushGateway 推送的 `job`/`instance` 标签会被覆盖。

## 推送指标

```bash
# 推送单次指标（HTTP PUT，覆盖该分组全部指标）
echo "batch_job_duration_seconds 12.3" | \
  curl --data-binary @- http://pushgateway:9091/metrics/job/batch_clean/instance/node1

# 多指标一次推送
cat <<EOF | curl --data-binary @- http://pushgateway:9091/metrics/job/backup/instance=db1
# TYPE backup_rows counter
backup_rows 10240
backup_last_success_timestamp_seconds $(date +%s)
EOF

# 删除分组指标（DELETE）
curl -X DELETE http://pushgateway:9091/metrics/job/batch_clean/instance/node1
```

分组标识：`/metrics/job/<job名>` 必需，`/instance/<实例名>` 可选。相同 job+instance 为一组，PUT 整体替换、POST 增量更新。

## Python 示例（prometheus_client）

```python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
g = Gauge('batch_rows', 'rows processed', registry=registry)
g.set(10240)
push_to_gateway('pushgateway:9091', job='batch_clean', registry=registry)
```

## 注意事项

- PushGateway 是**指标中转站**，本身不做长期存储，数据最终仍由 Prometheus 抓取留存。
- 推送的分组若不再更新会一直保留，需自行清理（DELETE）或用 `pushgateway --persistence.file` 谨慎配置。
- 长期运行服务不要用 PushGateway，否则会掩盖服务宕机（指标还在）。
- 生产建议加入认证（反向代理）与定时清理策略。
