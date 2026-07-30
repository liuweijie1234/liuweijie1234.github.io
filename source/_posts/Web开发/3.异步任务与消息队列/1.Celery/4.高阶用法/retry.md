讲解任务重试机制的配置和使用。




# 任务重试机制

#### 使用 Celery 的内置重试机制

**autoretry_for** 
**retry_kwargs**
autoretry_for=(Exception,),  # 自动重试的异常类型
retry_kwargs={
    'max_retries': 3,        # 最大重试次数
    'countdown': 5,          # 每次重试的间隔（秒）
},
retry_backoff=True,          # 是否启用指数退避
retry_backoff_max=60,        # 最大退避时间（秒）
retry_jitter=True,           # 是否添加随机抖动（避免雪崩）
default_retry_delay=30,      # 默认重试间隔（秒）

```python
@celery_app.task(bind=True, autoretry_for=(Exception,), max_retries=MAX_RETRIES, default_retry_delay=INITIAL_DELAY * MULTIPLIER)
def start_taks_polling(self, bot_uid: str, input_str: str, task_type: str = None, key_words: str = None):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(start_task(bot_uid, input_str, task_type, key_words))
        return result
    except Exception as e:
        logger.error(f"Error in start_taks_polling: {e}", exc_info=True)
        raise  # 触发 Celery 的自动重试机制[^12^]
```
优点
- 简单易用：只需在装饰器里配置，无需手动重试逻辑。
- 支持指数退避 (retry_backoff) ：避免短时间内频繁重试导致系统过载。
- 支持随机抖动 (retry_jitter) ：防止多个任务同时重试造成“惊群效应”。
- 自动记录重试次数，Celery 会管理重试状态。

缺点
- 无法精细控制重试逻辑（如某些错误不重试）。
- 重试间隔固定或指数增长，无法动态调整。

#### 基础版：手动调用 self.retry()

```python
from celery import Celery, Task

app = Celery()

@app.task(bind=True)  # 必须加 bind=True 才能使用 self.retry()
def start_taks_polling(self, bot_uid: str, input: str, task_type: str = None, key_words: str = None):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(start_task(bot_uid, input, task_type, key_words))
        return result
    except ConnectionError as e:
        # 仅对 ConnectionError 重试
        raise self.retry(
            exc=e,
            countdown=5,
            max_retries=3,
        )
    except ValueError as e:
        # 对 ValueError 不重试，直接失败
        logger.error(f"ValueError occurred: {e}")
        raise
    except Exception as e:
        # 其他异常重试
        raise self.retry(
            exc=e,
            countdown=10,
            max_retries=5,
        )
```
优点
- 更灵活：可以针对不同异常采用不同重试策略。
- 可以动态调整重试间隔（如根据错误类型调整 countdown）。
- 支持自定义重试逻辑（如某些错误不重试）。

缺点
- 代码更复杂，需要手动管理重试逻辑。
- 需要手动记录重试次数（Celery 会跟踪，但需要自己处理异常）。

#### 优化版：self.retry() + 指数退避 + 随机抖动

```python
import random
import time

@app.task(bind=True)
def start_taks_polling(self, bot_uid: str, input: str, task_type: str = None, key_words: str = None):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(start_task(bot_uid, input, task_type, key_words))
        return result
    except Exception as e:
        # 计算指数退避 + 随机抖动
        retry_count = self.request.retries   # 当前重试次数
        backoff = min(2 ** retry_count, 60)  # 最大 60 秒
        jitter = random.uniform(0.5, 1.5)   # 随机抖动因子（0.5~1.5 倍）
        countdown = backoff * jitter     # 计算最终的退避时间
        
        if retry_count < 3:  # 最多重试 3 次
            raise self.retry(
                exc=e,
                countdown=countdown,
                max_retries=3,
            )
        else:
            logger.error(f"Task failed after 3 retries: {e}")
            raise
```
优点
- 更智能的重试策略，避免雪崩效应。
- 适用于高并发场景，减少任务堆积。
- 可以动态调整退避时间。

缺点
- 实现较复杂，需要计算退避时间。
- 需要手动管理重试次数。


#### 使用 tenacity 库（高级重试策略）

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),  # 最多重试 3 次
    wait=wait_exponential(multiplier=1, min=4, max=10),  # 指数退避
    reraise=True,  # 重试失败后抛出原异常
)
async def start_task(bot_uid: str, input: str, task_type: str = None, key_words: str = None):
    # 你的业务逻辑
    pass

@app.task
def start_taks_polling(bot_uid: str, input: str, task_type: str = None, key_words: str = None):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(start_task(bot_uid, input, task_type, key_words))
        return result
    except Exception as e:
        logger.error(f"Error in start_taks_polling: {e}", exc_info=True)
        raise
```

优点
- 极其灵活，支持复杂重试策略（如组合条件）。
- 支持异步任务的重试（tenacity 兼容 asyncio）。
- 可以定义自定义停止条件（如超时后停止）。

缺点
- 依赖额外库（tenacity）。
- 与 Celery 的重试机制可能冲突（建议只选一种）。
