---
title: Python3 集合 常用方法
date: 2022-07-04 16:14:00
tags:
- Python
- python 集合
categories:
- Python
---

集合（set）是一个无序的不重复元素序列。

> 集合一般用于去重，其他地方我很少用到，可能是我菜了


```python
s1 = set(range(3))
s2 = set(range(2,5))
print(s1,s2)
# {0, 1, 2} {2, 3, 4}
print(s1 & s2)
# {2}
print(s1 | s2)
# {0, 1, 2, 3, 4}
print(s1 - s2)
# {0, 1}
print(s1 ^ s2)
# {0, 1, 3, 4}
```

## 集合推导式

待补充

## 内置方法


### add()

为集合添加元素

### update()

给集合添加元素

### clear()

移除集合中的所有元素

### pop()

随机移除元素

### remove()

移除指定元素

### copy()
拷贝一个集合

### difference()

返回多个集合的`差集`

### difference_update()

移除集合中的元素，该元素在指定的集合也存在。

### discard()

删除集合中指定的元素

### intersection()

返回集合的`交集`。可以使用 `&`

### intersection_update()

返回集合的交集，原始的集合上移除不重叠的元素。

### isdisjoint()

判断两个集合是否包含相同的元素，如果没有返回 True，否则返回 False。

### issubset()

判断指定集合是否为该方法参数集合的子集。

### issuperset()

判断该方法的参数集合是否为指定集合的子集


### symmetric_difference()

返回两个集合中不重复的元素集合。对称差集


### symmetric_difference_update()

移除当前集合中在另外一个指定集合相同的元素，并将另外一个指定集合中不同的元素插入到当前集合中。

### union()

返回两个集合的`并集`，可以使用 `|`


[菜鸟教程-集合](https://www.runoob.com/python3/python3-set.html)


## 类型转换


# str-list-tuple

```python
a_string = "abcdef"
print(f'a_string:{a_string}')

输出：a_string:abcdef

a_list = list(a_string)
print(f'a_list:{a_list}')

输出：a_list:['a', 'b', 'c', 'd', 'e', 'f']

a_tuple = tuple(a_list)
print(f'a_tuple:{a_tuple}')

输出：a_tuple:('a', 'b', 'c', 'd', 'e', 'f')

a = ''.join(a_tuple)
print(f'a:{a}')

输出：a:abcdef

for index, char in enumerate(a_string):
    print((index, char),end=" ")

输出：(0, 'a') (1, 'b') (2, 'c') (3, 'd') (4, 'e') (5, 'f')

for index, element in enumerate(a_list, 1):
    print((index, element),end=" ")

输出：(1, 'a') (2, 'b') (3, 'c') (4, 'd') (5, 'e') (6, 'f')

for index, element in enumerate(a_tuple, 11):
    print((index, element),end=" ")

输出：(11, 'a') (12, 'b') (13, 'c') (14, 'd') (15, 'e') (16, 'f')

```