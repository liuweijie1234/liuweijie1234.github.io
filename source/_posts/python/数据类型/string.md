---
title: Python3 字符串 常用方法
date: 2022-07-04 16:14:00
tags:
- Python
- python 字符串
categories:
- Python
---

## 字符串介绍

字符串是 Python 中最常用的数据类型

字符串可以进行的操作包括 索引、切片、加、乘、检查成员。

| 操作符 | 描述                                               |
| ------ | -------------------------------------------------- |
| `+`    | 字符串连接                                         |
| *      | 重复输出字符串                                     |
| []     | 通过索引获取字符串中字符                           |
| [ : ]  | 截取字符串中的一部分                               |
| in     | 成员运算符 - 如果字符串中包含给定的字符返回 True   |
| not in | 成员运算符 - 如果字符串中不包含给定的字符返回 True |

## 字符串格式化

| 格式化符号 | 替换内容     |
| ------ | ------------ |
| %s     | 字符串       |
| %d     | 整数，%06d 表示输出的整数显示位数，不足的地方使用 0 补全         |
| %f     | 浮点数，**%.02f** 表示小数点后只显示两位       |
| %x     | 十六进制整数 |

- 推荐使用 f-string

```python
>>> x = 1
>>> print(f'{x+1}')   # Python 3.6
2

>>> x = 1
>>> print(f'{x+1=}')   # Python 3.8
x+1=2
```
- format():格式化输出


## 转义字符

\n   换行
\t   制表

[其他转义字符请翻阅 菜鸟教程](https://www.runoob.com/python3/python3-string.html)

## 字节串

### bytes.decode(encoding="utf-8", errors="strict")

Python3 中没有 decode 方法，但我们可以使用 bytes 对象的 decode() 方法来解码给定的 bytes 对象，这个 bytes 对象可以由 str.encode() 来编码返回。

### encode(encoding='UTF-8',errors='strict')

以 encoding 指定的编码格式编码字符串，如果出错默认报一个 ValueError 的异常，除非 errors 指定的是'ignore'或者'replace'


## 内置方法

### 转换/替换/排版

#### replace(old, new [, max])

- 作用

把 将字符串中的 old 替换成 new,如果 max 指定，则替换不超过 max 次。



#### capitalize()

将字符串的第一个字符转换为大写

#### upper()

转换字符串中的小写字母为大写

#### lower()

转换字符串中所有大写字符为小写.

#### swapcase()

将字符串中大写转换为小写，小写转换为大写


#### title()

返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写(见 istitle())

#### center(width, fillchar)

返回一个指定的宽度 width 居中的字符串，fillchar 为填充的字符，默认为空格。

#### expandtabs(tabsize=8)

把字符串 string 中的 tab 符号转为空格，tab 符号默认的空格数是 8 。

#### ljust(width[, fillchar])

返回一个原字符串左对齐,并使用 fillchar 填充至长度 width 的新字符串，fillchar 默认为空格。

#### rjust(width,[, fillchar])


返回一个原字符串右对齐,并使用 fillchar(默认空格）填充至长度 width 的新字符串

#### zfill (width)


返回长度为 width 的字符串，原字符串右对齐，前面填充 0

#### maketrans()


创建字符映射的转换表，对于接受两个参数的最简单的调用方式，第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。


#### translate(table, deletechars="")


根据 table 给出的表(包含 256 个字符)转换 string 的字符, 要过滤掉的字符放到 deletechars 参数中


### 拼接/截取

#### join(seq)

- 作用

以指定字符串作为分隔符，将 seq 中所有的元素(的字符串表示)合并为一个新的字符串

- 语法

```python
str.join(sequence)
```
sequence -- 要连接的元素序列。



#### split(str="", num=string.count(str))

- 作用

以 str 为分隔符截取字符串，如果 num 有指定值，则仅截取 num+1 个子字符串

#### splitlines([keepends])

按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。

#### lstrip()

截掉字符串左边的空格或指定字符。

#### rstrip()

删除字符串末尾的空格或指定字符。

#### strip([chars])

- 作用

用于移除字符串头尾指定的字符（默认为空格）或字符序列。

> 注意：**该方法只能删除开头或是结尾的字符，不能删除中间部分的字符**。

### 查询/检测

#### find(str, beg=0, end=len(string))

检测 str 是否包含在字符串中，如果指定范围 beg 和 end ，则检查是否包含在指定范围内，如果包含返回开始的索引值，否则返回-1

#### rfind(str, beg=0,end=len(string))

类似于 find()函数，不过是从右边开始查找.

#### index(str, beg=0, end=len(string))

跟 find()方法一样，只不过如果 str 不在字符串中会报一个异常。

#### rindex( str, beg=0, end=len(string))

类似于 index()，不过是从右边开始.

#### len(string)

返回字符串长度

#### count(str, beg= 0,end=len(string))

返回 str 在 string 里面出现的次数，如果 beg 或者 end 指定则返回指定范围内 str 出现的次数

#### max(str)

返回字符串 str 中最大的字母。

#### min(str)

返回字符串 str 中最小的字母。

#### startswith(substr, beg=0,end=len(string))

检查字符串是否是以指定子字符串 substr 开头，是则返回 True，否则返回 False。如果beg 和 end 指定值，则在指定范围内检查。

#### endswith(suffix, beg=0, end=len(string))

检查字符串是否以 obj 结束，如果 beg 或者 end 指定则检查指定的范围内是否以 obj 结束，如果是，返回 True,否则返回 False.

#### isdigit()

如果字符串只包含数字则返回 True 否则返回 False..

#### isnumeric()

如果字符串中只包含数字字符，则返回 True，否则返回 False

#### isalnum()

如果字符串至少有一个字符并且所有字符都是字母或数字则返 回 True，否则返回 False

#### isalpha()

如果字符串至少有一个字符并且所有字符都是字母或中文字则返回 True, 否则返回 False

#### isspace()

如果字符串中只包含空白，则返回 True，否则返回 False.

#### istitle()

如果字符串是标题化的(见 title())则返回 True，否则返回 False

#### islower()

如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是小写，则返回 True，否则返回 False

#### isupper()

如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是大写，则返回 True，否则返回 False

#### isdecimal()

检查字符串是否只包含十进制字符，如果是返回 true，否则返回 false。


[python 字符串补全填充固定长度（补0）的三种方法](https://blog.csdn.net/weixin_42317507/article/details/93411132)
