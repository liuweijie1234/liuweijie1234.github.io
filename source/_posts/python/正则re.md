---
title: Python3 模块 re 正则表达式
date: 2022-08-15 10:22:00
tags:
- Python module
- re
categories:
- Python
---

Python 的 re 模块是一个正则表达式库，用于对字符串进行模式匹配和搜索。
它提供了多个函数和方法，用于执行不同的正则表达式操作，下面简要介绍一些常用的函数和方法及其参数解释和示例：

## 常用匹配规则

| 模式 | 描述 |
| -- | -- |
| \w | 匹配字母、数字及下划线 |
| \W | 匹配不是字母、数字及下划线的字符 |
| \s | 匹配任意空白字符，等价于[\t\n\r\f] |
| \S | 匹配任意非空字符 |
| \d | 匹配任意数字，等价于[0-9] |
| \D | 匹配任意非数字的字符 |
| \A | 匹配字符串开头 |
| \z | 匹配字符串结尾。如果存在换行，同时还会匹配换行符 |
| \Z | 匹配字符串结尾。如果存在换行，只匹配换行前的结束字符串 |
| \G | 匹配最后匹配完成的位置 |
| \n | 匹配一个换行符 |
| \t | 匹配一个制表符 |
| ^ | 匹配一行字符串的开头 |
| $ | 匹配一行字符串的结尾 |
| . | 匹配任意字符，除了换行符，当 re.DOTALL 标记被指定时，可以匹配包括换行符的任意字符 |
| [abc] | 用来表示一组字符，单独列出，例如 [abc] 用来匹配a、b 或 c |
| [^abc] | 匹配不在[]中的字符，例如匹配除了a、b、c 之外的字符 |
| * | 匹配 0 个或多个表达式 |
| + | 匹配 1 个或多个表达式 |
| ? | 匹配 0 个或1个前面的正则表达式定义的片段，非贪婪方式 |
| {n} | 精确匹配 n 个前面的表达式 |
| {n, m} | 匹配 n 到 m 次由前面正则表达式定义的片段，贪婪方式 |
| a|b | 匹配 a 或 b |
| () | 匹配括号内的表达式，也表示一个组 |

| 修饰符 | 描述 |
| -- | -- |
| re.I | 使匹配对大小写不敏感 |
| re.L | 做本地化识别（locale-aware）匹配 |
| re.M | 多行匹配，影响 ^ 和 $ |
| re.S | 使 . 匹配包括换行在内的所有字符 |
| re.U | 根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B. |
| re.X | 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。 |


### re.match

从字符串的开头开始匹配指定的正则表达式，如果匹配成功就返回一个匹配对象，否则返回 None。

```python
re.match(pattern, string, flags=0)
```

- pattern：正则表达式的字符串形式。
- string：需要匹配的字符串。
- flags：可以通过这个参数来控制匹配模式。默认为 0，表示忽略大小写和换行符。其他可选值包括：re.I（忽略大小写）、re.M（多行模式）、re.S（点号匹配任意字符，包括换行符）等。

示例代码：

```python
import re

pattern = r"hello"
string = "Hello, world!"

match_obj = re.match(pattern, string, flags=re.I)
if match_obj:
    print("Matched:", match_obj.group())
else:
    print("Not matched.")
```

### re.search

在字符串中搜索指定的正则表达式，如果找到匹配项就返回一个匹配对象，否则返回 None。

```python
re.search(pattern, string, flags=0)
```
- pattern：正则表达式的字符串形式。
- string：需要搜索的字符串。
- flags：可以通过这个参数来控制匹配模式。

示例代码：

```python
import re

pattern = r"world"
string = "Hello, world!"

match_obj = re.search(pattern, string)
if match_obj:
    print("Matched:", match_obj.group())
else:
    print("Not matched.")
```

### re.findall

在字符串中查找所有与正则表达式匹配的子串，返回一个包含所有匹配结果的列表。

```python
re.findall(pattern, string, flags=0)
```

- pattern：正则表达式的字符串形式。
- string：需要查找的字符串。
- flags：可以通过这个参数来控制匹配模式。

示例代码：

```python
import re

pattern = r"\d+"
string = "I have 3 apples and 2 bananas."

digits_list = re.findall(pattern, string)
print(digits_list)
```

```python
import re

a = '* [White Paper](./test.md)'

chapter_path = re.findall(r'[(](.*?)[)]', a, re.S)
chapter_name = re.findall(r'[\[](.*?)[\]]', a, re.S)

print(chapter_name, chapter_path)
# 返回 ['White Paper'] ['./test.md']
```

### re.sub

用指定的替换字符串**替换**所有符合正则表达式的子串，并返回替换后的新字符串。如果没有找到匹配项，则返回原字符串本身。

```python
re.sub(pattern, repl, string, count=0, flags=0)
```

- pattern：正则表达式的字符串形式。
- repl：用来替换匹配子串的字符串。
- string：需要进行替换操作的字符串。
- count：最多替换次数。默认为 0，表示替换所有匹配项。
- flags：可以通过这个参数来控制匹配模式。

示例代码：

```python
import re

pattern = r"\d+"
string = "I have 3 apples and 2 bananas."

replaced_str = re.sub(pattern, "5", string)
print(replaced_str)
# 输出结果为："I have 5 apples and 5 bananas."
```

![](/images/641.jfif)


### re.compile

将正则表达式编译成一个对象，提高执行效率。返回的对象可以调用多种方法来进行正则表达式操作，例如 match()、search() 等。

```python
re.compile(pattern, flags=0)
```

- pattern：正则表达式的字符串形式。
- flags：可以通过这个参数来控制匹配模式。

示例代码：

```python
import re

pattern = r"\d+"
string = "I have 3 apples and 2 bananas."

regex_obj = re.compile(pattern)
digits_list = regex_obj.findall(string)
print(digits_list)
```

### re.fullmatch(pattern, string, flags=0)

在字符串中匹配整个正则表达式，如果成功就返回一个匹配对象，否则返回 None。与 match() 不同的是，fullmatch() 要求整个字符串都必须和正则表达式完全匹配。

- pattern：正则表达式的字符串形式。
- string：需要匹配的字符串。
- flags：可以通过这个参数来控制匹配模式。

示例代码：

```python
import re

pattern = r"hello"
string1 = "Hello, world!"
string2 = "hello"

match_obj1 = re.fullmatch(pattern, string1, flags=re.I)
match_obj2 = re.fullmatch(pattern, string2, flags=re.I)
if match_obj1:
    print("Matched:", match_obj1.group())
else:
    print("Not matched.")

if match_obj2:
    print("Matched:", match_obj2.group())
else:
    print("Not matched.")

```

### re.split(pattern, string, maxsplit=0, flags=0)

根据正则表达式分割字符串，返回分割后的子串列表。

- pattern：正则表达式的字符串形式。
- string：需要分割的字符串。
- maxsplit：最多分割次数。默认为 0，表示不限制分割次数。
- flags：可以通过这个参数来控制匹配模式。

示例代码：

```python
import re

pattern = r"\W+"  # 匹配非字母数字字符
string = "Hello, world! How are you?"

words_list = re.split(pattern, string)
print(words_list)
```

### match.group([group1, ...])

返回匹配到的子串或子组（即圆括号包含的部分）。

group1, ...：可选参数，指定要返回哪些子组。默认为 0，表示返回整个匹配的子串。其他数字表示返回对应索引的子组。
示例代码：

```python
import re

pattern = r"(\w+), (\w+) (\w+)!"
string = "Hello, world!"

match_obj = re.search(pattern, string)
if match_obj:
    print(match_obj.group())  # 返回整个匹配的子串："Hello, world!"
    print(match_obj.group(1))  # 返回第一个子组："Hello"
    print(match_obj.group(2))  # 返回第二个子组："world"
    print(match_obj.group(3))  # 返回第三个子组：无，因为正则表达式中只有两个组。

```

### match.start([group]) 和 match.end([group])

返回匹配到的子串或子组在原字符串中的起始位置和结束位置。

group：可选参数，指定要返回哪个子组的起始位置或结束位置。默认为 0，表示返回整个匹配的子串的位置。其他数字表示返回对应索引的子组的位置。

示例代码：

```python
import re

pattern = r"(\w+), (\w+) (\w+)!"
string = "Hello, world!"

match_obj = re.search(pattern, string)
if match_obj:
    print(match_obj.start())  # 返回匹配子串的起始位置
```