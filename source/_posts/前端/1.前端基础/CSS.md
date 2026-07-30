---
title: CSS 基本用法
date: 2022-12-25 11:42:00
tags:
- CSS
- 前端基础
categories:
- 前端
- 前端基础
---

# CSS 基本用法

层叠样式表（CSS）负责页面表现。本文涵盖常用属性速查、盒模型与 Flex 布局要点。

## 1. 显示类型 display

`display` 规定元素生成的框类型。

| 值 | 描述 |
| --- | --- |
| `none` | 不显示，用来隐藏元素 |
| `block` | 块级元素，前后带换行 |
| `inline` | 内联元素，前后无换行 |
| `inline-block` | 行内块元素 |
| `flex` / `grid` | 弹性 / 网格布局容器 |
| `table` 系列 | 以表格方式显示 |
| `inherit` | 继承父元素的值 |

## 2. 盒模型 box-sizing

`box-sizing` 决定 `width/height` 是否包含 padding 与 border。

```css
/* 推荐全局使用 border-box，尺寸更可控 */
*, *::before, *::after { box-sizing: border-box; }
```

- `content-box`（默认）：`width` 仅内容区，padding/border 在外。
- `border-box`：`width` 包含 content + padding + border。

## 3. 边框 border

`border` 简写：`border: 5px solid red;`。可拆为 `border-width` / `border-style`（必需）/ `border-color`。

- `border-radius`：圆角，如 `border-radius: 25px;`
- `border-style` 常用值：`none` / `solid` / `dashed` / `dotted` / `double`

```css
div { border: 2px solid; border-radius: 25px; }
```

## 4. 字体 font

`font` 简写顺序：`font-style font-variant font-weight font-size/line-height font-family`。

| 属性 | 说明 |
| --- | --- |
| `font-style` | 风格（`normal` / `italic`） |
| `font-weight` | 粗细（`normal`/`bold`/`100-900`） |
| `font-size` | 尺寸（`px`、相对单位、`%`） |
| `font-family` | 字体系列 |

## 5. 尺寸与间距

- `width` / `height`：内容区宽高；行内非替换元素忽略。
- `max-width`：最大宽度，常用于响应式约束。
- `margin`（外边距）/`padding`（内边距）均为 1~4 值：`上 右 下 左`（缺省对称取值）。
- `line-height`：行高，不允许负值。

```css
p { margin: 10px 5px 15px 20px; padding: 10px 5px; }
```

## 6. 溢出 overflow

`overflow` 规定内容溢出元素框时的处理：`visible`（默认）/ `hidden` / `scroll` / `auto`。

- `overflow-x` / `overflow-y`：单独控制水平/垂直方向裁剪，值含 `visible/hidden/scroll/auto/no-display/no-content`。

```css
div { width: 150px; height: 150px; overflow: auto; }
```

## 7. 定位与浮动

- `float: left/right`：元素左右浮动（经典多列布局手段，现代多用 Flex/Grid 替代）。
- 定位（`position`）：`static`（默认）/ `relative` / `absolute` / `fixed` / `sticky`，配合 `top/right/bottom/left` 与 `z-index`。

## 8. Flex 布局速记（现代首选）

```css
.container {
  display: flex;
  justify-content: center;   /* 主轴对齐 */
  align-items: center;       /* 交叉轴对齐 */
  flex-wrap: wrap;
}
.item { flex: 1; }            /* 等分剩余空间 */
```

## 参考

- [CSS display 元素显示类型](http://c.biancheng.net/css3/display.html)
- [css hover 用法](https://www.php.cn/css-tutorial-417948.html)
- [css ::before 用法](https://www.php.cn/css-tutorial-474802.html)
- [css opacity 不透明度](https://www.php.cn/css-tutorial-410372.html)
- [css 级联菜单](https://blog.csdn.net/LZGS_4/article/details/46490637)
