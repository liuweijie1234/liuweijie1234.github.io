---
title: Node.js 使用
date: 2023-03-13 09:30:00
tags:
- Node.js
- 前端基础
categories:
- 前端
- 前端基础
---

# Node.js 使用

Node.js 是基于 Chrome V8 引擎的 JavaScript 运行环境，让 JS 能脱离浏览器运行，是前端工程化（Vite、Webpack、各类 CLI）的基础。

## 1. 安装

- 官网下载：<https://nodejs.org/zh-cn/download>
- 教程参考：<https://www.runoob.com/nodejs/nodejs-install-setup.html>

> 开发前端项目（如 Vite）通常要求 Node 18+，否则可能报兼容错误。

## 2. 版本管理 nvm

推荐用 nvm 管理多版本 Node，避免全局版本冲突。

- Windows 版：<https://github.com/coreybutler/nvm-windows>，[安装教程](https://zhuanlan.zhihu.com/p/495053578)

### nvm 常用命令

| 命令 | 说明 |
| --- | --- |
| `nvm list` / `nvm list installed` | 显示已安装版本 |
| `nvm list available` | 显示可下载版本 |
| `nvm install 18.17.1` / `latest` | 安装指定/最新版本 |
| `nvm use 18.17.1` | 切换使用某版本 |
| `nvm uninstall 18.17.1` | 卸载指定版本 |
| `nvm on` / `nvm off` | 开启/关闭版本管理 |
| `nvm proxy [url]` | 设置下载代理（none 移除） |
| `nvm node_mirror [url]` | 设置 node 镜像 |
| `nvm npm_mirror [url]` | 设置 npm 镜像 |
| `nvm root [path]` | 设置版本存储目录 |
| `nvm version` / `nvm v` | 显示 nvm 版本 |

> Windows 下 `nvm install` 若提示无权限，请以管理员身份运行命令行。

## 3. 基本命令

```bash
node -v          # 查看 node 版本
node app.js      # 运行脚本
node             # 进入 REPL 交互
```

## 4. 模块系统

- **CommonJS**（Node 传统）：`require()` / `module.exports`。
- **ES Module**（现代，Node ≥ 14 稳定）：`import` / `export`，需在 `package.json` 设 `"type": "module"` 或使用 `.mjs` 后缀。

```js
// ESM
import fs from 'node:fs'
fs.writeFileSync('a.txt', 'hello')

// CommonJS
const fs = require('fs')
fs.writeFileSync('a.txt', 'hello')
```

## 5. 相关工具链

- 包管理：见 [npm 命令](npm命令.md)。
- 前端构建：Vite / Webpack 均依赖 Node 运行；详见 [Vue3 工程化](../框架/Vue3/1.环境搭建与Vite工程化.md)、[React 工程化](../框架/React/1.环境搭建与工程化.md)。
