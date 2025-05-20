---
title: Prometheus windows 安装 Alertmanager
date: 2024-04-01 09:00:00
tags:
- Prometheus
categories:
- [Prometheus]
---

部署 Alertmanager , 配置 prometheus监控  node exporter 的一些 metrics,预警,邮件(微信、短信)通知， prometheus web 显示查看 alert 等


## 下载安装

https://prometheus.io/download/#alertmanager

下载 windows 版本的安装包，解压到指定目录，如 `D:\prometheus\alertmanager`


## 注册服务

使用 nssm.exe 把 alertmanager.exe 注册成系统服务

```bash
nssm install Alertmanager
```

注意：

Application 
path：就是选择你 exe 文件的路径。例如：`D:\prometheus\alertmanager\alertmanager.exe`

Startup directory：会自动加载exe所对应目录，不需改动

Service name ：自定义服务名称，可在服务列表找到。

Arguments：启动参数，默认即可。`--config.file=alertmanager.yml`

## 启动服务

```bash
nssm start Alertmanager
```

浏览器访问 `http://127.0.0.1:9093/` 即可看到 Alertmanager 的页面。

## 配置文件 *_rules.yml

alert:告警规则的名称。

expr:基于 PromQL 表达式告警触发条件，用于计算是否有时间序列满足该条件。

for:评估等待时间，可选参数。用于表示只有当触发条件持续一段时间后才发送告警。在 等待期间新产生告警的状态为 pending。

labels:自定义标签，允许用户指定要附加到告警上的一组附加标签。

annotations:用于指定一组附加信息，比如用于描述告警详细信息的文字等，annotations 的内容在告警产生时会一同作为参数发送到 Alertmanager。

summary 描述告警的概要信息，description 用于描述告警的详细信息。

```yaml
groups:
- name: node-rules
  rules:
  - alert: HighRequestLatency
    expr: job:request_latency_seconds:mean5m{job="myjob"} > 0.5
    for: 10m
    labels:
      severity: page
    annotations:
      summary: High request latency

  - alert: node-up
    expr: up{job="Windows"} == 0
    for: 15s
    labels:
      severity: 1
      team: node
    annotations:
      summary: "{{$labels.instance}}Instance has been down for more than 15 seconds"

```



Prometheus Alert 告警状态有三种状态:Inactive、Pending、Firing

第一种：Inactive:非活动状态，表示正在监控，但是还未有任何警报触发。

第二种：Pending:表示这个警报必须被触发。由于警报可以被分组、压抑/抑制或静默/静音，所 以等待验证，一旦所有的验证都通过，则将转到 Firing 状态。

第三种：Firing:将警报发送到 AlertManager，它将按照配置将警报的发送给所有接收者。一旦警 报解除，则将状态转到 Inactive，如此循环。

Prometheus:使用 AlertManager 实现 Windows 下邮件告警
https://www.notepad.com.cn/65.html

记-Windows环境下Prometheus+alertmanager+windows_exporter+mtail监控部署提起网关日志
https://blog.csdn.net/qq_41372916/article/details/129036418


prometheus实战之四：alertmanager的部署和配置
https://cloud.tencent.com/developer/article/2291971

从零开始搭建Prometheus+Grafana+AlertManager+Node-exporter自动监控报警系统（非docker方式安装：推荐） 
https://www.cnblogs.com/wangjunjiehome/p/15080362.html

Prometheus 监控Windows Exporter并设置相关告警
https://i4t.com/16728.html