redis:
特点，背景，memcached和redis区别，
为什么快（引申io多路复用，避免上下文切换，引申和协程的相同点），
数据类型：string，list（引申队列，消息中间件），set（去重功能引申商品标签，在线人数统计），sorted set（有序集合引申出排行榜），hash 分别深入研究，
各个数据类型的实现原理，使用背景，持久化方案（三种，怎么用，在什么场景下用什么方案），
缓存集群（哨兵模式，同步，选举），并发竞争问题和分布式锁（setnx），incr(自动计数)，
与mysql数据同步问题怎么解决（终极方案由mysql的binlog日志入手，撰写同步脚本），
redisearch全文检索（为什么用，背景，怎么用）