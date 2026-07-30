---
name: 前端文档体系重组方案
overview: 将零散的 source/_posts/前端 目录重组成「框架(Vue3/React) / UI库(Element Plus) / 前端基础 / 项目实战」知识树，全部重写为高质量文档，并新建 React 与 Element Plus 内容。
todos:
  - id: build-skeleton
    content: 创建新目录骨架与总导航 readme 及各模块 readme 索引
    status: completed
  - id: reorg-basics
    content: 整合重写前端基础模块（JS/CSS/Node/npm/WebSocket/jQuery/加密混淆）并补 front-matter
    status: completed
    dependencies:
      - build-skeleton
  - id: reorg-vue3
    content: 整合 vue_install 并撰写框架/Vue3 六篇核心文档
    status: completed
    dependencies:
      - build-skeleton
  - id: author-react
    content: 原创撰写框架/React 六篇文档（环境/JSX/Hooks/状态/路由）
    status: completed
    dependencies:
      - build-skeleton
  - id: author-elementplus
    content: 将 ElementUI 改写为 Element Plus 并撰写 UI库 五篇文档
    status: completed
    dependencies:
      - build-skeleton
  - id: finalize-links
    content: 补全项目实战 front-matter，校验全站相对链接，git 暂存整体变更
    status: completed
    dependencies:
      - reorg-basics
      - reorg-vue3
      - author-react
      - author-elementplus
---

## 用户需求

作为精通 Vue3 + React 的高级前端工程师与文档整理者，对 `source/_posts/前端` 目录进行全面重组并撰写内容：以「框架（Vue3 / React）+ UI 库（Element Plus）」为主线重构知识树，同时保留并归整前端基础与项目实战。

## 产品概述

将原本零散、分类不统一的扁平 Markdown 文档，重组成结构清晰、带 Hexo front-matter 与相对链接导航的层级化技术文档站点。所有文档可全部重写，React 与 Element Plus 内容由高级工程师视角原创撰写。

## 核心特性

- 重组目录为「框架 / UI库 / 前端基础 / 项目实战」四大模块，顶层保留总导航 readme.md
- 框架模块：Vue3（环境工程化、响应式与 Composition API、组件通信与生命周期、Vue Router、Pinia、axios 封装）；React（环境工程化、JSX 与组件、Hooks、状态管理、React Router）
- UI 库模块：Element Plus（原 Vue2 的 ElementUI 改写为 Vue3 版，含安装、Form 校验、Table 分页、主题定制与按需引入）
- 前端基础模块：整合 JavaScript 核心、CSS、Node.js、npm 命令、WebSocket、网站加密混淆、jQuery 等现有零散文档
- 每篇统一 front-matter（title/date/tags/categories 层级标签），内部链接全部改用相对路径，总 readme 做模块索引
- 项目实战保留并补全 front-matter；完成后整体 git 暂存（不改动 _config.yml 与主题配置）

## 技术栈与约定

- 站点类型：Hexo 静态博客（`source/_posts` 下 Markdown 即文章）
- 文件规范：每篇需 front-matter，含 `title`、`date`、`tags`、`categories`（层级数组，如 `["前端","框架","Vue3"]`）
- 链接规范：站内引用统一使用相对路径（如 `../框架/Vue3/1.环境搭建与Vite工程化.md`），沿用此前「数据库」重命名时建立的相对路径与 git 暂存模式
- 不动 `_config.yml`、主题（`themes/`）及任何站点级配置

## 实现方案

- 策略：先建目录骨架与总导航，再分模块整合旧文（css/nodejs/npm/websocket/JavaScript/jQuery/MiXed/vue_install/ElementUI）到新结构，最后原创撰写缺失的 React 与 Element Plus 内容。
- 关键决策：

1. 采用「框架 / UI库 / 前端基础 / 项目实战」四顶层，与 readme 大纲（Vue3 核心、Element Plus 工程化、前端基础）对齐，扩展性强。
2. ElementUI.md 整体重写为 Element Plus（Vue3），保留少量 Vue2 对比说明，满足用户「改为 Element Plus」要求。
3. React 全套原创撰写，不依赖仓库既有内容。

- 性能与可靠性：链接采用相对路径并批量校验可达性（python 校验脚本），避免 Hexo 构建时报坏链；旧文件删除前内容已并入新文件，不丢稿。

## 实现注意

- 旧文件整合时保留原有技术要点，避免内容丢失（尤其 MiXed 的加密混淆、websocket 的 Vue 用法）。
- 全站相对链接需按新目录深度修正（框架/Vue3 下引用前端基础需 `../../前端基础/...`）。
- 完成用 `git add -A source/_posts/前端` 暂存重命名 + 新增；不提交（plan 仅到暂存）。

## 架构设计

扁平散文件 → 层级模块（总导航 readme 索引到 框架/UI库/前端基础/项目实战，各模块含 readme 知识地图 + 专题文档）。沿用既有 Hexo 渲染链路，无需新增架构模式。

## 目录结构

```
source/_posts/前端/
├── readme.md                         # [MODIFY] 总导航大纲，重写为模块索引，相对链接到各子模块
├── 框架/
│   ├── Vue3/
│   │   ├── readme.md                 # [NEW] Vue3 知识地图与索引
│   │   ├── 1.环境搭建与Vite工程化.md  # [NEW] 整合 vue_install + Vite 工程化
│   │   ├── 2.响应式原理与Composition API.md # [NEW] Proxy/响应式/setup
│   │   ├── 3.组件通信与生命周期.md    # [NEW] props/emit/provide/生命周期
│   │   ├── 4.路由VueRouter与路由守卫.md # [NEW] 路由与守卫
│   │   ├── 5.状态管理Pinia.md         # [NEW] Pinia 用法
│   │   └── 6.网络请求axios封装.md      # [NEW] axios 拦截器封装
│   └── React/
│       ├── readme.md                 # [NEW] React 知识地图
│       ├── 1.环境搭建与工程化.md       # [NEW] Vite+React 工程化
│       ├── 2.JSX与组件.md             # [NEW] JSX/函数组件/Class组件
│       ├── 3.Hooks详解.md             # [NEW] useState/useEffect 等
│       ├── 4.状态管理.md              # [NEW] Redux/Zustand
│       └── 5.路由ReactRouter.md       # [NEW] React Router v6
├── UI库/
│   └── Element Plus/
│       ├── readme.md                 # [NEW] 组件库地图
│       ├── 1.安装与快速上手.md        # [NEW] 改写自 ElementUI.md(Vue3版)
│       ├── 2.表单Form与校验.md        # [NEW] Form 校验规则
│       ├── 3.表格Table与分页.md       # [NEW] Table 与分页
│       └── 4.主题定制与按需引入.md    # [NEW] 主题/自动导入
├── 前端基础/
│   ├── readme.md                     # [NEW] 基础模块索引
│   ├── JavaScript核心.md             # [NEW] 整合原型/Promise/async/跨域/防抖节流
│   ├── CSS.md                        # [NEW] 整合 css.md
│   ├── Node.js.md                    # [NEW] 整合 nodejs.md
│   ├── npm命令.md                    # [NEW] 整合 npm_command.md
│   ├── WebSocket.md                  # [NEW] 整合 websocket.md
│   ├── 网站加密与混淆技术.md          # [NEW] 整合 MiXed.md
│   └── jQuery.md                     # [NEW] 整合 JavaScript/jQuery.md
└── 项目实战/
    └── 韩进new-freight.md            # [MODIFY] 补全 front-matter(categories: 前端/项目实战)

# 删除旧文件（内容已并入新结构）：
#   vue_install.md、ElementUI.md、css.md、nodejs.md、websocket.md、npm_command.md
#   JavaScript/jQuery.md、JavaScript/MiXed.md、JavaScript/ 目录
```