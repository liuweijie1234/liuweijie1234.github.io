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

## 一、python 语言基础

### Python 中的列表（List）和元组（Tuple）有什么区别？
列表：可变序列，用 [] 定义，支持增删改操作。
元组：不可变序列，子元素可变，用 () 定义，哈希化后可作字典键，性能更优。

应用场景：
列表适合用于需要频繁修改的数据集合，如存储动态更新的用户信息列表；

存储常量或字典键用元组

### python切片，负索引，

切片：list[start:stop:step]，获取子序列。
负索引：list[-1] 表示最后一个元素。

### range和xrange区别

range()：直接返回完整列表，内存占用高。
xrange()：返回生成器，惰性计算（Python3 中 range 等同于此行为）。


### 三元运算符
```python
value = true_value if condition else false_value
```
### 推导式

列表推导式
字典推导式
集合推导式

生成器表达式



- 数据结构

## 二、面对对象编程

### 简述面向对象中 __new__ 和 ___init__ 区别
__new__：负责创建实例（类方法），返回未初始化的对象。
__init__：负责初始化实例（实例方法），无返回值。
示例：单例模式中通过 __new__ 控制实例创建。

### 类方法，静态方法，实例方法
类方法：@classmethod，操作类属性，首个参数为 cls。
静态方法：@staticmethod，无需类或实例参数。
实例方法：首个参数为 self，操作实例属性。

### 继承与多态

支持多重继承，通过 MRO（方法解析顺序）解析方法调用顺序（C3算法）。

子类可重写父类方法实现多态。


### 魔术方法（Magic Methods）
__init__：构造初始化。
__new__：对象创建。
__str__：定义 print(obj) 的输出。
__call__：使实例可调用（如 obj()）。

## 三、函数式编程

### 闭包 (Closure)

定义：闭包是由函数及其引用环境组合而成的实体，内部函数可以访问外部作用域的变量（即使外部函数已执行完毕）。

原理：
```python
def outer_func(x):     # 外部函数
    def inner_func(y): # 内部函数（闭包）
        return x + y  # 捕获外部变量 x
    return inner_func  # 返回闭包函数

closure = outer_func(10)
print(closure(5))  # 输出 15（10+5）
```

关键特性：

变量捕获：inner_func 记住了 x=10
状态持久化：outer_func 执行后，其局部变量仍存在
私有性：外部无法直接访问闭包变量（仅通过闭包函数）

常用场景：计数器生成器, 配置预设函数
```python
# 计数器生成器
def counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = counter()
print(c())  # 1
print(c())  # 2
```

```python
# 配置预设函数
def power_factory(exp):
    def calc(base):
        return base ** exp
    return calc

square = power_factory(2)
cube = power_factory(3)

print(square(3))  # 9
print(cube(2))    # 8
```

### 装饰器

装饰器原理：
装饰器本质上是一个接受函数作为参数并返回一个新函数的函数。
它的主要目的是在不修改被装饰函数代码的情况下，增强函数的功能。
例如，装饰器可以在函数执行前后添加额外的操作，如日志记录、权限验证等。

核心机制：
- 函数作为参数传递
- 通过闭包保持原始函数引用
- 返回增强版函数

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function execution")
        result = func(*args, **kwargs)
        print("After function execution")
        return result
    return wrapper

@decorator # 语法糖 ≡ example_function = decorator(example_function)
def example_function():
    print("Inside example function")

example_function()
"""输出
Before function execution
Inside example function
After function execution
"""
```

应用场景：
- 日志记录：可以记录函数的调用时间、调用参数等信息。
```python
def log_exec(func):
    def wrapper(*args):
        print(f"Executing: {func.__name__}{args}")
        return func(*args)
    return wrapper

@log_exec
def add(a, b):
    return a + b

add(2, 3)  # 输出: Executing: add(2, 3)
```
- 权限验证/参数验证：在执行某些敏感操作的函数前验证用户权限/参数。
```python
def validate_non_negative(func):
    def wrapper(*args):
        if any(x < 0 for x in args):
            raise ValueError("参数必须非负")
        return func(*args)
    return wrapper

@validate_non_negative
def sqrt(x):
    return x ** 0.5

sqrt(4)   # 2.0
sqrt(-1)  # 报错: ValueError
```

- 计时功能：计算函数的执行时间，用于性能分析。

```python
import time

def timer(func):
    def wrapper(*args):
        start = time.perf_counter()
        res = func(*args)
        print(f"{func.__name__}耗时: {time.perf_counter()-start:.5f}s")
        return res
    return wrapper

@timer
def heavy_calc(n):
    return sum(range(n))

heavy_calc(10000000)  # 输出耗时
```

- 带参数的装饰器
```python
def repeat(n_times):  # 装饰器工厂
    def decorator(func):  # 实际装饰器
        def wrapper(*args, **kwargs):
            for _ in range(n_times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(n_times=3)
def say_hello(name):
    print(f"Hello {name}!")

say_hello("Alice")
# 输出:
# Hello Alice!
# Hello Alice!
# Hello Alice!
```


### lambda表达式

优点：简洁的匿名函数，适用于简单操作。
缺点：无法写复杂逻辑，不支持语句。

示例：
```pythonm
sorted(list, key=lambda x: x[1])。
```

### 迭代器 vs 生成器
迭代器：
迭代器是遵循迭代器协议（具有 __iter__() 和 __next__() 方法）的对象。
__iter__() 方法返回迭代器本身，__next__() 方法返回下一个值，直到没有值可以返回时抛出 StopIteration 异常。
例如，使用内置的 iter() 函数可以获取一个列表的迭代器：

```python
my_list = [1, 2, 3]
iterator = iter(my_list)
print(next(iterator))  # 输出 1
print(next(iterator))  # 输出 2
print(next(iterator))  # 输出 3
print(next(iterator))  # 抛出 StopIteration 异常
```


生成器：
生成器是一种特殊的迭代器，它使用函数和 yield 关键字来定义。
当函数中包含 yield 语句时，它就变成了一个生成器函数。调用生成器函数返回的是一个生成器对象。
生成器在遇到 yield 表达式时会暂停执行并返回值，下次调用 next() 方法时从暂停处继续执行。例如：

```python
def generator_example():
    yield 1
    yield 2
    yield 3
gen = generator_example()
print(next(gen))  # 输出 1
print(next(gen))  # 输出 2
print(next(gen))  # 输出 3
print(next(gen))  # 抛出 StopIteration 异常
```

yield 暂停执行并保留状态，return 终止函数；send() 可向生成器发送值。

应用场景：处理大文件时惰性读取（生成器）。

[python花式读取大文件(10g/50g/1t)遇到的性能问题（面试向）](https://v3u.cn/a_id_97)

```python
def chunked_file_reader(file, block_size=1024 * 8):
    for chunk in iter(partial(file.read, block_size), ''):
        yield chunk

def count_lines(fname):
    count = 0
    with open(fname, "rb") as fp:  # 二进制模式避免编码问题
        for chunk in chunked_file_reader(fp):
            count += chunk.count(b"\n")  # 统计换行符
        # 处理最后一行无换行符的情况
        if not chunk.endswith(b"\n") and chunk:
            count += 1
    return count
```

### 高阶函数（Python2 vs 3）

Python2：map(), filter(), reduce() 返回列表。
Python3：返回迭代器，需 list(iter) 转换。

## 四、并发编程

### GIL （全局解释器锁）
原因：CPython 的内存管理非线程安全，GIL 保证同一时刻仅一个线程执行字节码。
规避方案：
多进程：multiprocessing 模块。
其他解释器：Jython（无GIL）、PyPy（STM技术）。
影响：CPU密集型任务多线程无效，I/O密集型任务影响较小。

### 进程、线程、协程

线程 进程 协程（引申出原生协程async await和greenlet以及gevent的区别，引申出大文件操作） 

多进程：multiprocessing，绕过GIL，适合CPU密集型任务（如计算）。
多线程：threading，适合I/O密集型任务（如网络请求）。
协程：
    原生协程：async/await（Python3.5+）。
    第三方库：gevent（基于greenlet，自动切换协程）。
    大文件操作：协程异步I/O高效处理（如 aiofiles）。

- 算法
- 内存

## 五、内存管理

### 垃圾回收机制
引用计数：对象引用数为0时立即回收（主要机制）。
每个对象都有一个引用计数器，当一个变量引用对象时，计数器加 1；当变量不再引用对象时，计数器减 1。当计数器为 0 时，对象会被垃圾回收器回收。

```python
a = [1, 2, 3]  # a 引用列表，引用计数为 1
b = a          # b 引用列表，引用计数加 1，变为 2
del a          # a 被删除，引用计数减 1，变为 1
del b          # b 被删除，引用计数减 1，变为 0，列表对象被回收
```

垃圾回收：标记-清除，解决循环引用（如链表）。循环引用是指两个或多个对象互相引用，导致它们的引用计数无法减到 0 的情况。Python 的垃圾回收器会定期检测和清理这些不可达对象（即不能被程序中任何变量访问的对象）

```python
a = []
b = []
a.append(b)
b.append(a)
# 此时 a 和 b 形成循环引用，当它们的引用被删除后，垃圾回收器会回收它们占用的内存
```

分代回收：根据对象存活时间分代（0/1/2代），减少扫描频率。

### 深拷贝 vs 浅拷贝
浅拷贝：copy.copy()，仅复制顶层对象（嵌套对象共享引用）。
深拷贝：copy.deepcopy()，递归复制所有层级对象。
示例：修改嵌套列表时深拷贝避免副作用。


## 六、Web开发

### 框架Flask、Django、FastAPI、Tornado的区别
Flask：轻量级，灵活，路由和视图分离。
Django：重量级，MVC架构，ORM简化数据库操作。
FastAPI：高性能，异步，自动生成API文档。
Tornado：非阻塞，异步，适合长连接。

### Session vs Cookie
Cookie：客户端存储（如用户偏好），键值对，大小限制（4KB）。
Session：服务端存储（如用户登录状态），依赖Session ID（通常存储于Cookie）。
区别：Session更安全但占用服务端资源。

### RESTful API
使用HTTP方法（GET/POST/PUT/DELETE）对应资源操作（CRUD）。
无状态请求，资源通过URI标识（如 /api/users/1）。
数据格式通常为JSON/XML。

### 跨域解决方案
Nginx反向代理：配置 proxy_pass 转发请求（同源）。
后端框架中间件：Flask-CORS、Django-cors-headers，设置 Access-Control-Allow-Origin。
预检请求（CORS）：复杂请求前发送OPTIONS请求验证。
JSONP：通过 <script> 标签跨域（仅限GET）。


## 七、设计模式

### 单例模式
实现：通过 __new__ 控制实例化（线程安全需加锁）。
用途：数据库连接池、全局配置。
缺点：全局状态增加耦合度。

### 工厂模式
抽象工厂：创建相关对象族（如不同数据库连接）。
示例：
```python
class DatabaseFactory:
    def create_conn(self, db_type):
        if db_type == "mysql": return MySQLConn()
        elif db_type == "postgres": return PostgresConn()
```

### 上下文管理器（with语句）

上下文管理器是一种确保资源正确分配和释放的机制。
它通过定义 __enter__() 和 __exit__() 方法来管理资源的获取和释放。
with 语句用于执行上下文管理器，它会在代码块执行前调用 __enter__() 方法，在代码块执行后调用 __exit__() 方法。

例如，文件操作是一个典型的上下文管理器应用场景：
示例：
```python
with open("file.txt", "r") as f:
    data = f.read()
```

- 自定义上下文管理器:可以通过创建一个类并定义 __enter__() 和 __exit__() 方法来实现自定义上下文管理器
```python
class MyContextManager:
    def __enter__(self):
        print("Entering context")
        # 返回资源对象
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        # 处理异常等操作

with MyContextManager() as cm:
    print("Inside context")
# 输出结果：
# Entering context
# Inside context
# Exiting context
```


## 八、解释器与自省

解释器类型

CPython：官方解释器（有GIL）。
PyPy：JIT编译加速（部分场景提升显著）。
Jython：基于JVM，无GIL。

自省
运行时获取对象信息：
```python
type(obj), dir(obj), hasattr(obj, 'method'), getattr(obj, 'attr')
```

























# 基础知识


## Python中的列表（List）和元组（Tuple）有什么区别？

解释 ：
列表是可变的（Mutable），可以对列表中的元素进行修改、添加和删除等操作。
元组是不可变的（Immutable），一旦创建后，元组中的元素就不能被修改。

例如：
列表示例：list_example = [1, 2, 3]，可以通过 list_example.append(4) 添加元素，list_example[1] = 10 修改元素。
元组示例：tuple_example = (1, 2, 3)，不能使用类似 tuple_example[1] = 10 这样的语句来修改元素。

应用场景 ：
列表适合用于需要频繁修改的数据集合，如存储动态更新的用户信息列表。
元组适合用于不需要修改的数据，如配置项、数据库查询结果等，因为其不可变性可以保证数据的稳定性，并且在某些情况下（如作为字典的键）是必要的。


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

