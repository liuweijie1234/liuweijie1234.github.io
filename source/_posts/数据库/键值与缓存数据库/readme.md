# 3. 键值与缓存数据库

以 Key-Value 形式存储，读写极快（通常常驻内存），API 简单。多用于缓存、会话存储、计数器、排行榜、分布式锁、消息队列、限流等高性能场景。

## 本分组包含

- **Redis**：最流行的内存键值数据库。单线程模型 + IO 多路复用 + 丰富数据结构（String/List/Hash/Set/ZSet），支持 RDB/AOF 持久化、哨兵与主从、Cluster 集群。

> 与 Memcached 的对比见 `Redis → 9.与 Memcached 对比及实战`。
