## 1.2 API 调用基础

### 1.2.1 SDK 使用

Chat Completion API 详解

以 OpenAI SDK 为例，最核心的调用：

```python
from openai import OpenAI
client = OpenAI(api_key="sk-xxx")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一个智能助手。"},
        {"role": "user", "content": "解释AI Agent"}
    ],
    temperature=0.7,
    max_tokens=1024
)
print(response.choices[0].message.content)
```

关键参数说明：

- messages：角色包括 system（全局指令）、user（用户输入）、assistant（模型回复）、tool（工具调用结果）。
- temperature（0~2）：越高越随机，越低越确定。工具调用时建议 0~0.2 保证输出稳定。
- max_tokens：限制生成最大 Token 数，防止跑飞。
- stop：可指定停止词，常用于解析。
- response_format：需要 JSON 输出时设 {"type": "json_object"} 或使用结构化输出（Function Calling 专属）。

#### 异步调用示例

Agent 后端大多是异步框架（FastAPI、asyncio），给出 AsyncOpenAI 示例很必要：

```python
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key="sk-xxx")

async def get_response():
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}]
    )
    return response.choices[0].message.content
```
### 多模型适配（通过 base_url 切换）

你本地跑 Ollama 或私有化 vLLM 时，不用换 SDK，只需改 base_url + api_key：

```python
# Ollama
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# vLLM
client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")
```

#### API Key 安全管理
绝对不要硬编码！统一用环境变量：

```python
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```


#### 官方文档链接

必备参考：

OpenAI Chat API 文档：https://platform.openai.com/docs/api-reference/chat

Anthropic Messages API：https://docs.anthropic.com/en/api/messages

Ollama OpenAI兼容接口说明：https://github.com/ollama/ollama/blob/main/docs/openai.md


### 1.2.2 多轮对话上下文管理：

只需将整个对话历史追加到 messages 列表中，模型本身无状态：

```python
history = []
while True:
    user_input = input("用户：")
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=history
    )
    assistant_reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_reply})
    print(f"助手：{assistant_reply}")
```

#### 上下文窗口管理技巧：

- 每个模型都有最大上下文（如 128k），需要主动截断。
- 简单做法：保留最近 N 轮，或使用 Token 计数动态丢弃最早消息。
- Token 估算：中文 1 个字≈1.5~2 token，英文 1 词≈1.3 token。可用 tiktoken 库精确计算。
- Agent 常用截断策略：估算总 token 数，若超过模型上限的 80%，则从最早的非 system 消息开始丢弃；对工具返回的超长内容，可截取前 N 字符并追加 …[已截断] 标记。


### 1.2.3 流式输出（SSE）处理

后端代码（FastAPI 示例）：

```python
from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat(messages: list):
    async def generate():
        stream = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```
前端（Vue）接收：

```javascript
const response = await fetch('/chat', {
  method: 'POST',
  body: JSON.stringify({ messages }),
  headers: { 'Content-Type': 'application/json' }
});
const reader = response.body.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  // 按行解析 data: 开头的内容，更新界面
}
```
注意事项：

- 流式输出时，choices[0].delta 通常不包含 role，只有 content 片段。
- 需要在客户端累积字符串以显示完整消息。
- 一旦开启流式，无法使用 response.choices[0].message.content 一次性获取，除非非流式。


### 1.2.4 并发与限流(速率限制)

**为什么有限流？**
API 有 RPM（每分钟请求数）和 TPM（每分钟 Token 数）配额，不同模型/Tier 配额不同，超出后返回 429 错误。

#### 控制并发的常用手段：

1. 客户端限速（令牌桶/漏桶）：使用 asyncio.Semaphore 控制同时请求数。
2. 自动重试 + 指数退避（见 1.2.5）。
3. 合并请求：将多个 prompt 合并为一个调用，减少请求次数。

代码示例（异步并发控制）：

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()
sem = asyncio.Semaphore(10)  # 最多10个并发请求

async def limited_request(prompt):
    async with sem:
        return await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

# 批量调用
tasks = [limited_request(p) for p in prompts]
results = await asyncio.gather(*tasks, return_exceptions=True)
```

**查看额度**： 在 OpenAI Platform 的 Usage 页面，或通过 API https://api.openai.com/v1/usage 查询。


### 1.2.5 异常重试

调用 API 最常见的错误：

- RateLimitError（429）：并发太高或 QPS 超限，需指数退避重试。

- APIConnectionError / APIError：网络问题，可重试。

- InvalidRequestError：请求参数有误，直接检查参数，不重试。

重试装饰器示例：

```python
import time
from openai import RateLimitError, APIError

def retry_on_limit(max_retries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    wait = 2 ** i
                    print(f"限流，{wait}秒后重试...")
                    time.sleep(wait)
                except APIError as e:
                    if e.status_code >= 500:
                        wait = 2 ** i
                        print(f"服务错误，{wait}秒后重试...")
                        time.sleep(wait)
                    else:
                        raise
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**常见 HTTP 错误码速查表**

｜ 状态码 ｜ 含义 ｜ 处理策略 ｜
｜ -- ｜ -- ｜ -- ｜
｜ 401 ｜ 密钥无效 ｜ 检查 API Key / 环境变量 ｜
｜ 429 ｜ 速率限制 ｜ 指数退避重试，或降低并发 ｜
｜ 500 ｜ 服务器内部错误 ｜ 等待重试，可联系服务商｜
｜ 503 ｜ 服务不可用/过载 ｜ 等待重试｜

### 1.2.6 Token 计费与上下文窗口

**计费方式**：按 Prompt Token + Completion Token 分别计费。GPT-4o $2.50/$10 每 1M token（价格会变，需查官网）。

**窗口限制**：如 GPT-4o 上下文 128,000 token，超过后需截断或换模型。

**精确计数**：使用 tiktoken。

```python
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")
tokens = enc.encode("你的文本内容")
len(tokens)  # 返回 token 数
```
对于 Agent 开发，务必将对话历史总 Token 数限制在模型上限的 80% 以内，给工具返回留出空间。

### 1.2.7 工具调用初探

这是 Agent 调用外部工具的核心机制，后续在 04_Agent核心组件 中会深入，这里给出原生 API 的最小示例作为接口锚点。

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    tools=tools
)
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    print(tool_calls[0].function.name)      # "get_weather"
    print(tool_calls[0].function.arguments) # '{"city":"Beijing"}'
```

之后只需执行对应函数，将结果以 role: "tool" 回传给模型，即可完成一次工具调用闭环。