---
title: 运维 · Kafka
date: 2026-07-30 10:00:00
tags:
- 消息队列
- Kafka
categories:
- 运维
- 消息队列
- Kafka
---

# Kafka

Kafka 是分布式高吞吐消息流平台，常用于日志管道、事件溯源与异步解耦。

> Kafka 重点复习消息丢失/重复消费/顺序消费的解决方案，画出架构图。

## 目录

- 核心概念（Producer / Broker / Consumer / Consumer Group / Topic / Partition / Offset）
- 存储与副本（ISR、Leader/Follower、HW/LEO）
- 高可用与选举
- 消息可靠性（acks、幂等生产者、事务）
- 重复消费与幂等消费
- 顺序消费（分区内有序）
- 消息积压与消费扩容
- 常用运维命令（topic 创建、消费组、位移重置）

## 关键命令锚点

```bash
kafka-topics.sh --create --topic order --partitions 3 --replication-factor 2
kafka-console-consumer.sh --topic order --from-beginning --bootstrap-server localhost:9092
kafka-consumer-groups.sh --describe --group g1 --bootstrap-server localhost:9092
```

## 待补充清单

- [ ] 架构图
- [ ] 消息丢失排查清单
- [ ] 与 RabbitMQ 对比
