---
title: Python3 aiomysql（异步 MySQL 客户端）
date: 2026-07-30 10:00:00
tags:
- Python
- 数据库
- MySQL
categories:
- Python
---

## 说明

`aiomysql` 是基于 `asyncio` 的 MySQL 异步驱动，底层复用了 PyMySQL 的协议实现，API 风格与 PyMySQL 基本一致。
适合在 asyncio / aiohttp / FastAPI 等异步框架中访问 MySQL。

```bash
pip install aiomysql
```

## 基本用法

```python
import asyncio
import aiomysql

async def main():
    conn = await aiomysql.connect(
        host="127.0.0.1", port=3306,
        user="root", password="123456",
        db="test", charset="utf8mb4",
    )
    async with conn.cursor() as cur:
        await cur.execute("SELECT id, name FROM user WHERE id = %s", (1,))
        row = await cur.fetchone()
        print(row)
    conn.close()

asyncio.run(main())
```

## 连接池（推荐）

```python
import asyncio
import aiomysql

async def main():
    pool = await aiomysql.create_pool(
        host="127.0.0.1", port=3306,
        user="root", password="123456",
        db="test", charset="utf8mb4",
        minsize=1, maxsize=10,
        autocommit=True,
    )
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:   # 返回字典
            await cur.execute("SELECT * FROM user LIMIT 10")
            rows = await cur.fetchall()
            print(rows)

    pool.close()
    await pool.wait_closed()

asyncio.run(main())
```

## 增删改与事务

```python
async def update(pool):
    async with pool.acquire() as conn:
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO user (name) VALUES (%s)", ("tom",)
                )
                await cur.executemany(
                    "INSERT INTO user (name) VALUES (%s)", [("a",), ("b",)]
                )
            await conn.commit()          # autocommit=False 时需手动提交
        except Exception:
            await conn.rollback()
            raise
```

## 注意事项

- SQL 参数使用 `%s` 占位符（与 PyMySQL 一致），**不要用字符串拼接**，防止 SQL 注入。
- 连接池的 `maxsize` 要结合 MySQL `max_connections` 配置。
- 与同步的 PyMySQL 相比，aiomysql 只在 IO 等待时让出事件循环，适合高并发 IO 密集场景。
