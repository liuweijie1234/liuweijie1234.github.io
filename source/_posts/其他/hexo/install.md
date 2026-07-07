---
title: hexo 入门与使用
date: 2022-07-01 16:27:10
tags: hexo
categories: hexo
---

## 用 hexo 搭建博客

个人通过使用以下工具来实现个人博客搭建

1、hexo（框架）： [文档入口](https://hexo.io/zh-cn/docs/)
2、next（主题）： [文档入口](https://theme-next.js.org/)
3、github pages（服务）： [文档入口](https://docs.github.com/cn/pages)


## 本地部署

### 安装环境

- 安装框架依赖
  - 安装 git、node.js
    [git 安装文档](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)
    [Node.js 安装文档](https://nodejs.org/zh-cn/)
    一般安装 node.js 默认安装 npm

  - 查看版本
   ```bash
   git --version
   node -v
   npm -v
   ```

- 安装 框架
  - 安装 hexo（mac 需要切换权限 `sudo -s`）
   ```bash
   npm install -g hexo-cli
   npm install -g hexo
   ```
  - 添加环境变量
   将 Hexo 所在的目录下的 node_modules 添加到环境变量之中即可直接使用 hexo <command>：
   ```bash
   echo 'PATH="$PATH:./node_modules/.bin"' >> ~/.profile
   ```

### 新建博客

```bash
## hexo init <folder> 在指定文件夹中新建所需要的文件
hexo init liuweijie1234.github.io

cd liuweijie1234.github.io/

npm install

# 生成静态文件，简写 hexo g
hexo generate
# 启动服务器。默认情况下，访问网址为： http://localhost:4000/。简写 hexo s
hexo server
```

这样本地一个 demo 博客就启动了，下面讲 【基本知识】 和 【hexo 使用】怎么修改主题、写文章 并部署到 gitHub。

## 基本知识和命令

### 基本知识

文件及其作用 可以[参考：--文件解释--](https://hexo.io/zh-cn/docs/setup#config-yml)

重点关注 `_config.yml`，这是博客的配置信息，可以配置大部分的参数，可以[参考：--配置详解--](https://hexo.io/zh-cn/docs/configuration)

`source`，是你存放文章的地方


`themes`，是主题文件夹，一般下载主题至该文件。
实例命令：
```bash
git clone https://github.com/next-theme/hexo-theme-next themes/next-theme
```

### 常用命令

[参考：--命令详解--](https://hexo.io/zh-cn/docs/commands)

- new（新建文章）

布局默认使用 _config.yml 中的 `default_layout: post`，默认在`source/_posts`创建文章，

```bash
$ hexo new [布局] -p 文章路径 <文章标题>

# 示例，创建 source/_posts/python/dict.md
hexo new -p python/dict "Python dict使用"
```

- generate(生成静态文件并部署)

```bash
# 生成静态文件，文件生成后立即部署网站
hexo generate --deploy
```
常用简写来部署到 github

```bash
hexo g -d

## 等效于
hexo deploy -g 或 hexo d -g
```

- server

```bash
启动服务器
hexo server
```
常用简写
```bash
hexo s
```

常跟清除缓存文件`hexo clean` 结合使用，来本地预览

```bash
hexo clean & hexo server
```

- version

显示 Hexo 版本
```bash
hexo version
```

## 修改主题

- 下载主题
```bash
cd liuweijie1234.github.io/

git clone https://github.com/next-theme/hexo-theme-next themes/next-theme
```

- 修改主题配置
打开 _config.yml 文件，将主题修改为 next-theme

```yaml
theme: next-theme
```

- 本地测试
`hexo clean && hexo server`

## 部署至 github pages

- 安装 hexo-deployer-git

```bash
npm install hexo-deployer-git --save
```

- 修改配置

修改根目录下的 `_config.yml`，配置 GitHub 相关信息

```yaml
deploy:
  type: git
  repo: https://github.com/liuweijie1234/liuweijie1234.github.io
  branch: main
  token: xxxxxxxxxxxxxxxxxxxxxx
  name: liuweijie1234
```
其中 token 为 GitHub 的 [Personal access tokens](https://docs.github.com/cn/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

- 部署

`hexo g -d`

## 主题配置

[参考 theme-next 官方文档](https://theme-next.js.org/)