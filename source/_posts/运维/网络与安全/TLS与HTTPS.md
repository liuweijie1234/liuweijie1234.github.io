---
title: TLS 与 HTTPS
date: 2026-07-30 10:00:00
tags:
- 运维
- 网络
- 安全
- TLS
- HTTPS
categories:
- 运维
- 网络与安全
---

# TLS 与 HTTPS

HTTPS = HTTP over TLS，通过 TLS 协议提供数据加密、完整性校验与身份认证。理解握手流程与证书体系是运维排障的基础。

## TLS 握手流程

**TLS 1.2（约 2-RTT）：**

1. Client Hello：客户端发送支持的协议版本、加密套件、随机数。
2. Server Hello：服务端选定套件并返回随机数、证书。
3. 客户端校验证书，生成预主密钥（用服务端公钥加密发送）。
4. 双方基于随机数 + 预主密钥派生会话密钥，开始加密通信。

**TLS 1.3（1-RTT，支持 0-RTT）：**

- 精简握手，合并密钥交换，默认移除不安全的加密套件。
- 0-RTT：客户端在首次请求即可携带数据（需防范重放攻击）。

## 证书链与 CA

- **CA（证书颁发机构）**：受信任的根证书机构，操作系统/浏览器内置其根证书。
- **证书链**：站点证书 → 中间证书（Intermediate CA）→ 根证书。服务端需返回完整链，否则客户端校验失败。
- **自签证书**：自己充当 CA，仅用于测试，浏览器会告警。

## 证书格式

| 后缀 | 含义 |
| --- | --- |
| `.pem` | Base64 编码，可含证书或私钥（文本） |
| `.crt` | 证书文件，常为 PEM 格式 |
| `.key` | 私钥文件 |
| `.csr` | 证书签名请求 |
| `.pfx/.p12` | 含证书+私钥的 PKCS#12 包（常带密码） |

## 使用 OpenSSL 生成与校验

```bash
# 生成自签证书（测试用）
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout key.pem -out cert.pem -days 365 -subj "/CN=example.com"

# 查看证书
openssl x509 -in cert.pem -text -noout

# 测试连接并查看远端证书
openssl s_client -connect example.com:443 -servername example.com
```

详见 [OpenSSL](OpenSSL.md)。

## 证书自动续期（Let's Encrypt / certbot）

```bash
# 安装 certbot（以 Nginx 为例）
apt-get install -y certbot python3-certbot-nginx

# 申请证书并自动修改 Nginx 配置
certbot --nginx -d example.com -d www.example.com

# 手动申请（DNS 验证，适合无 80 端口）
certbot certonly --manual --preferred-challenges dns -d '*.example.com'

# 测试自动续期（证书 <30 天才会真正续）
certbot renew --dry-run

# 实际续期（通常加入 crontab 每日执行）
certbot renew
```

证书默认存于 `/etc/letsencrypt/live/<域名>/`，含 `fullchain.pem` 与 `privkey.pem`。

## 常见安全配置

- **HSTS**：响应头 `Strict-Transport-Security: max-age=31536000; includeSubDomains`，强制浏览器使用 HTTPS。
- **加密套件**：优先使用 ECDHE 密钥交换 + AES-GCM / CHACHA20，前向安全。
- **协议**：禁用 SSLv3、TLS 1.0/1.1，仅启用 TLS 1.2/1.3。
- **OCSP Stapling**：服务端缓存证书状态，减少客户端校验延迟。
- 使用 [SSL Labs](https://www.ssllabs.com/ssltest/) 评估配置强度。
