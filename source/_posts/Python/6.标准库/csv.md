---
title: Python3 操作csv文件
date: 2022-12-12 09:04:00
tags:
- Python
categories:
- Python
---

CSV ，中文叫做逗号分隔值或字符分割值，其文件以纯文本形式存储表格数据


## 背景

工作时候有些数据是CSV形式存储，处理数据前，先处理下csv的数据格式

[Excel科学计数法转换成文本完整显示: 分列](https://blog.csdn.net/dongyuxu342719/article/details/79401140)

## 写入

### 利用csv写入

列表数据

```python
import csv

with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)  # 默认以逗号分隔每条记录
    # writer = csv.writer(csvfile, delimiter=' ')  # delimiter 参数修改分隔符
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'Mike', '20'])  # writerow 写入一行数据
    writer.writerows([['10002', 'Bob', '21'],['10003', 'Jordan', '22']])  # writerows 同时写入多行
```

字典数据

```python
import csv

with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:  # 若有中文写入需要声明编码
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '10001', 'name': 'Mike', 'age': '20'})
    writer.writerow({'id': '10002', 'name': 'Bob', 'age': '21'})
    writer.writerow({'id': '10003', 'name': 'Jordan', 'age': '22'})
    writer.writerow({'id': '10004', 'name': '乔丹', 'age': '23'})

```

### 利用pandas写入

```python
import pandas as pd

data = [
    {'id': '10001', 'name': 'Mike', 'age': '20'},
    {'id': '10002', 'name': 'Bob', 'age': '21'},
    {'id': '10003', 'name': 'Jordan', 'age': '22'}
]

df = pd.DataFrame(data)
df.to_csv('data.csv', index=False)
```

## 读取

### 利用csv读取


```python
import csv

with open('data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
```

```python
import csv
 
filename='C:\\Users\\lenovo\\Desktop\\parttest.csv'
data = []
with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    #header = next(csv_reader)        # 读取第一行每一列的标题
    for row in csv_reader:            # 将csv 文件中的数据保存到data中
        data.append(row[5])           # 选择某一列加入到data数组中
    print(data)
```
或者使用DictReader，第一行即作为标签。
 
```python
import csv
 
with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    column = [row['weight'] for row in reader]   # weight 同列的数据
print(column)
```

### 利用numpy读取

```python
import numpy as np
data = np.loadtxt(open("文件路径.csv","rb"),delimiter=",",skiprows=n,usecols=[2,3]) 
```

delimiter是分隔符，skiprows是跳过前n行，usecols是使用的列数，例子中读取的是3,4列。

### 利用pandas读取

```python
import pandas as pd
data = pd.read_csv(r'C:\Users\lenovo\Desktop\parttest.csv',sep=',',delimiter=None,header='infer',usecols=[5])
```

sep 相当于上面的 delimiter，是分隔符。
delimiter ，它属于备用的分隔符(csv用不同的分隔符分隔数据)。
header 是列名，是每一列的名字，如果header=1，将会以第二行作为列名，读取第二行以下的数据。
usecols 同上，是读取第几列。

值得注意的是，例如，我们查看某个值，print(data[1])，是会报错的。我们可以借由下面程序。

data 是 DataFrame 类型需要进一步转化为列表或者元组

```python
array=data.values[0::,0::]  #读取全部行，全部列
print(array)              #array是数组形式存储，顺序与data读取的数据顺序格式相同
print(type(array))  # numpy.ndarray

data_list=data.values.tolist()
print(data_list)
print(type(data_list))  # list
```

```python
import pandas as pd

df = pd.read_csv(r'data.csv')

for index,row in df.iterrows():
    print(row.tolist())
```