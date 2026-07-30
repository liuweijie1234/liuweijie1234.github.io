后端服务：FastAPI/Django 封装 Agent 接口、SSE/WebSocket 流式输出、Celery 异步任务
前端交互：Vue 对话界面开发、流式渲染、Markdown / 代码高亮、Agent 执行流程可视化
存储与中间件：业务数据库设计、Redis 缓存、RabbitMQ/Kafka 消息队列
可观测性：LangSmith/Langfuse 接入、调用链追踪、Token 成本统计、错误监控
部署运维：Docker 容器化、Docker Compose 编排、私有化部署、高可用架构


07_工程化落地与部署
├── 7.1 服务封装
│   ├── FastAPI 封装Agent接口
│   ├── 流式响应（SSE/WebSocket）
│   └── 异步任务与后台作业
├── 7.2 容器化与云部署
│   ├── Docker 镜像构建
│   ├── 环境变量与密钥管理
│   └── Serverless 函数部署（可选）
├── 7.3 可观测性
│   ├── LangSmith / LangFuse 全链路追踪
│   ├── 自定义日志与指标采集（Token、延迟、步数）
│   └── 告警与大盘可视化
├── 7.4 前端交互
│   ├── Vue 集成Agent对话组件
│   ├── 工具调用状态展示（步骤可视化）
│   └── 操作确认与用户干预UI
└── 7.5 CICD与版本管理
    ├── 提示词版本管理
    └── 模型与Agent服务灰度发布