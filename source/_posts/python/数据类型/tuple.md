---
title: Python3 元组 常用方法
date: 2022-07-04 16:14:00
tags:
- Python
- python 元组
categories:
- Python
---

元组与列表类似，不同之处在于元组的元素不能修改，但是子元素是可以修改的

元组使用小括号 `( )`

元组可以进行的操作包括 索引、切片、加(形成新的元组)、乘、删(删除整个元组)、检查成员(in)。


```python
a_tuple = ('physics', 'chemistry', 1997, 2000, [])
a_tuple[-1].append(1)
print(a_tuple)
# ('physics', 'chemistry', 1997, 2000, [1])
```