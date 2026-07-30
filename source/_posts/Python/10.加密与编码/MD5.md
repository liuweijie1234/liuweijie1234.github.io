---
title: Python3 MD5 与哈希摘要（hashlib）
date: 2026-07-30 10:00:00
tags:
- Python
- 加密
categories:
- Python
---

## 说明

MD5 是一种**摘要算法（哈希算法）**，输入任意长度数据，输出固定 128 位（32 位十六进制字符串）摘要。
特点：不可逆、输入相同则输出相同、输入微小变化输出差异巨大。

> 安全提示：MD5 已被证明可以构造碰撞，**不应再用于密码存储和安全签名**，密码场景推荐 `hashlib.pbkdf2_hmac`、`bcrypt` 等；MD5 仍常用于文件校验、缓存 key、去重指纹。

## 基本用法

```python
import hashlib

# 注意：必须传 bytes，字符串需先 encode
m = hashlib.md5()
m.update("hello world".encode("utf-8"))
print(m.hexdigest())   # 5eb63bbbe01eeed093cb22bb8f5acdc3

# 一行写法
print(hashlib.md5(b"hello world").hexdigest())
```

## 分块更新（大文件校验）

`update()` 可以多次调用，等价于拼接后一次计算：

```python
import hashlib

def file_md5(path, chunk_size=8192):
    m = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            m.update(chunk)
    return m.hexdigest()
```

## 加盐（salt）

为防止彩虹表攻击，对密码类数据加盐后再哈希：

```python
import hashlib

def md5_with_salt(text: str, salt: str) -> str:
    return hashlib.md5((text + salt).encode("utf-8")).hexdigest()
```

## 其他常用摘要算法

```python
import hashlib

hashlib.sha1(b"data").hexdigest()     # 160 位
hashlib.sha256(b"data").hexdigest()   # 256 位，目前更推荐
hashlib.sha512(b"data").hexdigest()

# HMAC：带密钥的消息认证码，常用于接口签名
import hmac
sig = hmac.new(b"secret_key", b"message", hashlib.sha256).hexdigest()
```

## 密码存储推荐做法

```python
import hashlib, os

salt = os.urandom(16)
dk = hashlib.pbkdf2_hmac("sha256", b"password", salt, iterations=100_000)
print(dk.hex())
```
