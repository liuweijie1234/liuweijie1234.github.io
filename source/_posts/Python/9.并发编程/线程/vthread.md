## vthread（第三方库）

## 原理：

基于协程的用户级线程
在单个内核线程上实现多个虚拟线程
通过事件循环（event loop）调度

```python
from vthread import pool

# 创建虚拟线程池
vpool = pool.pool(20)  # 20个虚拟线程

@vpool.threads(5)       # 每个任务5个虚拟线程
def task(num):
    print(f"VThread: {num}")

for i in range(100):
    task(i)  # 提交100个任务
```

## 优点

1. **超高并发**：

```python
# 创建10万个虚拟线程
vpool = pool.pool(100000)
```

2. **极低内存开销**：每个虚拟线程 ≈ 5KB

内存对比:
    1000 标准线程: 8MB * 1000 = 8GB
    1000 虚拟线程: 5KB * 1000 = 5MB

3. **无上下文切换**：协作式切换无系统调用开销
4. **规避 GIL**：在 I/O 密集型场景接近并行效果


## 缺点：

1. CPU 阻塞代价大：

```python
def cpu_bound_task():
    # 若在虚拟线程中执行
    result = 0
    for i in range(10**8):  # 长时间占用CPU
        result += i
```
阻塞整个事件循环

2. 兼容性问题：
    不支持需要内核线程的 C 扩展（如某些 GPU 库）
3. 调试困难：
    栈追踪不直观
    与传统调试工具集成差
4. 同步机制特殊：

```python
# 不能用 threading.Lock()
from vthread import VLock
vlock = VLock()
```


## 关键区别对比

| 特性 | threading | vthread |
| --- | --- | --- |
| 实现层级 | 操作系统内核线程 | 用户空间协程 |
| 内存开销 | ≈8MB/线程 | ≈5KB/虚拟线程 |
| 调度方式 | 抢占式（OS调度） | 协作式（事件循环） |
| 最佳场景 | I/O 操作 + 少量阻塞调用 | 超高并发 I/O (10K+连接) |
| 适用任务 | 数据库查询，文件处理 | Web服务，API网关，爬虫 |
| GIL 影响 | 严重限制 CPU 并行 | 对 I/O 任务几乎无影响 |
| 阻塞操作影响| | 仅阻塞单个线程 | 阻塞整个事件循环 |
| 创建数量 | 数百~数千 | 数万~数十万 |
| 同步原语 | threading.Lock/Event | 需使用 vthread 专用同步工具 |


## 性能基准测试对比

```python
# 测试脚本: 创建1000个任务执行网络请求
import time
import requests
from threading import Thread
from vthread import pool

def http_task():
    requests.get("http://test-api/delay=0.1")  # 100ms延迟API

# 标准线程测试
def test_threading():
    threads = []
    start = time.time()
    for _ in range(1000):
        t = Thread(target=http_task)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(f"threading: {time.time()-start:.2f}s")

# 虚拟线程测试
def test_vthread():
    vpool = pool.pool(1000)  # 1000虚拟线程
    start = time.time()
    for _ in range(1000):
        vpool.put(http_task)
    vpool.wait()
    print(f"vthread: {time.time()-start:.2f}s")

test_threading()  # ≈3.2s
test_vthread()    # ≈1.8s (网络延迟主导时)
```

## 选型决策指南


### 选择 threading 当：
需要执行阻塞式系统调用
使用基于内核线程的 C 扩展库
任务数量 < 1000 的中等并发

```python
# 案例: 并行处理文件
threads = []
for file in files:
    t = threading.Thread(target=process_file, args=(file,))
    t.start()
    threads.append(t)
```

### 选择 vthread 当：
超高并发 I/O 操作（HTTP/DB 请求）
需要维持大量空闲连接
内存受限环境

```python
# 案例: Web爬虫
@pool.threads(500)
def crawl(url):
    html = download(url)
    data = parse(html)
    save_to_db(data)
```

### 混合方案：

```python
from concurrent.futures import ThreadPoolExecutor
from vthread import pool

# CPU密集型用标准线程
cpu_pool = ThreadPoolExecutor(8)  

# I/O密集型用虚拟线程
@pool.threads(200)
def io_task():
    result = cpu_pool.submit(cpu_bound_func)  # 委派给CPU池
    process(result)
```

### 未来趋势：Python 3.11+ 的新方案

Python 3.11 引入 asyncio.TaskGroup 提供更高效的协程方案：
```python
# Python 3.11 async/await 方案
async def main():
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch(url))

# 性能接近vthread，兼容标准库
```