# 示例

创建一个简单的 Celery 应用：
```python
from celery import Celery

# 创建 Celery 实例
app = Celery('my_app', broker='redis://localhost:6379/0')

# 定义一个任务
@app.task
def add(x, y):
    return x + y
```

启动 Celery worker：

```bash
celery -A my_app worker --loglevel=info
```

调用任务

```python
result = add.delay(2, 3)
print(result.get())  # 输出 5
```