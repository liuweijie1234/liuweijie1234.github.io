---
title: django 之 requirements.txt
date: 2022-11-11 14:52:00
tags:
- Django
categories:
- Django
---


## django项目所需依赖写入requirements.txt文件


部署django项目到新的环境时，需要先安装所需的依赖。

因此，确定项目所需依赖很关键，日常使用中，有两个命令可以将依赖写入到requirements.txt文件，如下：

1. pip freeze > requirements.txt

该命令在项目目录下执行，会将当前环境的所有依赖全部写到requirements.txt文件，其中包含很多冗余依赖，可用但不推荐

2. pipreqs ./ --encoding=utf-8 --force

该命令在项目目录下执行，会将当前django项目的import的依赖写到requirements.txt文件，不会冗余，推荐使用。

备注：
1.pipreqs命令使用时可能会报该模块不存在，使用pip安装即可，

安装命令：pip install pipreqs

2.pipreqs 命令写入的依赖可能不全，需要手动写入依赖或者改版本

最后：pip install -r requirements.txt  该命令即将依赖安装。


查看已安装包的版本
pip show xxxx

pip 查看某个包有哪些版本
pip install xxx==




原文链接：https://blog.csdn.net/steven_zhulin/article/details/105296897



```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QualitySystem.settings')
django.setup()

```