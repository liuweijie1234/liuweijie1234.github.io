---
title: Python3 模块 sys
date: 2022-08-15 10:22:00
tags:
- Python module
- sys
categories:
- Python
---


## sys
sys 模块提供了一系列有关 Python 运行环境的变量和函数

sys.argv     命令行参数 List, 第一个元素是程序本身路径
sys.exit(n)  退出程序，正常退出时 exit(0)
sys.version  获取 Python 解释程序的版本信息
sys.maxint   最大的 Int 值
sys.path     返回模块的搜索路径，初始化时使用的 PYTHONPATH 环境变量的值
sys.platform 返回操作系统平台名称
sys.stdout.write('please')
val = sys.stdin.readline()[:-1]