---
title: Python3 模块 Json
date: 2022-08-15 10:22:00
tags:
- Python module
- Json
categories:
- Python
---

参考：https://blog.csdn.net/qq_46293423/article/details/105785007

## 简介

JSON，全称为 JavaScript Object Notation, 也就是 JavaScript 对象标记，它通过对象和数组的组合来表示数据，构造简洁但是结构化程度非常高，是一种轻量级的数据交换格式。


## json数据类型

何支持的类型都可以通过 JSON 来表示，例如字符串、数字、对象、数组等，但是对象和数组是比较特殊且常用的两种类型，下面简要介绍一下它们。


- **对象**：

它在 JavaScript 中是使用花括号 {} 包裹起来的内容，数据结构为 `{key1：value1, key2：value2, ...}` 的键值对结构。

在面向对象的语言中，key 为对象的属性，value 为对应的值。

键名可以使用整数和字符串来表示。值的类型可以是任意类型。

- **数组**：

数组在 JavaScript 中是方括号 [] 包裹起来的内容，数据结构为 `["java", "javascript", "vb", ...]` 的索引结构。

在 JavaScript 中，数组是一种比较特殊的数据类型，它也可以像对象那样使用键值对，但还是索引用得多。
同样，值的类型可以是任意类型。

所以，一个 JSON 对象可以写为如下形式：

```json
[
  {
    name: "Bob",
    gender: "male",
    birthday: "1992-10-18",
  },
  {
    name: "Selina",
    gender: "female",
    birthday: "1995-10-18",
  },
];
```

由中括号包围的就相当于列表类型，列表中的每个元素可以是任意类型，这个示例中它是字典类型，由大括号包围。



## 数据类型区别

Json 的数据类型和 Python 数据类型的区别

| Python | Json |
| -- | -- |
| dict | object |
| list,tuple | array |
| str,unicode | string |
| int,long,float | number |
| True | true |
| False | false |
| None | null |

## Json 的方法

| 方法 | 作用 |
| -- | -- |
| **json.dumps()** | 将 Python 对象(列表/字典) 编码成 Json 字符串 |
| json.dump() | 将 Python 中的对象 转化成 Json 储存到文件中 |
| **json.loads()** | 将 Json 字符串(需使用双引号) 解码成 Python 对象(列表/字典), 常用于解析接口,读取json |
| json.load() | 将文件中的 Json 的格式 转化成 Python 对象提取出来 |


```python
import json

list_demo = [{'name': 'Bob', 'gender': 'male', 'birthday': '1992-10-18'}, {'name': 'Selina', 'gender': 'female', 'birthday': '1995-10-18'}]

print(type(list_demo))  # <class 'list'>
data = json.dumps(list_demo)
print(data)  # [{"name": "Bob", "gender": "male", "birthday": "1992-10-18"}, {"name": "Selina", "gender": "female", "birthday": "1995-10-18"}]
print(type(data))  # <class 'str'>
```

```python
import json

data = [{
    'name': 'Bob',
    'gender': 'male',
    'birthday': '1992-10-18'
}]
with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=2))  # indent ，代表缩进字符个数

```


```python
import json

data = [{
    'name': '王伟',
    'gender': '男',
    'birthday': '1992-10-18'
}]
with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))  # ensure_ascii=False,支持输出中文
    # json.dump(data, open('data.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

```

```python
import json

str = '''
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
'''

print(type(str))  # <class'str'>
data = json.loads(str)
print(data)  # [{'name': 'Bob', 'gender': 'male', 'birthday': '1992-10-18'}, {'name': 'Selina', 'gender': 'female', 'birthday': '1995-10-18'}]
print(type(data))  # <class 'list'>
```

```python
import json

with open('data.json', encoding='utf-8') as file:
    str = file.read()
    data = json.loads(str)
    print(data)
```


### json.dump()和json.dumps()的区别

json.dumps() 是把 Python 对象转换成 Json 对象的一个过程，生成的是字符串。

json.dump() 是把 Python 对象转换成 Json 对象生成一个fp的文件流，和文件相关。

### json.dumps

将 Python 对象编码成 Json 字符串，单引号变成双引号(Json)

```python
json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)
```


```python
import json
x = {'name':'你猜','age':19,'city':'四川'}

print(json.dumps(x))
{"name": "\u4f60\u731c", "age": 19, "city": "\u56db\u5ddd"}
```

- 参数详解

| 参数 | 说明 |
| -- | -- |
| obj | 就是你要转化成json的对象。 |
| skipkeys=True | 默认值是False，如果dict的keys内的数据不是python的基本类型(str,unicode,int,long,float,bool,None)，设置为False时，就会报TypeError的错误。此时设置成True，则会跳过这类key 。 |
| ensure_ascii=True | 默认输出ASCLL码，如果把这个该成False,就可以输出中文。 |
| check_circular=True | 如果check_circular为false，则跳过对容器类型的循环引用检查，循环引用将导致溢出错误(或更糟的情况)。 |
| allow_nan=True | 如果allow_nan为假，则ValueError将序列化超出范围的浮点值(nan、inf、-inf)，严格遵守JSON规范，而不是使用JavaScript等价值(nan、Infinity、-Infinity)。 |
| **cls=None** | **用于解决 json 不能转换的类型数据报错** |
| indent = 2 | 参数根据数据格式缩进显示，读起来更加清晰。 |
| separators=(',',':') | 是分隔符的意思，参数意思分别为不同dict项之间的分隔符和dict项内key和value之间的分隔符，把：和，后面的空格都除去了。 |
| encoding | 编码 |
| default="utf-8" | efault(obj)是一个函数，它应该返回一个可序列化的obj版本或引发类型错误。默认值只会引发类型错误。 |
| sort_keys=True | 是告诉编码器按照字典排序(a到z)输出。如果是字典类型的python对象，就把关键字按照字典排序。 |

#### 报错

- json.dumps 报错：TypeError: Object of type 'datetime' is not JSON serializable

json模块根本没有定义如何转换datetime 和 date类型的数据


```python
import json

class CJsonEncoder(json.JSONEncoder):
    """
    将datetime或者date数据类型转化为json字符串
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


data = json.dumps(data, cls=CJsonEncoder)
```


### json.dump

```python
json.dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True,allow_nan=True, cls=None, indent=None, separators=None,default=None, sort_keys=False, **kw)
```

json.dump() 和 json.dumps() 就是多了一个fp的文件参数


### json.load()和json.loads()的区别

json.loads()是针对内存对象，将string转换为dict。

json.load()针对文件句柄，将json格式的字符转换为dict，从文件中读取 (将string转换为dict)

### json.loads()

```python

import json

x = {'name':'你猜','age':19,'city':'四川'}

#用dumps将python编码成json字符串
x = json.dumps(x)
print(x)
'{"name": "\\u4f60\\u731c", "age": 19, "city": "\\u56db\\u5ddd"}'


#用loads将json编码成python
print(json.loads(x))
{'name': '你猜', 'age': 19, 'city': '四川'}
```


### json.load()


```python
import json

x = {'name':'你猜','age':19,'city':'四川'}

filename = 'pi_x.txt'
with open (filename,'w') as f:
    json.dump(x,f)
with open (filename) as f_1:
    print(json.load(f_1))

```
