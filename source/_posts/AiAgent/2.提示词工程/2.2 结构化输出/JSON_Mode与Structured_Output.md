## 2.2 结构化输出：JSON Mode 与 Structured Output

### 为什么 Agent 必须要结构化输出

Agent 内部经常要把模型返回结果喂给代码解析，典型场景：

- 工具调用：模型返回「要调用 search 工具，参数是 `{'query': '北京天气'}`」，代码要能 parse 出来。
- 分类路由：模型返回「意图 = 退款」，代码 `if intent == 'refund'` 走不同分支。
- 多字段抽取：从合同里抽出 `{甲方, 乙方, 金额, 有效期}`。

如果模型吐的是一段自然语言散文，代码根本没法稳定解析。所以「让模型吐出固定格式」是 Agent 工程的刚需。

### 方案一：JSON Mode（JSON 模式）

OpenAI 等厂商提供的开关，强制模型只输出合法 JSON：

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一个信息抽取器，只输出 JSON。"},
        {"role": "user", "content": "从这句话抽取：张三在2024年1月1日向李四借了5000元。"}
    ],
    response_format={"type": "json_object"}  # 关键：开启 JSON 模式
)
print(resp.choices[0].message.content)
# {"借款人": "张三", "出借人": "李四", "金额": 5000, "日期": "2024-01-01"}
```

注意点：

- JSON Mode 只保证「格式是合法 JSON」，**不保证字段名和类型符合你的预期**，你仍然要在 prompt 里写清楚要哪些字段。
- 部分模型（如早期 gpt-3.5）开启后可能和你「说话」变得很生硬，这是正常的。
- 国内很多兼容 OpenAI 接口的模型也支持该参数，但稳定性参差，要做容错。

### 方案二：Structured Output（结构化输出 / 严格模式）

比 JSON Mode 更强：你给一份 JSON Schema，模型**保证**输出严格符合该 Schema（字段不漏、类型不错、必填项齐全）。

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    skills: list[str]

resp = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": "描述一下名叫王五、30岁、会Python和SQL的人"}],
    response_format=Person,   # 直接传 Pydantic 模型
)
person = resp.choices[0].message.parsed  # 已经是 Python 对象，不用自己 json.loads
print(person.name, person.age, person.skills)
```

Structured Output 的本质是：服务端先校验，若模型产出不合规就拒绝/重试，直到拿到符合 Schema 的结果再返回。这样就从「概率性正确」变成了「结构性保证」。

### 二者怎么选

| 维度 | JSON Mode | Structured Output |
| -- | -- | -- |
| 保证程度 | 仅保证是合法 JSON | 保证符合 Schema（字段/类型/必填） |
| 使用成本 | 低，传个开关即可 | 需定义 Schema（Pydantic/JSON Schema） |
| 适用场景 | 简单、字段不固定的抽取 | 强类型、要直接进代码的解析 |

小白建议：能用 Structured Output 就用它，省去大量解析容错代码；老模型不支持时退回 JSON Mode + 手动校验。

### 常见坑

- 开了 JSON Mode 却没在 prompt 里声明字段 → 模型自己瞎编字段名，解析报错。
- Schema 里用 `enum` 约束枚举值，比让模型「自由写」稳定得多。
- 嵌套过深、字段过多的 Schema 会让模型更容易出错，尽量扁平化。
