---
title: Django Admin 后台管理
date: 2026-07-30 10:20:00
tags:
- Django
- Admin
- 后台
categories:
- Web开发
- Django
---

## 一、Admin 是什么

`django.contrib.admin` 是 Django 的**自动后台管理界面**，基于已注册的模型自动生成增删改查页面，是 Django「开箱即用」的标志性特性。

启用条件：`INSTALLED_APPS` 含 `django.contrib.admin`、`django.contrib.auth`、`django.contrib.contenttypes`、`django.contrib.sessions`，且 `urls.py` 含 `admin.site.urls`。

## 二、注册模型

```python
# admin.py
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

更推荐用 `ModelAdmin` 定制：

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'author')
    search_fields = ('title', 'body')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('title', 'body')}),
        ('高级', {'fields': ('author', 'is_published'), 'classes': ('collapse',)}),
    )
```

## 三、常用配置项

| 选项 | 作用 |
|------|------|
| `list_display` | 列表页展示的字段 |
| `list_filter` | 右侧筛选器 |
| `search_fields` | 顶部搜索（模糊） |
| `prepopulated_fields` | 自动填充（如 slug 由 title 生成） |
| `raw_id_fields` | 外键改为弹窗选择，避免下拉过长 |
| `inlines` | 内联编辑关联对象（如文章+评论） |
| `readonly_fields` | 只读字段 |
| `actions` | 自定义批量操作 |

## 四、内联编辑

```python
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
```

## 五、权限与可见性

Admin 的权限依赖 `django.contrib.auth` 的 group/permission 系统：

```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    if request.user.is_superuser:
        return qs
    return qs.filter(author=request.user)

def has_add_permission(self, request):
    return request.user.is_staff
```

## 六、自定义 Admin 视图

可重写 `save_model`、`save_related` 在保存前后注入逻辑：

```python
def save_model(self, request, obj, form, change):
    if not change:
        obj.author = request.user
    super().save_model(request, obj, form, change)
```

## 七、最佳实践

- 生产环境务必保护好 `/admin`：强密码、必要时隐藏路径（`path('secret-admin/', admin.site.urls)`）。
- 超大数据量表用 `raw_id_fields` / `list_select_related` 优化性能。
- 内部运营后台用 Admin 极快；对外复杂业务建议自建界面或 DRF。
