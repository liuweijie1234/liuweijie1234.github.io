---
title: 爬虫解析：XPath 语法与 lxml 使用
date: 2026-07-30 10:00:00
tags:
- Python
- 爬虫
categories:
- Python
---

## 说明

XPath 是在 XML/HTML 文档中定位节点的路径语言。Python 中通常配合 `lxml` 使用。

```bash
pip install lxml
```

## 常用语法速查

| 表达式 | 含义 |
| --- | --- |
| `/` | 从根节点选取（绝对路径） |
| `//` | 从任意位置选取后代节点 |
| `.` / `..` | 当前节点 / 父节点 |
| `@` | 选取属性，如 `//a/@href` |
| `*` | 任意元素，如 `//div/*` |
| `[n]` | 第 n 个（从 1 开始），如 `//li[1]` |
| `[last()]` | 最后一个 |
| `[@class="x"]` | 属性等于 |
| `[contains(@class, "x")]` | 属性包含 |
| `text()` | 文本节点，如 `//a/text()` |
| `\|` | 或，如 `//h1 \| //h2` |

## 基本使用

```python
from lxml import etree

html = """
<html><body>
  <ul class="menu">
    <li><a href="/a">首页</a></li>
    <li class="active"><a href="/b">新闻</a></li>
  </ul>
</body></html>
"""

tree = etree.HTML(html)                       # 自动修复不规范 HTML

# 提取所有链接文本和地址
tree.xpath("//ul[@class='menu']//a/text()")   # ['首页', '新闻']
tree.xpath("//ul[@class='menu']//a/@href")    # ['/a', '/b']

# 属性包含匹配
tree.xpath("//li[contains(@class, 'active')]/a/text()")   # ['新闻']

# 先取节点再相对查找（注意 ./ 开头）
for li in tree.xpath("//ul/li"):
    print(li.xpath("./a/text()"), li.xpath("./a/@href"))
```

## 常用技巧

```python
# string(.)：取节点下所有文本并拼接（处理文本被子标签分割的情况）
node = tree.xpath("//ul")[0]
node.xpath("string(.)")

# normalize-space：去除首尾空白
tree.xpath("normalize-space(//li[1])")

# 取兄弟节点
tree.xpath("//li[@class='active']/preceding-sibling::li")
tree.xpath("//li[@class='active']/following-sibling::li")
```

## 调试建议

- Chrome 开发者工具 Elements 面板 `Ctrl+F` 可直接测试 XPath。
- 右键元素 → Copy → Copy XPath 可快速获取（但生成的绝对路径较脆弱，建议手动改成基于 class/id 的相对路径）。
- 浏览器看到的 DOM 可能经过 JS 渲染，与 `requests` 拿到的源码不一致，以实际响应内容为准。
