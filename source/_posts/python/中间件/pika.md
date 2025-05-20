---
title: pika 使用操作 rabbitmq
date: 2024-02-20 09:00:00
tags:
- pika
categories:
- [pika]
---


## 安装 RabbitMQ

https://rabbitmq.com/install-windows.html


参考 https://cuiqingcai.com/33044.html

### 使用 Chocolatey 安装

Chocolatey 是最佳安装方法

[chocolatey的安装与使用与chocolatey安装失败的解决方法](https://blog.csdn.net/cckevincyh/article/details/92082374)

[Chocolatey 的安装](https://gentletk.gitee.io/Chocolatey%E5%AE%89%E8%A3%85%E4%B8%8E%E4%BD%BF%E7%94%A8/)

[Chocolatey安装过程中失败，再安装报错的解决办法](https://blog.csdn.net/zdhsoft/article/details/115376094)

[Chocolatey 安装 RabbitMQ ](https://community.chocolatey.org/packages/rabbitmq#install)

### 使用 exe 安装

[Windows下安装Erlang和RabbitMQ](https://blog.csdn.net/qq_42402854/article/details/103032007)

安装 rabbitmq 报错 Erlang could not be detected ,没有那就安装 Erlang

## 安装 Pika

Pika 是 Python 中用于连接和操作 RabbitMQ 的库

```bash
pip3 install pika
```

## 基本使用

```python
# 生产者
import pika

QUEUE_NAME = 'scrape'  # 定义消息队列的名称
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # 创建了一个连接到本地 RabbitMQ 服务器的connection对象，使用pika.ConnectionParameters指定了连接参数
channel = connection.channel()  # 从连接中创建了一个通道channel，用于执行大部分的 RabbitMQ 操作。
channel.queue_declare(queue=QUEUE_NAME)  # 声明了一个名为scrape的队列，如果该队列不存在则会被创建。

channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='Hello World!')  # 向指定的目的地发送消息。在这里，它将消息Hello World!发送到名为scrape的队列中，exchange为空表示直接发送到队列。

# 消费者
import pika

QUEUE_NAME = 'scrape'
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)


def callback(ch, method, properties, body):
    print(f"Get {body}")

channel.basic_consume(queue=QUEUE_NAME, auto_ack=True, on_message_callback=callback)  # 向消息队列中的名为 QUEUE_NAME 的队列注册一个消费者，并设置 auto_ack=True，表示消息一旦被消费者接收，就会被自动确认消费，同时指定 callback 函数作为消息的回调处理函数。
channel.start_consuming()  # 启动了一个无限循环，不断从消息队列中接收消息并调用之前注册的 callback 函数来处理这些消息，直到程序手动停止或出现异常。
```


[RabbitMQ的web管理界面打不开解决方案](https://blog.csdn.net/Mrzhang567/article/details/114591701)


[RabbitMQ删除Queue队列的方法](https://blog.csdn.net/pan_junbiao/article/details/112966833)


**优先队列**: 声明队列的时候增加 'x-max-priority' 的参数,用于指定最大优先级

```python
# 生产者
import pika

MAX_PRIORITY = 100
QUEUE_NAME = 'scrape'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, arguments={'x-max-priority': MAX_PRIORITY})

while True:
    data, priority = input().split()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, properties=pika.BasicProperties(priority=int(priority)),body=data)
    print(f"Put {data}")

# 消费者
import pika

MAX_PRIORITY = 100
QUEUE_NAME = 'scrape'
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, arguments={'x-max-priority': MAX_PRIORITY})

while True:
    input()
    method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
    if body:
        print(f'Get {body}')

```

**队列持久化**: 声明队列的时候,指定 durable=True ,即可开启持久化存储
同时添加消息的时候需要指定 BasicProperties 对象的 delivery_mode = 2


```python
# 生产者
import pika

MAX_PRIORITY = 100
QUEUE_NAME = 'scrape'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, arguments={'x-max-priority': MAX_PRIORITY}, durable=True)

while True:
    data, priority = input().split()
    channel.basic_publish(exchange='', 
                          routing_key=QUEUE_NAME, 
                          properties=pika.BasicProperties(priority=int(priority),
                                                          delivery_mode=2),
                          body=data)
    print(f"Put {data}")

```


## 实战

```python
# 生产者
import pika
import requests
import pickle


TOTAL = 100
QUEUE_NAME = 'scrape'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

for i in range(1, TOTAL + 1):
    url = f'http://ssr1.scrape.center/detail/{i}'
    request = requests.Request('GET', url)
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          properties=pika.BasicProperties(delivery_mode=2),
                          body=pickle.dumps(request))
    print(f"Put request of {url}")


# 消费者
import pika
import requests
import pickle


QUEUE_NAME = 'scrape'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

session =requests.Session()
session.trust_env = False


def scrape(request):
    try:
        response = session.send(request.prepare())
        print(f"success scraped {response.url}")
    except requests.RequestException as err:
        print(f"error occurred when scraping {err}")

while True:
    method_frame, header, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
    if body:
        request = pickle.loads(body)
        print(f'Get {request}')
        scrape(request)


```