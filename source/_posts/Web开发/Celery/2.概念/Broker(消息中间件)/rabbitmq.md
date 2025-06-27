---
title: django celery broker rabbitmq
date: 2022-08-15 15:52:00
tags:
- Django
categories:
- Django
---



一、rabbitmq的安装
   
   rabbitmq是celery常用的broker之一，它的角色是消息队列。
  
   1. 安装依赖的erlang语言开发包

   安装程序：otp_win32_R16B03-1.exe
   
   安装说明：在win7下建议默认安装，安装完后，
   
             设置环境变量，例如ERLANG_HOME=C:\Program Files\erl5.10.4，
	     
	     添加到PATH中，PATH=%ERLANG_HOME%\bin

   2. 安装rabbitmq

   安装程序：rabbitmq-server-3.2.4.exe
   
   安装说明：安装成功后设置环境变量，例如RABBITMQ_SERVER=C:\Program Files\RabbitMQ Server\rabbitmq_server-3.2.4
             
	     添加到PATH中， PATH=%RABBITMQ_SERVER%\sbin 
   
	     进入%RABBITMQ_SERVER%\sbin目录，执行rabbitmq-plugins enable rabbitmq_management
	     
             最后执行下面3行命令
	      
	     rabbitmq-service.bat stop

	     rabbitmq-service.bat install

	     rabbitmq-service.bat start

   3. 测试安装

   浏览器中输入http://localhost:15672/#/ 默认账号：guest, 密码guest。登陆成功后，表示rabbitmq安装成功。


二、celery的包安装

    celery是一个异步任务队列/基于分布式消息传递的作业队列，以python语言实现，正在被广泛应用，每天处理数以百万计的任务。

    结合django，需要安装两个包：celery和django-celery。命令python setup.py install.

    1. celery安装(依赖包见"celery安装依赖包.rar"中)
    
     首先安装依赖包，顺序为anyjson-0.3.3->py-amqp-3.3.0.30->kombu-3.0.26->billiard-3.3.0.30->pytz-2015.4
     
     最后安装celery-3.1.25
    
    2. djcelery安装
      
     直接安装django-celery-3.2.1


ps:由于安装了新的python包，如果以eclipse开发的话，记得在eclipse下重新配置下python环境。如果遇到问题，请联系蓝鲸助手！！


具体的celery使用请参考《django+celery的使用介绍》
      



