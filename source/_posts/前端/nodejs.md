---
title: Node.js 使用
date: 2023-03-13 09:30:00
tags:
- Node.js
categories:
- Node.js
---

## 安装

### nodejs 安装

https://nodejs.org/zh-cn/download

https://www.runoob.com/nodejs/nodejs-install-setup.html

### nodejs 管理工具

[nvm安装（Windows篇）](https://zhuanlan.zhihu.com/p/495053578)

https://github.com/coreybutler/nvm-windows

#### nvm 常用命令

1. nvm list - 显示版本列表

nvm list ：显示已安装的版本（同 nvm list installed
nvm list installed：显示已安装的版本
nvm list available：显示所有可以下载的版本

2. nvm install - 安装指定版本nodejs

nvm install 18.17.1：安装 18.17.1 版本的 node.js
nvm install latest：安装最新版本

3. nvm use - 使用指定版本node

nvm use 18.17.1： 切换到 18.17.1 版本的 node.js

4. nvm uninstall - 卸载指定版本 node

nvm uninstall 18.17.1：卸载到 18.17.1 版本的 node.js

[ ps：在运行nvm install 的时候，有可能会出现无权限安装的问题，请 以管理员身份运行 cmd ]

5. 其他命令

nvm arch ：
显示node是运行在32位还是64位系统上的

nvm on ：
开启nodejs版本管理

nvm off ：
关闭nodejs版本管理

nvm proxy [url] ：
设置下载代理，不加可选参数url，显示当前代理；将 url 设置为 none 则移除代理。

nvm node_mirror [url] ：
设置node镜像。默认是http://nodejs.org/dist/，如果不写url，则使用默认url；设置后可至安装目录settings.txt文件查看，也可直接在该文件操作。

nvm npm_mirror [url] ：
设置npm镜像，http://github.com/npm/cli/arc… 如果不写url，则使用默认url；设置后可至安装目录 settings.txt文件查看，也可直接在该文件操作

nvm root [path] ：
设置存储不同版本node的目录，如果未设置，默认使用当前目录

nvm version ：

显示 nvm 版本，version 可简化为 v



## 基本命令

- 查看node版本

node -v


## npm 使用

{% post_link vue/npm_command %}