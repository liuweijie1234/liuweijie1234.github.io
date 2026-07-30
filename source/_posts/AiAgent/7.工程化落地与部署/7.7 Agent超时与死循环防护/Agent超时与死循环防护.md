## 7.7 Agent 超时与死循环防护

生产环境最怕两件事：Agent 卡死不返回（超时）、Agent 转圈停不下来（死循环）。必须有硬防护。

### 1. 死循环的常见成因

- 模型反复调用同一工具，观察结果没推进思考；
- 没有明确的终止信号（没约定 `finish`）；
- 工具一直返回「需要更多信息」，模型陷进去；
- 多 Agent 互相推翻，永远达不成一致（见「多 Agent 冲突解决」）。

### 2. 步数上限（最基础的护栏）

```python
MAX_STEPS = 8
for step in range(MAX_STEPS):
    action = llm_decide(...)
    if action == "finish":
        return answer
    obs = run_tool(action)
# 超过上限，强制终止并兜底
return fallback("任务未能在限定步数内完成，请简化问题或联系人工")
```

### 3. 超时控制

- **单步超时**：每个工具调用 / 模型调用设 timeout，超时即报错走降级；
- **整体超时**：整个 Agent 运行设全局 deadline（如 60s），到点强制返回已完成部分或兜底。
- 代码执行（沙箱）尤其要限时长 + 限资源，防恶意/失控代码卡死。

```python
import asyncio
try:
    answer = await asyncio.wait_for(run_agent(q), timeout=60)
except asyncio.TimeoutError:
    answer = fallback("处理超时，请稍后重试")
```

### 4. 循环检测

- **重复检测**：记录近期行动序列，若连续 N 步动作相同且观察无变化 → 判定卡死，强制跳出；
- **相似度检测**：连续两轮「思考内容」高度相似，说明在空转，提前终止。

### 5. 兜底策略

终止后绝不能「报错给用户看」，要有优雅降级：

- 返回「部分结果 + 说明未完成」；
- 转人工 / 提示用户换种问法；
- 记录 trace 供后续优化（这一步往往是提示词需要改进的信号）。

### 经验口诀

任何 Agent 循环都必须有「**步数上限 + 单步超时 + 循环检测 + 优雅兜底**」四件套。没有这四样的 Agent，绝不允许上生产。
