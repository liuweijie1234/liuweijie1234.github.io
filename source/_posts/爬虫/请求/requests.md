---
title: Python3 请求库 requests
date: 2022-08-15 10:22:00
tags:
- Python module
- requests
categories:
- Python
---

推荐软件 Postman、Apipost 来进行接口测试。


### 简介

一个 HTTP 客户端库，跟 urllib, urllib2 类似

- 用途

发送请求

### 安装

```bash
# 安装
pip install requests

python -m pip install requests
```

### 基本使用

```python
import requests

r = requests.get('https://github.com/timeline.json')
r = requests.post('https://httpbin.org/post')
r = requests.put("http://httpbin.org/put")
r = requests.delete("http://httpbin.org/delete")
r = requests.patch('https://httpbin.org/patch')
r = requests.head("http://httpbin.org/get")
r = requests.options("http://httpbin.org/get")

```

### 参考链接

http://docs.python-requests.org/zh_CN/latest/user/quickstart.html

https://cuiqingcai.com/202222.html


### requests.get()方法

```python
try:
  r = requests.get('http://www.google.com.hk', timeout=5)
  return r.text
except requests.exceptions.RequestException as e:
  print(e)
print(time.strftime('%Y-%m-%d %H:%M:%S'))
```

params参数：

```python
import requests

data = {
    'name': 'germey',
    'age': 25
}
r = requests.get('https://httpbin.org/get', params=data)
print(r.text)  # 字符串
print(type(r.text))
print(r.json())  # json格式
print(type(r.json()))
print(r.content)  # 字节流(二进制数据)
```

添加headers参数：

```python
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get('https://ssr1.scrape.center/', headers=headers)
print(r.text)
```

### requests.post()方法

https://www.begtut.com/python/ref-requests-post.html

在requests.post()方法中，data和json参数是用于发送POST请求时传递数据的两种常用方式。

**data参数：**

- 类型：字典、元组列表或字节串。
- 作用：用于以**表单**形式传递数据。
- 示例：

```python
import requests

url = 'https://www.httpbin.org/post'
data = {"name": "germey", "age": "25"}
with requests.Session() as session:
    session.trust_env = False
    response = session.post(url=url, data=data)
print(response.text)

{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "age": "25", 
    "name": "germey"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "18", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "www.httpbin.org", 
    "User-Agent": "python-requests/2.27.1", 
    "X-Amzn-Trace-Id": "Root=1-65699f3e-4f0e76432b5b7bf85c607ea7"
  }, 
  "json": null, 
  "origin": "114.112.238.18", 
  "url": "https://www.httpbin.org/post"
}
```

注意事项：
使用data参数发送的数据将会以表单（form）形式编码，并且请求头中的Content-Type将设置为application/x-www-form-urlencoded。
如果data参数传递的是字节串，则请求头中的Content-Type将根据请求头中的Content-Type字段自动设置。

**json参数：**

- 类型：字典或可转换为JSON格式的对象。
- 作用：用于发送**JSON格式**的数据。
- 示例：
```python
import requests

url = 'https://www.httpbin.org/post'
data = {"name": "germey", "age": "25"}
s = requests.Session()
s.trust_env = False
response = s.post(url=url, json=data)
print(response.text)

{
  "args": {}, 
  "data": "{\"name\": \"germey\", \"age\": \"25\"}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "31", 
    "Content-Type": "application/json", 
    "Host": "www.httpbin.org", 
    "User-Agent": "python-requests/2.27.1", 
    "X-Amzn-Trace-Id": "Root=1-65699d68-7cc034fc484014862f10348a"
  }, 
  "json": {
    "age": "25", 
    "name": "germey"
  }, 
  "origin": "114.112.238.18", 
  "url": "https://www.httpbin.org/post"
}
```

注意事项：
使用json参数发送的数据将会以JSON (data) 格式编码，并且请求头中的Content-Type将设置为application/json。
requests库会自动将json参数转换为JSON格式，并且编码为字节串。

综上所述，data参数用于发送表单形式的数据，而json参数用于发送JSON格式的数据。在使用时根据需要选择合适的参数进行数据传递。


### response 对象(响应)

```python
import json
import requests

url = 'https://bk.tencent.com'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "xxx",
    "Host": "bk.tencent.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    "X-CSRFToken": ""
}

response = requests.get(url=url, headers=headers)
# Response_get = requests.get(url, params=None, **kwargs)
# Response_post = requests.post(url, data=None, json=None, **kwargs)
print(response.__dir__())
['_content', '_content_consumed', '_next', 'status_code', 'headers', 'raw', 'url', 'encoding', 'history', 'reason', 'cookies', 'elapsed', 'request', 'connection',
'__module__', '__doc__', '__attrs__', '__init__', '__enter__', '__exit__', '__getstate__', '__setstate__', '__repr__', '__bool__', '__nonzero__', '__iter__', 'ok', 'is_redirect', 
'is_permanent_redirect', 'next', 'apparent_encoding', 'iter_content', 'iter_lines', 'content', 'text', 'json', 'links', 'raise_for_status', 'close', '__dict__', '__weakref__',
'__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__',
'__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']

print(f'获取响应的状态码:{response.status_code}')
print(f'获取响应头（字典）:{response.headers}')
print(f'获取响应的cookies:{response.cookies}')
print(f'获取响应内容（字节流）:{response.content}')
print(f'获取响应内容（字符串）:{response.text}')
print(f'获取响应内容（JSON）:{response.json()}')
print(f'响应返回了错误状态码，引发一个异常（通常是 HTTPError）:{response.raise_for_status()}')
print(f'获取响应时间间隔:{str(response.elapsed.total_seconds()}')  # 执行时间，类似 response.elapsed.microseconds / 1000000
print(f'获取最后实际访问的 URL（用于处理重定向）:{response.url}')
print(f'获取请求历史:{response.history}')
print(f'response.apparent_encoding:{response.apparent_encoding}')
print(f'response.encoding:{response.encoding}')
print(f'判断是否请求成功（状态码在 200-299 范围内）:{response.ok}') 
```

json.loads(response.text)和response.json()是两种不同的方法来解析HTTP响应中的JSON数据。

1、json.loads(response.text)：

response.text返回HTTP响应的内容，通常为字符串。
json.loads()是json模块提供的方法，用于将JSON格式的字符串解析为Python对象（通常是字典或列表）。
所以，json.loads(response.text)是将HTTP响应的内容（字符串）解析为Python对象。

2、response.json()：

response.json()是requests模块的方法，专门用于处理HTTP响应为JSON格式的数据。
它会首先检查HTTP响应的 Content-Type 头部是否指定为 JSON 类型，然后尝试将响应的内容解析为JSON格式。
如果响应的内容不是有效的JSON格式，或者 Content-Type 不是 JSON 类型，那么 response.json() 方法会引发一个异常。
response.json()会直接返回解析为JSON的内容（通常是Python字典或列表），而不需要额外的解析步骤。

综上所述，主要区别在于使用json.loads(response.text)需要手动提取响应的内容，并进行额外的解析步骤；而response.json()方法会自动处理和解析响应的JSON数据，提供一种更便捷的方式。




### 绕过系统设置的代理

第1种方法
```python
with requests.Session() as session:
    session.trust_env = False
    response = session.get('http://httpbin.org/')
```


第2种方法
```python
proxies = { "http": None, "https": None}
requests.get("http://httpbin.org/", proxies=proxies)
```

### 工作遇到的问题

[Python多线程Request问题](https://segmentfault.com/q/1010000023124901)

[python多线程接口案例](https://blog.csdn.net/qq_43400993/article/details/105591240)



[python requests发起请求，报“Max retries exceeded with url”](https://blog.csdn.net/AugustMe/article/details/124466301)

[Python 关于requests 关闭连接，优化内存](https://blog.csdn.net/weixin_44777680/article/details/108961565)

[Python 关闭http请求](https://stackoom.com/question/gRPC)


```python
import requests
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor

# 定义请求的URL和参数
url = "http://192.168.0.109/getSn/"

body_json = {
    "barcode": "D173LBA41C210402A04196",
    "MAC": "000000000000",
    "series": "W90"
}

# 定义Excel表格
wb = Workbook()
ws = wb.active

# 写入表头
ws['A1'] = '状态码'
ws['B1'] = '响应时间'


# 定义一个函数来发送请求并记录结果
def send_request(i):
    response = requests.post(url, data=body_json)
    status_code = response.status_code
    elapsed_time = response.elapsed.total_seconds()

    # 将结果写入Excel表格
    ws.cell(row=i+2, column=1, value=status_code)
    ws.cell(row=i+2, column=2, value=elapsed_time)

# 使用ThreadPoolExecutor创建多个线程来发送请求
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for i in range(10):  # 循环发送10次请求
        future = executor.submit(send_request, i)
        futures.append(future)

    # 等待所有请求结束
    for future in futures:
        future.result()

# 保存Excel表格
wb.save('result.xlsx')
```



### 文件上传

```python
import requests

files = {'file': open('favicon.ico', 'rb')}
r = requests.post('https://httpbin.org/post', files=files)
print(r.text)
```

### Cookies 设置

```python
import requests

headers = {
    'Cookie': '_octo=GH1.1.1849343058.1576602081; _ga=GA1.2.90460451.1576602111; __Host-user_session_same_site=nbDv62kHNjp4N5KyQNYZ208waeqsmNgxFnFC88rnV7gTYQw_; _device_id=a7ca73be0e8f1a81d1e2ebb5349f9075; user_session=nbDv62kHNjp4N5KyQNYZ208waeqsmNgxFnFC88rnV7gTYQw_; logged_in=yes; dotcom_user=Germey; tz=Asia%2FShanghai; has_recent_activity=1; _gat=1; _gh_sess=your_session_info',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
}
r = requests.get('https://github.com/', headers=headers)
print(r.text)
```

### Session 设置

```python
import requests

s = requests.Session()
s.get('https://httpbin.org/cookies/set/number/123456789')
r = s.get('https://httpbin.org/cookies')
print(r.text)
```


### SSL证书验证

```python
import requests
from requests.packages import urllib3

urllib3.disable_warnings()
response = requests.get('https://ssr2.scrape.center/', verify=False)
print(response.status_code)
```

### 超时设置

```python
import requests

r = requests.get('https://httpbin.org/get', timeout=1)
print(r.status_code)

# 请求分为两个阶段，即连接（connect）和读取（read）。
r = requests.get('https://httpbin.org/get', timeout=(5, 30))
```

### 身份认证

```python

import requests

r = requests.get('https://ssr3.scrape.center/', auth=('admin', 'admin'))  # 默认使用 HTTPBasicAuth 这个类来认证。
print(r.status_code)
```

- 使用 OAuth1 认证

```python
import requests
from requests_oauthlib import OAuth1

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
              'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
requests.get(url, auth=auth)
```

### 代理设置


requests 还支持 SOCKS 协议的代理，需要安装 socks 这个库
```bash
pip3 install "requests[socks]"
```

```python
import requests

proxy = '127.0.0.1:7890'
proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy,
}
try:
    response = requests.get('https://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
```

```python
import requests

proxies = {
  'http': 'http://10.10.10.10:1080',
  'https': 'http://10.10.10.10:1080',
}
requests.get('https://httpbin.org/get', proxies=proxies)
```


```python
import requests

proxies = {'https': 'http://user:password@10.10.10.10:1080/',}
requests.get('https://httpbin.org/get', proxies=proxies)
```