---
title: JavaScript 核心
date: 2023-03-13 09:30:00
tags:
- JavaScript
- 前端基础
categories:
- 前端
- 前端基础
---

# JavaScript 核心

JS 是前端的根基，本文梳理变量与类型、原型链、异步编程、事件循环、跨域与高频性能技巧（防抖/节流）。

## 1. 变量与类型

### 声明方式

- `var`：ES5 及之前，函数作用域/全局作用域，存在变量提升。
- `let`：ES6 引入，块级作用域，不提升（存在暂时性死区）。
- `const`：ES6 引入，块级作用域的常量，引用不可重新赋值（对象属性仍可改）。

优先使用 `const`，需要重新赋值时用 `let`，避免 `var`。

### 数据类型

- 基本类型：`undefined`、`null`、`boolean`、`number`、`string`、`symbol`（ES6）、`bigint`（ES2020）。
- 引用类型：`object`（含 `array`、`function`、`Date`、`RegExp` 等）。

> 基本类型按值存储，引用类型按引用（堆地址）存储；比较时基本类型比「值」，引用类型比「地址」。

## 2. 原型与原型链

- 每个函数都有 `prototype` 属性（显式原型），每个实例都有 `__proto__`（隐式原型）指向构造函数的 `prototype`。
- 访问属性时沿 `__proto__` 向上查找，形成「原型链」，直到 `Object.prototype.__proto__ === null`。
- `instanceof` 基于原型链判断；`Object.create(proto)` 可指定原型创建对象。

```js
function Person(name) { this.name = name }
Person.prototype.say = function () { console.log(this.name) }
const p = new Person('Tom')
p.say() // Tom，沿原型链找到 Person.prototype.say
```

## 3. 异步：Promise 与 async/await

- `Promise` 三种状态：`pending` → `fulfilled` / `rejected`，状态一旦改变不可逆转。
- `async` 函数返回 `Promise`，`await` 暂停执行直到 `Promise` 完成，用 `try/catch` 捕获异常。

```js
async function fetchUser(id) {
  try {
    const res = await fetch(`/api/user/${id}`)
    if (!res.ok) throw new Error('网络错误')
    return await res.json()
  } catch (e) {
    console.error(e)
  }
}
```

- 并发：`Promise.all([p1, p2])` 全成功才成功；`Promise.race` 取最先落地的结果；`Promise.allSettled` 等待全部落定。

## 4. 事件循环（Event Loop）

- 宏任务（macrotask）：`script`、`setTimeout`、`setInterval`、`I/O`、`setImmediate`。
- 微任务（microtask）：`Promise.then`、`MutationObserver`、`queueMicrotask`、`process.nextTick`（Node）。
- 执行顺序：同步代码 → 清空微任务队列 → 取一个宏任务 → 再清空微任务 …… 循环往复。

```js
console.log(1)
setTimeout(() => console.log(2), 0)
Promise.resolve().then(() => console.log(3))
console.log(4)
// 输出：1 4 3 2
```

## 5. 跨域与解决方案

浏览器同源策略：协议、域名、端口三者相同才同源。常见跨域方案：

- **CORS**：服务端设置 `Access-Control-Allow-Origin` 等响应头（最常用）。
- **JSONP**：利用 `<script>` 不受同源限制，仅支持 GET（逐步淘汰）。
- **代理**：开发用 Vite `server.proxy`，生产用 Nginx 反向代理，把跨域转为同源。
- **postMessage**：跨窗口/iframe 通信。

## 6. 防抖与节流

用于高频事件（输入、滚动、resize）性能优化。

- **防抖（debounce）**：停止触发 N 毫秒后才执行（如搜索联想）。

```js
function debounce(fn, wait = 300) {
  let t
  return (...args) => {
    clearTimeout(t)
    t = setTimeout(() => fn.apply(this, args), wait)
  }
}
```

- **节流（throttle）**：每隔 N 毫秒最多执行一次（如滚动加载）。

```js
function throttle(fn, wait = 300) {
  let last = 0
  return (...args) => {
    const now = Date.now()
    if (now - last >= wait) { fn.apply(this, args); last = now }
  }
}
```

## 参考

- [变量类型（jQuery 旧文整理）](JavaScript核心.md)
- 深入阅读建议：MDN JavaScript 指南、现代 JavaScript 教程（javascript.info）
