---
title: Kubernetes Pod 与 Workload
date: 2026-07-30 10:00:00
tags:
- 运维
- Kubernetes
- Pod
categories:
- 运维
- 容器与编排
- Kubernetes
---

# Kubernetes Pod 与 Workload

Pod 是 K8s 最小的调度与运行单元。Workload（工作负载）控制器负责管理 Pod 的副本、发布与自愈。

## Pod 基本概念

- Pod 包含一个或多个紧密关联的容器，共享**网络命名空间**（同一 IP）与**存储卷**。
- 同 Pod 内容器通过 `localhost` 通信，通过 Volume 共享文件。
- Pod 本身不自愈，通常由控制器管理（Pod 被删除后由控制器重建）。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web
  labels:
    app: web
spec:
  containers:
  - name: web
    image: nginx:1.26
    ports:
    - containerPort: 80
```

## 探针（Probe）：liveness / readiness

- **livenessProbe**：失败则重启容器（判定"卡死"）。
- **readinessProbe**：失败则从 Service 摘除（判定"暂未就绪"）。
- **startupProbe**：启动保护，避免慢启动被误杀。

```yaml
livenessProbe:
  httpGet: { path: /healthz, port: 8080 }
  initialDelaySeconds: 10
  periodSeconds: 10
readinessProbe:
  httpGet: { path: /ready, port: 8080 }
  periodSeconds: 5
```

## 副本与自愈：ReplicaSet

ReplicaSet 保证指定数量的 Pod 副本始终运行（节点宕机自动在别的节点重建）。通常不直接写 RS，而是用 Deployment。

## 无状态部署：Deployment

最常用的工作负载，支持滚动更新与回滚：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
      - name: web
        image: myapp:1.0
        resources:
          requests: { cpu: 100m, memory: 128Mi }
          limits:   { cpu: 500m, memory: 256Mi }
```

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/web        # 观察滚动更新
kubectl rollout undo deployment/web          # 回滚到上一版
kubectl rollout history deployment/web       # 查看历史版本
kubectl scale deployment/web --replicas=5    # 手动扩缩容
```

更新策略：`RollingUpdate`（默认，逐批替换）与 `Recreate`（先删后建，适合不可并存场景）。

## 有状态：StatefulSet

为需要稳定网络标识与持久存储的应用（数据库、中间件）设计：

- 稳定的 Pod 名（`web-0`、`web-1`）与稳定 DNS。
- 稳定的持久卷（PVC 随 Pod 重建保留）。
- 有序部署/扩缩（0→N 顺序）。

```bash
kubectl rollout status sts/mysql
kubectl exec -it mysql-0 -- mysql -uroot -p
```

## 批处理：Job / CronJob

```yaml
apiVersion: batch/v1
kind: Job
metadata: { name: batch-job }
spec:
  template:
    spec:
      containers:
      - name: job
        image: myjob:1.0
      restartPolicy: Never
  backoffLimit: 3
---
apiVersion: batch/v1
kind: CronJob
metadata: { name: daily-backup }
spec:
  schedule: "0 2 * * *"          # 每天 2 点
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup:1.0
          restartPolicy: OnFailure
```

## 守护进程：DaemonSet

每个（或匹配的）节点运行一个 Pod，常用于日志采集（Filebeat）、监控 Agent（node-exporter）：

```bash
kubectl get ds -n kube-system
```
