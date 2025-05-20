---
title: Python3 模块 pymsyql
date: 2024-01-04 10:00:00
tags:
- Python module
- pymsyql
categories:
- Python
---


## 安装

```bash
pip3 install pymysql
```

## 使用

### 连接数据库

```python
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306)  # 声明mysql连接对象db
cursor = db.cursor()  # cursor方法获取mysql的操作游标
cursor.execute('SELECT VERSION()')  # 利用游标可以执行sql语句，execute方法执行语句
data = cursor.fetchone()  # fetchone方法获取第一条数据
print(f'Database Version:{data}')
cursor.execute('CREATE DATABASE spiders DEFAULT CHARACTER SET utf8mb4')
db.close()
```

### 创建表


需要指定库，不然报错 `pymysql.err.OperationalError: (1046, 'No database selected')`

```python
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()

create_table_sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL,' \
                   'age INT NOT NULL, PRIMARY KEY (id))'
cursor.execute(create_table_sql)
db.close()
```

### 插入数据

```python
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()

data = {
    'id': '20240105',
    'name': 'bob',
    'age': 20
}
table = 'students'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))
insert_sql = f'INSERT INTO {table}({keys}) values({values})'

try:
    if cursor.execute(insert_sql, tuple(data.values())):
        print('Successful')
        db.commit()
except Exception as err:
    print(f"Faild,{err}")
    db.rollback()
db.close()

```


### 更新数据

```python
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()

data = {
    'id': '20240105',
    'name': 'bob',
    'age': 21
}

table = 'students'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

sql = f'INSERT INTO {table}({keys}) values({values}) ON DUPLICATE KEY UPDATE '
update = ','.join(["{key} = %s".format(key=key) for key in data])
sql += update

try:
    if cursor.execute(sql, tuple(data.values())*2):
        print('Successful')
        db.commit()
except Exception as err:
    print(f"Faild,{err}")
    db.rollback()
db.close()

```

### 删除数据

```python
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()

table = 'students'
condition = 'age > 20'

sql = f'DELETE FROM {table} WHERE {condition}'

try:
    if cursor.execute(sql):
        print('Successful')
        db.commit()
except Exception as err:
    print(f"Faild,{err}")
    db.rollback()
db.close()
```

### 查询数据

```python
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()

table = 'students'
condition = 'age >= 20'

sql = f'SELECT * FROM {table} WHERE age >= 20'

try:
    cursor.execute(sql)
    print(f'count:{cursor.rowcount}')
    one = cursor.fetchone()
    print(f'one:{one}')
    results = cursor.fetchall()  # fetchall会将结果全部返回,数据量大的情况,占用系统性能
    print(f'results:{results}')
    print(f'results type:{type(results)}')
    for row in results:
        print(row)

except Exception as err:
    print(f"Faild,{err}")

db.close()

```


```python
try:
    cursor.execute(sql)
    print(f'count:{cursor.rowcount}')
    row = cursor.fetchone()
    
    while row:
        print(f'row:{row}')
        row = cursor.fetchone()

except Exception as err:
    print(f"Faild,{err}")
```