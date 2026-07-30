---
title: Django 缓存（Cache）
date: 2026-07-30 10:25:00
tags:
- Django
- 缓存
- Cache
categories:
- Web开发
- Django
---

## 一、为什么需要缓存

缓存把**昂贵的计算结果/数据库查询结果**暂存到更快的存储（内存）中，后续直接命中，降低 DB 压力、缩短响应时间。典型场景：首页聚合数据、热点文章、配置项、会话。

## 二、缓存后端配置

`settings.py` 的 `CACHES`：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

可选后端：`RedisCache`（推荐）、`MemcachedCache`、`LocMemCache`（开发/单进程）、`FileBasedCache`。

## 三、四种使用方式

### 1. 视图缓存

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)          # 缓存 15 分钟
def index(request):
    ...
```

### 2. 模板片段缓存

```html
{% load cache %}
{% cache 600 sidebar request.user.username %}
  ...
{% endcache %}
```

### 3. 底层 API

```python
from django.core.cache import cache

cache.set('key', value, timeout=300)
val = cache.get('key')
cache.add('key', value)          # 仅当不存在时
cache.delete('key')
cache.get_or_set('key', lambda: expensive(), 300)
cache.incr('counter')
```

### 4. 站点级缓存

`UpdateCacheMiddleware` + `FetchFromCacheMiddleware` 配合 `CACHE_MIDDLEWARE_SECONDS`，缓存整站响应（谨慎，需处理好个性化内容）。

## 四、缓存击穿/雪崩/穿透

- **穿透**：查不存在的 key → 每次打 DB。解决：缓存空值或布隆过滤器。
- **击穿**：热点 key 过期瞬间大量并发。解决：`add()` 加锁重建，或用 `get_or_set`。
- **雪崩**：大量 key 同一时刻失效。解决：过期时间加随机抖动。

## 五、与数据库缓存对比

`redis.md` 记录了 Redis 作为独立存储/队列的用法；这里的缓存是把 Redis 当作**加速层**。注意缓存与 DB 的一致性：写操作后及时 `cache.delete` 相关 key。

## 六、最佳实践

- 给缓存 key 加统一前缀，便于清理：`cache.delete_pattern('article:*')`（需 Redis 后端）。
- 不要在缓存里放大对象或敏感信息（如用户凭证）。
- 缓存超时必须设置，避免脏数据永久驻留。
- 测试环境用 `LocMemCache`，并用 `@override_settings` 隔离。
