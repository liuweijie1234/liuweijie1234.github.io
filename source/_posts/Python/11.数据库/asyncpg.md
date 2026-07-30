---
title: Python3 asyncpg（异步 PostgreSQL 客户端）
date: 2026-07-30 10:00:00
tags:
- Python
- 数据库
- PostgreSQL
categories:
- Python
---

## 说明

`asyncpg` 是专为 asyncio 设计的 PostgreSQL 驱动，直接实现了 PostgreSQL 二进制协议，性能优于 psycopg2 等驱动。
注意它**不遵循 DB-API 2.0**，有自己的一套 API。

```bash
pip install asyncpg
```

## 基本用法

```python
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        host="127.0.0.1", port=5432,
        user="postgres", password="123456",
        database="test",
    )
    # 占位符使用 $1、$2 ...（不是 %s）
    row = await conn.fetchrow("SELECT id, name FROM users WHERE id = $1", 1)
    print(row["id"], row["name"])       # Record 对象，可按字段名取值

    rows = await conn.fetch("SELECT * FROM users LIMIT 10")   # 多行
    value = await conn.fetchval("SELECT count(*) FROM users") # 单个值

    await conn.execute("INSERT INTO users (name) VALUES ($1)", "tom")
    await conn.close()

asyncio.run(main())
```

## 连接池（推荐）

```python
import asyncio
import asyncpg

async def main():
    pool = await asyncpg.create_pool(
        dsn="postgresql://postgres:123456@127.0.0.1:5432/test",
        min_size=1, max_size=10,
    )
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")
        print(rows)
    await pool.close()

asyncio.run(main())
```

## 事务

```python
async with pool.acquire() as conn:
    async with conn.transaction():          # 异常自动回滚，正常自动提交
        await conn.execute("UPDATE users SET name=$1 WHERE id=$2", "new", 1)
        await conn.execute("DELETE FROM logs WHERE user_id=$1", 1)
```

## 批量与预编译

```python
# executemany 批量插入
await conn.executemany(
    "INSERT INTO users (name) VALUES ($1)", [("a",), ("b",), ("c",)]
)

# 预编译语句，重复执行更快
stmt = await conn.prepare("SELECT * FROM users WHERE id = $1")
row = await stmt.fetchrow(1)
```

## 与 aiomysql 的主要差异

| 项 | asyncpg | aiomysql |
| --- | --- | --- |
| 数据库 | PostgreSQL | MySQL |
| 占位符 | `$1, $2` | `%s` |
| API 风格 | 自有 API（fetch/fetchrow/execute） | DB-API 风格（cursor） |
| 返回行 | `Record`（支持按名取值） | tuple / DictCursor |
