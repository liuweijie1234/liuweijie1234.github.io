---
title: Python3 模块 pymaongo
date: 2024-01-10 10:00:00
tags:
- Python module
- pymaongo
categories:
- Python
---


## 安装

```bash
pip3 install pymongo
```

## 使用

### 插入数据

- 插入单条数据

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)  # 连接数据库
# 连接数据库方法二：client = pymongo.MongoClient('mongodb://localhost:27017/')

db = client.test  # 指定数据库，数据库名称为 test
# 指定数据库方法二：db = client['test']

collection = db.students  # 指定集合，集合名称为 students
# 指定集合方法二：collection = db['students']


student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
result = collection.insert_one(student)
print(result)  # <pymongo.results.InsertOneResult object at 0x00000236137150F0>
print(result.inserted_id)  # 65b2159c1d26473b4cba352c
```

- 插入多条数据

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students


student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}
result = collection.insert_many([student1, student2])
print(result)
print(result.inserted_ids)

```


### 查询数据

- 查询单条数据

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

result = collection.find_one({'name': 'Mike'})
print(result)  # {'_id': ObjectId('65b2185b7d328fca05781735'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
print(type(result))  # <class 'dict'>

```

- 查询多条数据

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

results = collection.find({'name': 'Jordan'})
# results = collection.find({'age': {'$gt': 20}})  # 查询 age 大于 20的数据
print(results)  # <pymongo.cursor.Cursor object at 0x0000017618139978>
print(type(results))  #pymongo.cursor.Cursor

for result in results:
    print(result)
"""
{'_id': ObjectId('65b2159c1d26473b4cba352c'), 'id': '20170101', 'name': 'Jordan', 'age': 20, 'gender': 'male'}
{'_id': ObjectId('65b2185b7d328fca05781734'), 'id': '20170101', 'name': 'Jordan', 'age': 20, 'gender': 'male'}
"""
```


**比较符号**

| 符号 | 含义 | 实例 |
| -- | -- | -- |
| $lt | 小于  | `{'age': {'$lt': 20}}` |
| $gt | 大于 | `{'age': {'$gt': 20}}` |
| $lte | 小于等于 | `{'age': {'$lte': 20}}` |
| $gte | 大于等于 | `{'age': {'$gte': 20}}` |
| $ne | 不等于 | `{'age': {'$ne': 20}}` |
| $in | 在范围内 | `{'age': {'$in': [20, 23]}}` |
| $nin | 不在范围内 | `{'age': {'$nin': [20, 23]}}` |


**功能符号**
| 符号 | 含义 | 实例 | 实例含义 |
| -- | -- | -- | -- |
| $regex | 匹配正则表达式 | `{'name': {'$regex': '^M.*'}}` | name 以 M 为开头 |
| $exists | 属性是否存在 | `{'name': {'$exists': True}}` | 存在 name 属性 |
| $type | 类型判断 | `{'age': {'$type': 'int'}}` | age 的类型为 int |
| $mod | 数字模操作 | `{'age': {'$mod': [5, 0]}}` | age 模 5 余 0 |
| $text | 文本查询 | `{'$text': {'$search': 'Mike'}}` | text 类型的属性中包含 Mike 字符串 |
| $where | 高级条件查询 | `{'$where': 'obj.fans_count == obj.follows_count'}` | 自生粉丝数等于关注数 |


#### 计数

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

# results = collection.count_documents({'name': 'Jordan'})  # 带条件的计数
results = collection.estimated_document_count()  # 不带条件的计数==统计该表有多少数据
print(results)
print(type(results))
```
[Python3 pymongo 使用 count 报警告解决办法](https://blog.csdn.net/W_chuanqi/article/details/126083837)


#### 排序

pymongo.ASCENDING 升序
pymongo.DESCENDING 降序

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

results = collection.find().sort('age', pymongo.ASCENDING)  # 升序
# results = collection.find().sort('age', pymongo.DESCENDING)  # 降序

for result in results:
    print(result)
"""
{'_id': ObjectId('65b2159c1d26473b4cba352c'), 'id': '20170101', 'name': 'Jordan', 'age': 20, 'gender': 'male'}
{'_id': ObjectId('65b2185b7d328fca05781735'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
{'_id': ObjectId('65b2185b7d328fca05781734'), 'id': '20170102', 'name': 'Jordan2', 'age': 23, 'gender': 'male'}
"""
```

#### 偏移

skip(n) 方法偏移位置

skip(1), 忽略前1个元素，获取第二个及以后的元素

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

results = collection.find().sort('age', pymongo.ASCENDING).skip(1)

for result in results:
    print(result)

'''
{'_id': ObjectId('65b2185b7d328fca05781735'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
{'_id': ObjectId('65b2185b7d328fca05781734'), 'id': '20170102', 'name': 'Jordan2', 'age': 23, 'gender': 'male'}
'''
```

limit(n) 指定获取个数

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

results = collection.find().sort('age', pymongo.ASCENDING).skip(1).limit(1)

for result in results:
    print(result)
'''
{'_id': ObjectId('65b2185b7d328fca05781735'), 'id': '20170202', 'name': 'Mike', 'age': 21, 'gender': 'male'}
'''

```


### 更新数据

- 更新单条数据

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

condition = {'age': 20}

student = collection.find_one(condition)

student['name'] = 'Liuweijie'
result = collection.update_one(condition, {'$set': student}, upsert=True)  # update_one 需要配合 {'$set': student} 更新使用  , upsert=True 存在即更新，不存在即插入
print(result)
print(result.matched_count, result.modified_count)  # matched_count匹配的数据条数，modified_count 影响的数据条数
'''
<pymongo.results.UpdateResult object at 0x000002704A36AE10>
1 1
'''

```


- 更新多条数据

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

condition = {'age': {'$gt': 20}}

result = collection.update_many(condition, {'$inc': {'age': 1}})  # {'$inc': {'age': 1}} 对 age 加1
print(result)
print(result.matched_count, result.modified_count)
'''
<pymongo.results.UpdateResult object at 0x0000029A308F9DA0>
2 2
'''

```

### 删除数据


- 删除一条数据

```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

result = collection.delete_one({'age': 20})
print(result)
print(result.deleted_count)
'''
<pymongo.results.DeleteResult object at 0x000001DB777CAA90>
1
'''
```

- 删除多条数据


```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

result = collection.delete_many({'age': {'$gt': 20}})
print(result)
print(result.deleted_count)
'''
<pymongo.results.DeleteResult object at 0x000002C915899AC8>
2
'''
```

### 复合操作

find_one_and_delete : 查找并删除满足查询条件的单个数据

```python
result = collection.find_one_and_delete({"key": "value"})
```

find_one_and_replace ： 查找并替换满足查询条件的单个数据
```python
result = collection.find_one_and_replace({"key": "value"}, {"new_key": "new_value"})
```

find_one_and_update ： 查找并更新满足查询条件的单个数据
```python
result = collection.find_one_and_update({"key": "value"}, {"$set": {"new_key": "new_value"}})
```

### 索引

#### 创建索引

create_index(keys, options=None, session=None, **kwargs) : 用于在MongoDB集合中创建一个索引

create_indexes(indexes, session=None, **kwargs) : 用于在MongoDB集合中创建多个索引

#### 删除索引

drop_index(index_or_name, session=None, **kwargs) : 用于删除MongoDB集合中的一个索引