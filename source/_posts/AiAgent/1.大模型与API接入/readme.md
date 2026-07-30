01_大模型与API调用接入
├── 1.1 主流模型选型
│   ├── 闭源模型：GPT-4o, Claude 3.5, Gemini
│   ├── 开源模型：DeepSeek, Llama 3, Qwen
│   └── 本地部署方案：Ollama, vLLM, LM Studio
├── 1.2 API调用基础
│   ├── Chat Completion API 详解
│   ├── 流式输出（SSE）处理
│   ├── 异常重试与速率限制
│   └── Token计费与上下文窗口
└── 1.3 多模态调用
    ├── 视觉理解（图生文）
    └── 语音接口概述（Whisper, TTS）

底层基础，所有 Agent 的算力底座

模型选型对比：闭源模型（GPT-4o/Claude/DeepSeek 等）、开源模型（Llama/Qwen/GLM 等）的特性、适用场景、能力差异
API 基础调用：SDK 使用、多轮对话上下文管理、流式输出、并发与限流
成本与窗口：Token 计费规则、上下文窗口限制、Token 估算与截断策略
开源部署：Ollama/vLLM 本地部署、私有化模型调用适配
