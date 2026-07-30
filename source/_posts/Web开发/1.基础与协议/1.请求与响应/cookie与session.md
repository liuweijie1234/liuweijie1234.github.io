---
title: Cookie 与 Session
date: 2026-07-30 13:00:00
tags:
- Cookie
- Session
- 认证
categories:
- Web开发
- 基础与协议
---

## 一、为什么需要它们

HTTP 是**无状态**协议，每次请求相互独立。但业务需要「记住用户是谁」（登录态），于是有了 Cookie 与 Session。

## 二、Cookie

Cookie 是**服务器通过响应头 Set-Cookie 下发、浏览器存储并随后续同域请求自动带上**的小文本。

```
Set-Cookie: sessionid=abc123; Path=/; HttpOnly; Secure; SameSite=Lax
```

特点：
- 存储在客户端，大小受限（约 4KB/个）。
- 每次请求自动携带，过多会拖慢请求。
- 关键安全属性：`HttpOnly`（防 JS 读取/XSS 偷）、`Secure`（仅 HTTPS 传）、`SameSite`（防 CSRF）。

## 三、Session

Session 是**服务端保存的用户状态**，客户端只持有一个 ID（通常存 Cookie 里）。

流程：
1. 用户登录成功，服务端生成 `session_id`，把会话数据存服务端（内存/Redis/DB）。
2. 通过 `Set-Cookie: sessionid=xxx` 把 ID 交给浏览器。
3. 后续请求带上 Cookie，服务端据 `session_id` 取出会话。

## 四、存储方案

- **内存**：简单，但多进程/重启即丢，不适合生产。
- **Redis**（推荐）：集中、可持久、快，适合多实例。
- **数据库**：持久但慢。

## 五、与 JWT 的区别

| 维度 | Session | JWT |
|------|---------|-----|
| 状态 | 服务端有状态 | 无状态（token 自带信息） |
| 注销 | 删服务端记录即可 | 需黑名单或等过期 |
| 扩展性 | 依赖共享存储 | 天然易扩展 |

详见 `5.认证与权限/OAuth2概览.md` 与 `5.认证与权限/Session-Cookie认证.md`。

## 六、最佳实践

- Cookie 必须 `HttpOnly` + `Secure` + `SameSite`。
- Session 数据放 Redis，设合理过期。
- 不在 Cookie/Session 放大敏感信息。
- 注销时同时清服务端 Session 与客户端 Cookie。
