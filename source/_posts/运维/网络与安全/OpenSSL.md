---
title: OpenSSL
date: 2026-07-30 10:00:00
tags:
- 网络与安全
categories:
- 运维
- 网络与安全
---

# OpenSSL

OpenSSL 是常用的加密工具库与命令行工具，运维中常用于生成密钥、签发证书、测试 TLS 连接、加解密文件等。

## 安装

```bash
# 查看版本（注意 1.1.1 之后为 3.x，命令行为 openssl）
openssl version

# Debian/Ubuntu
apt-get install -y openssl

# RHEL/CentOS
yum install -y openssl openssl-devel
```

Windows 安装可参考：https://www.cnblogs.com/dingshaohua/p/12271280.html

## 密钥与证书生成

```bash
# 生成 RSA 私钥（2048 位，无密码保护）
openssl genrsa -out key.pem 2048

# 生成带密码保护的私钥
openssl genrsa -aes256 -out key.pem 2048

# 从私钥提取公钥
openssl rsa -in key.pem -pubout -out pub.pem

# 生成证书签名请求 CSR
openssl req -new -key key.pem -out req.csr \
  -subj "/C=CN/ST=Beijing/L=Beijing/O=MyOrg/CN=example.com"

# 自签证书（一步到位，常用于测试）
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=example.com"
```

## 查看与校验

```bash
# 查看证书内容
openssl x509 -in cert.pem -text -noout

# 查看 CSR 内容
openssl req -in req.csr -text -noout

# 校验证书与私钥是否匹配（哈希应一致）
openssl x509 -in cert.pem -noout -modulus | openssl md5
openssl rsa  -in key.pem  -noout -modulus | openssl md5

# 测试与远端 TLS 握手
openssl s_client -connect example.com:443 -servername example.com
```

## 格式转换

```bash
# PEM -> DER
openssl x509 -in cert.pem -out cert.der -outform DER

# PEM -> PFX/P12（含私钥，需设置导出密码）
openssl pkcs12 -export -in cert.pem -inkey key.pem -out cert.pfx

# PFX -> PEM
openssl pkcs12 -in cert.pfx -out cert.pem -nodes
```

## 加解密与摘要

```bash
# 文件对称加密（AES-256-CBC），输出密码提示
openssl enc -aes-256-cbc -salt -in file.txt -out file.enc
openssl enc -d -aes-256-cbc -in file.enc -out file.txt

# 计算摘要
openssl dgst -sha256 file.txt
```

## 常见用途

- 生成自签证书用于测试环境 HTTPS。
- 排查 HTTPS 握手失败（用 `s_client` 看证书链与服务端配置）。
- 证书格式互转（Nginx 用 PEM，Tomcat 常需 PFX/JKS）。
- 校验公私钥配对、证书有效期。

更多 TLS/HTTPS 配置参见 [TLS 与 HTTPS](TLS与HTTPS.md)。
