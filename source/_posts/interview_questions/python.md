---
title: Python 相关面试题
date: 2022-08-11 14:14:00
tags:
- Python
categories:
- [面试题]
- [Python]
---


[知乎：110 道 Python 面试题（真题）](https://zhuanlan.zhihu.com/p/54430650)



1、谈下 python 的 GIL x
2、简述面向对象中 __new__ 和 ___init__ 区别
3、python2和 python3区别?请列举几个
4、list和 tuple的区别
5、range和xrange
6、深浅copy的区别
7、session和 cookle 分别是什么，有什么区别?
8、请写一个装饰器
9、谈下你对restfulapi的理解
10、跨域有哪些解决方案(至少列举3种）
Nginx同进同出、后端框架准许跨域、在请求头加alloworigin

11、简述多进程、多线程、协程

## 字典

### Python 如何对字典排序

- 思路

字典本身是无序，排序可使用 [sorted(iterable, key=None, reverse=False)](https://www.runoob.com/python3/python3-func-sorted.html)

- 排序：


```python

test_dict = {6: 9, 10: 5, 3: 11, 8: 2, 7: 6}

# 对字典的所有key进行排序
test_data_0 = sorted(test_dict.keys())
print(test_data_0)  # [3, 6, 7, 8, 10]

# 对字典（key，value）按照key的大小升序排列
test_data_1 = sorted(test_dict.items(), key=lambda x: x[0])
print(test_data_1)  # [(3, 11), (6, 9), (7, 6), (8, 2), (10, 5)]

# 对字典（key，value）按照value的大小升序排列
test_data_2 = sorted(test_dict.items(), key=lambda x: x[1])
print(test_data_2)  # [(8, 2), (10, 5), (7, 6), (6, 9), (3, 11)]

# 对字典（key，value）按照value的大小降序排列
test_data_3 = sorted(test_dict.items(), key=lambda x: x[1], reverse=True)
print(test_data_3)  # [(3, 11), (6, 9), (7, 6), (10, 5), (8, 2)]


```

- 面试题

`m1 = {'a': 1, 'b': 2, 'c': 1}` 将同样的 value 的 key 集合在 list 里，输出 `{1: ['a', 'c'], 2: ['b']}`

```python
m1 = {'a': 1, 'b': 2, 'c': 1}

f = {}

for key,value in m1.items():
    if value not in f:
        f[value] = [key]
    else:
        f[value].append(key)
print(f)
```

## 列表

### 取出列表里重复的元素的位置

```python
a = [1, 2, 3, 2, 1, 5, 6, 5, 5, 5]
source = a
from collections import defaultdict


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return ((key, locs) for key, locs in tally.items() if len(locs) > 1)


for dup in sorted(list_duplicates(source)):
    print(dup)
```

输出

```bash
(1, [0, 4])
(2, [1, 3])
(5, [5, 7, 8, 9])
```



## 字符串

### 将字符串中字母按照规则转换

```python
# -*- coding: utf-8 -*-
"""
K-M
O-Q
E-G
"""

# 方法一
def main():
    encrypt_sen = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml_back rfc spj."

    # 解密逻辑为：按字⺟次序往前加2，例如 a -> c, b -> d, c -> e
    # 这⼏个字⺟加2后需要往前循环，单独处理
    tran_map = {'y': 'a', 'z': 'b', 'Y': 'A', 'Z': 'B'}
    for alnum in range(24):
        tran_map[chr(97 + alnum)] = chr(97 + alnum + 2) # ⼩写字⺟
        tran_map[chr(65 + alnum)] = chr(65 + alnum + 2) # ⼤写字⺟
    decrypt_sen = []
    # 字⺟进⾏转换，其它不需要转换
    for s in encrypt_sen:
        decrypt_sen.append(tran_map[s]) if s.isalnum() else decrypt_sen.append(s)
    print(''.join(decrypt_sen))


if __name__ == '__main__':
    main()

# 方法二


def main2():
    string2 = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml_back rfc spj."

    intab  = "abcdefghijklmnopqrstuvwxyz"
    outtab = "cdefghijklmnopqrstuvwxyzab"
    trantab = str.maketrans(intab, outtab)

    print(string2.translate(trantab))

main2()


```
### 将"hello world"转换为首字母大写"Hello World"(相互转换)

```python
>>> 'hello world'.title() # 返回"标题化"的字符串
'Hello World'

>>> 'hello world'.capitalize() # 将字符串的第一个字符转换为大写
'Hello world'

>>> 'hello world'.upper() # 转换字符串中所有小写字母为大写
'HELLO WORLD'

>>> 'HELLO WORLD'.lower() # 转换字符串中所有大写字符为小写.
'hello world'

>>> 'hello world'.swapcase() # 将字符串中大写转换为小写，小写转换为大写
'HELLO WORLD'
>>> 'HELLO WORLD'.swapcase()
'hello world'
```

### 如何检测字符串中只含有数字?

```python
>>> '123bp'.isdigit() # 如果字符串只包含数字则返回 True 否则返回 False..
False

# 或者使用正则：
>>> import re
>>> bool(re.search(r'\d','qw123'))
True

# 或者使用Unicode码：
>>> uchar = '123'
... if uchar >= u'\u0030' and uchar <= u'\u0039':
...     print('True')
... else:
...     print('False')
True

```

### 将字符串"ilovechina"进行反转

```python
>>> "ilovechina"[::-1]
'anihcevoli'
```

### Python 中的字符串格式化方式你知道哪些

```python
'I %s her %s'%('love','cat')
'I {a} her {b}'.format(a='love',b='cat')
f'I {a} her {b}' #【Python3.6推荐写法】
```

### 有一个字符串开头和末尾都有空格，比如“ adabdw ”，要求写一个函数把这个字符串的前后空格都去掉。

lstrip() 截掉字符串左边的空格或指定字符。

rstrip() 删除字符串字符串末尾的空格。

strip([chars]) 在字符串上执行 lstrip()和 rstrip()

- chars -- 移除字符串头尾指定的字符序列。

```python
>>> ' adabdw '.lstrip()
'adabdw '
>>> ' adabdw '.rstrip()
' adabdw'
>>> ' adabdw '.lstrip().rstrip()
'adabdw'

>>> ' adabdw '.strip()
'adabdw'

def strip_function(str_):
    return str_.strip()

```

### 获取字符串”123456“最后的两个字符

```python
Str[-2: ]
```

### bytes 编码解码

```python
str = "蓝鲸";
str_utf8 = str.encode("UTF-8")
str_gbk = str.encode("GBK")
 
print(str)
 
print("UTF-8 编码：", str_utf8)
print("GBK 编码：", str_gbk)
 
print("UTF-8 解码：", str_utf8.decode('UTF-8','strict'))
print("GBK 解码：", str_gbk.decode('GBK','strict'))


蓝鲸
UTF-8 编码： b'\xe8\x93\x9d\xe9\xb2\xb8'
GBK 编码： b'\xc0\xb6\xbe\xa8'
UTF-8 解码： 蓝鲸
GBK 解码： 蓝鲸
```

### s=“info：xiaoZhang 33 shandong”，用正则切分字符串输出[‘info’, ‘xiaoZhang’, ‘33’, ‘shandong’]

```python
>>> s = "info：xiaoZhang 33 shandong"
>>> print(re.split(r"：| ", s))
['info', 'xiaoZhang', '33', 'shandong']
```

### a = "你好 中国 "，去除多余空格只留一个空格

```python
>>> a = "你好 中国 "      # split() 通过指定分隔符对字符串进行切片，如果第二个参数 num 有指定值，则分割为 num+1 个子字符串。
>>> ''.join(a.split())   #join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
'你好中国'

```




## 循环

### 斐波那契数列

[Python 实现 斐波那契数列](https://bk.tencent.com/s-mart/community/question/891?type=answer)


### 输出质数
```python
a = int(input("输入一个整数："))

for num in range(1, a):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                break
        else:
            print(num)
```


### 九九乘法表
```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f'{i}x{j}={i*j}', end=' ')
    print()

print("-----------------")
for i in range(9, 0, -1):
    for j in range(i, 0, -1):
        print(f'{i}x{j}={i * j}', end=' ')
    print()
```


### 摄氏和华氏温度相关转换
```python
class System:
    def __init__(self, name):
        self.name = name
        self.fahrenheit = []
        self.celsiu = []
        self.a = []

    def Celsius(self, fahrenheit):
        celsius = (fahrenheit - 32) / 1.8
        print(celsius)

    def Fahrenheit(self, celsius):
        fahrenheit = celsius * 1.8 + 32
        print(fahrenheit)

    def start(self):
        while True:
            self.show_menu()
            a = input('输入计算的数字和符号：')
            self.if1(a)

    def show_menu(self):
        print(f"""
        *****************
        欢迎使用 {self.name} 的【摄氏度和华氏度转换器】
        请输入相应格式的数字加符号。
        例：输入37.6C 或者 37.6c,将会转换成相应的华氏度
        例：输入37.6F 或者 37.6f,将会转换成相应的摄氏度
        *****************
        """)

    def if1(self,a):
        if a[-1] in ['F', 'f']:
            self.fahrenheit = a[:-1]
            self.Celsius(eval(self.fahrenheit))
        elif a[-1] in ['C', 'c']:
            self.celsius = a[:-1]
            self.Fahrenheit(eval(self.celsius))


if __name__ == '__main__':
    system = System('刘伟杰')
    system.start()
```

