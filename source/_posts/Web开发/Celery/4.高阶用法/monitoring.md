介绍如何监控 Celery worker 和任务


# 监控和日志
## 花屏监控

```bash
celery -A my_app events --dump
```


## Flower 监控工具
安装 Flower：
```bash
pip install flower
```
启动 Flower：
```bash
flower -A my_app --port=5555
```

访问 Flower 监控界面：URL_ADDRESS访问 Flower 监控界面：http://localhost:5555/
