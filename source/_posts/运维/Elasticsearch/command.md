---
title: Elasticsearch 常用命令
date: 2022-08-15 15:11:00
tags:
- Elasticsearch
categories:
- Elasticsearch
---


### 查询和分析

- **定义您自己的搜索方式**

通过 Elasticsearch，您能够执行及合并多种类型的搜索（结构化数据、非结构化数据、地理位置、指标），搜索方式随心而变。先从一个简单的问题出发，试试看能够从中发现些什么。

- **分析大规模数据**

找到与查询最匹配的 10 个文档并不困难。但如果面对的是十亿行日志，又该如何解读呢？Elasticsearch 聚合让您能够从大处着眼，探索数据的趋势和规律。


### 常用命令

```bash
#如果有账号密码验证需要加： -u esuser:espassword
例如：curl -v  -u esuser:espassword  http://esip:esport/_cluster/health |jq  #其他请求同理

健康状态：curl -v http://esip:esport/_cluster/health |jq

列出所有索引:curl -s http://esip:esport/_cat/indices?v

列出所有索引详情:curl -v  http://esip:esport/_cluster/health?level=indices

新建索引：curl  -XPUT    http://esip:esport/indexname

查询索引：curl   http://esip:esport/indexname

删除索引：curl -XDELETE  http://esip:esport/indexname

修改索引：

关闭索引：curl -XPOST  -s http://esuser:espassword/indexname/_close

开启索引：curl -XPOST  -s http://esuser:espassword/indexname/_open
```


[ElasticSearch入门篇（保姆级教程）](https://www.cnblogs.com/coderxz/p/13268417.html)


