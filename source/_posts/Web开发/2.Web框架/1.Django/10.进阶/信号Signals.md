---
title: Django 信号（Signals）
date: 2026-07-30 10:35:00
tags:
- Django
- 信号
- Signals
categories:
- Web开发
- Django
---

## 一、信号的作用

**信号（Signal）** 是 Django 的**解耦通知机制**：当某事件发生时（如 model 保存、请求开始），发送者广播信号，接收者（receiver）被动执行逻辑，彼此无需直接引用。

典型用途：保存用户后自动建 Profile、删除文章后清理缓存、记录审计日志。

## 二、内置信号

- `pre_save` / `post_save`（model 保存前后）
- `pre_delete` / `post_delete`
- `m2m_changed`（多对多变更）
- `request_started` / `request_finished`
- `got_request_exception`

## 三、定义与连接 receiver

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

`@receiver` 装饰器自动连接；也可手动 `post_save.connect(handler, sender=User)`。

## 四、自定义信号

```python
import django.dispatch
order_placed = django.dispatch.Signal()

# 发送
order_placed.send(sender=Order, order=order)

# 接收
def on_order_placed(sender, order, **kwargs):
    ...
order_placed.connect(on_order_placed)
```

## 五、注意事项与坑

- **不要在信号里再触发同信号**，否则死循环（如 `post_save` 里 `save()` 同一对象）。
- 信号逻辑难以追踪，滥用会让数据流不清晰；能用 `save_model` / 显式调用就别用信号。
- receiver 里抛异常会中断主流程，务必处理异常或放到事务外。
- 与事务配合：`post_save` 在事务提交前触发，若需「事务提交后再执行」，用 `transaction.on_commit(lambda: ...)` 包裹。

## 六、最佳实践

- 仅用于「横切、弱依赖」场景（日志、缓存失效、通知）。
- 核心业务逻辑优先放在 service 层显式调用。
- app 的 `signals.py` 要在 `apps.py` 的 `ready()` 中 `import` 以完成连接，避免「信号不生效」。
