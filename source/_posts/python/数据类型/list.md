---
title: Python3 list 常用方法
date: 2022-07-04 16:12:53
tags: 
- Python
- python 列表
categories:
- Python
---

## list 介绍

列表是 Python 中最常用的数据类型

Python 中的数组叫做 list

列表可以进行的操作包括 索引、切片、加、乘、检查成员。


切片 list[0:9]

## 索引和负索引



- 索引从 0 开始，-1 表示最后一个元素，-2 表示倒数第二个元素，以此类推。

## 内置函数


- len(list)：列表元素个数
- max(list)：返回列表元素最大值
- min(list)：返回列表元素最小值
- list(tuple)：将元组转换为列表

## 内置方法

### 常用方法

#### list.append(obj)

- 作用

在列表末尾添加新的对象

#### list.extend(seq)

- 作用

在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）类似 `+=`


#### list.insert(index, obj)

- 作用

将指定对象插入列表的指定位置。


#### list.count(obj)

- 作用

统计某个元素在列表中出现的次数


#### list.index(obj)

- 作用

从列表中找出某个值第一个匹配项的索引位置

- 语法
```python
list.index(x[, start[, end]])
```
x-- 查找的对象。
start-- 可选，查找的起始位置。
end-- 可选，查找的结束位置。


#### list.sort( key=None, reverse=False)

- 作用

对原列表进行排序

- 语法

key -- 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
reverse -- 排序规则，reverse = True 降序， reverse = False 升序（默认）。


> 注意：sort 和 sorted
> sort 是列表独有的


#### list.reverse()

- 作用

反向列表中元素

### 其他方法

#### list.pop([index=-1])

- 作用

移除列表中的一个元素（默认最后一个元素），并且返回该元素的值

#### list.remove(obj)

- 作用

移除列表中某个值的第一个匹配项

#### list.clear()

- 作用

清空列表

#### list.copy()

- 作用

复制列表


## 类型转换

list() 方法用于将元组或字符串转换为列表。

注：元组与列表是非常类似的，区别在于元组的元素值不能修改，元组是放在括号中，列表是放于方括号中。

## 嵌套列表 转 字典(dict)

- dict

```python
list1 = [['id', '1'], ['name', 'admin'], ['ip', '10.0.0.1']]
dict1 = dict(list1)
print(dict1)
```

- 遍历

```python
list2 = [['id', '1'], ['name', 'admin'], ['ip', '10.0.0.1']]
dict2 = {}
for i in list2:
    dict2[i[0]] = i[1]
print(dict2)
```

## 两个列表 转 字典(zip函数，dict函数)

```python
keys = ['id', 'name', 'ip']
values = ['1', 'admin', '10.0.0.1']
dictionary = dict(zip(keys, values))
print(dictionary)
```

## 特殊列表 转 字典(列表推导式，zip函数，dict函数)

```python
keys1 = ['id', 'name', 'pwd']
values1 = [[2, '123', '567'], [3, '456', '899']]
a = [dict(zip(keys1, row)) for row in values1] if values1 else None
print(a)
```


## 拷贝

### 浅拷贝

```python
fruits = ['apple', 'banana', 'orange']
big_fruits = [fruits,fruits,fruits]
print(big_fruits)

输出：
[['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange']]

fruits.append('mongo')
print(big_fruits)

输出：
[['apple', 'banana', 'orange', 'mongo'],
 ['apple', 'banana', 'orange', 'mongo'],
 ['apple', 'banana', 'orange', 'mongo']]
```

### 深拷贝

```python
fruits = ['apple', 'banana', 'orange']
big_fruits = [list(fruits),list(fruits),list(fruits)]
print(big_fruits)

输出：
[['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange']]

fruits.append('mongo')
print(big_fruits)

输出：
[['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange']]

print(big_fruits[1][2])
输出：orange

big_fruits[1][2] = 'strawberry'
print(big_fruits)

输出：
[['apple', 'banana', 'orange'],
 ['apple', 'banana', 'strawberry'],
 ['apple', 'banana', 'orange']]
```



## 列表推导式


```python
fruits = ['apple', 'banana', 'orange']
big_fruits = [list(fruits) for i in range(3)]
print(big_fruits)
```

```bash
输出：
[['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange'],
 ['apple', 'banana', 'orange']]
```

```python
a = [i for i in range(10) if i%2 == 0]
print(a)
```

```bash
输出：[0, 2, 4, 6, 8]
```
