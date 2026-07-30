---
title: 基本的爬虫操作
date: 2022-08-29 10:00:00
tags:
- [Python]
- [爬虫]
- [request]
categories:
- [Python]
- [爬虫]
---

### 抓取网页

爬取网站的标题

```python
import requests
import re

http_url = 'https://ssr1.scrape.center/'
s = requests.Session()
s.trust_env = False  # 若有国外代理可以，不要从操作系统环境中读取代理配置
response = s.get(url=http_url)
pattern = re.compile('<h2.*?>(.*?)</h2>', re.S)
titles = re.findall(pattern, response.text)
print(titles)
```

### 抓取二进制数据

爬取网站的图标（音频或视频文件）

```python
import requests

ico_url = 'https://scrape.center/favicon.ico'
response = requests.get(url=ico_url)
with open('favicon.ico', 'wb') as f:
    f.write(response.content)
```


### 上传文件

```python
import requests

files = {'file': open('favicon.ico', 'rb')}
r = requests.post('https://httpbin.org/post', files=files)
print(r.text)
```

### 认证

- cookies 认证

```python
import requests

cookies = '_octo=GH1.1.363118247.1648188944; _device_id=436af42cbf537605bf03ecf6ea9c0bf0; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=light; tz=Asia%2FShanghai; user_session=qaquwH0HItoSGqaMlvOJx6ABDdHqM-SZzoOiqgvOYUR4P40g; __Host-user_session_same_site=qaquwH0HItoSGqaMlvOJx6ABDdHqM-SZzoOiqgvOYUR4P40g; tz=Asia%2FShanghai; logged_in=yes; dotcom_user=liuweijie1234; has_recent_activity=1; _gh_sess=ZOoliajHidc6L9LYYlCVJxU4rgttVgdipS5GY4O61EKtL4ixqzAplUTGbrMAI5xApKMaZm93E9e4NysJ0T5Xue8WolTSRvDEdxQ4VQA97GGZNDotUpQSZf4CDvT3NXQaJdiPykur4e7F40xISNLHAcPYdmRF73VrE9DQEsEATH7CSQThuJlZLFu5p6Bb%2BuXPJYg9IM6%2B5CVyP28FgNVo9uzLnfYX4NTN2buVN1FViB8SRp7yv9HBCQyMvNR0FBYve1sOiStD0DvoOu1SX7v%2FLN%2FuyW0RM8mZ0YvA71P%2BX%2BW%2FAsYFg7t1TL81Y8sBaRPRfULb1vQmTy6LwWAEUTQbbnup%2BuOmfzmxEWgMFIZZY%2BtZCTe%2FQ5wlXYWPl3mJ69Pt%2Bb73hyK36dybnlFVJU3X6bXrMC6OarC0sy5wraiqiA70VxW7UwzOEafF%2FcTBwrznYzcHqSiR%2B6i1of2CIP%2B8ORuThG0yiZLDzK%2F3lhQl3YNxm9DFLe9tPRrMMIpcdg0cRBi3%2Bgs84WoE2PIDkRFXYI5GjivwuvQC%2BnsaPWfIW8BfxVuPXmcCB%2FWOxJo3n3FPA8aBv3ZL4fjvRSETuRO6vK1XBlEHLRYUV9vZG2%2B505%2FCUduDPO%2FB581cSWBJtzKKaPMAnZ3ORx%2B0Oy%2F2hGbozL7IIvr9PrbShJOb9OEq3NyDJY1CeMKmq0GgFoBPgNV43WKQAWXRupg5OvN3fPhV6V%2FhQE3NLnfhW3vuBvX4VjLDD28qZQHGj6%2FXizgCzD%2F78xE%2BFJRVegg6NgzX--RsoqDr%2BvnWMxFlq9--UUNnuGRNnA67cvVYDW8cfw%3D%3D'
jar = requests.cookies.RequestsCookieJar()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
}
for cookie in cookies.split(';'):
    key, value = cookie.split('=', 1)
    jar.set(key, value)

r = requests.get('https://github.com/', headers=headers, cookies=jar)
print(r.text)

```

- 身份认证

```python

import requests

r = requests.get('https://ssr3.scrape.center/', auth=('admin', 'admin'))
print(r.status_code)

```

- OAuth 认证

pip3 install requests_oauthlib

```python
import requests
from requests_oauthlib import OAuth1

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
              'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
requests.get(url, auth=auth)
```

### Session 维持

```python
s = requests.Session()  # 创建了一个 Session 对象，它是用于发送请求并保持会话状态的实例。Session 对象可以跨多个请求共享参数和状态，例如 cookie 值、身份验证信息等。
s.trust_env = False  # 不要从操作系统环境中读取代理配置
response = s.get(url=self.url, headers=self.headers)
```

通过代码的对比可发现使用 session 对象效率会更好，不用每次都将cookie信息放到请求内容中了
session对象能够自动获取到cookie并且可以在下一次请求红自动带上我们所得到的的cookie信息，不用人为的去填写

[session 让网络请求变得更快](https://benpaodewoniu.github.io/2022/01/05/python152/)

### 忽略SSL证书验证


```python
import requests

http_url = 'https://ssr1.scrape.center/'
s = requests.Session()
s.trust_env = False
response = s.get(url=http_url, verify=False)
print(response.status_code)
```

### 代理

```python
import requests

proxies = {
    'http': 'http://user:password@10.10.10.10:1080/',
    'https': 'http://user:password@10.10.10.10:1080/'
}
requests.get('https://httpbin.org/get', proxies=proxies)
```

### SOCKS 协议代理

```python
import requests

proxies = {
    'http': 'socks5://user:password@host:port',
    'https': 'socks5://user:password@host:port'
}
requests.get('https://httpbin.org/get', proxies=proxies)
```


### 代理池

需要自行搭建

https://blog.csdn.net/xiaobai729/article/details/124079260



### 异常处理


```log
requests.exceptions.SSLError: HTTPSConnectionPool(host='ssr1.scrape.center', port=443): Max retries exceeded with url: /
 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:833)'),))
```

方法一：下载相关库

https://www.cnblogs.com/wang-jx/p/12235679.html

方法二：使用Session
```python
s = requests.Session()
s.trust_env = False
response = s.get(url=http_url)
```


### 示例

#### 传统前端html 页面爬虫

参考 https://cuiqingcai.com/202224.html

```python
import requests
import logging
import time
import re
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists
import multiprocessing

filename = time.strftime("%Y_%m_%d", time.localtime()) + '.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        proxies = {"http": None, "https": None}
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)
    except Exception as err:
        logging.error(f'{url}error occurred while scraping {err}', exc_info=True)


def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url


def scrape_detail(url):
    return scrape_page(url)


def parse_detail(html):
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }


pattern = r'[\\/:*?<>|]'


def save_data(data):
    name = re.sub(pattern, '', data.get('name'))
    print(name)
    data_path = f'{RESULTS_DIR}/{name}.json'
    print(data_path)
    try:
        json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        # print("Data saved successfully!")
    except Exception as e:
        logging.error(f"Failed to save {data_path}data:{e}")


def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)

    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('saving data to json file')
        save_data(data)
        logging.info('data saved successfully')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()
```

#### ajax 数据爬取




Ajax 分析方法 https://cuiqingcai.com/202252.html

Ajax 案例爬取实战 https://cuiqingcai.com/202253.html

```python
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'
LIMIT = 10
TOTAL_PAGE = 10

session = requests.Session()
session.trust_env = False


def scrape_api(url):
    logging.info('scraping %s...', url)
    try:
        response = session.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'movies'
MONGO_COLLECTION_NAME = 'movies'

import pymongo
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client['movies']
collection = db['movies']


def save_data(data):
    collection.update_one({
        'name': data.get('name')
    }, {
        '$set': data
    }, upsert=True)


def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail data %s', detail_data)
            save_data(detail_data)
            logging.info('data saved successfully')


if __name__ == '__main__':
    main()


```