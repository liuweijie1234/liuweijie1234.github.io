---
title: Kubernetes Service 与 Ingress
date: 2026-07-30 10:00:00
tags:
- 运维
- Kubernetes
- Service
- Ingress
categories:
- 运维
- 容器与编排
- Kubernetes
---

# Kubernetes Service 与 Ingress

Pod IP 会随重建变化，Service 提供稳定的访问入口与负载均衡，Ingress 则管理集群外部 HTTP/HTTPS 路由。

## Service 类型

| 类型 | 说明 | 访问方式 |
| --- | --- | --- |
| `ClusterIP`（默认） | 集群内部虚拟 IP | 仅集群内可访问 |
| `NodePort` | 在每个节点开放固定端口（30000-32767） | `<节点IP>:<NodePort>` |
| `LoadBalancer` | 调用云厂商创建外部负载均衡器 | 公网/内网 LB IP |
| `ExternalName` | 映射到外部 DNS 名称（CNAME） | 集群内解析到外部服务 |

```bash
kubectl expose deployment web --port=80 --target-port=8080 --type=NodePort
kubectl get svc
```

## 服务发现与 DNS

集群内置 CoreDNS，Service 可通过 `<svc>.<namespace>.svc.cluster.local` 互访：

```yaml
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }        # 匹配后端 Pod 标签
  ports:
  - port: 80
    targetPort: 8080
```

同命名空间内直接 `curl http://web` 即可。

## Headless Service

`clusterIP: None` 时返回后端 Pod IP 列表，常用于有状态服务（StatefulSet）做点对点发现：

```yaml
spec:
  clusterIP: None
  selector: { app: redis }
```

## Ingress 与 Ingress Controller

Ingress 定义 HTTP 路由规则，需配套 **Ingress Controller**（如 ingress-nginx、Traefik）才能生效：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: web
            port: { number: 80 }
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port: { number: 80 }
  tls:
  - hosts: [example.com]
    secretName: example-tls      # 引用包含 cert+key 的 Secret
```

```bash
kubectl apply -f ingress.yaml
kubectl describe ingress web-ingress
kubectl get ingress -o wide
```

## TLS 与证书

Ingress TLS 通过 Secret 挂载证书（PEM）：`kubectl create secret tls example-tls --cert=fullchain.pem --key=privkey.pem`。证书自动续期可用 cert-manager。

## 网络策略：NetworkPolicy

默认 Pod 间全通，可用 NetworkPolicy 做微隔离（需 CNI 支持，如 Calico）：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: deny-other-ns }
spec:
  podSelector: { matchLabels: { app: db } }
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector: { matchLabels: { app: web } }
    ports:
    - port: 3306
```

## 灰度/金丝雀流量

- ingress-nginx 通过 `nginx.ingress.kubernetes.io/canary` 注解实现基于权重/Header 的灰度。
- 或服务网格（Istio/Linkerd）做更精细的流量切分。

> 入口流量链路：客户端 → Ingress Controller（Service NodePort/LoadBalancer）→ Service → Pod。
