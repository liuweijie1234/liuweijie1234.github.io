---
title: Python3 jieba 中文分词
date: 2026-07-30 10:00:00
tags:
- Python
- 数据分析
categories:
- Python
---

## 说明

`jieba`（结巴分词）是最常用的中文分词库，支持三种分词模式、自定义词典和关键词提取。

```bash
pip install jieba
```

## 三种分词模式

```python
import jieba

text = "我来到北京清华大学"

# 1. 精确模式（默认，最常用）：试图将句子最精确地切开
print(jieba.lcut(text))
# ['我', '来到', '北京', '清华大学']

# 2. 全模式：把所有可能成词的词语都扫描出来，速度快但有冗余
print(jieba.lcut(text, cut_all=True))
# ['我', '来到', '北京', '清华', '清华大学', '华大', '大学']

# 3. 搜索引擎模式：在精确模式基础上对长词再切分，适合搜索索引
print(jieba.lcut_for_search(text))
# ['我', '来到', '北京', '清华', '华大', '大学', '清华大学']
```

> `jieba.cut()` 返回生成器，`jieba.lcut()` 直接返回列表。

## 自定义词典

```python
import jieba

jieba.lcut("小明毕业于中国科学院计算所")

# 动态添加/删除词
jieba.add_word("计算所")
jieba.del_word("计算所")

# 加载自定义词典文件（每行：词语 [词频] [词性]）
# userdict.txt 示例：
#   云计算 5 n
#   自然语言处理 10 n
jieba.load_userdict("userdict.txt")

# 调整词频，使某个词能（或不能）被切出
jieba.suggest_freq(("中", "将"), True)
```

## 关键词提取

```python
import jieba.analyse

text = "结巴分词是最好用的中文分词组件之一，支持关键词提取和词性标注"

# TF-IDF 算法
jieba.analyse.extract_tags(text, topK=5, withWeight=True)

# TextRank 算法
jieba.analyse.textrank(text, topK=5)
```

## 词性标注

```python
import jieba.posseg as pseg

for word, flag in pseg.cut("我爱北京天安门"):
    print(word, flag)
# 我 r（代词）
# 爱 v（动词）
# 北京 ns（地名）
# 天安门 ns
```

## 实战：词频统计（配合 Counter）

```python
import jieba
from collections import Counter

text = open("article.txt", encoding="utf-8").read()
words = [w for w in jieba.lcut(text) if len(w) > 1]   # 过滤单字与标点
print(Counter(words).most_common(10))
```
