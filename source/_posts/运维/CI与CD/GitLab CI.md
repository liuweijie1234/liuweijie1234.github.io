---
title: GitLab CI 持续集成
date: 2026-07-30 10:00:00
tags:
- 运维
- CI
- CD
- GitLab
categories:
- 运维
- CI与CD
---

# GitLab CI 持续集成

GitLab CI 是 GitLab 内置的 CI/CD，通过仓库中的 `.gitlab-ci.yml` 定义流水线，由 Runner 执行，与代码仓库、Merge Request、容器仓库深度集成。

## `.gitlab-ci.yml` 结构

```yaml
stages:
  - build
  - test
  - deploy

variables:
  IMAGE: registry.example.com/app:${CI_COMMIT_SHORT_SHA}

build:
  stage: build
  image: maven:3.9
  script:
    - mvn clean package -DskipTests
  artifacts:
    paths:
      - target/app.jar
    expire_in: 1 hour

test:
  stage: test
  script:
    - mvn test

deploy:
  stage: deploy
  only:
    - main
  script:
    - ./deploy.sh
```

- **stages**：定义阶段顺序（串行依赖）。
- **job**：最小执行单元，归属某个 stage；同名默认并行。
- **script**：执行的 shell 命令。
- **only/except** 或 `rules`：控制触发条件（`main` 分支、MR、tag 等）。

## Runner 注册与类型

```bash
# 安装 gitlab-runner
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | bash
yum install -y gitlab-runner

# 注册（交互填入 URL、token、executor）
gitlab-runner register
#   - executor: shell / docker / kubernetes / ssh
#   - 注册后成为 specific（项目专属）或 shared（实例共享）Runner
gitlab-runner status
```

- **shared runner**：全实例可用；**specific runner**：绑定项目。
- **executor**：`shell`（本机执行）、`docker`（容器隔离，最常用）、`kubernetes`（动态 Pod）。

## 缓存（cache）与制品（artifacts）

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/

build:
  artifacts:
    paths:
      - dist/
    expire_in: 1 day
```

- `cache`：跨流水线/任务重用（如依赖目录），加速构建，不可靠依赖。
- `artifacts`：任务产物，可传递给后续 stage 或供下载，受 `expire_in` 控制。

## 变量与密钥

- 项目/群组级：Settings → CI/CD → Variables，支持普通与 `masked`（日志掩码）、`protected`（仅保护分支暴露）。
- 文件型变量（如 K8s kubeconfig、SSH key）以 `file` 类型注入临时文件。
- 内置变量：`CI_COMMIT_SHA`、`CI_COMMIT_REF_NAME`、`CI_PIPELINE_ID` 等。

## 镜像构建与推送

```yaml
build-image:
  stage: build
  image: docker:24
  services: [docker:24-dind]
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE .
    - docker push $IMAGE
```

## 环境部署与审批

- `environment: production` 结合 GitLab Environments 做多环境管理与一键回滚。
- 审批：用 `when: manual` 的 job 做人工卡点：

```yaml
deploy-prod:
  stage: deploy
  environment: production
  when: manual
  script: ./deploy-prod.sh
```

- K8s 部署：Runner 用 `kubectl` 或 `helm` 更新集群；详见 [Kubernetes 部署](../容器与编排/Kubernetes/集群部署与运维.md)。

相关：Jenkins 见 [Jenkins](Jenkins.md)。
