---
title: Python3 常用函数
date: 2022-08-13 16:14:00
tags:
- Python
categories:
- Python
---


#####  map

map()接收两个参数，一个是函数，一个是 Iterable，map 将传入的函数依次作用到序列的每个元素，并把结果作为新的 Iterator 返回。

```python
def f(x):
  return x * x

r = map(f, [1, 2, 3, 4, ..., 9])
list(r)        # [1, 4, 9, 16, ..., 81]

list(map(str, [1, 2, 3, 4, ..., 9])) ['1', '2', '3', ..., '9']
```

#####  reduce

reduce 把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce 把结果继续和序列的下一个元素做累积计算：

```python
from functools import reduce
def add(x, y):
  return x + y

reduce(add, [1, 3, 5, 7, 9])         # 25
'--------------------------------------------'
def fn(x, y):
  return x * 10 + y

reduce(fn, [1, 3, 5, 7, 9])          # 13579
```

####  filter

Python 内建的 filter()函数用于过滤序列，filter 也接收一个函数和一个序列，filter 把传入的函数依次作用于每个元素，然后根据返回值是 True 还是 False 决定。

```python
# 在一个list中，删掉偶数
def is_odd(n):
  return n % 2 == 1

list(filter(is_odd, [1, 2, 3, 4, ..., 10])) # [1, 3, 5, 7, 9]

# 把序列中的空字符串删掉
def not_empty(s):
  return s and s.trip()

list(filter(not_empty, ['A', '', 'B', None, 'C', ' ']))  # ['A', 'B', 'C']
```

#### sorted

Python 内置的 sorted()函数可以对 list 进行排序。

```python
sorted([35, 2, 3, -2, 0])              # [-2, 0, 2, 3, 35]
# 可以接收一个key函数来实现自定义的排序，例如按绝对值大小排序
sorted([36, 5, -12, 9, -21], key=abs)  # [5, 9, -12, -21, 36]

sorted(list_test,key = lambda i:i['bk_world_id'])
```

###  返回函数

高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。

```python
def sum_lazy(*args):
  def sum():
    res = 0
    for arg in args:
        res = res + arg
    return res
  return sum

# 这样调用
sum = sum_lazy(1, 3, 5)
sum()      # 9
```

这种形式也被称为闭包，即保存函数的状态信息，使函数的局部变量信息可以保存下来，不被回收。

###  匿名函数

关键字 lambda 表示匿名函数，好处在于因为函数没有名字，不必担心函数名冲突：

```python
f = lambda x: x * x
f(5)         # 25
```

也可以将匿名函数作为返回值返回：

```python
def build(x, y):
  return lambda: x * x + y * y
```

###  装饰器

在代码运行期间动态增加功能的方式，称之为“装饰器”，即返回添加功能后的函数再调用。装饰器的本质就是闭包，即函数的嵌套定义。

```python
# 不带参数 

def deco(func):
    def wrapper():
        print("debug -- ")
        return func()
    return wrapper

@deco
def say_hello():
    print('hello!')

@deco
def say_bye():
    print('bye!')
    
if __name__ == '__main__':
    # say_hello_boss = deco(say_hello)
    # say_hello_boss()
    say_hello()
```

```python
# 带参数

def logging(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print('[{level}]: enter function {func}()'.format(
                level=level,
                func=func.__name__
            ))
            return func(*args, **kwargs)
        return inner_wrapper
    return wrapper


@logging(level='INFO')
def say(something):
    print("say {}!".format(something))


say('hello')
```

```python
import functools

def log(func):
    @functools.wraps(func)
    # python提供的装饰器，它能把原函数d的元信息拷贝到装饰器里面的func函数中，
    def wrapper(*args, **kwargs):
        print('call %s(): ' % func.__name__)
        print('args = {}'.format(*args))
        return func(*args, **kwargs)
    return wrapper


@log
def test(p):
    print(test.__name__ + " param: " + p)


test('hello')

```



###  偏函数

偏函数的作用就是把一个函数的部分参数给固定住（设置默认值），返回一个新的函数，调用这个新函数会更简单。

```python
int('12345', base=2)

# 封装后只需传入字符串
def int2(x, base=2):
  return int(x, base)

# 另一种写法
int2 = functools.partial(int, base=2)

```


### setattr()


setattr() 函数，用于设置属性值，该属性不一定是存在的。

用法详解
http://c.biancheng.net/view/2378.html


### hasattr()

hasattr(self.model, order_by_field)

作用：
检查模型类 self.model 是否包含名为 order_by_field 的属性或列
防止尝试访问不存在的字段导致 AttributeError，特别是在处理用户输入的排序/过滤字段时

参数：

self.model：SQLAlchemy 模型类（如 MonitorAccountStats）
order_by_field：要检查的字段名称（字符串）

返回值：

True：如果字段存在
False：如果字段不存在
```python
if hasattr(MonitorAccountStats, 'is_focus'):
    # 安全地访问 is_focus 字段
    is_focus_value = getattr(MonitorAccountStats, 'is_focus')
    # 执行其他操作...
else:
    # 处理字段不存在的情况
    print("字段 'is_focus' 不存在")
```


### getattr()

作用
用于获取对象的属性值或方法。

getattr(object, name[, default]) 函数接受最少两个参数：

object：表示要获取属性或方法的对象。
name：表示要获取的属性名或方法名。
default（可选）：表示如果属性或方法不存在时返回的默认值。

下面是 getattr() 函数的用法示例：

```python
class MyClass:
    def __init__(self):
        self.name = 'Alice'
    
    def greet(self):
        print('Hello!')

obj = MyClass()

# 获取对象的属性值
name = getattr(obj, 'name')
print(name)  # 输出: Alice

# 获取对象的方法并调用
method = getattr(obj, 'greet')
method()  # 输出: Hello!

# 获取不存在的属性并设置默认值
age = getattr(obj, 'age', 25)
print(age)  # 输出: 25

# 获取不存在的方法并设置默认值
default_method = getattr(obj, 'say_hello', None)
if default_method:
    default_method()
else:
    print('Method not found.')  # 输出: Method not found.
```
上述示例中，首先定义了一个类 MyClass，其中包含一个属性 name 和一个方法 greet。然后创建了该类的一个实例 obj。通过 getattr() 函数，可以动态地获取 obj 对象的属性值、方法，并进行操作。如果获取的属性或方法不存在，可以通过设置默认值来处理。


getattr(self.model, order_by_field)

作用：
动态获取模型类中指定的列对象

参数：

self.model：SQLAlchemy 模型类
order_by_field：字段名称（字符串）

返回值：
对应的 SQLAlchemy 列对象（如 Column 实例）

典型使用场景：

```python
# 获取 is_traitor 列对象
column = getattr(MonitorAccountStats, 'is_traitor')
```

### issubclass 和 isinstance 函数

检查类型

http://c.biancheng.net/view/2298.html


### eval()

eval() 是 Python 中的一个内置函数，它的作用是将字符串表达式作为代码执行，并返回执行结果。其基本语法如下：

```python
eval(expression, globals=None, locals=None)
```
其中 expression 是要求值的字符串表达式，globals 和 locals 是可选参数，用于指定全局和局部命名空间。如果 globals 参数未给定，则会使用当前全局命名空间；如果 locals 参数未给定，则会使用当前局部命名空间。

下面是一些示例说明：

```python
# 整数加法表达式
x = eval('1 + 2')
print(x)  # 输出 3

# 浮点数运算表达式
y = eval('3.4 * 5.6')
print(y)  # 输出 19.04

# 字符串拼接表达式
s = eval('"hello, " + "world!"')
print(s)  # 输出 hello, world!

# 变量计算表达式
a = 10
b = 20
c = eval('a + b')
print(c)  # 输出 30

# 使用 globals 和 locals 参数
x = 1
y = 2
z = eval("x + y", {'x': 10, 'y': 20})  # 指定 globals 参数
print(z)  # 输出 30

def myfunc():
    x = 3
    y = 4
    z = eval("x + y", None, {'x': 10, 'y': 20})  # 指定 locals 参数
    print(z)  # 输出 30

myfunc()
```

需要注意的是，eval() 函数可以执行任意的 Python 表达式，包括函数调用、模块导入等高级语法，因此在使用时应该谨慎考虑安全性。
不当使用 eval() 可能会造成代码注入等安全问题。



### any()

any()是Python内置函数之一，它用于判断一个可迭代对象中是否有元素为真(True)。

语法：

any(iterable)
参数iterable是可迭代对象，如列表、元组、集合、生成器等。当该可迭代对象中至少有一个元素为真(True)时，函数返回True；否则，函数返回False。

示例:
```python
# 列表中有元素为真
my_list = [0, '', False, None, [], (), 1]
print(any(my_list))  # 输出True

# 列表中所有元素都为假
my_list2 = [0, '', False, None, [], ()]
print(any(my_list2))  # 输出False

# 迭代器中存在元素为真
def my_gen():
    yield 0
    yield ''
    yield False
    yield None
    yield []
    yield ()
    yield 1
    
gen = my_gen()
print(any(gen))  # 输出True

# 迭代器中所有元素都为假
def my_gen2():
    yield 0
    yield ''
    yield False
    yield None
    yield []
    yield ()
    
gen2 = my_gen2()
print(any(gen2))  # 输出False
```

以上代码中，我们定义了两个列表和两个生成器，其中第一个列表和第一个生成器包含了一个元素为真的值，而第二个列表和第二个生成器中所有元素都为假。分别使用any()函数对这四个可迭代对象进行判断，得到的结果分别为True和False。

### reversed()

reversed()是 Python 内置函数之一，用于返回一个反向迭代器对象，即按照与原序列相反的顺序迭代序列中的元素。它可以用于字符串、列表、元组等可迭代对象，但不支持字典和集合。

下面是它的语法示例：

```Python
reversed(seq)
其中，seq 是一个可迭代对象，如字符串、列表或元组。

以下是使用 reversed() 函数的示例：

Python
string = "hello world"
for char in reversed(string):
    print(char)

# 输出: 
# d
# l
# r
# o
# w
#  
# o
# l
# l
# e
# h

lst = [1, 2, 3, 4]
for num in reversed(lst):
    print(num)

# 输出:
# 4
# 3
# 2
# 1

```
在这两个示例中，我们使用 reversed() 将一个字符串和一个列表以相反的顺序进行迭代，并打印每个元素。

请注意，在第一个示例中，字符串中的空格也被视为元素并打印出来了。


### enumerate()

enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。


语法：

enumerate(sequence, [start=0])

参数：

sequence -- 一个序列、迭代器或其他支持迭代对象。
start -- 下标起始位置的值。

```bash
>>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
>>> list(enumerate(seasons, start=1))       # 下标从 1 开始
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]


>>> seq = ['one', 'two', 'three']
>>> for i, element in enumerate(seq):
...     print i, element
...
0 one
1 two
2 three

```


