---
title: Python3 模块 datetime
date: 2022-08-15 10:22:00
tags:
- Python module
- datetime
categories:
- Python
---

* datetime 是 Python 处理日期和时间的标准库。

Python 对日期时间数据的处理
https://bk.tencent.com/s-mart/community/question/917?type=answer



datetime.date.today()
```python

from datetime import datetime, timedelta

from django.utils import timezone

# 获取当前时间
now = timezone.now()


# 计算5天前的时间
five_days_ago = now - timedelta(days=5)

# 计算5天后的时间
five_days_later = now + timedelta(days=5)

# 格式化日期
print(now.strftime('%Y-%m-%d %H:%M:%S'))

```