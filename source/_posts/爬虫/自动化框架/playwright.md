---
title: Python3 爬虫 playwright
date: 2022-08-15 10:22:00
tags:
- [Python module]
- [爬虫]
- [playwright]
categories:
- Python
---

## 参考

python+playwright 合集 https://www.cnblogs.com/yoyoketang/tag/python%2Bplaywright/default.html

新兴动态渲染工具 Playwright 的使用 https://cuiqingcai.com/202262.html


## 简介

Playwright 是一款开源的自动化测试工具，它可以让你轻松地编写高效、可靠的自动化测试。
它支持多种浏览器，包括 Chromium、Firefox、WebKit，并且提供了一系列 API 来操纵浏览器、捕获屏幕截图、截取元素、生成 PDF 等。

特点:

- 安装和配置非常简单，安装过程中会自动安装对应的浏览器和驱动，不需要额外配置 WebDriver 等。
- Playwright 支持多种浏览器, 包括 Chrome 和 Edge（基于 Chromium）、Firefox、Safari（基于 WebKit）
- Playwright 支持移动端页面测试，使用设备模拟技术可以使我们在移动 Web 浏览器中测试响应式 Web 应用程序。
- 支持所有浏览器的 Headless 模式和非 Headless 模式的测试。
- 提供了自动等待相关的 API，当页面加载的时候会自动等待对应的节点加载，大大简化了 API 编写复杂度。


## 安装

要使用 Playwright，需要 Python 3.7 版本及以上，请确保 Python 的版本符合要求。

要安装 Playwright，可以直接使用 pip3，命令如下：

```python
pip3 install playwright
```

安装完成之后需要进行一些初始化操作：

```python
playwright install
```


这时候 Playwrigth 会安装 Chromium, Firefox and WebKit 浏览器并配置一些驱动，我们不必关心中间配置的过程，Playwright 会为我们配置好。

具体的安装说明可以参考：https://setup.scrape.center/playwright。

安装完成之后，我们便可以使用 Playwright 启动 Chromium 或 Firefox 或 WebKit 浏览器来进行自动化操作了。