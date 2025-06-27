讲解如何根据负载进行扩容和缩容

# 扩容和缩容策略
## 扩容
在高峰负载期间，启动更多的 worker 实例：

```bash
celery -A my_app worker --loglevel=info -n worker3 -c 4
celery -A my_app worker --loglevel=info -n worker4 -c 4
```

## 缩容
在低谷负载期间，停止部分 worker 实例：

```bash
pkill -f 'celery -A my_app worker -n worker3'
pkill -f 'celery -A my_app worker -n worker4'
```