---
title: NPM 使用教程
date: 2023-03-13 09:30:00
tags:
- NPM
categories:
- NPM
---

## npm 配置

- 初始化 package.json 文件

npm init


- 指定镜像源

npm install --registry=https://mirrors.tencent.com/npm/


- 设置环境变量

$ npm set init-author-name 'Your name'
$ npm set init-author-email 'Your email'
$ npm set init-author-url 'http://yourdomain.com'
$ npm set init-license 'MIT'

- 设置和取消代理

npm config set proxy=http://127.0.0.1:8087
npm config set registry=http://registry.npmjs.org

export http_proxy=http://127.0.0.1:12639
export https_proxy=http://127.0.0.1:12639

npm config set http_proxy=http://127.0.0.1:12639
npm config set https_proxy=http://127.0.0.1:12639

- 查看 npm 配置

npm config list -l

- 查看 npm 版本

npm -v

- 删除代理

npm config delete proxy
npm config delete https-proxy

npm config set registry http://r.npm.taobao.org/
npm config set registry https://mirrors.tencent.com/npm/

npm config delete registry

## 安装

- 升级到最新版本

npm install -g npm@latest


- 本地安装

```bash
$ npm install
$ npm install <package name>
$ npm install git://github.com/package/path.git
$ npm install git://github.com/package/path.git#0.1.0
```

- 全局安装
```bash
npm install -g @vue/cli
npm install -g @vue/cli-init
```
- 强制重新安装

```bash
$ npm install <packageName> --force
```

## 升级

- 升级当前项目的指定模块
$ npm update [package name]

- 升级全局安装的模块
$ npm update -global [package name]



## 查看

- 查看源版本

npm info jquery

- 查看安装版本

npm ls jquery


- 列出当前项目安装的所有模块，以及它们依赖的模块

npm list
npm list -global
npm list vue


## 卸载

$ npm uninstall [package name]

- 卸载全局模块

$ npm uninstall [package name] -global
