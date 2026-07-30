---
title: Python3 time 模块
date: 2026-07-30 10:00:00
tags:
- Python module
categories:
- Python
---

## 说明

`time` 是处理时间的标准库，围绕三种时间表示：

1. **时间戳（timestamp）**：1970-01-01 00:00:00 UTC 至今的秒数，float。
2. **struct_time**：含年月日时分秒等 9 个字段的结构化时间。
3. **格式化字符串**：如 `2026-07-30 10:00:00`。

更面向对象的日期处理见 {% post_link Python/6.标准库/datetime %}。

## 常用函数

```python
import time

time.time()          # 当前时间戳: 1785376800.123
time.localtime()     # 当前本地 struct_time
time.gmtime()        # 当前 UTC struct_time
time.sleep(1)        # 休眠 1 秒
```

## 三种表示互转

```python
import time

ts = time.time()

# 时间戳 -> struct_time
st = time.localtime(ts)

# struct_time -> 格式化字符串
time.strftime("%Y-%m-%d %H:%M:%S", st)     # '2026-07-30 10:00:00'

# 格式化字符串 -> struct_time
st = time.strptime("2026-07-30 10:00:00", "%Y-%m-%d %H:%M:%S")

# struct_time -> 时间戳
time.mktime(st)
```

常用格式符：`%Y` 年、`%m` 月、`%d` 日、`%H` 时、`%M` 分、`%S` 秒、`%w` 星期。

## 计时：perf_counter 优于 time

```python
import time

start = time.perf_counter()      # 高精度单调时钟，适合测耗时
do_something()
print(f"耗时 {time.perf_counter() - start:.4f}s")

time.monotonic()     # 单调时钟，不受系统改时间影响，适合超时判断
time.process_time()  # 仅统计本进程 CPU 时间（不含 sleep）
```

> `time.time()` 受系统时间同步（NTP）影响可能回拨，测耗时应使用 `perf_counter()`。
