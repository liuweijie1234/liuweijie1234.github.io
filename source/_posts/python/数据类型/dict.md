---
title: Python3 dict 常用方法
date: 2022-07-04 16:14:00
tags:
- Python
- python 字典
categories:
- Python
---

[Python 官方文档](https://docs.python.org/zh-cn/3/)

[官方文档-字典](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)


`字典名 == { 键值对 }`

## 字典特性

1. 不允许同一个键出现两次。创建时如果同一个键被赋值两次，后一个值会被记住。
2. 键必须不可变，所以可以用数字，字符串或元组充当


## 内置函数

- type()：返回输入的变量类型，如果变量是字典就返回字典类型。

```python
>>> tel = {'jack': 4098, 'sape': 4139}
>>> type(tel)
<class 'dict'>
```

- len()：计算字典元素个数，即键的总数。

```python
>>> tel = {'jack': 4098, 'sape': 4139}
>>> len(tel)
2
```

- str()：输出字典，可以打印的字符串表示。

```python
>>> tel = {'jack': 4098, 'sape': 4139}
>>> str(tel)
"{'jack': 4098, 'sape': 4139}"
```

- list()：返回该字典中所有键的列表

```python
>>> tel = {'jack': 4098, 'sape': 4139}
>>> list(tel)
['jack', 'sape']
```

## 内置方法

### 字典推导式

```python
>>> {x: x**2 for x in (2, 4, 6)}
{2: 4, 4: 16, 6: 36}
```

### 常用方法


#### dict.get(key[, value])

- 作用

用于返回指定 key 的值，如果值不在字典中返回默认值

- 语法

key -- 字典中要查找的键。
value -- 可选，如果指定键的值不存在时，返回该默认值。

- `get()` 方法 与 `dict[key]` 访问元素 区别

get(key) 方法在 key（键）不在字典中时，可以返回默认值 None 或者设置的默认值。

dict[key] 在 key（键）不在字典中时，会触发 KeyError 异常。

- 示例：嵌套字典使用

```python
#!/usr/bin/python3

testdict = {'tencent': {'url': 'https://www.qq.com/'}}

res = testdict.get('tencent', {}).get('url')
# 输出结果
print(f"tencent url 为 : {str(res)}")
```

以上实例输出结果为：

```bash
tencent url 为 : https://www.qq.com/
```
#### dict.setdefault(key, default=None)

常用

- 作用

setdefault() 方法和 get()方法 类似, 使用指定的键返回项目的值。 **如果键不存在于字典中，将会添加键并将值设为默认值**。


#### Key in dict

- 作用

用于判断 key 是否存在字典中，返回值是布尔类型(true/false)

- 语法

常和 if 配合使用

```python
if dict.key in dict:

if dict.key not in dict:
```


#### dict.items()

- 作用

返回该字典的包含键值的列表作为字典的元组对

- 语法

不接受任何参数，如果字典为空，则 dict.items() 方法返回一个空列表。

```python
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)
print(knights.items())
```

返回

```python
dict_items([('gallahad', 'the pure'), ('robin', 'the brave')])
```
#### dict.keys() + dict.values()

- 作用

返回字典的视图对象(只读)，可以使用 list() 转换成列表

- 语法

不接受任何参数

```python
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k in knights.keys():
    print(k)

for v in knights.values():
    print(v)
print(knights.keys())
print(knights.values())

```

#### dict.update(dict2)

- 作用

update() 函数把字典参数 dict2 的 key/value(键/值) 对更新到字典 dict 里。


### 其他方法

#### dict.clear()

- 作用

clear() 函数用于删除字典内所有元素。


#### dict.copy()

- 作用

copy() 函数返回一个字典的浅复制，子对象是引用


[Python 直接赋值、浅拷贝和深度拷贝解析](https://www.runoob.com/w3cnote/python-understanding-dict-copy-shallow-or-deep.html)

#### dict.fromkeys(seq[, value])

- 作用

fromkeys() 函数用于创建一个新字典，以序列 seq 中元素做字典的键，value 为字典所有键对应的初始值。


#### pop(key[, default])

- 作用

pop() 方法删除字典 key（键）所对应的值，返回被删除的值，当键 key 不存在时返回的值为 default

#### popitem()

- 作用

popitem() 方法随机返回并删除字典中的最后一对键和值，返回格式是元组。如果字典已经为空，却调用了此方法，就报出 KeyError 异常。



## 类型转换
### 字典转列表
#### 无序列表

```python
dit = {'name':'zxf',
       'age':'22',
       'gender':'male',
       'address':'shanghai'}

# 将字典的key转换成列表
lst = list(dit.keys()) # lst = list(dit)
print(lst)  # ['name', 'age', 'gender', 'address']

# 将字典的value转换成列表
lst2 = list(dit.values())
print(lst2)  # ['zxf', '22', 'male', 'shanghai']
```

```python
dit = {'name':'zxf',
       'age':'22',
       'gender':'male',
       'address':'shanghai'}
lst, lst2 = [], []

for key,value in dit.items():
    lst.append(key)
    lst2.append(value)

print(lst, lst2)
```

#### 有序列表
```python
import collections
z = collections.OrderedDict()
z['b'] = 2
z['a'] = 1
z['c'] = 3
z['r'] = 5
z['j'] = 4

#字典中的key转换为列表
key_value = list(z.keys())
print('字典中的key转换为列表：', key_value)

#字典中的value转换为列表
value_list = list(z.values())
print('字典中的value转换为列表：', value_list)
```