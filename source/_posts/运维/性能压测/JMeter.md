---
title: JMeter 性能压测
date: 2026-07-30 10:00:00
tags:
- 运维
- 压测
- JMeter
categories:
- 运维
- 性能压测
---

# JMeter 性能压测

Apache JMeter 是基于 Java 的开源压测工具，支持 HTTP、FTP、JDBC、TCP 等协议，适合复杂的接口场景、参数化与分布式压测。

## 核心概念

- **测试计划（Test Plan）**：所有元件的容器，是整个压测的根。
- **线程组（Thread Group）**：定义并发用户数、ramp-up 时间与循环次数。
- **取样器（Sampler）**：真正发起请求的元件，如 HTTP 请求、JDBC 请求。
- **断言（Assertion）**：校验响应是否符合预期（响应码、内容、大小）。
- **监听器（Listener）**：收集并展示结果，如聚合报告、查看结果树、图形结果。
- **配置元件（Config Element）**：HTTP 请求默认值、CSV 数据集、请求头等。
- **定时器（Timer）**：在请求间插入延迟，模拟真实用户思考时间。

## 线程组设计

| 字段 | 说明 |
| --- | --- |
| Number of Threads | 并发虚拟用户数 |
| Ramp-up period | 全部线程启动耗时，避免瞬间打满 |
| Loop Count | 循环次数（勾选 Forever 则持续） |
| Duration | 计划持续时间 |

经验：Ramp-up 建议 = 线程数 / 期望的每秒新增用户，避免瞬间洪峰导致误判。

## 参数化与关联

- **CSV 数据驱动**：通过 `CSV Data Set Config` 读取账号、参数文件，实现多用户不同数据。
- **正则表达式提取器**：从响应中提取 token，供后续请求使用（如登录后获取 session）。
- **JSON Extractor**：从 JSON 响应中提取字段（JMeter 3+ 支持）。

## 分布式压测

当单机无法产生足够压力时，使用 Master + 多个 Slave：

```bash
# slave 节点启动
jmeter-server -Dserver.rmi.ssl.disable=true

# master 执行，指定远程节点
jmeter -n -t plan.jmx -R 192.168.1.10,192.168.1.11 -l result.jtl
```

注意：只把测试脚本发到 Slave，压测产生的数据在 Slave 本地执行，结果汇总到 Master。

## 非 GUI 模式运行

生产压测务必使用命令行（GUI 会消耗大量资源）：

```bash
# -n 非 GUI，-t 测试计划，-l 结果文件，-e -o 生成 HTML 报告
jmeter -n -t plan.jmx -l result.jtl -e -o report/

# 指定远程节点分布式
jmeter -n -t plan.jmx -R slave1,slave2 -l result.jtl
```

## 报告与结果分析

- **聚合报告**：关注 Average、90% Line、99% Line、Throughput（吞吐量）、Error%。
- **HTML 报告**：`report/index.html` 含响应时间趋势、TPS、并发图。
- **查看结果树**：调试阶段使用，正式压测关闭以免内存溢出。

关键指标：错误率应 < 1%（视业务而定），99% 响应时间满足 SLA，吞吐量随并发上升且不过载。

## 调优建议

- 关闭不必要的监听器（GUI 调试除外）。
- 调整 JVM 堆：编辑 `jmeter` 中的 `HEAP="-Xms1g -Xmx4g"`。
- 使用 `Throughput Shaping Timer` 控制目标 TPS，而非仅堆并发。
