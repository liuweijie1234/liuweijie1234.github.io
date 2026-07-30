---
title: Python3 Unicode 与字符编码
date: 2026-07-30 10:00:00
tags:
- Python
- 编码
categories:
- Python
---

## 基本概念

- **Unicode**：字符集，为每个字符分配唯一码点（如 `汉` 是 `U+6C49`）。
- **UTF-8 / GBK 等**：编码方式，规定码点如何存成字节。UTF-8 中英文占 1 字节、中文一般占 3 字节。
- Python3 中 `str` 是 Unicode 字符串，`bytes` 是字节串，两者必须显式转换。

## encode / decode

```python
s = "中文"

b = s.encode("utf-8")        # str -> bytes
# b'\xe4\xb8\xad\xe6\x96\x87'

b.decode("utf-8")            # bytes -> str
# '中文'

s.encode("gbk")              # b'\xd6\xd0\xce\xc4'（GBK 中文占 2 字节）
```

编码与解码使用的字符集必须一致，否则报错或乱码：

```python
s.encode("utf-8").decode("gbk")
# UnicodeDecodeError 或得到乱码

# 容错处理
b"\xe4\xb8".decode("utf-8", errors="ignore")    # 忽略非法字节
b"\xe4\xb8".decode("utf-8", errors="replace")   # 用 � 替换
```

## ord / chr：字符与码点互转

```python
ord("A")       # 65
ord("汉")      # 27721
chr(27721)     # '汉'
hex(ord("汉")) # '0x6c49'
```

## Unicode 转义

```python
"\u6c49"                 # '汉'，\u 后跟 4 位十六进制码点
"汉".encode("unicode_escape")          # b'\\u6c49'
b"\\u6c49".decode("unicode_escape")    # '汉'
```

爬虫中常见的 `\uXXXX` 形式响应，可以用 `unicode_escape` 或 `json.loads` 还原：

```python
import json
json.loads('"\\u6c49\\u5b57"')   # '汉字'
```

## 文件读写编码

```python
# 显式指定 encoding，避免不同平台默认编码不一致
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("中文")

with open("a.txt", "r", encoding="utf-8") as f:
    print(f.read())
```

## 常见问题

- `UnicodeEncodeError`：str 转 bytes 时目标编码不支持该字符（如用 ASCII 编码中文）。
- `UnicodeDecodeError`：bytes 转 str 时字节序列不符合指定编码，确认数据真实编码（可用 `chardet`/`charset-normalizer` 检测）。
