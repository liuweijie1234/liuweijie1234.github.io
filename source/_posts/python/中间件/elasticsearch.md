---
title: Python3 模块 elasticsearch
date: 2022-08-15 10:22:00
tags:
- Python module
- elasticsearch
categories:
- Python
---


### 准备工作

```bash
pip3 install elasticsearch
```


### 使用 Python 操作 Elasticsearch


#### 创建索引

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()  # 默认连接本地9200端口
"""
es = Elasticsearch(
    ['https://[username:password@]hostname:port'],
    verify_certs=True, # 是否验证 SSL 证书
)
"""
result = es.indices.create(index='news', ignore=400)
print(result)

```

#### 删除索引

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()
result = es.indices.delete(index='news', ignore=[400, 404])
print(result)
```


#### 插入数据

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()
es.indices.create(index='news', ignore=400)

data = {
  'title': '乘风破浪不负韶华，奋斗青春圆梦高考',
  'url': 'http://view.inews.qq.com/a/EDU2021041600732200'
}
result = es.create(index='news', id=1, body=data)
# es.index(index='news', body=data)
print(result)
```

#### 更新数据

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()
data = {
    'title': '乘风破浪不负韶华，奋斗青春圆梦高考',
    'url': 'http://view.inews.qq.com/a/EDU2021041600732200',
    'date': '2021-07-05'
}
result = es.update(index='news', body=data, id=1)
# es.index(index='news', body=data, id=1)
print(result)
```

#### 删除数据

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()
result = es.delete(index='news', id=1)
print(result)
```


#### 查询数据

对于中文来说，我们需要安装一个分词插件，这里使用的是 elasticsearch-analysis-ik，
其 GitHub 链接为 https://github.com/medcl/elasticsearch-analysis-ik。

这里我们使用 Elasticsearch 的另一个命令行工具 elasticsearch-plugin 来安装，

这里安装的版本是 7.13.2，请确保和 Elasticsearch 的版本对应起来，命令如下：

elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.13.2/elasticsearch-analysis-ik-7.13.2.zip



```python
# 创建索引 并 指定需要分词的字段
from elasticsearch import Elasticsearch

es = Elasticsearch()
mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}
es.indices.delete(index='news', ignore=[400, 404])
es.indices.create(index='news', ignore=400)
result = es.indices.put_mapping(index='news', body=mapping)
print(result)
```




```python
# 插入数据 以供查询
from elasticsearch import Elasticsearch

es = Elasticsearch()

datas = [
    {
        'title': '高考结局大不同',
        'url': 'https://k.sina.com.cn/article_7571064628_1c3454734001011lz9.html',
    },
    {
        'title': '进入职业大洗牌时代，“吃香”职业还吃香吗？',
        'url': 'https://new.qq.com/omn/20210828/20210828A025LK00.html',
    },
    {
        'title': '乘风破浪不负韶华，奋斗青春圆梦高考',
        'url': 'http://view.inews.qq.com/a/EDU2021041600732200',
    },
    {
        'title': '他，活出了我们理想的样子',
        'url': 'https://new.qq.com/omn/20210821/20210821A020ID00.html',
    }
]

for data in datas:
    es.index(index='news', body=data)

result = es.search(index='news')
print(result)
```

```python
# 查询数据
from elasticsearch import Elasticsearch
import json

dsl = {
    'query': {
        'match': {
            'title': '高考 圆梦'
        }
    }
}

es = Elasticsearch()
result = es.search(index='news', body=dsl)
print(result)
```