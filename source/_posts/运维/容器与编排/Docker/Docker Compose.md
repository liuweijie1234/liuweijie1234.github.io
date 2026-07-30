---
title: Docker Compose
date: 2026-07-30 10:00:00
tags:
- 运维
- Docker
- Compose
categories:
- 运维
- 容器与编排
- Docker
---

# Docker Compose

Compose 用一份 `docker-compose.yml` 定义多容器应用（服务、网络、卷），一条命令即可拉起整套环境，非常适合开发、测试与中小型部署。

## compose 文件结构

```yaml
version: "3.8"

services:
  web:
    image: myapp:1.0
    build: .                       # 本地构建
    ports:
      - "8080:80"
    environment:
      - TZ=Asia/Shanghai
    depends_on:
      - db
    networks:
      - appnet

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - dbdata:/var/lib/mysql
    networks:
      - appnet

  redis:
    image: redis:7
    networks:
      - appnet

networks:
  appnet:
    driver: bridge

volumes:
  dbdata:
```

## 多容器编排要点

- **services**：每个服务对应一个容器（或一组容器），可指定 `image` 或 `build`。
- **networks**：自定义网络让服务以服务名互访（内置 DNS）。
- **volumes**：声明命名卷做数据持久化；也可 `bind` 挂载配置。
- **depends_on**：控制启动顺序（不等待"就绪"，仅顺序启动）。

## 环境变量与 .env

Compose 自动读取同目录 `.env`：

```bash
# .env
MYSQL_ROOT_PASSWORD=secret
IMAGE_TAG=1.0
```

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    image: myapp:${IMAGE_TAG}
```

也可通过 `environment` / `env_file` 注入。

## 常用命令

```bash
docker compose up -d            # 后台启动
docker compose up -d --build    # 重新构建后启动
docker compose ps               # 查看服务状态
docker compose logs -f web      # 跟踪某服务日志
docker compose exec web sh      # 进入服务容器
docker compose stop             # 停止（保留容器）
docker compose down             # 停止并删除容器、网络
docker compose down -v          # 同时删除卷（数据会丢！谨慎）
docker compose restart web      # 重启某服务
```

> 老版本命令为 `docker-compose`（连字符），新版已整合进 `docker compose`。

## 依赖与健康检查

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy   # 等待 db 健康后再启动
  db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10
```

`healthcheck` 让 Compose 感知服务真正"就绪"，避免 web 在 db 未起好时连接失败。

## 生产注意事项

- 生产建议用 `restart: unless-stopped` 保证容器意外退出自动重启。
- 敏感配置用 `.env`（加入 `.gitignore`）或外部 secrets，避免明文入库。
- 数据务必挂卷，否则 `down` 后数据丢失。
- 大规模、需调度与自愈的场景，建议迁移到 Kubernetes（见 [Kubernetes](../Kubernetes/readme.md)）；Swarm 也可做多主机编排。
