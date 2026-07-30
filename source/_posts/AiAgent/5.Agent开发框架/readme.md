快速落地 Agent 的工具集，避免重复造轮子

LangChain：核心组件（LLM/Tool/Memory/Chain/Agent）、内置 Agent 类型、链式调用设计
LangGraph：状态管理、节点与边设计、分支循环、人机介入、状态持久化
多 Agent 框架：CrewAI 角色化开发、AutoGen 协作模式、MetaGPT 工程化思想、选型对比
LlamaIndex：侧重 RAG 的 Agent 开发、数据连接器使用

05_Agent开发框架
├── 5.1 LangGraph
│   ├── StateGraph概念（状态、节点、边）
│   ├── 条件分支与路由
│   ├── 多步骤持久化与回溯
│   └── 可视化调试（LangSmith集成）
├── 5.2 LangChain
│   ├── AgentExecutor旧模式分析
│   ├── Tool与Toolkit抽象
│   └── 与LangGraph的对比选型
├── 5.3 LlamaIndex
│   ├── 数据连接器与索引
│   └── 基于Agent的查询引擎
├── 5.4 其他框架
│   ├── Dify（可视化编排）
│   ├── Coze（快速实验）
│   └── AutoGen / CrewAI 初览
└── 5.5 框架内部机制剖析
    ├── 提示词自动拼装原理
    └── Token缓存与加速