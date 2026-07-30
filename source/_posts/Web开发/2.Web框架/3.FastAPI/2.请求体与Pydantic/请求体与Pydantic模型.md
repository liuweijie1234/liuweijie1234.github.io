---
title: FastAPI 请求体与 Pydantic
date: 2026-07-30 11:45:00
tags:
- FastAPI
- Pydantic
- 请求体
categories:
- Web开发
- FastAPI
---

## 一、Pydantic 模型

FastAPI 用 **Pydantic** 定义数据模型，负责**校验、序列化、文档生成**。

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    tags: list[str] = []
    description: str | None = None
```

## 二、请求体

```python
@app.post('/items/')
def create_item(item: Item):
    return item
```

FastAPI 自动把 JSON 请求体解析为 `Item`，校验失败返回 422，并在 `/docs` 提供表单。

## 三、嵌套模型

```python
class Address(BaseModel):
    city: str
    street: str

class User(BaseModel):
    name: str
    address: Address
```

支持任意嵌套与 `list[Model]`。

## 四、字段校验与默认值

`Field(..., title=, example=, ge=, regex=, max_length=)`。必填用 `...`（Ellipsis）表示。

## 五、多请求体参数

```python
@app.post('/items/{item_id}')
def update(item_id: int, item: Item, importance: int = Body(..., gt=0)):
    ...
```

用 `Body()` 把本会被当作查询的参数强制放进请求体。

## 六、Pydantic v2 要点

- 校验更快（Rust 内核），配置用 `model_config = ConfigDict(...)`。
- `model_dump()` / `model_dump_json()` 替代旧 `dict()` / `json()`。
- 自定义校验用 `@field_validator` / `@model_validator`。

## 七、最佳实践

- 所有入参用 Pydantic 模型统一校验，避免散落的 `if` 判断。
- 用 `Field` 显式约束，错误信息对用户友好。
- 出参与入参模型分离（见 `3.响应模型/响应模型.md`），别把内部字段泄露出去。
