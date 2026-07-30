---
title: 韩进 new-freight 前端系统
date: 2026-07-30 10:00:00
tags:
- 项目实战
- 前端
- Vite
- pnpm
categories:
- 前端
- 项目实战
---

新前端系统：(new-freight)(OMP端)

0. 云效拉取 new-freight 项目，然后使用 VSCode 或者 PyCharm 打开 new-freight 项目
1. 安装 nvm
2. 执行 `nvm install 22.14.0` 安装 node 环境
3. 然后输入 `nvm use 22.14.0` 使用刚才下载的 node 版本

> tips：必须要安装 18 以上版本的 node 环境，否则无法运行 Vite 项目

4. 执行 `npm install -g pnpm` 安装 pnpm
5. 执行 `pnpm install` 或者 `yarn install` 安装 node 插件依赖
6. 执行 `pnpm dev --mode 环境名称` 即可运行指定环境的前端

如 `pnpm dev --mode hanjinTest` 则运行的是 hanjinTest 的环境：

```bash
pnpm dev --mode hanjinTest
pnpm dev --mode developmentHJ
```

> 多环境通过 `--mode` 指定，对应项目根目录下的 `.env.hanjinTest` / `.env.developmentHJ` 等环境变量文件。
