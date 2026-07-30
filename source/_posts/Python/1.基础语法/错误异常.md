---
title: Python3 错误和异常
date: 2022-08-15 10:14:00
tags:
- Python
categories:
- Python
---
##  错误处理

Python 中也提供了 try...except...finally...的错误处理机制：

```python
try:
    r = 10 / 0
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
```

如果 try 中没有错误出现，则 except 中语句不会被执行，而如果有 finally，则一定会执行。可以通过 except 来捕捉不同类型的错误，捕捉后则会执行相应的逻辑。

可以通过 Pyhton 内置的 logging 来记录错误信息：

```python
# err_logging.py

import logging

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)

main()
```

在 Python 中，可以通过 raise 来抛出错误：

```python
if n==0:
        raise FooError('invalid value: %s' % s)
```



[Python 输出详细的异常信息(traceback)方式](https://cloud.tencent.com/developer/article/1731086)
```python
import traceback

traceback.format_exc()
```