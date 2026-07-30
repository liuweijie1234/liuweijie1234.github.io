---
title: Python 文档入口
date: 2022-08-10 16:14:00
tags:
- Python
categories:
- Python
---

[Python 官方文档](https://docs.python.org/zh-cn/3/) | [Google Python 语言规范](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/)

## 目录结构

```
Python/
├── 基础语法/        三元运算、*args/**kwargs、深浅拷贝、错误异常、文件管理、正则、猴子补丁
├── 数据类型/        number、string、list、tuple、dict、set、queue
├── 内置函数/        高阶函数、lambda、自定义
├── 函数进阶/        闭包、装饰器、生成器和迭代器、单例
├── 标准库/          os、sys、time、datetime、json、csv、logging、itertools、pickle
├── 第三方库/        loguru、openpyxl、thriftpy2
├── 包管理器/        pip、conda、venv、virtualenv、poetry、uv
├── 并发编程/        进程、线程、协程、GIL、IO密集型与CPU密集型
├── 数据库/          pymysql、aiomysql、asyncpg、pymongo、motor、redis
├── 加密与编码/      MD5、base64、URL、Unicode
├── 算法与数据结构/  复杂度、数组、链表、哈希、二叉树、双指针、递归、动态规划、排序、查找
├── 爬虫/            请求、解析提取、自动化框架、爬虫框架、JS/APP逆向、验证码
├── 数据分析/        numpy、pandas、jieba
├── 性能与调优/      内存管理、性能优化、接口压测
├── 图形UI/          PyQt、turtle
├── 机器学习/
└── 实用案例/
```

## 基础语法

{% post_link Python/1.基础语法/三元运算 %}<br>
{% post_link Python/1.基础语法/args和kwargs的含义 %}<br>
{% post_link Python/1.基础语法/深浅拷贝 %}<br>
{% post_link Python/1.基础语法/错误异常 %}<br>
{% post_link Python/1.基础语法/文件管理 %}<br>
{% post_link Python/1.基础语法/正则re %}<br>
{% post_link Python/1.基础语法/猴子补丁 %}<br>

## 数据类型

{% post_link Python/2.数据类型/number %}<br>
{% post_link Python/2.数据类型/string %}<br>
{% post_link Python/2.数据类型/list %}<br>
{% post_link Python/2.数据类型/tuple %}<br>
{% post_link Python/2.数据类型/dict %}<br>
{% post_link Python/2.数据类型/set %}<br>
{% post_link Python/2.数据类型/queue %}<br>

## 内置函数

{% post_link Python/3.内置函数/Higher_order_functions %}<br>
{% post_link Python/3.内置函数/lambda %}<br>
{% post_link Python/3.内置函数/customize %}<br>

## 函数进阶

{% post_link Python/4.函数进阶/闭包 %}<br>
{% post_link Python/4.函数进阶/装饰器 %}<br>
{% post_link Python/4.函数进阶/生成器和迭代器 %}<br>
{% post_link Python/4.函数进阶/单例 %}<br>

## 标准库

{% post_link Python/6.标准库/os %}<br>
{% post_link Python/6.标准库/sys %}<br>
{% post_link Python/6.标准库/time %}<br>
{% post_link Python/6.标准库/datetime %}<br>
{% post_link Python/6.标准库/json %}<br>
{% post_link Python/6.标准库/csv %}<br>
{% post_link Python/6.标准库/logging %}<br>
{% post_link Python/6.标准库/itertools %}<br>
{% post_link Python/6.标准库/pickle %}<br>
{% post_link Python/6.标准库/other %}<br>

## 第三方库

{% post_link Python/7.第三方库/loguru %}<br>
{% post_link Python/7.第三方库/openpyxl %}<br>
{% post_link Python/7.第三方库/thriftpy2 %}<br>

## 包管理器

{% post_link Python/5.包管理器/pip %}<br>
{% post_link Python/5.包管理器/conda %}<br>
{% post_link Python/5.包管理器/venv %}<br>
{% post_link Python/5.包管理器/virtualenv %}<br>
{% post_link Python/5.包管理器/poetry %}<br>
{% post_link Python/5.包管理器/uv %}<br>

## 并发编程

{% post_link Python/9.并发编程/GIL全局解释器锁 %}<br>
{% post_link Python/9.并发编程/IO密集型和CPU密集型 %}<br>
{% post_link Python/9.并发编程/进程/multiprocessing %}<br>
{% post_link Python/9.并发编程/线程/threading %}<br>
{% post_link Python/9.并发编程/协程/asyncio %}<br>
{% post_link Python/9.并发编程/协程/gevent %}<br>

## 数据库

{% post_link Python/11.数据库/pymysql %}<br>
{% post_link Python/11.数据库/aiomysql %}<br>
{% post_link Python/11.数据库/asyncpg %}<br>
{% post_link Python/11.数据库/pymongo %}<br>
{% post_link Python/11.数据库/motor %}<br>
{% post_link Python/11.数据库/redis %}<br>

## 加密与编码

{% post_link Python/10.加密与编码/MD5 %}<br>
{% post_link Python/10.加密与编码/base64 %}<br>
{% post_link Python/10.加密与编码/URL %}<br>
{% post_link Python/10.加密与编码/Unicode %}<br>

## 算法与数据结构

{% post_link Python/8.算法与数据结构/时间复杂度 %}<br>
{% post_link Python/8.算法与数据结构/数组 %}<br>
{% post_link Python/8.算法与数据结构/链表 %}<br>
{% post_link Python/8.算法与数据结构/哈希 %}<br>
{% post_link Python/8.算法与数据结构/二叉树 %}<br>
{% post_link Python/8.算法与数据结构/双指针 %}<br>
{% post_link Python/8.算法与数据结构/递归 %}<br>
{% post_link Python/8.算法与数据结构/动态规划 %}<br>
{% post_link Python/8.算法与数据结构/排序/快排 %}<br>
{% post_link Python/8.算法与数据结构/查找/二分 %}<br>

## 爬虫

请求库：requests、urllib、httpx、aiohttp、curl_cffi、pyhttpx、tls_client、websocket 等（见 `爬虫/请求/`）

解析提取：xpath、lxml、bs4、parsel、pyquery（见 `爬虫/解析提取/`）

自动化：selenium、playwright、pyppeteer（见 `爬虫/自动化框架/`）

框架：{% post_link Python/13.爬虫/爬虫框架/Scrapy/readme %}<br>

## 数据分析

{% post_link Python/14.数据分析/numpy %}<br>
{% post_link Python/14.数据分析/pandas %}<br>
{% post_link Python/14.数据分析/jieba %}<br>

## 性能与调优

{% post_link Python/12.性能与调优/内存管理 %}<br>
{% post_link Python/12.性能与调优/性能优化 %}<br>
{% post_link Python/12.性能与调优/接口压测 %}<br>

## 实用案例

{% post_link Python/17.实用案例/shell_run_python_script %}<br>
{% post_link Python/17.实用案例/excel %}<br>
{% post_link Python/17.实用案例/BackupMySQLdata %}<br>
