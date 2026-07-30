## 2.2 结构化输出：JSON Schema 约束设计

Structured Output 的灵魂是 Schema。Schema 写得好不好，直接决定模型输出稳不稳。

### 一个最小可用的 Schema

```json
{
  "type": "object",
  "properties": {
    "intent": {
      "type": "string",
      "enum": ["退款", "咨询", "投诉", "其他"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "keywords": {
      "type": "array",
      "items": {"type": "string"}
    }
  },
  "required": ["intent", "confidence"],
  "additionalProperties": false
}
```

要点：

- `enum`：把开放文本变成有限选项，模型几乎不会乱写，强烈推荐用于分类、路由。
- `required`：声明必填项。模型偶尔会漏字段，靠它兜底。
- `additionalProperties: false`：禁止模型额外塞字段，解析更干净。
- 数值加 `minimum/maximum`，字符串加 `pattern`（正则）能进一步约束。

### 设计原则（实战经验）

1. **扁平优于嵌套**：`{"a": {"b": {"c": 1}}}` 远不如 `{"a_b_c": 1}` 稳定。嵌套越深，模型越易跑偏。
2. **枚举优先**：能用 enum 表达的分类、状态、类型，绝不让模型自由发挥。
3. **字段名用拼音/英文短词**：中文长字段名（如 `用户是否已登录`）在 JSON 里易被截断或转义出错，建议 `is_logged_in`。
4. **给每个字段加 `description`**：模型会读 description 理解语义，写清楚「这个字段是什么、取值含义」，准确率明显提升。
5. **数组项也要约束**：`items` 里别只写 `{"type": "string"}`，能加 enum/pattern 就加上。

### 反例 vs 正例

反例（太松）：

```json
{
  "type": "object",
  "properties": {
    "result": {"type": "string"}
  }
}
```

模型可能返回一整段话塞进 `result`，等于没约束。

正例（收紧）：

```json
{
  "type": "object",
  "properties": {
    "result": {
      "type": "string",
      "enum": ["success", "need_clarify", "fail"],
      "description": "任务结果：success=已完成，need_clarify=需向用户追问，fail=执行失败"
    },
    "reply": {"type": "string", "description": "返回给用户的最终话术"}
  },
  "required": ["result", "reply"],
  "additionalProperties": false
}
```

### 复杂对象的取舍

当业务对象真的复杂（如一份合同），不要指望一次让模型吐出 50 个字段的完美 JSON。更稳的做法是：

- 拆成多步抽取，每步只抽一小块；
- 或用「先抽取关键字段 + 再针对性补充」的两阶段提示词。

Schema 是给模型「减负」的，不是越全越好。
