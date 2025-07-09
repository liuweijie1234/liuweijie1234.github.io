---
title: Python3 性能优化
date: 2022-07-04 16:14:00
tags:
- Python
- 优化
categories:
- Python
---


1.数据结构一定要选对 能用字典就不用列表：字典在索引查找和排序方面远远高于列表。
2.多用python中封装好的模块库关键代码使用外部功能包（Cython，pylnlne，pypy，pyrex）
3.使用生成器
4.针对循环的优化 尽量避免在循环中访问变量的属性


###  递归函数

先看一个简单的 demo：

```python
def fac(n):
"""
求阶乘
"""
  if n == 1:
    return n
  return n * fac(n-1)
```

使用递归函数需要注意防止栈溢出，每当进入一个函数调用，栈就会加一层栈帧，每当函数返回就会减一层栈帧，栈的大小不是无限的，所以当递归调用次数过多，就会导致栈溢出(maximum recursion depth exceeded in comparison)。

解决溢出的办法是通过尾递归优化，尾递归是指在函数返回的时候，调用自身本身，并且 return 语句不能包含表达式。这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧。

```python
def fac(n):
  return fac_iter(n, 1)

def fac_iter(n, res):
  if n == 1:
    return res
  return fac_iter(n - 1, n * res)
```

需要注意的是 Pyhon 标准的解释器没有针对尾递归做优化，任何递归函数都存在栈溢出的问题。

