---
title: Python3 数字 常用方法
date: 2022-07-04 16:14:00
tags:
- Python
- python 数字
categories:
- Python
---

## 数值类型

- 整型(int) 
- 浮点型(float)
- 复数(complex)

## 数学函数

| 函数 | 描述 |
| -- | -- |
| abs(x) | 返回数字的绝对值。|
| max(x1, x2,...) | 返回给定参数的最大值，参数可以为序列。|
| min(x1, x2,...) | 返回给定参数的最小值，参数可以为序列。|
| round(x [,n]) | 返回浮点数 x 的四舍五入值，如给出 n 值，则代表舍入到小数点后的位数。<br>其实准确的说是保留值将保留到离上一位更近的一端。|

## 随机数函数

| 函数 | 描述 |
| -- | -- |
| random() | 随机生成下一个实数，它在[0,1)范围内。|
| randrange() | 返回指定递增基数集合中的一个随机数，基数默认值为 1。|
| choice(seq) | 从序列的元素中随机挑选一个元素，比如 random.choice(range(10))，从 0 到 9 中随机挑选一个整数。|

## 数学常量

| 常量 | 描述 |
| -- | -- |
| pi | 数学常量 pi（圆周率，一般以π来表示）|
| e | 数学常量 e，e 即自然常数（自然常数）。|
| inf | 正无穷 |

## 类型判断

### type()


type() 函数返回对象的类型

```python
type(123) == type(456)       # True
type(123) == int             # True
```

[类型注解支持](https://docs.python.org/zh-cn/3/library/typing.html)

### isinstance()

isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。

```python
>>> a = 2
>>> isinstance (a,int)
True
>>> isinstance (a,str)
False
>>> isinstance (a,(str,int,list))    # 是元组中的一个返回 True
True
```

- isinstance() 与 type() 区别：

type() 不会认为子类是一种父类类型，不考虑继承关系。

isinstance() 会认为子类是一种父类类型，考虑继承关系。

如果要判断两个类型是否相同推荐使用 isinstance()。
```python
class A:
    pass
 
class B(A):
    pass
 
isinstance(A(), A)    # returns True
type(A()) == A        # returns True
isinstance(B(), A)    # returns True
type(B()) == A        # returns False
```


使用 dir 可以获得一个对象的所有属性和方法：

```python
dir('ABC')
# ['__add__', '__class__',..., '__subclasshook__', 'capitalize', 'casefold',..., 'zfill']
```

## 类型转换


### string –> int/float

int() 函数用于将一个字符串或数字转换为整型，不能直接转换浮点型字符串

float() 函数用于将整数和字符串转换成浮点数。

```python
# 10进制string 转化为int
>>> int('12')
12

# 16进制string 转化为int
>>> int('12', 16)
18

>>> float('12')
12.0

float('%.2f' % 5.026)
5.03
```

### int –> string

```python
# int转化为 10进制string
>>> str(18)
'18'

# int转化为 16进制string
# hex() 函数返回的十六进制字符串中的字母默认为小写
>>> hex(18)
'0x12'
```
## 进制转换

![](/images/image-20210220.png)

int() 函数用于将一个字符串或数字转换为整型（十进制）。
```python
# 十六进制 到 十进制
>>> int('0xf',16) 
15

# 二进制 到 十进制
>>> int('10100111110',2)
1342

# 八进制 到 十进制
>>> int('17',8)
15
```
bin() 返回一个整数 int 或者长整数 long int 的二进制表示。
```python
# 十进制转二进制
>>> bin(10)
'0b1010'

# 十六进制转 二进制
# 十六进制->十进制->二进制
>>> bin(int('ff',16))
'0b11111111'

# 八进制 到 二进制
# 八进制先到十进制，再到二进制
>>> bin(int('17',8))
'0b1111'
```

oct() 函数将一个整数转换成 8 进制字符串。
```python
# 二进制 到 八进制
>>> oct(0b1010)
'012'

# 十进制到八进制
>>> oct(11)
'013'

# 十六进制到八进制
>>> oct(0xf) 
'017'
```

hex() 函数用于将 10 进制整数转换成 16 进制，以字符串形式表示。

```python
# 十进制 转 十六进制
>>> hex(1033)
'0x409'

# 二进制 转 十六进制
# 就是 二进制先转成 十进制， 再转成 十六进制。
>>> hex(int('101010',2))
'0x2a'

# 八进制到 十六进制
# 就是 八进制先转成 十进制， 再转成 十六进制。
>>> hex(int('17',8))
'0xf'
```



