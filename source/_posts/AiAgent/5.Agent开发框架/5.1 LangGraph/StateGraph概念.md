## 5.1 LangGraph

LangGraph 是 LangChain 团队推出的**有状态、可循环**的 Agent 编排框架。它的核心思想：把 Agent 流程建模成一张**图（Graph）**。

### 核心概念：状态、节点、边

- **State（状态）**：贯穿整个流程的共享数据，通常是一个 TypedDict / Pydantic 对象（含 messages、中间结果等）。每次节点执行后返回的对 State 的「更新」会被合并。
- **Node（节点）**：一个函数，接收当前 State，返回对 State 的部分更新。节点可以是「调 LLM」「执行工具」「做判断」。
- **Edge（边）**：节点之间的连接，决定流转方向。分为普通边（无条件）和**条件边（Conditional Edge）**——根据 State 动态决定下一步去哪（如「还有工具要调吗？」）。

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

class State(TypedDict):
    messages: list          # 对话 + 工具调用记录
    step: int

def call_model(state):
    # 调 LLM，返回要追加的 messages
    return {"messages": [llm_response], "step": state["step"] + 1}

def call_tool(state):
    return {"messages": [tool_result]}

def should_continue(state):
    # 条件边：是否继续调工具
    if "finish" in last_message(state):
        return END
    return "call_tool"

builder = StateGraph(State)
builder.add_node("call_model", call_model)
builder.add_node("call_tool", call_tool)
builder.add_edge("call_tool", "call_model")        # 工具结果回模型
builder.add_conditional_edges("call_model", should_continue)
builder.set_entry_point("call_model")
graph = builder.compile()
```

### 条件分支与路由

条件边是 LangGraph 的精髓，让流程能「if/else」：按模型输出选择不同节点（如意图分类后路由到不同处理链）、按置信度决定是否人工介入。

### 多步骤持久化与回溯

- **Checkpointer**：用内存 / Redis / SQLite 保存每次执行的 State 快照。
- 价值：1）支持**断点续跑**（中途挂了从 checkpoint 恢复）；2）支持**回溯/时光机**（回到某一步重走）；3）多轮对话可按 `thread_id` 恢复上下文。
- 这是 LangGraph 相对普通 Chain 的最大优势——天然支持长任务的状态管理。

### 可视化调试（LangSmith）

- LangGraph 与 **LangSmith** 深度集成，可把每次节点执行、State 变化、token 消耗可视化为调用链，方便 debug 和评测。
- 没 LangSmith 也可用 `graph.get_graph().draw_mermaid()` 画出流程图。

### 适用场景

- 流程复杂、有循环/分支/人工介入的 Agent；
- 需要状态持久化、可恢复、可观测的生产系统；
- 多 Agent 协作（用一张大图串起多个子图）。

### 一句话

LangGraph = 用「图 + 状态」把 Agent 的循环、分支、持久化变得可控可观测，是构建生产级 Agent 的首选框架之一。
