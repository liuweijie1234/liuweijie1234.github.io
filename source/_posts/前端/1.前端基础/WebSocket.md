---
title: Vue 使用 WebSocket
date: 2023-11-28 09:30:00
tags:
- websocket
- Vue
- 前端基础
categories:
- 前端
- 前端基础
---

# WebSocket 使用

WebSocket 是全双工通信协议，在单个 TCP 连接上提供客户端与服务端的双向实时通道，适用于聊天、实时数据推送、监控大屏等场景。

> 协议介绍：[ws 协议详解](https://blog.csdn.net/sanmi8276/article/details/119995481)

## 1. 原生 API

```js
const ws = new WebSocket('wss://example.com/ws')

ws.onopen = () => {
  console.log('连接已建立')
  ws.send(JSON.stringify({ type: 'hello' }))
}
ws.onmessage = (e) => {
  console.log('收到消息:', e.data)
}
ws.onclose = () => console.log('连接关闭')
ws.onerror = (e) => console.error('发生错误', e)
```

相比 HTTP 轮询，WebSocket 建立连接后服务端可主动推送，延迟更低、开销更小。

## 2. 在 Vue3 中封装为 Composable

推荐把连接逻辑抽成 `useWebSocket` 组合式函数，配合 `ref` 响应式管理状态：

```ts
// composables/useWebSocket.ts
import { ref, onUnmounted } from 'vue'

export function useWebSocket(url: string) {
  const ws = ref<WebSocket>()
  const messages = ref<string[]>([])
  const status = ref<'connecting' | 'open' | 'closed'>('connecting')

  ws.value = new WebSocket(url)
  ws.value.onopen = () => (status.value = 'open')
  ws.value.onmessage = (e) => messages.value.push(e.data)
  ws.value.onclose = () => (status.value = 'closed')

  const send = (data: string) => ws.value?.send(data)

  onUnmounted(() => ws.value?.close())

  return { messages, status, send }
}
```

组件中使用：

```vue
<script setup lang="ts">
import { useWebSocket } from '@/composables/useWebSocket'
const { messages, status, send } = useWebSocket('wss://example.com/ws')
</script>

<template>
  <div>状态：{{ status }}</div>
  <ul><li v-for="(m, i) in messages" :key="i">{{ m }}</li></ul>
  <button @click="send('ping')">发送</button>
</template>
```

## 3. 断线重连要点

- 在 `onclose` / `onerror` 中用 `setTimeout` 延迟重连，并设置最大重试次数。
- 建议心跳机制（定时 `send('ping')`），避免代理/网关因空闲断开。
- 生产环境优先 `wss://`（TLS 加密），与 HTTPS 页面同源策略兼容。
