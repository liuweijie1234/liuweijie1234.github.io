---
title: OAuth2 概览
date: 2026-07-30 13:40:00
tags:
- OAuth2
- 认证
- 授权
categories:
- Web开发
- 基础与协议
---

## 一、OAuth2 是什么

OAuth2 是**授权框架**（也常用于认证，叠加 OpenID Connect）。它允许用户把**有限权限**委托给第三方应用，而不泄露自己的密码。

常见场景：用 GitHub/微信登录第三方网站。

## 二、四种授权模式

| 模式 | 适用 |
|------|------|
| 授权码（Authorization Code） | 有后端的 Web 应用（最安全，推荐） |
| 授权码 + PKCE | 公开客户端（SPA/移动端） |
| 密码模式（Resource Owner Password） | 第一方可信应用（已不推荐） |
| 客户端凭证（Client Credentials） | 服务到服务 |

## 三、授权码流程（简化）

1. 客户端引导用户到授权服务器：`/authorize?client_id=...&redirect_uri=...&scope=...&state=...`。
2. 用户登录并同意授权。
3. 授权服务器回调 `redirect_uri?code=xxx`。
4. 客户端用 `code` + `client_secret` 换取 `access_token`（和 `refresh_token`）。
5. 客户端持 `access_token` 调资源服务器 API。

## 四、Token 与 JWT

- `access_token`：短期有效，调接口用。
- `refresh_token`：长期，用于换发新 access_token。
- token 可以是**不透明随机串**（需 introspection 校验）或 **JWT**（自包含、自校验，见 FastAPI 教程）。

## 五、与 OpenID Connect

OIDC 在 OAuth2 之上加 `id_token`（JWT），提供**身份认证**标准（`profile`/`email` scope）。

## 六、最佳实践

- 优先授权码 + PKCE，避免密码模式。
- `redirect_uri` 严格白名单，防跳转泄露 code。
- `state` 防 CSRF；`scope` 最小授权。
- access_token 短时效，敏感资源用 `scope` 细分权限。
- 详见各框架实现：`2.Web框架/3.FastAPI/5.安全与认证`、`2.Web框架/2.Flask/8.认证与授权`。
