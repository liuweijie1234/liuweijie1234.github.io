---
title: Redis 配置文件解读及用法、报错解解方法
date: 2024-01-25 10:00:00
tags:
- Redis
categories:
- Redis
---

## 准备工作


```bash
pip3 install redis
```

验证安装

```bash
$ python3
>>> import redis
>>> redis.VERSION
(2, 10, 6)
>>>
```

[安装Redis: 参考](https://cuiqingcai.com/31091.html)

## 配置文件

安装依赖

1、Redis 客户端库：

pip install redis

2、如果使用 Celery：

pip install celery redis

3、如果使用 RQ（Redis Queue）：

pip install rq


## 使用


```python
>>> import redis
>>> db = redis.Redis(host='localhost')
>>> db.set('name', 'ZhangSan')
True
>>> db.get('name')  # 在默认情况下，redis 返回的结果是字节对象
b'ZhangSan'


>>> import redis
>>> db = redis.Redis(host='localhost', decode_responses=True)
>>> db.set('name', 'ZhangSan')
True
>>> db.get('name')  # 通过设定参数 decode_responses=True 使 redis 返回字符串
'ZhangSan'

```

```python
from redis import StrictRedis

redis = StrictRedis(host='localhost', port=6379, db=0, password='')
redis.set('name', 'ADC')
print(redis.get('name'))  # b'ADC'
```

```python
from redis import StrictRedis, ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0, password='')
redis = StrictRedis(connection_pool=pool)
redis.set('name', 'ADC1')
print(redis.get('name'))
```


```python
from redis import StrictRedis, ConnectionPool
url = "redis://@localhost:6379"
pool = ConnectionPool.from_url(url)
redis = StrictRedis(connection_pool=pool)
redis.set('name', 'ADC2')
print(redis.get('name'))
```

URL格式：
```bash
# Redis TCP连接
redis://[:password]@host:port/db
# Redis TCP+SSL连接
rediss://[:password]@host:port/db
# Redis UNIX socket连接
unix://[:password]@/path/to/socket.sock?db=db
```


## 数据类型

### String(字符串)

简介: 二进制安全
特性: 可以包含任何数据,比如jpg图片或者序列化的对象,一个键最大能存储512M

```bash
# 初始化字符串 
> set key value

# 获取字符串的内容
> get key

# 获取字符串的长度
> strlen key

# 获取子串 提供「变量名称」以及开始和结束位置[start, end]
> getrange key 0 3

# 覆盖子串 提供「变量名称」以及开始位置和目标子串
> setrange key 2 test

# 追加子串
> append key abcdefg

# 设置过期时间，到点会自动删除
> expire key 60
(integer) 1  # 1表示设置成功，0表示变量ireader不存在

# 获取字符串的寿命
> ttl key
(integer) 50  # 还有50秒的寿命，返回-2表示变量不存在，-1表示没有设置过期时间

# 删除Key
> del key
(integer) 1  # 删除成功返回1

# 将 key 对应的值增加指定的整数值, Key 需要是int 或者 字符串数字
> incrby key 10
> incr key  # 等价于incrby key 1

# 将 key 对应的值减少指定的整数值
> decrby key 19
> decr key  # 等价于decrby key 1

# 计数器是有范围的，它不能超过Long.Max，不能低于Long.MIN
> set ireader 9223372036854775807
OK
> incr ireader
(error) ERR increment or decrement would overflow
> set ireader -9223372036854775808
OK
> decr ireader
(error) ERR increment or decrement would overflow
```

### List(列表)
简介: 链表(双向链表) 类似异步队列
特性: 增删快,提供了操作某一段元素的API
场景: 1.最新消息排行等功能(比如朋友圈的时间线) 2.消息队列

```bash
# 左进右出
lpush key value1 value2 ... 
# 移除最左边的一个
lpop key
# 右进左出
rpush key value1 value2 ...
# 移除最右边一个元素
rpop key 

# 获取链表长度
llen key

# 根据下标访问指定位置的元素，0 表示第一个
lindex key 1

# 根据下标范围访问指定位置范围的元素，0 表示第一个，-1表示倒数第一
lrange key 0 -1

# 修改元素 使用lset指令在指定位置修改元素。
lset key 1 value1

# 在value1的左边 插入元素value2
linsert key before value1 value2

# 在value1的右边 插入元素value2
linsert key after value1 value2

# 删除元素需指定删除的最大个数以及元素的值
lrem key 1 value1
```

### Hash(哈希表)

> hset major_key key value

简介: 键值对集合,即编程语言中的Map类型，Python语言的dict
特性: 适合存储对象,并且可以像数据库中update一个属性一样只修改某一项属性值(Memcached中需要取出整个字符串反序列化成对象修改完再序列化存回去)
场景: 存储、读取、修改用户属性

```bash
# hset 增加一个键值对
> hset major_key key value
(integer) 1

# hmset 增加多个键值对
> hmset major_key key1 value1 key2 value2
OK

# hget 获取一个 key 对应的 value
> hget major_key key
"fast"

# hmget 获取多个 key 对应的 value
> hmget major_key key1 key2
1) "fast"
2) "slow"
# hgetall 获取所有的键值对
> hgetall major_key

# hkeys 获取所有的key列表
> hkeys major_key

# hvals 获取所有的value列表
> hvals major_key

# hdel 删除一个或者多个key
> hdel major_key key1 key2

# hexists 判断key元素是否存在
> hexists major_key key

# hincrby 对 key 增加计数，需要value值是整数，不然会报错
> hincrby major_key key 1
```

### Set(集合)

简介: 哈希表实现,元素不重复
特性: 1.添加、删除,查找的复杂度都是O(1) 2.为集合提供了求交集、并集、差集等操作
场景: 1.共同好友 2.利用唯一性,统计访问网站的所有独立ip 3,好用推荐时,根据tag求交集,大于某个阈值就可以推荐

```bash
# sadd 增加一个或多个元素
sadd key value1 value2 ... 

# smembers 读取 所有元素
smembers key

# scard 获取集合长度
scard key

# srandmember 获取随机count个元素，如果不提供count参数，默认为1
srandmember key [1]

# srem 删除一到多个元素
srem key value1 value2

# spop 删除随机一个元素
spop key

# sismember 判断元素是否存在
sismember key value1
```


### Sorted Set(有序集合)


简介: 将Set中的元素增加一个权重参数score,元素按score有序排列
特性: 数据插入集合时,已经进行天然排序
场景: 1.排行榜 2.带权重的消息队列

SortedSet(zset)是Redis提供的一个非常特别的数据结构，一方面它等价于Java的数据结构Map<String, Double>，可以给每一个元素value赋予一个权重score，
另一方面它又类似于TreeSet，内部的元素会按照权重score进行排序，可以得到每个元素的名次，还可以通过score的范围来获取元素的列表。

zset底层实现使用了两个数据结构，第一个是hash，第二个是跳跃列表，hash的作用就是关联元素value和权重score，保障元素value的唯一性，可以通过元素value找到相应的score值。
跳跃列表的目的在于给元素value排序，根据score的范围获取元素列表。

```bash
# zadd 可添加一个或多个值
zadd key score1 value1 score2 value2 ...

# zcard 可以得到 key 的元素个数
zcard key

# zrem 可以删除 key 中的元素，可以一次删除多个
zrem key value1 value2

# zincrby 也可以计数
zincrby key 1.0 value1

# zscore 获取 在key的 value 的 score
zscore key value

# zrank 指令 获取指定元素的正向排名，正向是由小到大
zrank key value  # 分数低的排名考前，rank值小

# zrevrank 指令获取指定元素的反向排名[倒数第一名]，负向是由大到小
zrevrank key value

# zrange 指令指定排名范围参数获取对应的元素列表
zrange key 0 -1  # 获取所有元素

# 携带 withscores 参数可以一并获取元素的权重
zrange key 0 -1 withscores

# zrevrange 指令按负向排名获取元素列表[倒数]
zrevrange key 0 -1 withscores

# zrangebyscore指令 指定score范围 获取对应的元素列表
zrangebyscore key 0 5

zrangebyscore key -inf +inf withscores

# zrevrangebyscore指令获取倒排元素列表
zrevrangebyscore key +inf -inf withscores  # 注意正负反过来了

# zremrangebyrank 通过排名范围移除多个元素
zremrangebyrank key 0 1

# zremrangebyscore 通过score范围来一次性移除多个元素
zremrangebyscore ireader -inf 4
```


### 其他命令

键值相关命令:
1.  keys *                   查看当前所有的key
2.  exists name              查看数据库是否有name这个key
3.  del name                 删除 key name
4.  expire key 100           设置 key 100秒过期
5.  ttl key                  获取 key 的有效时长
6.  select 0                 选择到0数据库 redis默认的数据库是0~15一共16个数据库
7.  move key 1               将当前数据库中的key移动到其他的数据库中，这里就是把 key 从当前数据库中移动到1中
8.  persist key              移除 key 的过期时间
9.  randomkey                随机返回数据库里面的一个key
10. rename key2 key3         重命名key2 为key3
11. type key2                返回key的数据类型

服务器相关命令:
1.  ping                     PING返回响应是否连接成功
2.  echo                     在命令行打印一些内容
3.  select                   0~15 编号的数据库
4.  quit                     退出客户端
5.  dbsize                   返回当前数据库中所有key的数量
6.  info                     返回redis的相关信息
7.  config get dir/*         实时传储收到的请求
8.  flushdb                  删除当前选择数据库中的所有key
9.  flushall                 删除所有数据库中的数据库

Tips：
打开cmd输入 redis-cli.exe 即可进入redis命令行



### 键操作

**exists(name)**
作用：判断一个键是否存在
参数说明：name(键名)
实例：`redis.exists('name')`
实例说明：是否存在 name 这个键
实例结果： True

**delete(name)**
作用：删除一个键
参数说明：name(键名)
实例：`redis.delete('name')`
实例说明：删除 name 这个键
实例结果：1

**type(name)**
作用：判断键类型
参数说明：name(键名)
实例：`redis.type('name')`
实例说明：
实例结果：

**key(pattern)**
作用：获取所有符合规则
参数说明：pattern(匹配规则)
实例：`redis.key('n*')`
实例说明：获取所有以 n 为开头的键
实例结果：[b'name']

**randomkey()**
作用：获取随机的一个键
参数说明：
实例：`randomkey()`
实例说明：获取随机的一个键
实例结果：b'name'

**rename(src, dst)**
作用：对键重命名
参数说明：src(原键名), dst(新键名)
实例：`redis.rename('name', 'nickname')`
实例说明：将 name 重命名为 nickname
实例结果： True

**dbsize()**
作用：获取当前数据库中键的数目
参数说明：
实例：`dbsize()`
实例说明：获取当前数据库中键的数目
实例结果：100

**expire(name, time)**
作用：设定键的过期时间，单位为秒
参数说明：name(键名),time(秒数)
实例：`redis.expire('name', 2)`
实例说明：将 name 键的过期时间设置为 2 秒
实例结果： True

**tll(name)**
作用：获取键的过期时间，单位为秒
参数说明：name(键名)
实例：`redis.tll('name')`
实例说明：获取 name 这个键的过期时间
实例结果：1 (1表示永久不过期)

**move(name, db)**
作用：将键移动到其他数据库
参数说明：name(键名)，db(其他的数据库代号)
实例：`move('name',2)`
实例说明：将 name 键移动到2号数据库
实例结果： True

**flushdb()**
作用：删除当前所选数据库中的所有键
参数说明：
实例：`flushdb()`
实例说明：删除当前所选数据库中的所有键
实例结果： True

**flushall()**
作用：删除所有数据库中的所有键
参数说明：
实例：`flushall()`
实例说明：删除所有数据库中的所有键
实例结果： True

### 字符串操作

**set(name, value)**
作用： 将数据库中指定键名对应的键值赋值为字符串 value
参数说明：name(键名),value(值)
实例：`redis.set('name', 'Bob')`
实例说明：将 name 这个键的键值赋值为 Bob
实例结果： True

**get(name)**
作用：返回数据库中指定键名对应的键值
参数说明：name(键名)
实例：`redis.get('name')`
实例说明：返回 name 这个键对应的键值
实例结果： b'Bob'

**getset(name, value)**
作用： 将数据库中指定键名对应的键值赋值为字符串 value，并返回上次的 value
参数说明：name(键名),value(新值)
实例：`redis.getset('name', 'Mike')`
实例说明：将 name 这个键的键值赋值为 Mike，并返回上次的 value
实例结果： b'Bob'

**mget(keys, *args)**
作用：返回油多个键名对应的 value 组成的列表
参数说明： keys(键名序列)
实例：`redis.mget(['name', 'nickname'])`
实例说明：返回 name 和 nickname 的value
实例结果： [b'Mike', b'Miker']

**setnx(name, time, value)**
作用：若不存在指定的键值对，则更新 value，否则保持不变
参数说明：name(键名)
实例：`redis.setnx('newname', 'James')`
实例说明：如果不存在 newname 这个键名，则设置相应键值对，对应键值为 James
实例结果： 第一次的运行结果是 True ，第二次的运行结果是 False

**setex(name, time, value)**
作用：设置键名对应的键值为字符串类型的value, 并指定此键值的有效期
参数说明：name(键名),time(有效期),value(新值)
实例：`redis.setex('name', 1, 'James')`
实例说明：将 name 这个键设置为 James，有效期设置为 1 秒
实例结果： True

**setrange(name, offset, value)**
作用：设定指定键名对应的键值的子字符串
参数说明：name(键名),offset(偏移量),value(子字符串)
实例：
`redis.set('name', 'Hello')`
`redis.setrange('name', 6, 'world')`
实例说明：将 name 这个键对应的键值赋值为 Hello, 并在该键值中的 Index 为6的位置补充 world
实例结果： 11(修改后的字符串长度)

**mset(mapping)**
作用：批量赋值
参数说明：mapping(字典或关键字参数)
实例：`redis.mset({'name1':'Durant','name2':'James'})`
实例说明： 将 name1 赋值为 Durant，name2 赋值为 James
实例结果： True 

**msetnx(mapping)**
作用：指定键名均不存在，才批量赋值
参数说明：mapping(字典或关键字参数)
实例：`redis.msetnx({'name3':'Smith','name4':'Curry'})`
实例说明： 在 name3 和 name4 均不存在的情况下，才为二者赋值
实例结果： True 

**incr(name, amount=1)**
作用：对指定键名对应的键值做增值操作，默认增1。如果指定键名不存在，则创建一个，并将键值设为 amount
参数说明：name(键名), amount(增加的值)
实例：`redis.incr('age', 1)`
实例说明：将 age 对应的键值增加1。如果不存在 age 这个键名，则创建一个，并设置键值为1
实例结果： 1,即修改后的值

**decr(name, amount=1)**
作用：对指定键名对应的键值做减值操作，默认减1。如果指定键名不存在，则创建一个，并将键值设为 amount
参数说明：name(键名), amount(减少的值)
实例：`redis.decr('age', 1)`
实例说明：将 age 对应的键值减1。如果不存在 age 这个键名，则创建一个，并设置键值为1
实例结果： 1,即修改后的值

**append(key, value)**
作用：对指定键名对应的键值附加字符串 value
参数说明： key(键名)
实例：`redis.append('nickname', 'OK')`
实例说明：在键名 nickname 对应的键值后面追加字符串 OK
实例结果： 13，即修改后的字符串长度

**substr(name, start, end=-1)**
作用：返回指定键名对应的键值的子字符串
参数说明：name(键名)，start(起始索引)，end(终止索引，默认为1，表示截取到末尾)
实例：`redis.substr('name', 1, 4)`
实例说明： 返回键名 name 对应的键值的子字符串，截取键值字符串中索引为1~4的字符
实例结果： b'ello'

**getrange(name, start, end)**
作用：获取指定键名对应的键值中从 start 到 end 位置的子字符串
参数说明： name(键名)，start(起始索引)，end(终止索引)
实例：`redis.getrange('name', 1, 4)`
实例说明：返回键名 name 对应的键值的子字符串，截取键值字符串中索引为1~4的字符
实例结果： b'ello'


### 列表操作

**rpush(name, *values)**
作用：在键名为 name 的列表末尾添加值为 value 的元素，可以传入多个 value
参数说明： name(键名)， values(值)
实例：`redis.rpush('list', 1, 2, 3)`
实例说明：向键名为 list 的列表尾添加1、2、3
实例结果： 3，即列表大小

**lpush(name, *values)**
作用：在键名为 name 的列表头部添加值为 value 的元素，可以传入多个 value
参数说明： name(键名)， values(值)
实例：`redis.lpush('list', 0)`
实例说明：向键名为 list 的列表尾添加1、2、3
实例结果： 3，即列表大小

**llen(name)**
作用：返回键名为 name 的列表的长度
参数说明： name(键名)，start(起始索引)，end(终止索引)
实例：`redis.llen('list')`
实例说明：返回键名为 list 的列表的长度
实例结果： 4


**lrange(name, start, end)**
作用：返回键名为 name 的列表中索引从 start 到 end 之间的元素
参数说明： name(键名)，start(起始索引)，end(终止索引)
实例：`redis.lrange('list', 1, 3)`
实例说明：返回索引从1到3对应的列表元素
实例结果： [b'3',b'2',b'1']


**ltrim(name, start, end)**
作用：截取键名为 name 的列表，保留索引从 start 到 end 之间的元素
参数说明： name(键名)，start(起始索引)，end(终止索引)
实例：`redis.ltrim('list', 1, 3)`
实例说明：保留键名为 list 的列表中索引从1到3之间的元素
实例结果： True


**lindex(name, index)**
作用：返回键名为 name 的列表中 index 位置的元素
参数说明： name(键名)，index(索引)
实例：`redis.lindex('list', 1)`
实例说明：返回键名为 list 的列表中索引为 1 的元素
实例结果： b'2'

**lset(name, index, value)**
作用：给键名为 name的列表中 index 位置的元素赋值，如果 index  越界就报错
参数说明： name(键名)，index(索引)，value(值)
实例：`redis.lset('list', 1, 5)`
实例说明：将键名为 list 的列表中索引为 1 的位置赋值为 5
实例结果： True

**lrem(name, count, value)**
作用：删除键名为 name 的列表中 count 个值为 value 的元素
参数说明： name(键名)， count(删除个数)， value(值)
实例：`redis.lrem('list', 2, 3)`
实例说明：删除键名为 list 的列表中的 2 个 3
实例结果： 2,即删除的个数

**lpop(name)**
作用：返回并删除键名为 name 的列表中的首元素
参数说明： name(键名)
实例：`redis.lpop('list')`
实例说明：返回并删除键名为 list 的列表中的首元素
实例结果： b'5'

**rpop(name)**
作用：返回并删除键名为 name 的列表中的尾元素
参数说明： name(键名)
实例：`redis.rpop('list')`
实例说明：返回并删除键名为 list 的列表中的最后一个元素
实例结果： b'2'

**blpop(keys, timeout=0)**
作用：返回并删除键名为 name 的列表中的首元素。若列表为空，则一直阻塞等待
参数说明：key(键名)， timeout(超时等待时间，0表示一直等待)
实例：`redis.blpop('list')`
实例说明：返回并删除键名为 list 的列表中的首元素。
实例结果： [b'5']

**brpop(keys, timeout=0)**
作用：返回并删除键名为 name 的列表中的尾元素。若列表为空，则一直阻塞等待
参数说明：key(键名)， timeout(超时等待时间，0表示一直等待)
实例：`redis.blpop('list')`
实例说明：返回并删除键名为 list 的列表中的尾元素。
实例结果： [b'2']


**rpoplpush(src, dst)**
作用：返回并删除键名为 src 的列表中的尾元素，并将该元素添加到键名为 dst 的列表的头部
参数说明：src(源列表的键名)，dst(目标列表的键名)
实例：`redis.rpoplpush('list', 'list2')`
实例说明：删除键名为 list 的列表中的最后一个元素，并将其添加到键名为 list2 的列表的头部，然后返回
实例结果： b'2'


### 集合操作

**sadd(name, *values)**
作用：向键名为 name 的集合中添加元素
参数说明：name(键名)， values(值，可以为多个)
实例：`redis.sadd('tags', 'Book', 'Tea', 'Coffee')`
实例说明：向键名为 tags 的集合中添加 BooK、Tea和 Coffee 这三项内容
实例结果： 3，即添加的数据个数

**srem(name, *values)**
作用：从键名为 name 的集合中删除元素
参数说明：name(键名)， values(值，可以为多个)
实例：`redis.srem('tags', 'Book')`
实例说明：从键名为 tags 的集合中删除 Book
实例结果： 1，即删除的数据个数

**spop(name)**
作用：随机返回并删除键名为 name 的集合中的一个元素
参数说明：name(键名)
实例：`redis.spop('tags')`
实例说明：随机返回并删除键名为 tags 的集合中的一个元素
实例结果： b'Tea'

**smove(src, dst, value)**
作用：从键名为 src 的集合中移除 value，并将其添加到 dst 对应的集合中
参数说明：src(源列表的键名)，dst(目标列表的键名)， value(元素值)
实例：`redis.smove('tags', 'tags2', 'Coffee')`
实例说明：从键名为 tags 的集合中移除 Coffee ，并将其添加到 tags2 对应的集合中
实例结果： True

**scard(name)**
作用：返回键名为 name 的集合中的元素个数
参数说明：name(键名)
实例：`redis.scard('tags')`
实例说明：获取键名为 tags 的集合中的元素个数
实例结果： 3

**sismember(name, value)**
作用：判断 name 是否是键名为 name 的集合中的元素
参数说明：name(键名)， value(值)
实例：`redis.sismember('tags', 'Book')`
实例说明：判断 Book 是否是键名为 tags 的集合中的元素
实例结果： True

**sinter(keys, *args)**
作用：返回所有给定键名的集合的交集
参数说明：keys(键名序列)
实例：`redis.sinter(['tags','tags2'])`
实例说明：返回键名为 tags 的集合和键名为 tags2 的集合的交集
实例结果： {b'Coffee'}

**sinterstore(dest, keys, *args)**
作用：求多个集合的交集，并将交集保存到键名为 dest 的集合
参数说明： keys(键名序列)， dest(结果序列)
实例：`redis.sinterstore('inttag', ['tags', 'tags2'])`
实例说明：求键名为 tags 的集合和键名为 tags2 的集合的并集，并将其保存为键名是 inttag 的集合
实例结果：3


**sunion(keys, *args)**
作用：返回所有给定键名的集合的并集
参数说明：keys(键名序列)
实例：`redis.sunion(['tags', 'tags2'])`
实例说明：返回键名为 tags 的集合和键名为 tags2 的集合的并集
实例结果：{b'Coffee', b'Book', b'Pen'}

**sunionstore(dest, keys, *args)**
作用：求多个集合的并集，并将并集保存到键名为 dest 的集合
参数说明：keys(键名序列)， dest(结果序列)
实例：`redis.sunionstore('inttag', ['tags', 'tags2'])`
实例说明：求键名为 tags 的集合和键名为 tags2 的集合的并集，并将其保存为键名是 inttag 的集合
实例结果：3

**sdiff(keys, *args)**
作用：返回所有给定键名的集合的差集
参数说明：keys(键名序列)
实例：`redis.sdiff(['tags', 'tags2'])`
实例说明：返回键名为 tags 的集合和键名为 tags2 的集合的差集
实例结果：{b'Book', b'Pen'}

**sdiffstore(dest, keys, *args)**
作用：求多个集合的差集，并将差集保存到键名为 dest 的集合
参数说明：keys(键名序列)， dest(结果序列)
实例：`redis.sdiffstore('inttag', ['tags', 'tags2'])`
实例说明：求键名为 tags 的集合和键名为 tags2 的集合的差集，并将其保存为键名是 inttag 的集合
实例结果：3

**smembers(name)**
作用：返回键名为 name 的集合中的所有元素
参数说明：name(键名)
实例：`redis.smembers('tags')`
实例说明：返回键名为 tags 的集合中的所有元素
实例结果：{b'Pen', b'Book', b'Coffee'}

**srandmember(name)**
作用：随机返回键名为 name 的集合中的一个元素，但不删除该元素
参数说明：name(键名)
实例：`redis.srandmember('tags')`
实例说明：随机返回键名为 tags 的集合中的一个元素
实例结果：Srandmember(name)

### 有序集合操作

**zadd(name, args, *kwargs)**
作用：向键名为 name 的有序集合中添加元素。 score 字段用于排序，如果该元素存在，则更新各元素的顺序
参数说明：name(键名)，args(可变参数)
实例：`redis.zadd('grade', 100, 'Bob', 98, 'Mike')`
实例说明：向键名为 grade 的有序集合中添加 Bob (对应score为100)、Mike (对应score为 98)
实例结果：2，即添加的元素个数

**zrem(name, *values)**
作用：删除键名为 name 的有序集合中的元素
参数说明：name(键名)，values(元素)
实例：`redis.zrem('grade', 'Mike')`
实例说明：从键名为 grade 的有序集合中删除 Mike
实例结果：1，即删除的元素个数

**zincrby(name, value, amount=1)**
作用：如果有键名为 name 的有序集合中已经存在元素 value，则将该元素的 score 增加 amount；否则向该集合中添加 value 元素，其 score的值为 amount
参数说明：name(键名)，values(元素)，amount(增长的 score 值)
实例：`redis.zincrby('grade', 'Bob', -2)`
实例说明：将键名为 grade 的有序集合中的 Bob 元素的 score 减2
实例结果：98.0，即修改后的值


**zrank(name, value)**
作用：返回键名为 name 的有序集合中 value 元素的排名，或名次(对元素按照 score 从小到大排序)
参数说明：name(键名)，values(元素)
实例：`redis.zrank('grade', 'Amy')`
实例说明：得到键名为 grade 的有序集合中 Amy 的排名
实例结果：1


**zrevrank(name, value)**
作用：返回键为 name 的有序集合中 value 元素的倒数排名，或名次(对元素按照 score 从大到小排序)
参数说明：name(键名)，values(元素)
实例：`redis.zrevrank('grade', 'Amy')`
实例说明：得到键名为 grade 的有序集合中 Amy 的倒数排名
实例结果：2


**zrevrange(name, start, end, withscrores=False)**
作用：返回键名为 name 的有序集合中名词索引从 start 到 end 之间的所有元素 (按照 score 从大到小排序)
参数说明：name(键名)，start(开始索引)，end(结束索引)，withscrores(是否带 score)
实例：`redis.zrevrange('grade', 0, 3)`
实例说明：返回键名为 grade 的有序集合中的前四名元素
实例结果：[b'Bob', b'Mike', b'Amy', b'James']

**zrangebyscore(name, min, max, start=None, num=None, withscrores=False)**
作用：返回键名为 name 的有序集合中 score 在给定区间的元素
参数说明：name(键名)，min(最低 score)，max(最高 score)，start(起始索引)，num(个数)，withscrores(是否带 score)
实例：`redis.zrangebyscore('grade', 80, 95)`
实例说明：返回键名为 grade 的有序集合中 score 在 80 和 95 之间的元素
实例结果：[b'Bob', b'Mike', b'Amy', b'James']


**zcount(name, min, max)**
作用：返回键名为 name 的有序集合中 score 在给定区间的元素数量
参数说明：name(键名)，min(最低 score)，max(最高 score)
实例：`redis.zcount('grade', 80, 95)`
实例说明：返回键名为 grade 的有序集合中 score 在 80 和 95 之间的元素个数
实例结果：4

**zcard(name)**
作用：返回键名为 name 的有序集合中的元素个数
参数说明：name(键名)
实例：`redis.zcard('grade')`
实例说明：获取键名为 grade 的有序集合中元素个数
实例结果：3

**zremrangebyrank(name, min, max)**
作用：删除键名为 name 的有序集合中排名在给定区间的元素
参数说明：name(键名)，min(最低名次)，max(最高名次)
实例：`redis.zremrangebyrank('grade', 0, 0)`
实例说明：删除键名为 grade 的有序集合中排名第一的元素
实例结果：1，即删除的元素个数

**zremrangebyscore(name, min, max)**
作用：删除键名为 name 的有序集合中 score 在给定区间的元素
参数说明：name(键名)，min(最低 score)，max(最高 score)
实例：`redis.zremrangebyscore('grade', 80, 90)`
实例说明：删除键名为 grade 的有序集合中 score 在 80 和 90 之间的元素
实例结果：1，即删除的元素个数


### 散列操作

**hset(name, key, value)**
作用：向键名为 name 的散列表中添加映射
参数说明：name(散列表键名), key(映射键名), value(映射键值)
实例：`redis.hset('price', 'cake', 5)`
实例说明：向键名为 price 的散列表中添加映射关系，cake 的值为 5
实例结果：1，即添加的映射个数


**hsetnx(name, key, value)**
作用：如果键名为 name 的散列表中不存在给定映射，则向其中添加此映射
参数说明：name(散列表键名), key(映射键名), value(映射键值)
实例：`redis.hsetnx('price', 'book', 6)`
实例说明：向键名为 price 的散列表中添加映射关系，book 的值为 6
实例结果：1，即添加的映射个数

**hget(name, key)**
作用：返回键名为 name 的散列表中 key 对应的值
参数说明：name(散列表键名), key(映射键名)
实例：`redis.hget('price', 'cake')`
实例说明：获取键名为 price 的散列表中键名 cake 的值
实例结果：5

**hmget(name, keys, *args)**
作用：返回键名为 name 的散列表中各个键名对应的值
参数说明：name(散列表键名), key(键名序列)
实例：`redis.hmget('price', ['apple', 'orange'])`
实例说明：获取键名为 price 的散列表中 apple 和 orange 对应的值
实例结果：[b'3', b'7']


**hmset(name, mapping)**
作用：向键名为 name 的散列表中批量添加映射
参数说明：name(散列表键名),mapping(映射字典)
实例：`redis.hmset('price',{'banana':2, 'pear':6})`
实例说明：向键名为 price 的散列表中批量添加映射
实例结果：True

**hincrby(name, key, amount=1)**
作用：将键名为 name 的散列表中的映射键值增加 amount
参数说明：name(散列表键名), key(映射键名)，amount(增长量)
实例：`redis.hincrby('price', 'apple', 3)`
实例说明：将键名为 price 的散列表中的 apple 的键值增加 3
实例结果：6，修改后的值

**hexists(name, key)**
作用：返回键名为 name 的散列表中是否存在键名为 key 的映射
参数说明：name(散列表键名), key(映射键名)
实例：`redis.hexists('price', 'banana')`
实例说明：返回键名为 price 的散列表中是否存在键名为 banana 的映射
实例结果：True

**hdel(name, *keys)**
作用：在键名为 name 的散列表中，删除具有给定键名的映射
参数说明：name(散列表键名), keys(映射键名序列)
实例：`redis.hdel('price', 'banana')`
实例说明：从键名为 price 的散列表中，删除键名为 banana 的映射
实例结果：True

**hlen(name)**
作用：获取键名为 name 的散列表映射数量
参数说明：name(散列表键名)
实例：`redis.hlen('price')`
实例说明：获取键名为 price 的散列表中映射的个数
实例结果：6

**hkeys(name)**
作用：获取键名为 name 的散列表中的所有映射键名
参数说明：name(散列表键名)
实例：`redis.hkeys('price')`
实例说明：获取键名为 price 的散列表中的所有映射键名
实例结果：[b'cake', b'book', b'banana', b'pear']

**hvals(name)**
作用：获取键名为 name 的散列表中的所有映射键值
参数说明：name(散列表键名)
实例：`redis.hvals('price')`
实例说明：获取键名为 price 的散列表中的所有映射键值
实例结果：[b'5', b'6', b'2', b'6']

**hgetall(name)**
作用：获取键名为 name 的散列表中的所有映射键值对
参数说明：name(散列表键名)
实例：`redis.hgetall('price')`
实例说明：获取键名为 price 的散列表中的所有映射键值对
实例结果：{b'cake': b'5', b'book': b'6', b'banana':b'2', b'pear': b'6'}


## 实例

[Python连接Redis数据库进行增删改查（附带常用方法）](https://blog.csdn.net/weixin_43750377/article/details/103994387)

```python
# -*- coding:utf-8 -*-
import redis
import pickle
import datetime

__author__ = 'Evan'


class Redis(object):

    def __init__(self, host='localhost', port=6379, db=0, password=''):
        """
        初始化Redis连接池
        :param host: 主机名
        :param port: 端口
        :param db: 数据库
        :param password: 密码
        """
        pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=None  # 连接池最大值，默认2**31
        )
        self.redis = redis.Redis(connection_pool=pool)

    def __del__(self):
        """程序结束后，自动关闭连接，释放资源"""
        self.redis.connection_pool.disconnect()

    def exists(self, name):
        """
        检查name是否存在
        :param name:
        :return:
        """
        return self.redis.exists(name)

    def delete(self, name):
        """
        删除指定的name
        :param name:
        :return:
        """
        return self.redis.delete(name)

    def rename(self, old, new):
        """
        重命名
        :param old:
        :param new:
        :return:
        """
        if self.exists(old):
            return self.redis.rename(old, new)

    def set_expire_by_second(self, name, second=60 * 60 * 24 * 7):
        """
        以秒为单位设置过期时间
        :param name:
        :param second: 默认7天
        :return:
        """
        return self.redis.expire(name, time=second)

    def remove_expire(self, name):
        """
        移除name的过期时间，name将持久保持
        :param name:
        :return:
        """
        return self.redis.persist(name)

    def get_expire_by_second(self, name):
        """
        以秒为单位返回name的剩余过期时间
        :param name:
        :return:
        """
        return self.redis.ttl(name)

    def get_name_type(self, name):
        """
        获取name的数据类型
        :param name:
        :return:
        """
        return self.redis.type(name).decode()

    def check_name_type(self, name, expect_type='string'):
        """
        检查name的数据类型
        数据类型对照表：
            set   ->  'string'
            hset  ->  'hash'
            lpush ->  'list'
            sadd  ->  'set'
            zadd  ->  'zset'
        :param name:
        :param expect_type: string / hash / list / set / zset
        :return:
        """
        name_type = self.get_name_type(name)
        if name_type == expect_type:
            return True
        else:
            return False

    def set(self, name, value, do_pickle=True, expire=60 * 60 * 24 * 7):
        """
        添加set类型，使用pickle进行持久化存储
        :param name:
        :param value:
        :param do_pickle: 是否使用pickle进行二进制序列化，默认True
        :param expire: 单位second，默认7天
        :return:
        """
        if do_pickle:
            self.redis.set(name=name, value=pickle.dumps(value), ex=expire)
        else:
            self.redis.set(name=name, value=value, ex=expire)

    def get_set_value(self, name, do_pickle=True):
        """
        获取指定的set value
        :param name:
        :param do_pickle: 是否使用pickle进行二进制反序列化，默认True
        :return:
        """
        value = self.redis.get(name=name)
        if value:
            if do_pickle:
                return pickle.loads(value)
            else:
                return value
        else:
            return None

    def get_set_all(self, do_pickle=True):
        """
        获取所有的set value
        :param do_pickle: 是否使用pickle进行二进制反序列化，默认True
        :return: [{}, {}, {}]
        """
        all_data = []
        if self.redis.keys():
            for key in self.redis.keys():  # 获取所有的key
                flag = self.check_name_type(name=key, expect_type='string')  # 判断是否为set类型
                if not flag:
                    continue
                value = self.get_set_value(name=key, do_pickle=do_pickle)
                all_data.append({key.decode(): value})
        return all_data

    def zadd(self, name, value=[], do_pickle=True, expire=60 * 60 * 24 * 7):
        """
        添加有序集合类型，默认score为当前时间戳，使用pickle进行持久化存储
        :param name:
        :param value: [{}, {}, {}]
        :param do_pickle: 是否使用pickle进行二进制序列化，默认True
        :param expire: 单位second，默认7天
        :return:
        """
        assert value, 'value不能为空'
        value_dict = {}
        for each in value:
            score = each.get('timestamp') or datetime.datetime.now().timestamp()  # 如果没有timestamp，取当前时间戳为score
            if do_pickle:
                value_dict.setdefault(pickle.dumps(each), score)
            else:
                value_dict.setdefault(str(each), score)  # 如果不进行序列化，需要将字典转化为字符串作为Key，否则会报错

        self.redis.zadd(name=name, mapping=value_dict)
        self.set_expire_by_second(name, expire)  # 设置expire

    def get_zadd_data_by_score(self, name, start_score=None, end_score=None, do_pickle=True):
        """
        根据score范围，返回对应的数据，只用于有序集合
        :param name:
        :param start_score: timestamp时间戳
        :param end_score: timestamp时间戳
        :param do_pickle: 是否使用pickle进行二进制序列化，默认True
        :return:
        """
        # 如果start_score为空，默认为前一天的时间戳
        start_score = start_score or (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
        # 如果end_score为空，默认为当前时间的时间戳
        end_score = end_score or datetime.datetime.now().timestamp()

        data = self.redis.zrangebyscore(name, start_score, end_score)
        if do_pickle:
            return [pickle.loads(i) for i in data]
        else:
            return [i for i in data]

    def delete_zadd_data_by_score(self, name, start_score, end_score):
        """
        根据score范围，删除对应的数据，只用于有序集合
        :param name:
        :param start_score: timestamp时间戳
        :param end_score: timestamp时间戳
        :return:
        """
        return self.redis.zremrangebyscore(name, start_score, end_score)

    def get_zadd_timestamp_range(self, name):
        """
        获取指定name对应集合中的score最小值和最大值，只用于有序集合
        :param name:
        :return: [start_datetime, end_datetime]
        """
        status = self.exists(name)
        if status != 0:
            # 转换为datetime类型
            start_datetime = datetime.datetime.fromtimestamp(self.redis.zrange(name,
                                                                               start=0,
                                                                               end=0,
                                                                               desc=False,
                                                                               withscores=True)[0][1])
            end_datetime = datetime.datetime.fromtimestamp(self.redis.zrange(name,
                                                                             start=0,
                                                                             end=0,
                                                                             desc=True,
                                                                             withscores=True)[0][1])
            return [start_datetime, end_datetime]
        else:
            return []


if __name__ == '__main__':
    REDIS = Redis()
    # 测试set
    REDIS.set(name='name', value='Evan', do_pickle=True, expire=60)
    REDIS.set(name='id', value=6, do_pickle=True, expire=60)
    print(REDIS.get_set_value('name', do_pickle=True))
    print(REDIS.get_set_all())
    # 测试有序集合
    REDIS.zadd(name='demo', value=[{'name': 'Evan'}, {'id': 6}], do_pickle=True, expire=60)
    print(REDIS.get_zadd_data_by_score(name='demo', do_pickle=True))
    print(REDIS.get_zadd_timestamp_range(name='demo'))
'''
Evan
[{'name': 'Evan'}, {'id': 6}]
[{'id': 6}, {'name': 'Evan'}]
[datetime.datetime(2021, 1, 16, 19, 18, 57, 153845), datetime.datetime(2021, 1, 16, 19, 18, 57, 153845)]
'''
```




## 报错

缓存雪崩是指在一个特定的时间段内，缓存中的大量数据同时过期失效，导致大量请求直接访问数据库或其他后端服务，从而导致后端服务短时间内承受巨大压力，甚至崩溃。

常见的解决方法包括：

1、缓存数据过期时间随机化：将缓存数据的过期时间设置为一个随机值，避免因为缓存同时过期导致的雪崩问题。

2、多级缓存架构：将缓存分为多级，不同级别的缓存具有不同的生命周期和失效策略，可以有效减少缓存雪崩风险。

3、热点数据预加载：对于业务高频访问的热点数据，提前进行缓存，保证其缓存在高并发情况下仍能稳定提供服务。

4、限流降级：在发生缓存雪崩时，通过限制请求量或者降低服务等级等措施，保证系统可用性。




