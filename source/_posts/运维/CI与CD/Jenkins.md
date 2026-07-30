---
title: Jenkins 持续集成
date: 2026-07-30 10:00:00
tags:
- 运维
- CI
- CD
- Jenkins
categories:
- 运维
- CI与CD
---

# Jenkins 持续集成

Jenkins 是最流行的开源 CI/CD 引擎，通过 Pipeline 把构建、测试、部署流程代码化，支持海量插件与分布式构建。

## 安装与初始化

```bash
# Docker 方式（数据卷持久化）
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins-home:/var/jenkins_home \
  --name jenkins jenkins/jenkins:lts

# 包安装（RHEL）
yum install -y jenkins
systemctl enable --now jenkins
```

首次访问 `http://<host>:8080`，按提示解锁（初始密码在 `/var/jenkins_home/secrets/initialAdminPassword`），安装推荐插件并创建管理员。

## 节点（Agent / Node）管理

- **Master**：调度与 UI，不直接跑重构建。
- **Agent（节点）**：实际执行任务的 worker，支持 SSH 或 JNLP（Web 启动）连接。
- 管理：Manage Jenkins → Nodes → New Node，配置标签（labels）便于 Pipeline 按标签选节点。
- K8s 环境可用 `Kubernetes Plugin` 动态起 Pod 作为临时 Agent，用完即销。

## Pipeline 语法

**Declarative（声明式，推荐）**：

```groovy
pipeline {
  agent any
  options { timestamps(); timeout(time: 30, unit: 'MINUTES') }
  stages {
    stage('Build') {
      steps { sh 'make' }
    }
    stage('Test') {
      steps { sh 'make test' }
    }
    stage('Deploy') {
      when { branch 'main' }
      steps { sh './deploy.sh' }
    }
  }
  post {
    success { echo '部署成功' }
    failure { echo '构建失败' }
  }
}
```

**Scripted（脚本式）**：基于 Groovy，灵活但可读性差。

- `agent any`：任意可用节点；`agent { label 'docker' }`：指定标签节点。
- 多分支流水线（Multibranch Pipeline）：自动为每个分支/PR 建流水线，配合 `Jenkinsfile`。
- 共享库（Shared Libraries）：抽取公共步骤，多项目复用。

## 凭据与插件

- 凭据（Credentials）：Manage Jenkins → Credentials，支持账号密码、SSH Key、Secret text、证书；Pipeline 中以 `credentials('id')` 引用，避免明文。
- 常用插件：`Git`、`Pipeline`、`Docker Pipeline`、`Kubernetes`、`Blue Ocean`（可视化）、`Credentials Binding`。
- 建议停用不必要的插件，定期升级并备份 `JENKINS_HOME`。

## 与 Docker / Kubernetes 集成

```groovy
pipeline {
  agent {
    docker { image 'maven:3.9-eclipse-temurin-17' }
  }
  stages {
    stage('Build') { steps { sh 'mvn clean package' } }
  }
}
```

- 容器内构建，保证环境一致。
- 配合 `withDockerRegistry` 推镜像到仓库；K8s 动态 Agent 适合大规模弹性构建。

## 发布策略

- **蓝绿发布**：两套环境，流量整体切换，回滚快。
- **金丝雀发布**：先放少量流量，观察无异常再全量。
- 触发方式：Webhook（Git 推送）、定时（`cron`）、手动。

相关：GitLab CI 见 [GitLab CI](GitLab CI.md)；容器化部署见 [Docker](../容器与编排/Docker/readme.md)。
