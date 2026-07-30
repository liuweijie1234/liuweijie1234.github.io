---
title: NPM 使用教程
date: 2023-03-13 09:30:00
tags:
- NPM
- 前端基础
categories:
- 前端
- 前端基础
---

# NPM 使用教程

npm 是 Node.js 的默认包管理器，用于安装、升级、卸载依赖与发布包。镜像与代理配置对国内网络尤为重要。

## 1. 配置

```bash
npm init                       # 交互式初始化 package.json
npm init -y                    # 一键生成默认 package.json

# 指定镜像源安装
npm install --registry=https://mirrors.tencent.com/npm/

# 设置环境变量默认值
npm set init-author-name 'Your name'
npm set init-author-email 'Your email'
npm set init-author-url 'http://yourdomain.com'
npm set init-license 'MIT'

npm config list -l             # 查看所有配置
npm -v                         # 查看 npm 版本
```

### 镜像与代理

```bash
# 设置/删除代理
npm config set proxy=http://127.0.0.1:8087
npm config set https_proxy=http://127.0.0.1:12639
npm config delete proxy
npm config delete https-proxy

# 切换 registry 镜像
npm config set registry https://mirrors.tencent.com/npm/
npm config set registry http://r.npm.taobao.org/
npm config delete registry
```

> 环境变量方式：`export http_proxy=http://127.0.0.1:12639`、`export https_proxy=...`

## 2. 安装

```bash
npm install                    # 安装 package.json 全部依赖
npm install <pkg>              # 安装并写入 dependencies
npm install <pkg> -D           # 安装到 devDependencies（开发依赖）
npm install -g @vue/cli        # 全局安装
npm install <pkg> --force      # 强制重新安装
npm install git://github.com/user/repo.git#0.1.0  # 从 git 安装
```

## 3. 升级与卸载

```bash
npm install -g npm@latest      # 升级 npm 自身
npm update [pkg]               # 升级当前项目指定模块
npm update -g [pkg]            # 升级全局模块
npm uninstall [pkg]            # 卸载（项目）
npm uninstall [pkg] -g         # 卸载（全局）
```

## 4. 查看

```bash
npm info jquery                # 查看源上版本信息
npm ls jquery                  # 查看已安装版本
npm list                       # 列出当前项目依赖树
npm list -g                    # 列出全局依赖
npm list vue
```

## 5. 与 pnpm / yarn 的关系

现代项目常使用更快、更省磁盘的 `pnpm`（硬链接 + 全局 store）：

```bash
npm install -g pnpm           # 安装 pnpm
pnpm install                  # 安装依赖（等效 npm install）
pnpm add <pkg>                # 等效 npm install <pkg>
```

> 实际项目（如 [韩进 new-freight](../项目实战/韩进new-freight.md)）即用 `pnpm` 管理依赖。
