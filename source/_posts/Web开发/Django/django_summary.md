---
title: Django 文档入口
date: 2022-08-15 18:14:00
tags:
- Django
categories:
- Django
---

参考 http://djangobook.py3k.cn/2.0/

## 基础教程


{% post_link django/tutorial %}<br>


## 模型层

### 模型
ORM
模型介绍
字段类型
索引
Meta选项
Model类

### QuerySet

执行查询
QuerySet方法
查询表达式

### 模型实例
实例方法
访问关联的对象

### 迁移
迁移概述
操作参考
SchemaEditor
编写迁移

### 高级功能
管理器
原始SQL
事务
聚合函数 F , Q 对象
搜索
自定义字段
多个数据库
自定义查询
查询表达式
条件表达式
数据库函数

### 其他
支持的数据库
旧数据库
提供初始化数据
优化数据库访问
PostgreSQL的特有功能


## 视图层

### 基础
URL配置
视图函数
便捷工具
装饰器
异步支持

### 参考
内置视图
请求与响应对象
TemplateResponse对象

### 文件上传下载
概览
文件对象
存储API
管理文件
自定义存储

### 基于类的视图
概览
内置显示视图
内置编辑视图
使用混入
API参考
扁平化索引

### 高级
生成CSV
生成PDF

### 中间件
概览
内建的中间件类


## 模板层
### 模板对应关系
### 模板加载
### 静态资源
### 模板语法

## 表单

基础： 概述

对于设计者： 语法概述 | 内建标签及过滤器 | 人性化

对于开发者： 模板 API | 自定义标签和过滤器 | 自定义模板后端

## 管理

管理站点

管理动作

管理文档生成器

## 安全

安全概览

在 Django 中披露的安全问题

点击劫持保护

跨站请求伪造 CSRF 保护

登录加密

安全中间件


## 第三方插件使用

### 增强管理后台 


xadmin 介绍和使用

django-autocomplete-hight 优化性能

django-cheditor 开发富文本编辑器



### DRF（django-rest-framework）

{% post_link django/django-rest-framework/readme %}<br>


### 数据序列化
### 请求与响应
### 视图 转换器
### 关系 超链接
### 认证和权限





## 调试和优化


### 验证码
### 分页器
### 类视图
### 中间件
### 日志
### 缓存
### 信号
### Celery
### 用户角色和用户权限 



django-debug-toolhar 优化系统

[《Django 企业开发实战》](http://django-practice-book.com/)