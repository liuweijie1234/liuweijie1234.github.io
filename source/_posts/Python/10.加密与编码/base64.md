---
title: Python3 模块 base64
date: 2022-08-15 10:22:00
tags:
- Python module
- base64
categories:
- Python
---

* Base64 是一种用 64 个字符来表示任意二进制数据的方法。

在蓝鲸项目中，部分接口的报文是通过 base64 加密传输的，
所以在进行接口自动化时，需要对所传的参数进行 base64 编码，对拿到的响应报文进行解码

例如：作业平台的 fast_execute_script(快速执行脚本)的 script_content

python3.x 中字符都为 unicode 编码，而 b64encode 函数的参数为 byte 类型，所以必须先转码。

```python
import base64
# encode 编码
# decode 解码
s ='adsvsdega15s1dasda'
encodestr = base64.b64encode(s.encode('utf-8'))
print(encodestr)
# b'YWRzdnNkZWdhMTVzMWRhc2Rh'
print(str(encodestr, 'utf-8'))
# YWRzdnNkZWdhMTVzMWRhc2Rh

decodestr = base64.b64decode(encodestr)
print(decodestr)
# b'adsvsdega15s1dasda'
print(str(decodestr, 'utf-8'))
# adsvsdega15s1dasda
```