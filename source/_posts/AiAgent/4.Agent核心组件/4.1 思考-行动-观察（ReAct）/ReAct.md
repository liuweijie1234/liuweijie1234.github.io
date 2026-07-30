## 4.1 思考-行动-观察（ReAct）

### 论文背景

ReAct 出自 2022 年 Google 论文 *《ReAct: Synergizing Reasoning and Acting in Language Models》*。核心洞见：让大模型**把「推理（Reasoning）」和「行动（Acting）」交错进行**，而不是先想完再干，或只干不想。

> 思考（Thought）引导行动，行动拿回观察（Observation），观察再修正思考——形成闭环。

### 为什么比纯 CoT 强

- 纯思维链（CoT）只在脑子里想，无法获取外部实时信息，容易事实错误；
- ReAct 能在思考中调用工具（搜索、查库、算数），用真实反馈纠正自己的推理；
- 过程可观察、可干预，更适合 Agent 场景。

### 完整循环（含伪代码）

```python
def react_loop(question, tools, max_steps=8):
    messages = [system_prompt_with(tools), {"role": "user", "content": question}]
    for step in range(max_steps):
        # 1. 模型产出「思考 + 行动」
        resp = llm(messages)
        thought, action, args = parse_action(resp)   # 解析出 工具名 + 参数
        # 2. 执行工具，得到「观察」
        if action == "finish":
            return args["answer"]
        obs = execute_tool(action, args)              # 真实调用
        # 3. 把 思考/行动/观察 回填，继续下一轮
        messages.append({"role": "assistant", "content": resp})
        messages.append({"role": "user", "content": f"观察：{obs}"})
    return "超过最大步数，未得出答案"
```

### 推理与行动的边界控制

- **何时该思考**：拿到观察后、决定下一步前，必须显式「思考」；工具结果越意外，越要停下来分析。
- **何时该行动**：需要外部信息/执行操作（查天气、算账、调 API）时才行动，别为「已知事实」硬调工具。
- **何时终止**：产出 `finish` 或达成目标即停；用 `max_steps` 硬上限防死循环（详见「超时与死循环防护」）。
- **边界护栏**：行动范围限定在已注册工具内，未授权动作直接拒绝，防止模型「自作主张」。

### 局限与补充

- ReAct 是单线串行，遇到要并行/多角色协作的任务，需要多 Agent 或状态图（见 LangGraph、多 Agent 系统）；
- 长任务里「思考」会占用大量 token，可配合摘要压缩。

### 小白一句话

ReAct = 让模型「边想边干、干了看结果、看了再想」，是把 LLM 变成能动手的 Agent 的最小可行范式。
