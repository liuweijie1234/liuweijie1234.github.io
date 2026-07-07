---
title: Python3 模块 smtplib
date: 2022-08-15 10:22:00
tags:
- Python module
- smtplib
categories:
- Python
---

smtplib模块是 Python 标准库中用于发送邮件的模块。

### 基本概念

在使用 smtplib 发送邮件前，我们需要了解一些基本概念：

- SMTP（Simple Mail Transfer Protocol）：简单邮件传输协议，用于发送邮件。
- SSL（Secure Sockets Layer）：安全套接层，用于加密网络连接，防止数据被窃取。
- TLS（Transport Layer Security）：传输层安全协议，是 SSL 的继任者。

### 类与方法

smtplib 模块提供了一个名为 SMTP 的类，表示与邮件服务器的连接。该类的常用方法包括：

```python
SMTP(host='', port=0, local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None)
```

创建 SMTP 类实例，参数如下：

- host：邮件服务器主机名或 IP 地址，默认为空字符串。
- port：邮件服务器端口号，默认为 0。
- local_hostname：本地主机名，默认为 socket.getfqdn() 返回的结果。
- timeout：超时时间，默认为 socket._GLOBAL_DEFAULT_TIMEOUT，即不设置超时时间。
- source_address：用于连接 SMTP 服务器的本地地址，默认为 None。


```python
SMTP.connect(host='localhost', port=0)
```

与邮件服务器建立连接，参数如下：

- host：邮件服务器主机名或 IP 地址，默认为 'localhost'。
- port：邮件服务器端口号，默认为 0，表示使用默认端口。

```python
SMTP.login(user, password)
```

使用指定的用户名和密码登录到邮件服务器，参数如下：

- user：登录用户名。
- password：登录密码或者授权码。

```python
SMTP.sendmail(from_addr, to_addrs, msg, mail_options=[], rcpt_options=[])
```
发送邮件，参数如下：

- from_addr：发件人邮箱地址。
- to_addrs：收件人邮箱地址列表。
- msg：邮件内容，可以是纯文本或 HTML 格式。
- mail_options：邮件选项，用于控制传输方式等，例如 ['SMTPUTF8']。
- rcpt_options：收件人选项，一般为空列表。

```python
SMTP.quit()
```

退出与邮件服务器的连接。

### SSL/TLS 支持

如果需要使用 SSL 或 TLS 连接邮件服务器，则需要使用 smtplib.SMTP_SSL 或 smtplib.SMTP_TLS 类。

这两个类的方法与 SMTP 类相同，不同之处在于连接方式不同：

SMTP_SSL：使用 SSL 加密连接邮件服务器。
SMTP_TLS：使用 STARTTLS 命令启动 TLS 安全连接。

示例代码：

```python
import smtplib

# 连接 SMTP 服务器
smtp = smtplib.SMTP_SSL('smtp.example.com', 465)
smtp.login('your_email@example.com', 'your_password')

# 发送邮件
from_addr = 'your_email@example.com'
to_addrs = ['recipient1@example.com', 'recipient2@example.com']
msg = 'Subject: Test email\n\nThis is a test email.'
smtp.sendmail(from_addr, to_addrs, msg)

# 断开连接
smtp.quit()
```


```python
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header

sender_email = "odoo@kaadas.com"
sender_password = "xxxxx"

receiver_email_list = ["liuweijie@kaadas.com", '2496234829@qq.com']

to_addresses = ", ".join(receiver_email_list)

subject = 'ATECenter预警12345'  # 标题
html_content = """<html>
<body>
<h1>测试测试.12345</h1>
<p>这是一个HTML电子邮件。</p>
<img src="cid:image1">
</body></html>"""  # HTML内容

# 创建主消息对象
message = MIMEMultipart()
message['From'] = email.utils.formataddr(('ATE系统', sender_email))
message['To'] = Header(to_addresses)
message['Subject'] = Header(subject, 'utf-8')

# 添加HTML消息部分
html_part = MIMEText(html_content, 'html')
message.attach(html_part)

# 添加图片作为消息部分
with open('image.png', 'rb') as f:
    image_part = MIMEImage(f.read())
    image_part.add_header('Content-Disposition', 'attachment', filename='image.png')
    image_part.add_header('Content-ID', '<image1>')
    message.attach(image_part)

MAIL_HOST = 'smtp.qiye.163.com'
MAIL_PORT = 587

# 建立SMTP会话
server = smtplib.SMTP(host=MAIL_HOST, port=MAIL_PORT)
server.starttls()

# 登录SMTP服务器
server.login(user=sender_email, password=sender_password)

# 发送电子邮件
server.sendmail(from_addr=sender_email, to_addrs=receiver_email_list, msg=message.as_string())

# 终止SMTP会话
server.quit()
```

在上述示例代码中，我们创建了一个MIMEMultipart对象来构建包含HTML消息和图片的电子邮件。我们使用MIMEText类来创建HTML消息，并使用MIMEImage类将图片添加为嵌入式附件。

在MIMEImage类中，我们设置'Content-Disposition'标头以指定该部分为附件，'Content-ID'标头以指定附件的ID号，这个ID号需要与HTML代码中的'img'标签的'src'属性值相同，以便在电子邮件中正确显示图片。

请注意，添加作为嵌入式图片的附件时，你需要确保在HTML代码中引用的图片文件名与实际附件的文件名相匹配。