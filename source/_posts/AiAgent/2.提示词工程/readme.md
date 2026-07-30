Agent 能力的核心杠杆，直接决定智能体的表现

基础方法论：角色设定、指令结构化、Few-shot 示例、输出格式约束
进阶推理：思维链 CoT、思维树 ToT、自我校验、反幻觉引导
Agent 专用 Prompt：ReAct 模式写法、Plan-and-Execute 规划 Prompt、Reflexion 反思 Prompt
踩坑与优化：常见失效场景、幻觉抑制、鲁棒性提升技巧


02_提示词工程
├── 2.1 提示词基础
│   ├── 角色、指令、上下文、输出格式
│   ├── 少样本提示（Few-shot）
│   └── 思维链（Chain-of-Thought）
├── 2.2 高级技巧
│   ├── 结构化输出（JSON Mode）
│   ├── 自洽性（Self-Consistency）
│   └── 元提示词（Meta Prompting）
└── 2.3 Agent中的提示词模板
    ├── 工具调用的系统提示词设计
    ├── ReAct风格提示词模板
    └── 动态提示词组装策略