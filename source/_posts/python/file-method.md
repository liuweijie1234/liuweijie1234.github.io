---
title: Python3 文件
date: 2022-08-13 16:14:00
tags:
- Python
- python file
categories:
- Python
---


# 数据类型 - 文件


```python
open(file, mode='r', buffering=None, encoding=None, errors=None, newline=None, closefd=Tr
```

r：以**只读**方式打开文件，意思就是只能读取文件内容，不能写入文件内容。这是默认模式。
rb：以二进制只读方式打开一个文件，通常用于打开二进制文件，比如音频、图片、视频等等。
r+：以**读写**方式打开一个文件，既可以读文件又可以写文件。
rb+：以二进制读写方式打开一个文件，同样既可以读又可以写，但读取和写入的都是二进制数据。
w：以写入方式打开一个文件。如果该文件已存在，则将其覆盖。如果该文件不存在，则创建新文件。
wb：以二进制写入方式打开一个文件。如果该文件已存在，则将其覆盖。如果该文件不存在，则创建新文件。
w+：以读写方式打开一个文件。如果该文件已存在，则将其覆盖。如果该文件不存在，则创建新文件。
wb+：以二进制读写格式打开一个文件。如果该文件已存在，则将其覆盖。如果该文件不存在，则创建新文件。
a：以**追加**方式打开一个文件。如果该文件已存在，文件指针将会放在文件结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，则创建新文件来写入。
ab：以二进制追加方式打开一个文件。如果该文件已存在，则文件指针将会放在文件结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，则创建新文件来写入。
a+：以读写方式打开一个文件。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，则创建新文件来读写。
ab+：以二进制追加方式打开一个文件。如果该文件已存在，则文件指针将会放在文件结尾。如果该文件不存在，则创建新文件用于读写。


## 文件对象

```python
f = open('/Users/liuweijie/Python/python-study/md5', mode='r')
print(f)
#<_io.TextIOWrapper name='/Users/liuweijie/Python/python-study/md5' mode='r' encoding='UTF-8'>
```

```python
with open("md5.txt") as f:
    for line in f:
        print(line)
```


```python
with open('movies.txt', 'w', encoding='utf-8') as file:
    file.write(f'名称: {name}\n')
    file.write(f'类别: {categories}\n')
    file.write(f'上映时间: {published_at}\n')
    file.write(f'评分: {score}\n')
```


## 文件属性

```python
f.name #文件名
f.mode #modes: r,w,a,x
```

## 读取文件内容

```python
f.read(n)     #从文件读取指定的字节数
f.readline(n) #读取一整行，包括 "\n" 字符
f.readlines() #读取所有行并返回列表
f.seek(0)     #移动文件读取指针到指定位置
```

## 写入文件

```python
f.write("str") #将字符串写入文件，返回的是写入的字符长度。
```

## 关闭文件

```python
f.flush() #刷新文件内部缓冲，直接把内部缓冲区的数据立刻写入文件, 而不是被动的等待输出缓冲区写入。
f.close() #关闭文件
```


### 文件读写

读写文件是最常见的 IO 操作，Python 内置了读写文件的函数。

```python
file = open('/users/a/abc.txt', 'r')    # r表示读
file.read()     # 会读取出文件的内容并加载到内存
file.close()    # 关闭文件，否则会占用资源，操作系统同一时间能打开的文件数量也是有限的
```

由于文件读写时可能产生 IOError，所以我们需要进行处理：

```python
try:
    f = open('/path/to/file', 'r')
    print(f.read())
finally:
    if f:
        f.close()
        
# 使用with语句  
with open('/path/to/file', 'r') as f:
    print(f.read())        
```

写文件：

```python
file = open('/users/a/abc.txt', 'w')
file.write('Hello world')
file.close()

# 使用with, 如果以w模式则会进行覆盖，如果是追加则以'a'模式写入
with open('/Users/a/abc.txt', 'w') as f:
    f.write('Hello, world!')
    
```

### 操作文件和目录

操作文件和目录的函数一部分放在 os 模块中，一部分放在 os.path 中：

```python
# 查看当前目录的绝对路径:
os.path.abspath('.')   # '/Users/a'
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
os.path.join('/Users/a', 'testdir')  # '/Users/a/testdir'
# 然后创建一个目录:
os.mkdir('/Users/a/testdir')
# 删掉一个目录:
os.rmdir('/Users/a/testdir')
# 对文件重命名
os.rename('test.txt', 'test.py')
# 删除文件
os.remove('test.py')
```

### 序列化

把变量从内存中编程可存储或传输的过程称之为序列化，在 Python 中叫 pickling，Python 提供了 pickle 模块来实现序列化。

```python
import pickle
d = dict(name='Bob', age=20, score=88)
file = open('/users/a/desktop/as.txt', 'wb')
pickle.dump(d, file)
pickle.close()
# ü}q (X   nameqX   BobqX   ageqKX   scoreqKXu.

# 反序列化, 注意序列化后一定要close，否则会报错EOFError
file = open('/users/a/desktop/as.txt', 'rb')
d = pickle.load(file)
file.close()
print(d)
```



### 上下文


https://bk.tencent.com/s-mart/community/question/1121?type=answer


## 文件读取


[python 多线程文件读取](http://www.daimazhu.com/etagid8133b0/)


[python 多线程/进程文件读取](https://www.cnblogs.com/gongyanzh/p/14820926.html)

[python 多线程读取同一个文件](https://blog.csdn.net/lingerlanlan/article/details/45699931)



## 实例


```python
import requests
from pyquery import PyQuery as pq
import re

url = 'https://ssr1.scrape.center/'
html = requests.get(url).text
doc = pq(html)
items = doc('.el-card').items()

file = open('movies.txt', 'w', encoding='utf-8')
for item in items:
    # 电影名称
    name = item.find('a > h2').text()
    file.write(f'名称: {name}\n')
    # 类别
    categories = [item.text() for item in item.find('.categories button span').items()]
    file.write(f'类别: {categories}\n')
    # 上映时间
    published_at = item.find('.info:contains(上映)').text()
    published_at = re.search('(\d{4}-\d{2}-\d{2})', published_at).group(1) \
        if published_at and re.search('\d{4}-\d{2}-\d{2}', published_at) else None
    file.write(f'上映时间: {published_at}\n')
    # 评分
    score = item.find('p.score').text()
    file.write(f'评分: {score}\n')
    file.write(f'{"=" * 50}\n')
file.close()
```
