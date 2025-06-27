## Celery 架构
Celery 的架构主要包括以下几个组件：

- Worker：任务执行单元，负责执行任务。
- Broker：消息中间件，用于存储和转发任务消息。
- Task：任务单元，定义了要执行的逻辑。
- Result Backend：结果后端，用于存储任务执行结果。