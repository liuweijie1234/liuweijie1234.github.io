---
title: django 自定义用户模型
date: 2022-09-29 09:00:00
tags:
- Django
- auth
categories:
- [django]
- [用户模型]
---



## 模块详解

[Django身份认证系统auth模块详解](https://www.django.cn/article/show-18.html)

[Django进阶教程:如何扩展Django用户模型](https://www.django.cn/article/show-11.html)


Permission

Group


## 自定义重构

- 参考

https://zhuanlan.zhihu.com/p/530686744?utm_campaign=shareopn&utm_medium=social&utm_oi=998974026143776768&utm_psn=1558732708637073408&utm_source=wechat_session


The value of 'ordering[0]' refers to 'username', which is not an attribute of 'xtauth.User'

```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
```