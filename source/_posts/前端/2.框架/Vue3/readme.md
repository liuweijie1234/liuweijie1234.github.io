---
title: Vue3 知识地图
date: 2026-07-30 10:00:00
tags:
- Vue3
- 框架
categories:
- 前端
- 框架
- Vue3
---

# Vue3 知识地图

Vue3 是渐进式 JavaScript 框架，核心特性：基于 `Proxy` 的响应式系统、Composition API、更好的 TypeScript 支持与编译期优化（静态提升、PatchFlag）。

## 专题索引

1. [环境搭建与 Vite 工程化](1.环境搭建与Vite工程化.md)
2. [响应式原理与 Composition API](2.响应式原理与Composition%20API.md)
3. [组件通信与生命周期](3.组件通信与生命周期.md)
4. [路由 Vue Router 与路由守卫](4.路由Vue%20Router与路由守卫.md)
5. [状态管理 Pinia](5.状态管理Pinia.md)
6. [网络请求 axios 封装](6.网络请求axios封装.md)

## 关键速记

- **响应式**：`ref`（基本类型/对象）、`reactive`（对象）、`computed`、`watch`/`watchEffect`。
- **组合式**：`<script setup>` 语法糖，无需 `return`，顶层绑定自动暴露给模板。
- **工程化**：`npm init vue@latest`（create-vue 脚手架），内置 Vite、Router、Pinia、ESLint、Vitest 选项。
- **与 Vue2 差异**：`Object.defineProperty` → `Proxy`；`Options API` 与 `Composition API` 并存；`v-model` 支持多个；`.sync` 移除。
