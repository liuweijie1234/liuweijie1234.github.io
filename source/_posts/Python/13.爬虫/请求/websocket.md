---
title: Python3 WebSocket 客户端（websocket-client / websockets）
date: 2026-07-30 10:00:00
tags:
- Python
- 爬虫
- WebSocket
categories:
- Python
---

## 说明

WebSocket 是基于 TCP 的全双工协议（`ws://` / `wss://`），常用于行情推送、弹幕、实时消息等场景。
Python 常用两个库：

| 库 | 风格 | 安装 |
| --- | --- | --- |
| `websocket-client` | 同步，API 简单 | `pip install websocket-client` |
| `websockets` | asyncio 异步 | `pip install websockets` |

## websocket-client（同步）

### 短连接：收发一次

```python
import websocket

ws = websocket.create_connection("wss://echo.websocket.events")
ws.send("hello")
print(ws.recv())
ws.close()
```

### 长连接：回调模式（爬虫常用）

```python
import websocket

def on_open(ws):
    print("连接建立")
    ws.send("subscribe")            # 通常在这里发送订阅消息

def on_message(ws, message):
    print("收到:", message)

def on_error(ws, error):
    print("错误:", error)

def on_close(ws, code, msg):
    print("连接关闭")

ws = websocket.WebSocketApp(
    "wss://echo.websocket.events",
    header={"User-Agent": "Mozilla/5.0"},   # 可自定义握手请求头
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
ws.run_forever(ping_interval=30)            # 定时发 ping 保活
```

## websockets（异步）

```python
import asyncio
import websockets

async def main():
    async with websockets.connect("wss://echo.websocket.events") as ws:
        await ws.send("hello")
        async for message in ws:            # 持续接收
            print(message)

asyncio.run(main())
```

## 爬虫实战要点

- 抓包：浏览器开发者工具 Network 面板筛选 **WS**，查看握手请求头和消息帧。
- 握手常需携带 `Origin`、`Cookie`、`User-Agent` 等头，否则被拒绝。
- 消息内容可能是 JSON、二进制（protobuf）或压缩数据（gzip/deflate），需按站点协议解析。
- 断线重连 + 心跳（ping/pong）是长连接采集的标配。
