---
title: React 知识地图
date: 2026-07-30 10:00:00
tags:
- React
- 框架
categories:
- 前端
- 框架
- React
---

# React 知识地图

React 是 Meta 开源的声明式 UI 库，以组件化、虚拟 DOM 与单向数据流为核心。当前主流为函数组件 + Hooks 开发范式。

## 专题索引

1. [环境搭建与工程化](1.环境搭建与工程化.md)
2. [JSX 与组件](2.JSX与组件.md)
3. [Hooks 详解](3.Hooks详解.md)
4. [状态管理](4.状态管理.md)
5. [路由 React Router](5.路由React%20Router.md)

## 关键速记

- **范式**：函数组件 + `Hooks`（取代 Class 组件生命周期）。
- **核心 Hook**：`useState`、`useEffect`、`useMemo`、`useCallback`、`useRef`、`useContext`。
- **工程化**：`npm create vite@latest`（选 react/react-ts 模板），或 CRA（已逐步淘汰）。
- **生态**：状态管理 Redux / Zustand；路由 React Router v6（`<Routes>/<Route>`、`useNavigate`）；UI 可配合 Element Plus 之外选择 Ant Design / MUI。
- **与 Vue3 对比**：响应式靠 `setState` 显式触发 vs Vue 自动依赖追踪；模板 JSX vs SFC 模板；`key` 复用机制、列表渲染、`ref` 转发等各有差异。
