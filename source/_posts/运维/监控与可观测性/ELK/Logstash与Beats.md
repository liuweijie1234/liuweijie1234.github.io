---
title: Logstash 与 Beats
date: 2026-07-30 10:00:00
tags:
- 运维
- ELK
- Logstash
- Beats
categories:
- 运维
- 监控与可观测性
- ELK
---

# Logstash 与 Beats

在 ELK 体系中，**Beats** 是轻量级数据采集器（部署在源头），**Logstash** 是数据处理管道（清洗、富化、路由）。二者常配合完成"采集 → 处理 → 存储 → 展示"。

## Beats 家族

| Beat | 采集对象 |
| --- | --- |
| `Filebeat` | 日志文件（最常用） |
| `Metricbeat` | 系统/服务指标 |
| `Packetbeat` | 网络流量 |
| `Heartbeat` | 可用性探测（ICMP/TCP/HTTP） |
| `Auditbeat` | 审计日志 |

## Filebeat 采集与输出

`filebeat.yml`：

```yaml
filebeat.inputs:
  - type: log
    paths:
      - /var/log/nginx/*.log
    fields: { app: nginx }       # 附加字段

output.logstash:                  # 发给 Logstash（推荐，便于处理）
  hosts: ["logstash:5044"]
# 也可直连 ES：
# output.elasticsearch:
#   hosts: ["http://elasticsearch:9200"]
#   index: "nginx-%{+yyyy.MM.dd}"
```

启动：`filebeat -e -c filebeat.yml`。默认端口 5044（Logstash beats 输入）。

## Logstash 管道（input / filter / output）

配置文件三段式：

```ruby
input {
  beats { port => 5044 }          # 接收 Filebeat
}

filter {
  grok {                          # 解析非结构化日志
    match => { "message" => "%{IPORHOST:client} - %{USER:user} \[%{HTTPDATE:timestamp}\] \"%{WORD:method} %{URIPATH:path}\"" }
  }
  date {                          # 解析时间戳
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    target => "@timestamp"
  }
  mutate {                        # 字段清洗
    remove_field => ["message", "host"]
    convert => { "status" => "integer" }
  }
  geoip { source => "client" }    # IP 地理信息富化
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "nginx-%{+YYYY.MM.dd}"
  }
}
```

## grok 正则解析

grok 用预定义模式（`%{PATTERN:name}`）把文本解析成字段：

```
%{IP:clientip} %{WORD:method} %{NUMBER:response:int}
```

常用模式：`IPORHOST`、`USER`、`HTTPDATE`、`URIPATH`、`NUMBER`、`WORD`、`GREEDYDATA`。可用 [grokdebugger](https://grokdebug.herokuapp.com/) 在线调试。

## 与 Elasticsearch / Kafka 对接

```ruby
# 输出到 Kafka（削峰/解耦）
output {
  kafka {
    bootstrap_servers => "kafka:9092"
    topic_id => "logs-raw"
  }
}

# 读取 Kafka 再写 ES（典型解耦架构：Filebeat→Kafka→Logstash→ES）
input {
  kafka { bootstrap_servers => "kafka:9092" topics => ["logs-raw"] }
}
```

## 性能与背压处理

- Filebeat 轻量，几乎不占资源；Logstash 较重，建议独立机器部署并适当加 worker（`pipeline.workers`）。
- 高吞吐时引入 Kafka 做缓冲，避免 ES 写入瓶颈时丢数据。
- 使用 `persistent queue`（`queue.type: persisted`）在 Logstash 本地缓存防丢。
- 字段数量与 grok 复杂度影响性能，尽量在源头（Filebeat processors）预处理。

ELK 总览与 Elasticsearch 部署见 [ELK readme](../ELK/readme.md)；可视化见 [Kibana](Kibana/常用命令.md)。
