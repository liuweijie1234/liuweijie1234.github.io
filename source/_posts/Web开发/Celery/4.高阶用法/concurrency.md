分享并发性能优化的技巧和实践。

# 并发性能优化
## 调整 worker 并发数

```bash
celery -A my_app worker --loglevel=info -c 20
```

## 使用多进程和多线程
Celery 支持多种并发模型，可以通过 -P 参数指定：

```bash
# 使用 prefork（默认）
celery -A my_app worker --loglevel=info -P prefork

# 使用 eventlet
celery -A my_app worker --loglevel=info -P eventlet

# 使用 gevent
celery -A my_app worker --loglevel=info -P gevent
```

## 使用消息队列
Celery 默认使用 RabbitMQ 作为消息队列，可以通过 -b 参数指定其他消息队列：

```bash
# 使用 Redis 作为消息队列
celery -A my_app worker --loglevel=info -b redis://localhost:6379/0
```