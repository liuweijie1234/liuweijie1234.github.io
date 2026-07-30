---
title: Django 表单（Forms）
date: 2026-07-30 10:15:00
tags:
- Django
- 表单
- Forms
categories:
- Web开发
- Django
---

## 一、为什么用 Forms

`django.forms.Form` / `ModelForm` 统一管理：**字段定义、校验、清洗、HTML 渲染、错误回显**。手写 `<input>` + 手动校验既重复又易漏安全项。

## 二、基础 Form

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='姓名')
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        data = self.cleaned_data['message']
        if len(data) < 10:
            raise forms.ValidationError('留言至少 10 个字')
        return data
```

视图中使用：

```python
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.cleaned_data 已是清洗后数据
            return redirect('thanks')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
```

模板：

```html
<form method="post">{% csrf_token %}{{ form.as_p }}<button>提交</button></form>
```

## 三、ModelForm：与模型联动

```python
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author']
        # exclude = ['created_at']
        widgets = {'body': forms.Textarea(attrs={'rows': 10})}
        labels = {'title': '标题'}
```

`form.save()` 直接写库；`instance=` 用于编辑已有对象。

## 四、校验层级

1. 字段级：`clean_<field>()`。
2. 跨字段：`clean()` 里比较多个字段，错误写入 `form.add_error()` 或非字段错误。
3. 表单集：`formset_factory` 处理一组同构表单（如动态多行）。

```python
def clean(self):
    cd = super().clean()
    if cd.get('password') != cd.get('password2'):
        self.add_error('password2', '两次密码不一致')
```

## 五、CSRF 防护

模板里务必 `{% csrf_token %}`，否则 POST 会被 `CsrfViewMiddleware` 拒绝（403）。AJAX 提交需从 cookie 取 `csrftoken` 并在请求头带 `X-CSRFToken`。

## 六、文件上传

```python
class UploadForm(forms.Form):
    file = forms.FileField()

# views.py
if form.is_valid():
    handle_uploaded_file(form.cleaned_data['file'])
```

配合模型的 `FileField` / `ImageField` 使用 `ModelForm` 更方便。

## 七、最佳实践

- 校验逻辑放 `clean_*`，不要在视图里重复写。
- 用 `ModelForm` 减少样板代码；仅在特殊场景用裸 `Form`。
- 始终渲染 `form.errors` 让用户可见错误。
- 限定 `fields`（`fields = [...]`）而非 `exclude`，避免模型新增字段意外暴露。
