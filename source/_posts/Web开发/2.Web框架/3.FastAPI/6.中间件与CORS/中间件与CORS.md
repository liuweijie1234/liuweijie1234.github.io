---
title: FastAPI 中间件与 CORS
date: 2026-07-30 12:05:00
tags:
- FastAPI
- 中间件
- CORS
categories:
- Web开发
- FastAPI
---

## 一、中间件

中间件在每个请求前后执行，适合统一处理：日志、耗时、跨域、请求 ID、异常捕获。

```python
import time
from fastapi import Request

@app.middleware('http')
async def add_process_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers['X-Process-Time'] = str(time.perf_counter() - start)
    return response
```

`call_next(request)` 调用后续处理链，返回 `Response`。

## 二、CORS 跨域

浏览器同源策略会拦截跨域请求，需服务端声明允许的来源：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://example.com'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

- 开发可 `allow_origins=['*']`，但**生产不要**与 `allow_credentials=True` 同时用 `*`。
- 明确列出可信前端域名。

## 三、其他内置中间件

- `TrustedHostMiddleware`：防 Host 头攻击。
- `HTTPSRedirectMiddleware`：强制 HTTPS。
- `GZipMiddleware`：响应压缩。

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['example.com'])
```

## 四、自定义异常处理

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})
```

## 五、最佳实践

- 中间件保持轻量，重逻辑放到依赖或路由里。
- CORS 遵循最小权限，严格限定 `allow_origins`。
- 强制 HTTPS + TrustedHost 上线必备。
- 统一异常响应结构，便于前端处理。
