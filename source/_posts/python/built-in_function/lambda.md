---
title: Python3 lambda
date: 2022-08-13 16:14:00
tags:
- Python
categories:
- Python
---




```python
from functools import reduce

a = [0, 1, 2, 3, 4, 5]

filter_result = list(filter(lambda x: x % 2 == 0, a))
map_result = list(map(lambda x: x ** x, a))
reduce_result = reduce(lambda a, b :a + b, a, 0)
print('filter_result: %s, \nmap_result: %s, \nreduce_result: %s'%(filter_result, map_result, reduce_result))
```