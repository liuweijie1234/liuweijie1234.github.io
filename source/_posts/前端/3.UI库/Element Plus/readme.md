---
title: Element Plus 组件库地图
date: 2026-07-30 10:00:00
tags:
- Element Plus
- UI库
- Vue3
categories:
- 前端
- UI库
- Element Plus
---

# Element Plus 组件库地图

Element Plus 是 Vue3 的桌面端组件库（原 Vue2 的 Element UI 继任者），提供丰富的表单、表格、弹窗、导航等中后台常用组件。

官方文档：<https://element-plus.org/zh-CN/>

## 专题索引

1. [安装与快速上手](1.安装与快速上手.md)
2. [表单 Form 与校验](2.表单Form与校验.md)
3. [表格 Table 与分页](3.表格Table与分页.md)
4. [主题定制与按需引入](4.主题定制与按需引入.md)

## 关键速记

- **安装**：`npm i element-plus`，配合 `@element-plus/icons-vue` 使用图标。
- **完整引入**：`app.use(ElementPlus)`；**按需引入**：`unplugin-auto-import` + `unplugin-vue-components`。
- **Vue2 → Vue3 变化**：`el-dialog` 的 `:visible.sync` 改为 `v-model`；`this.$message` 改为 `import { ElMessage }`；事件绑定由 `@` 统一。
- **常用组件**：`el-form/el-form-item`、`el-table/el-table-column`、`el-pagination`、`el-dialog`、`el-menu`、`el-upload`。
