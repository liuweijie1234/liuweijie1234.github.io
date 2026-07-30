---
title: Python3 *args 和 **kwargs 的含义
date: 2026-07-30 10:00:00
tags:
- Python
categories:
- Python
---

## 含义

- `*args`：接收任意数量的**位置参数**，在函数内部是一个 `tuple`。
- `**kwargs`：接收任意数量的**关键字参数**，在函数内部是一个 `dict`。
- `args`、`kwargs` 只是约定俗成的名字，起作用的是 `*` 和 `**`。

## 基本用法

```python
def demo(*args, **kwargs):
    print(args)    # 元组
    print(kwargs)  # 字典

demo(1, 2, 3, a=4, b=5)
# (1, 2, 3)
# {'a': 4, 'b': 5}
```

## 参数顺序

定义函数时参数顺序必须是：

```python
def func(位置参数, *args, 关键字参数=默认值, **kwargs):
    ...

def func(a, b, *args, c=10, **kwargs):
    print(a, b, args, c, kwargs)

func(1, 2, 3, 4, c=5, d=6)
# 1 2 (3, 4) 5 {'d': 6}
```

## 解包（调用时使用 * 和 **）

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
add(*nums)          # 等价于 add(1, 2, 3)

params = {"a": 1, "b": 2, "c": 3}
add(**params)       # 等价于 add(a=1, b=2, c=3)
```

## 典型应用场景

```python
# 1. 装饰器中透传参数
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"call {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# 2. 子类调用父类构造方法时透传
class Child(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# 3. 合并字典（Python 3.5+）
d1, d2 = {"a": 1}, {"b": 2}
merged = {**d1, **d2}   # {'a': 1, 'b': 2}
```
