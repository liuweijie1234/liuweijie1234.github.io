---
title: 运维 · Kubernetes
date: 2026-07-30 10:00:00
tags:
- 运维
- Kubernetes
- K8s
- 容器编排
- 导航
categories:
- 运维
- 容器与编排
- Kubernetes
---

# Kubernetes

Kubernetes（K8s）是容器编排的事实标准，负责容器化应用的调度、伸缩、服务发现与自愈。

## 子页面

- [核心概念与架构](核心概念与架构.md)
- [Pod 与 Workload](Pod与Workload.md)
- [Service 与 Ingress](Service与Ingress.md)
- [配置与存储](配置与存储.md)
- [集群部署与运维](集群部署与运维.md)

## 一句话概览

Master（控制平面：API Server / Scheduler / Controller） + Node（工作节点：kubelet / kube-proxy / 容器运行时），通过声明式 YAML 管理 Pod 生命周期。
