---
title: 运维 · RabbitMQ
date: 2026-07-30 10:00:00
tags:
- 消息队列
- RabbitMQ
categories:
- 运维
- 消息队列
- RabbitMQ
---

# RabbitMQ

RabbitMQ 是基于 AMQP 的成熟消息中间件，强调灵活的路由与可靠投递。

> 重点复习消息丢失/重复消费/顺序消费的解决方案，画出架构图。

消息丢失、重复消费、消息积压、死信队列、削峰填谷场景
手写可靠生产者消费者，实现异步订单解耦

## 目录

- 核心模型（Exchange / Queue / Binding / RoutingKey）
- 交换机类型（direct / topic / fanout / headers）
- 工作模式（简单队列 / 工作队列 / 发布订阅 / 路由 / 主题）
- 消息可靠性（publisher confirm、消息持久化、手动 ack）
- 死信队列（DLX）与延时队列
- 消息积压处理
- 集群与镜像队列
- 常用运维命令（rabbitmqctl / 管理插件）

## 关键命令锚点

```bash
rabbitmqctl list_queues
rabbitmqctl list_exchanges
rabbitmq-plugins enable rabbitmq_management
```

## 待补充清单

- [ ] 可靠生产者消费者示例
- [ ] 死信队列实战
- [ ] 集群与镜像队列部署
