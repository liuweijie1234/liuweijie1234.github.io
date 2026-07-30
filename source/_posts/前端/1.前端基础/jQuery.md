---
title: jQuery 基础
date: 2023-03-13 09:30:00
tags:
- jQuery
- js
- 前端基础
categories:
- 前端
- 前端基础
---

# jQuery 基础

> jQuery 是早期主流的 DOM 操作库，现代项目已被 Vue3 / React 取代。本文仅供**老项目维护**参考。

## 1. 引入与基本选择器

```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script>
  $('#id')        // id 选择
  $('.class')     // 类选择
  $('div')        // 标签选择
</script>
```

## 2. 动画方法 .slideDown() / .slideUp()

用于控制元素展开/折叠，参数 0 表示无过渡立即执行，300 表示 300ms 动画。

- `.slideDown(0)`：立即向下展开，无动画。
- `.slideDown(300)`：以 300ms 缓慢向下展开（带过渡效果）。
- `.slideUp(0)`：立即向上折叠。
- `.slideUp(300)`：以 300ms 缓慢向上折叠。

这些方法主要用于控制元素的展开/折叠动画，根据持续时间参数调整速度与过渡效果。

## 3. 按钮禁用与启用

HTML 中设置按钮禁用：

```html
<input type='button' id='test' value='disabled'>
```

jQuery 通过 `attr()` / `removeAttr()` 控制 `disabled` 属性：

```javascript
$('#test').attr('disabled', 'true');    // 添加 disabled 属性（禁用）
$('#test').removeAttr('disabled');      // 移除 disabled 属性（启用）
```

> 现代框架（Vue/React）中应使用数据状态控制 `:disabled` / `disabled`，而非手动操作 DOM。
