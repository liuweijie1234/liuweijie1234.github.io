---
title: Tornado WebSocket
date: 2026-07-30 12:30:00
tags:
- Tornado
- WebSocket
categories:
- Web开发
- Tornado
---

## 一、WebSocket 场景

WebSocket 提供**全双工长连接**，适合聊天、实时推送、行情。Tornado 对 WebSocket 支持极好，是其经典用例。

## 二、服务端

```python
import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        self.connections.add(self)
        print('client connected')

    async def on_message(self, message):
        await self.write_message(f'echo: {message}')

    def on_close(self):
        self.connections.discard(self)

    def check_origin(self, origin):
        return True   # 生产按域名校验
```

## 三、路由注册

```python
app = tornado.web.Application([
    (r'/ws', EchoWebSocket),
])
```

## 四、广播

```python
@classmethod
def broadcast(cls, msg):
    for c in list(cls.connections):
        c.write_message(msg)
```

## 五、鉴权与关闭

- 在 `open()` 里校验 token（从 `self.request` 取 query/header）。
- `on_close()` 清理连接、释放资源。
- 用心跳 ping/pong 检测断线。

## 六、最佳实践

- 生产 `check_origin` 严格校验来源，防跨站 WebSocket。
- 连接集合要线程安全，Tornado 单线程下一般无碍，但注意 `run_in_executor` 回调里别直接操作。
- 海量连接时注意内存与各连接状态。
