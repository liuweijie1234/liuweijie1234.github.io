
演示如何在生产环境中配置和管理多个 worker


# 多 worker 配置和管理
## 启动多个 worker

```bash
# 启动第一个 worker
celery -A my_app worker --loglevel=info -n worker1 -c 4

# 启动第二个 worker
celery -A my_app worker --loglevel=info -n worker2 -c 4
```

## 负载均衡
通过多个 worker 分担任务负载，提高系统吞吐量。
