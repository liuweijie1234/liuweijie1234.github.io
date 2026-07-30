
```python
from django_redis import get_redis_connection

# 获取 Redis 连接
redis_client = get_redis_connection("default")

# 可以使用所有 Redis 命令
redis_client.set("key", "value")
redis_client.get("key")
redis_client.hset("user:1", "name", "张三")
redis_client.hgetall("user:1")
redis_client.lpush("queue:1", "item1")
redis_client.sadd("set:1", "member1")
redis_client.zadd("rank", {"user1": 100, "user2": 90})

# 支持事务
pipe = redis_client.pipeline()
pipe.set("a", 1)
pipe.set("b", 2)
pipe.execute()

# 发布订阅
redis_client.publish("channel", "message")
```

```python
from django.core.cache import cache

# 基本的缓存操作
cache.set("key", "value", timeout=3600)
value = cache.get("key")
cache.add("key", "value")  # 仅当key不存在时设置
cache.delete("key")
cache.clear()

# 批量操作
cache.set_many({"key1": "value1", "key2": "value2"})
values = cache.get_many(["key1", "key2"])

# 递增递减
cache.incr("counter")
cache.decr("counter")

# 设置超时
cache.touch("key", timeout=1800)
```