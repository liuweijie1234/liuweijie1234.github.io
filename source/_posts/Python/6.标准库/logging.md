---
title: Python3 模块 logging
date: 2022-08-15 10:22:00
tags:
- Python module
- logging
categories:
- Python
---

# Python 日志处理 （logging 模块）

> django 中多进程 多线程打日志,不建议使用Logging

```python
import logging,time

LOG_FORMAT = "%(levelname)s [%(asctime)s] %(pathname)s %(filename)s %(funcName)s [line:%(lineno)d] \n \t %(message)s \n"
filename = time.strftime("%Y_%m_%d", time.localtime()) + '.log'
logging.basicConfig(filename=filename, level=logging.DEBUG, format=LOG_FORMAT)

logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            logging.info(f"Args: {args}")
        if kwargs:
            logging.info(f"Kwargs:{kwargs}")
        try:
            logging.info(f"func_name：{func.__name__}")
            rsp = func(*args, **kwargs)
            logging.info(f"Response: {rsp}")
            return rsp
        except Exception as e:
            logging.error(repr(e))
            raise e
    return wrapper
```
logging 模块
https://www.cnblogs.com/yyds/p/6901864.html

基于 python 装饰器和 logging 模块实现清晰便于追踪的接口日志
https://juejin.cn/post/6844904187046658062

https://docs.djangoproject.com/zh-hans/3.2/topics/logging/

Loggers(记录器)
Handlers(处理器)
Filters(过滤器)
Formatters(格式化器)




## 自定义异常类
```python
class BizNameError(Exception):
    def __init__(self, biz_name, message=None):
        super().__init__(message)
        self.biz_name = biz_name

    def __str__(self):
        return (f"{self.biz_name}业务名称不符合规范，只支持下划线")
try:
    raise BizNameError(bk_biz_name)
except BizNameError as err:
    print('error: {}'.format(err))
```


https://bk.tencent.com/s-mart/community/question/1206?type=answer


[python多进程打日志的问题](https://www.jianshu.com/p/f85443c562d9)



#### propagate 参数说明

在 Django 的日志配置中，propagate 是一个可选参数，用于指定是否将日志消息传递给更高层级的 Logger 对象。

当 propagate=True 时，表示该 logger 对象的日志消息将被传递到上级 logger 对象中。如果上级 logger 对象也具有 propagate=True，则日志消息会不断地向上传递，直到某一个 logger 对象的 propagate=False，或者到达根 logger 对象为止。

当 propagate=False 时，表示该 logger 对象的日志消息不会被传递到上级 logger 对象中。这通常用于避免日志消息重复输出，或者控制日志消息的输出位置和格式。

在实际应用中，通常建议将顶级 logger 对象的 propagate 设置为 False，以避免出现日志消息的重复输出。


## Formatters(格式化器)

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(pathname)s '
                      '[line:%(lineno)d] %(funcName)s %(module)s %(process)d %(thread)d '
                      '\n \t %(message)s \n',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s [%(asctime)s] %(message)s',
        },
    }
}
```

## Handlers(处理器)



## Loggers(记录器)


### django.db.backends

django.db.backends 是 Django 中的一个日志记录器，用于记录数据库引擎的详细信息，包括 SQL 查询语句、执行时间等。

该日志记录器常常被用来调试和优化数据库查询性能。例如，在 settings.py 文件中进行如下配置：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```
上述配置将设置名为 'django.db.backends' 的 logger 对象将 DEBUG 及以上级别（即数据库查询相关的详细信息）的日志消息输出到控制台。这样可以方便地查看每个数据库查询所花费的时间，以及哪些查询会导致性能瓶颈等问题。