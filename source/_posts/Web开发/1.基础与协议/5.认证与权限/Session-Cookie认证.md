---
title: Session-Cookie 认证
date: 2026-07-30 13:35:00
tags:
- 认证
- Session
- Cookie
categories:
- Web开发
- 基础与协议
---

## 一、流程回顾

Session-Cookie 是 Web 最经典的**有状态**认证：服务端存会话，客户端持 `sessionid`。详见 `1.请求与响应/cookie与session.md`。

## 二、登录链路

1. 客户端提交账号密码（HTTPS）。
2. 服务端校验，生成 `session_id`，会话数据存 Redis。
3. 响应 `Set-Cookie: sessionid=xxx; HttpOnly; Secure; SameSite=Lax`。
4. 后续请求自动带 Cookie，服务端据 `session_id` 取会话，识别用户。

## 三、Django/Flask 的实现

- Django：`django.contrib.sessions` + `django.contrib.auth`；`login(request, user)` 写入会话。
- Flask：`Flask-Login` 管理 `session['_user_id']`。

## 四、安全要点

- Cookie 必须 `HttpOnly`（防 XSS 窃取）、`Secure`（仅 HTTPS）、`SameSite=Lax/Strict`（缓解 CSRF）。
- 会话存 Redis，设较短过期 + 滑动续期。
- 登录失败限流，防暴力破解。
- 注销/改密后**失效旧 session**（删除服务端记录）。
- 会话固定攻击防护：登录成功后轮换 `session_id`。

## 五、与 JWT 的取舍

- 单机/传统 Web 站点：Session-Cookie 简单、易注销。
- 多端/无状态 API、移动端：JWT 更合适（见 `OAuth2概览.md`、`2.Web框架/3.FastAPI/5.安全与认证`）。

## 六、最佳实践

- 全程 HTTPS，敏感操作二次校验。
- 集中会话存储，避免进程内 Session 导致多实例失效。
- 高危操作（改密码、转账）重新认证。
