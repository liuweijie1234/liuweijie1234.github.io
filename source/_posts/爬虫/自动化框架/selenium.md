---
title: Python3 爬虫 selenium
date: 2023-11-15 15:00:00
tags:
- [Python module]
- [爬虫]
- [selenium]
categories:
- Python
---


## 参考

https://cloud.tencent.com/developer/article/1743827

https://cuiqingcai.com/202261.html

## 简介

模拟浏览器爬取

Selenium 是一个自动化测试工具，利用它可以驱动浏览器执行特定的动作，如点击、下拉等操作，同时还可以获取浏览器当前呈现的页面的源代码，做到可见即可爬。
对于一些 JavaScript 动态渲染的页面来说，此种抓取方式非常有效。本节中，就让我们来感受一下它的强大之处吧。

## 安装

### 安装 ChromeDriver 和 Chrome 

ChromeDriver 的安装 https://cuiqingcai.com/31043.html

ChromeDriver 下载地址：

https://sites.google.com/chromium.org/driver/downloads

https://sites.google.com/chromium.org/driver/downloads/version-selection

https://googlechromelabs.github.io/chrome-for-testing/

https://github.com/GoogleChromeLabs/chrome-for-testing?tab=readme-ov-file#json-api-endpoints

https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_124.0.6367

https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json


### 安装 Selenium

https://cuiqingcai.com/33043.html

```bash
pip install selenium
```

验证

如果运行完毕之后弹出来了一个 Chrome 浏览器并加载了百度页面，2 秒之后就关闭了，那就证明没问题了。

```python
from selenium import webdriver
from time import sleep

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
sleep(2)
browser.close()
```


## 用法

### 基本用法

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(f'browser.current_url:{browser.current_url}')
    print(f'browser.get_cookies():{browser.get_cookies()}')
    print(f'browser.page_source:{browser.page_source}')
finally:
    browser.close()
```

### 声明浏览器对象

Selenium 支持非常多的浏览器，如 Chrome、Firefox、Edge 等，还有 Android、BlackBerry 等手机端的浏览器。我们可以用如下方式初始化：

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser = webdriver.Edge()
browser = webdriver.Safari()
```


### 访问页面

我们可以用 get 方法来请求网页，其参数传入链接 URL 即可。比如，这里用 get 方法访问淘宝，然后打印出源代码，代码如下：

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
print(browser.page_source)  # 打印出源代码
browser.close()
```

### 查找节点

Selenium 可以驱动浏览器完成各种操作，比如填充表单、模拟点击等。
比如，我们想要完成向某个输入框输入文字的操作，总需要知道这个输入框在哪里吧？

而 Selenium 提供了一系列查找节点的方法，我们可以用这些方法来获取想要的节点，以便下一步执行一些动作或者提取信息。

#### 单个节点

比如，想要从淘宝页面中提取搜索框这个节点，首先要观察它的源代码，如图所示。

```html
<input id="q" name="q" aria-label="请输入搜索文字" accesskey="s" autofocus="true" autocomplete="off" aria-haspopup="true" aria-combobox="list" role="combobox" x-webkit-grammar="builtin:translate">
```


我们可以看到，
搜索框的 id 是 q，所以我们可以用 find_element_by_id 方法来获取这个节点。
搜索框的 name 属性是 q，所以我们也可以用 find_element_by_name 方法来获取这个节点。

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element_by_id('q')  # 注意这里的 id 选择器
input_second = browser.find_element_by_css_selector('#q')  # 注意这里的 css 选择器
input_third = browser.find_element_by_xpath('//*[@id="q"]')  # 注意这里的 xpath 路径
print(input_first, input_second, input_third)
browser.close()
```

获取单个节点的方法

```python
find_element_by_id
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
```


通用方法 
find_element，它需要传入两个参数：查找方式 By 和值。
实际上，它就是 find_element_by_id 这种方法的通用函数版本，
比如 find_element_by_id(id) 就等价于 find_element(By.ID, id)，二者得到的结果完全一致。

我们用代码实现一下：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element(By.ID, 'q')
print(input_first)
browser.close()
```

#### 多个节点

如果查找的目标在网页中只有一个，那么完全可以用 find_element 方法。但如果有多个节点，再用 find_element 方法查找，就只能得到第一个节点了。

如果要查找所有满足条件的节点，需要用 find_elements 这样的方法。

> 注意，在这个方法的名称中，element 多了一个 s，注意区分。

比如，要查找淘宝左侧导航条的所有条目，就可以这样来实现：

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector('.service-bd li')
print(lis)
browser.close()
```

运行结果


```bash
[<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.12")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.13")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.14")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.15")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.16")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.17")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.18")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.19")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.20")>, 
<selenium.webdriver.remote.webelement.WebElement (session="92787daee09d36d39a0ad8242c54c09a", element="f.8B38D179D4A9E65EB144B6CBAC7E6AC6.d.36BFC95E8A1FE2D3623F8D0F586EF876.e.21")>]
```


获取多个节点的方法

```python
find_elements_by_id
find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector
```

当然，我们也可以直接用 find_elements 方法来选择，这时可以这样写：
```python
lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')
```


### 节点交互操作

Selenium 可以驱动浏览器来执行一些操作，也就是说可以让浏览器模拟执行一些动作。

比较常见的用法有：
输入文字时用 send_keys 方法，
清空文字时用 clear 方法，
点击按钮时用 click 方法。

示例如下：

```python
from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element_by_id('q')
input.send_keys('iPhone')
time.sleep(1)
input.clear()
input.send_keys('iPad')
button = browser.find_element_by_class_name('btn-search')
button.click()
```

这里首先驱动浏览器打开淘宝，然后用 find_element_by_id 方法获取输入框，然后用 send_keys 方法输入 iPhone 文字，等待一秒后用 clear 方法清空输入框，再次调用 send_keys 方法输入 iPad 文字，之后再用 find_element_by_class_name 方法获取搜索按钮，最后调用 click 方法完成搜索动作。

通过上面的方法，我们完成了一些常见节点的操作，
更多的操作可以参见官方文档的交互动作介绍 ：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement


### 动作链

在上面的实例中，一些交互动作都是针对某个节点执行的。
比如，对于输入框，我们就调用它的输入文字和清空文字方法；
对于按钮，就调用它的点击方法。
其实，还有另外一些操作，它们没有特定的执行对象，比如鼠标拖曳、键盘按键等，这些动作用另一种方式来执行，那就是动作链。

比如，现在实现一个节点的拖曳操作，将某个节点从一处拖曳到另外一处，可以这样实现：


```python
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')  # 拖动的源节点
target = browser.find_element_by_css_selector('#droppable')  # 目标节点
actions = ActionChains(browser)  # 创建动作链
actions.drag_and_drop(source, target)   # 执行拖动操作
actions.perform()     # 执行动作链
```

更多的动作链操作可以参考官方文档的动作链介绍：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains。

### 执行 JavaScript

Selenium 还可以执行 JavaScript 代码，比如可以用 execute_script 方法执行 JavaScript 代码，或者用 execute_async_script 方法执行异步 JavaScript 代码。

对于某些操作，Selenium API 并没有提供。比如，下拉进度条，它可以直接模拟运行 JavaScript，此时使用 execute_script 方法即可实现，代码如下：


```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')    # 下拉到页面底部
browser.execute_script('alert("To Bottom")')                             # 弹出提示框
```

这里就利用 execute_script 方法将进度条下拉到最底部，然后弹出 alert 提示框。

所以说有了这个方法，基本上 API 没有提供的所有功能都可以用执行 JavaScript 的方式来实现了。

### 获取节点信息


Selenium 提供了很多方法来获取节点信息，比如获取节点的文本内容、属性值、位置、大小等。

通过 page_source 属性可以获取网页的源代码，接着就可以使用解析库（如正则表达式、Beautiful Soup、pyquery 等）来提取信息了。

不过，既然 Selenium 已经提供了选择节点的方法，返回的是 WebElement 类型，那么它也有相关的方法和属性来直接提取节点信息，如属性、文本等。这样的话，我们就可以不用通过解析源代码来提取信息了，非常方便。

#### 获取属性

比如，要获取某个节点的属性值，可以用 get_attribute 方法，代码如下：


```python
from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://spa2.scrape.center/'
browser.get(url)
logo = browser.find_element_by_class_name('logo-image')
print(logo)
print(logo.get_attribute('src'))
print(logo.get_attribute('href'))
```

这里用 find_element_by_class_name 方法获取 class 为 logo-image 节点，然后用 get_attribute 方法获取其 src 属性值。

#### 获取文本内容

要获取某个节点的文本内容，可以用 text 属性，代码如下：


```python
from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://spa2.scrape.center/'
browser.get(url)
title = browser.find_element_by_class_name('logo-title')
print(title)
print(title.text)
```

这里用 find_element_by_class_name 方法获取 class 为 logo-title 节点，然后用 text 属性获取其文本内容。

#### 获取ID、位置、标签名和大小

id 属性可以获取节点 ID，location 属性可以获取该节点在页面中的相对位置，tag_name 属性可以获取标签名称，size 属性可以获取节点的大小，也就是宽高


```python
from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://spa2.scrape.center/'
browser.get(url)
input = browser.find_element_by_class_name('logo-title')
print(input.id)   # 获取节点 ID
print(input.location)  # 获取节点位置
print(input.tag_name)  # 获取标签名称
print(input.size)     # 获取节点大小
```

#### 获取父节点、子节点、兄弟节点

parent 属性可以获取该节点的父节点，find_element_by_xpath 方法可以获取子节点，find_elements_by_xpath 方法可以获取兄弟节点。


```python
from selenium import webdriver


browser = webdriver.Chrome()
url = 'https://spa2.scrape.center/'
browser.get(url)
input = browser.find_element_by_class_name('logo-title')
parent = input.parent
print(parent)
children = parent.find_elements_by_xpath('./*')
print(children)
sibling = input.find_elements_by_xpath('./following-sibling::*')
print(sibling)
```

这里用 parent 属性获取父节点，用 find_elements_by_xpath 方法获取父节点的所有子节点，用 find_elements_by_xpath 方法获取兄弟节点。

### 切换 Frame

我们知道网页中有一种节点叫作 iframe，也就是子 Frame，相当于页面的子页面，它的结构和外部网页的结构完全一致。
Selenium 打开页面后，它默认是在父级 Frame 里面操作，而此时如果页面中还有子 Frame，它是不能获取到子 Frame 里面的节点的。
这时就需要使用 switch_to.frame 方法来切换 Frame。

示例如下：

```python
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')         # 切换到子 Frame
try:
    logo = browser.find_element_by_class_name('logo')  # 获取子 Frame 里面的节点
except NoSuchElementException:
    print('NO LOGO')
browser.switch_to.parent_frame()                 # 切换回父 Frame
logo = browser.find_element_by_class_name('logo')  # 获取父 Frame 里面的节点
print(logo)
print(logo.text)
```

### 延时等待

在 Selenium 中，get 方法会在网页框架加载结束后结束执行，此时如果获取 page_source，可能并不是浏览器完全加载完成的页面，如果某些页面有额外的 Ajax 请求，我们在网页源代码中也不一定能成功获取到。

所以，这里需要延时等待一定时间，确保节点已经加载出来。

这里等待方式有两种：一种是隐式等待，一种是显式等待。

#### 隐式等待

当使用隐式等待执行测试的时候，如果 Selenium 没有在 DOM 中找到节点，将继续等待，超出设定时间后，则抛出找不到节点的异常。

换句话说，

当查找节点而节点并没有立即出现的时候，隐式等待将等待一段时间再查找 DOM，默认的时间是 0。

示例如下：

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.implicitly_wait(10)  # 设置隐式等待时间为 10 秒
browser.get('https://spa2.scrape.center/')
input = browser.find_element_by_class_name('logo-image')
print(input)
```


#### 显式等待

隐式等待的效果其实并没有那么好，因为我们只规定了一个固定时间，而页面的加载时间会受到网络条件的影响。

这里还有一种更合适的显式等待方法，它指定要查找的节点，然后指定一个最长等待时间。

如果在规定时间内加载出来了这个节点，就返回查找的节点；如果到了规定时间依然没有加载出该节点，则抛出超时异常。

示例如下：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait = WebDriverWait(browser, 10)    # 设置最长等待时间为 10 秒
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))  # 等待 ID 为 q 的节点出现
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))   # 等待 class 为 btn-search 的节点可点击
print(input, button)
```

#### 等待条件

| 等待条件 | 含义 |
| --- | --- |
| title_is | 标题是某内容 |
| title_contains | 标题包含某内容 |
| presence_of_element_located | 节点加载出来，传入定位元组，如 (By.ID, 'p') |
| visibility_of_element_located | 节点可见，传入定位元组 |
| visibility_of | 可见，传入节点对象 |
| presence_of_all_elements_located | 所有节点加载出来 |
| text_to_be_present_in_element | 某个节点文本包含某文字 |
| text_to_be_present_in_element_value | 某个节点值包含某文字 |
| frame_to_be_available_and_switch_to_it frame | 加载并切换 |
| invisibility_of_element_located | 节点不可见 |
| element_to_be_clickable | 节点可点击 |
| staleness_of | 判断一个节点是否仍在 DOM，可判断页面是否已经刷新 |
| element_to_be_selected | 节点可选择，传入节点对象 |
| element_located_to_be_selected | 节点可选择，传入定位元组 |
| element_selection_state_to_be | 传入节点对象以及状态，相等返回 True，否则返回 False |
| element_located_selection_state_to_be | 传入定位元组以及状态，相等返回 True，否则返回 False |
| alert_is_present | 是否出现 Alert |

更多等待条件的参数及用法介绍可以参考官方文档：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions。



### 前进后退

平常使用浏览器时，都有前进和后退功能，Selenium 也可以完成这个操作，它使用 back 方法后退，使用 forward 方法前进

```python
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.python.org/')
browser.back()
time.sleep(1)
browser.forward()
browser.close()
```

### Cookies

使用 Selenium，还可以方便地对 Cookies 进行操作，例如获取、添加、删除 Cookies 等。

示例如下：

```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())  # 获取所有 Cookies
browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'})  # 添加 Cookie
print(browser.get_cookies())
browser.delete_all_cookies()  # 删除所有 Cookies
print(browser.get_cookies())
browser.refresh()  # 刷新页面
```

selenium添加cookie自动登录 

https://www.cnblogs.com/loren880898/p/15107122.html

#### 在Selenium中，如何确保在调用delete_all_cookies()方法后cookies已经被完全清除?


**刷新页面**：

在调用delete_all_cookies()方法后，可以使用browser.refresh()方法刷新页面，以确保新的页面加载时不包含任何旧的cookies。

**等待一段时间**：

在调用delete_all_cookies()方法后，可以添加一个短暂的等待时间，例如使用time.sleep(seconds)方法等待几秒钟，以确保浏览器有足够的时间清除cookies。

**验证cookies**：

在调用delete_all_cookies()方法后，可以再次调用browser.get_cookies()方法获取当前的cookies列表，并检查列表是否为空，以验证是否成功清除了所有cookies。

### 选项卡管理


在访问网页的时候，会开启一个个选项卡。在 Selenium 中，我们也可以对选项卡进行操作。

示例如下：

```python
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')   # 打开一个新选项卡
print(browser.window_handles)   # 获取所有选项卡的句柄
browser.switch_to.window(browser.window_handles[1])   # 切换到第二个选项卡
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to.window(browser.window_handles[0])   # 切换回第一个选项卡
browser.get('https://python.org')
```

### 异常处理


在使用 Selenium 时，可能会遇到各种各样的异常，比如找不到节点、超时、页面加载失败等。

选择一个并不存在的节点，此时就会遇到异常 
```bash
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="hello"]"}
```

```python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('Time Out')
try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()
```

关于更多的异常类，可以参考官方文档：：http://selenium-python.readthedocs.io/api.html#module-selenium.common.exceptions。


### 反屏蔽

现在很多网站都加上了对 Selenium 的检测，来防止一些爬虫的恶意爬取。即如果检测到有人在使用 Selenium 打开浏览器，那就直接屏蔽。

在大多数情况下，检测的基本原理是检测当前浏览器窗口下的 window.navigator 对象是否包含 webdriver 这个属性。
因为在正常使用浏览器的情况下，这个属性是 undefined，然而一旦我们使用了 Selenium，Selenium 会给 window.navigator 设置 webdriver 属性。
很多网站就通过 JavaScript 判断如果 webdriver 属性存在，那就直接屏蔽。


这边有一个典型的案例网站：https://antispider1.scrape.center/，

这个网站就使用了上述原理实现了 WebDriver 的检测，如果使用 Selenium 直接爬取的话，那就会返回如图所示的页面。

这时候我们可能想到直接使用 JavaScript 语句把这个 webdriver 属性置空，比如通过调用 execute_script 方法来执行如下代码：

```javascript
Object.defineProperty(navigator, "webdriver", { get: () => undefined });
```

这行 JavaScript 语句的确可以把 webdriver 属性置空，但是 execute_script 调用这行 JavaScript 语句实际上是在页面加载完毕之后才执行的，执行太晚了，网站早在最初页面渲染之前就已经对 webdriver 属性进行了检测，所以用上述方法并不能达到效果。

在 Selenium 中，我们可以使用 CDP（即 Chrome Devtools-Protocol，Chrome 开发工具协议）来解决这个问题，通过它我们可以实现在每个页面刚加载的时候执行 JavaScript 代码，
执行的 CDP 方法叫作 Page.addScriptToEvaluateOnNewDocument，然后传入上文的 JavaScript 代码即可，这样我们就可以在每次页面加载之前将 webdriver 属性置空了。
另外，我们还可以加入几个选项来隐藏 WebDriver 提示条和自动化扩展信息，

代码实现如下：

```python
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()  # 创建 Options 对象
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏 WebDriver 提示条
option.add_experimental_option('useAutomationExtension', False)  # 禁用自动化扩展

browser = webdriver.Chrome(options=option)  # 创建浏览器对象
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
browser.get('https://antispider1.scrape.center/')
```

对于大多数情况，以上方法均可以实现 Selenium 反屏蔽。但对于一些特殊网站，如果它有更多的 WebDriver 特征检测，可能需要具体排查。

### 无头模式

我们可以观察到，上面的案例在运行的时候，总会弹出一个浏览器窗口，虽然有助于观察页面爬取状况，但在有时候窗口弹来弹去也会形成一些干扰。

Chrome 浏览器从 60 版本已经支持了无头模式，即 Headless。无头模式在运行的时候不会再弹出浏览器窗口，减少了干扰，而且它减少了一些资源的加载，如图片等，所以也在一定程度上节省了资源加载时间和网络带宽。

我们可以借助于 ChromeOptions 来开启 Chrome Headless 模式，

代码实现如下：

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = Options()  # 创建 Options 对象
option.add_argument('--headless')  # 开启 Headless 模式
browser = webdriver.Chrome(options=option)  # 创建浏览器对象
browser.set_window_size(1366, 7681)  # 设置浏览器窗口大小
browser.get('https://www.baidu.com')     # 打开网页
browser.get_screenshot_as_file('preview.png')   # 截图并保存

print(browser)
```

## 实战

### Selenium爬取拉勾网数据

参考 https://cloud.tencent.com/developer/article/1743827

```python
# logou_cookies.py
import time
import json
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')  # 禁用gpu
options.add_argument("--start-maximized")  # 窗口最大
options.add_argument('--ignore-certificate-errors') #忽略一些莫名的问题
# options.add_argument('--proxy-server={0}'.format(proxy.proxy))  # 加代理
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 开启开发者模式
options.add_argument('--disable-blink-features=AutomationControlled')  # 谷歌88版以上防止被检测
# options.add_argument('--headless')  # 无界面
driver = webdriver.Chrome(options=options)  # 将chromedriver放到Python安装目录Scripts文件夹下
driver.get('https://www.lagou.com/jobs/list_Python?xl=%E6%9C%AC%E7%A7%91&px=new&yx=15k-25k&city=%E6%B7%B1%E5%9C%B3')
# 此处手动输入账号密码登录网站
time.sleep(100)
cookies = driver.get_cookies()
print(cookies)
with open('cookies_180.json', 'w') as f:
    f.write(json.dumps(cookies))
driver.close()
```

```python
# lagou_spider.py
import json

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import openpyxl
import random
import logging


wb = openpyxl.Workbook()  # 创建工作薄对象
sheet = wb.active  # 获取活动的工作表
# 添加列名
sheet.append(
    ['add_time', 'href_value', 'job_name', 'company_name', 'city', 'industry', 'salary', 'experience_edu', 'welfare', 'job_label'])
# 输出日志的基本配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


# 抓取每页数据函数
def get_data():
    # Xpath提取想要的数据
    items = browser.find_elements("xpath", '//*[@id="s_position_list"]/ul/li')
    # 遍历 获取这一页的每条招聘信息
    for item in items:
        add_time = item.find_element("xpath", './/div[@class="p_top"]/span[@class="format-time"]').text
        href_value = item.find_element("xpath", './/div[@class="p_top"]/a').get_attribute('href')
        job_name = item.find_element("xpath", './/div[@class="p_top"]/a/h3').text
        company_name = item.find_element("xpath", './/div[@class="company_name"]').text
        city = item.find_element("xpath", './/div[@class="p_top"]/a/span[@class="add"]/em').text
        industry = item.find_element("xpath", './/div[@class="industry"]').text
        salary = item.find_element("xpath", './/span[@class="money"]').text
        experience_edu = item.find_element("xpath", './/div[@class="p_bot"]/div[@class="li_b_l"]').text
        welfare = item.find_element("xpath", './/div[@class="li_b_r"]').text
        job_label = item.find_element("xpath", './/div[@class="list_item_bot"]/div[@class="li_b_l"]').text

        data = f'{add_time},{job_name},{company_name},{city},{industry},{salary},{experience_edu},{welfare},{job_label},{href_value}'
        # 爬取数据  输出日志信息
        sheet.append([add_time, href_value, job_name, company_name, city, industry, salary, experience_edu, welfare, job_label])
        logging.info(data)

def search_product(key_word):
    # browser.find_element_by_id('cboxClose').click()     # 关闭让你选城市的窗口
    # time.sleep(2)
    # browser.find_element_by_id('search_input').send_keys(key_word)  # 定位搜索框 输入关键字
    # browser.find_element_by_class_name('search_button').click()     # 点击搜索
    # browser.maximize_window()    # 最大化窗口
    # time.sleep(2)
    # browser.find_element_by_class_name('body-btn').click()    # 关闭弹窗  啥领取红包窗口
    # time.sleep(random.randint(1, 3))

    browser.execute_script("scroll(0,3000)")      # 下拉滚动条
    get_data()           # 调用抓取数据的函数
    # 模拟点击下一页   翻页爬取数据  每爬取一页数据  休眠   控制抓取速度  防止被反爬 可能会让输验证码
    for i in range(10):
        browser.find_element(By.CLASS_NAME, 'pager_next ').click()
        time.sleep(3)
        browser.execute_script("scroll(0,3000)")   # 执行js代码下拉滚动条
        get_data()   # 调用抓取该页数据的函数
        time.sleep(random.randint(3, 5))   # 休眠


def main(url):
    # 访问目标url
    browser.get(url)
    browser.delete_all_cookies()
    time.sleep(random.randint(3, 5))
    with open('cookies_180.json', 'r', encoding='utf-8') as f:
        cookie_list = json.loads(f.read())
    for cookie in cookie_list:
        browser.add_cookie(cookie)
    browser.refresh()
    browser.get_cookies()

    search_product(keyword)
    # 保存数据
    wb.save('job_info.xlsx')


if __name__ == '__main__':
    # 待关键词 比如Python 数据分析
    keyword = 'Python'
    # 本地chromedriver.exe的路径
    chrome_driver = r'E:\chromedriver-win64\chromedriver.exe'

    options = Options()
    options.add_argument("window-size=1920,1080")
    options.add_argument('--disable-gpu')  # 禁用gpu
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏 WebDriver 提示条
    options.add_experimental_option('useAutomationExtension', False)  # 禁用自动化扩展

    browser = Chrome(options=options, executable_path=chrome_driver)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    url = 'https://www.lagou.com/jobs/list_Python?px=default&yx=15k-25k&city=%E6%B7%B1%E5%9C%B3#order'
    main(url=url)

    browser.quit()
    print('运行完成')

```


### 其他实战

Session + Cookie 模拟登录爬取实战 https://cuiqingcai.com/202282.html

## 其他同类库对比

DrissionPage

https://zhuanlan.zhihu.com/p/695402534


知乎
https://www.zhihu.com/question/562879512/answer/3467303740