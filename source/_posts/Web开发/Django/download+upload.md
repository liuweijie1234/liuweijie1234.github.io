---
title: django 下载文件实现
date: 2022-08-15 15:52:00
tags:
- Django
categories:
- Django
---

## django 上传文件 实现方式

[Django官方文档参考](https://docs.djangoproject.com/zh-hans/5.2/topics/http/file-uploads/)


## 用户上传问题

> 注意：可以考虑利用云服务或者 CDN提供静态文件服务来避免用户上传内容问题
> 在框架级别上没有防护技术方案可以安全地验证所有用户上传的文件内容，但是您可以采取其他步骤来减轻这些攻击

1、限制上传大小

如果您的网站接受文件上传，强烈建议您在服务器配置中将这些上传限制在合理大小范围中，以此来防御拒绝服务（DOS）攻击。

在 Apache 中，使用 [LimitRequestBody](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestbody) 指令可以很容易地实现这个设置。

2、限制文件类型

应用可以选择定义一个列表来限制允许用户上传的文件的扩展名，并将 Web 服务器配置为仅为此类文件服务

3、使用二级域名或者子域名

通过一直为来自不同顶级域名或二级域名的用户提供上传内容可以防御一类的攻击。
这可以防止被 same-origin policy 保护机制阻止的任何攻击，比如跨站脚本攻击。
例如您的网站是 example.com，您应当通过形如 usercontent-example.com 的方式来提供上传内容服务（配置 MEDIA_URL）。
仅仅从像 usercontent.example.com 这样的子域提供内容是*不够*的。



## django 下载文件 实现方式


https://bk.tencent.com/s-mart/community/question/1110?type=answer


[Django实用技巧:如何把数据导出到Excel](https://www.django.cn/article/show-9.html)
[django-import-export插件使用教程:处理导入和导出数据](https://www.django.cn/article/show-10.html)

