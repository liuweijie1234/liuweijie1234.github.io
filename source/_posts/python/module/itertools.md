---
title: Python3 模块 itertools
date: 2022-08-15 10:22:00
tags:
- Python module
- itertools
categories:
- Python
---


## 高效切片

```python
from itertools import islice

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

mail_limit1000_list = list(chunk(mail_list, 1000))
```