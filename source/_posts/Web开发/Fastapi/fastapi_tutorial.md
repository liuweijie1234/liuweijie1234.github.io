

## FastAPI 教程

https://www.runoob.com/fastapi/fastapi-tutorial.html
https://www.w3cschool.cn/fastapi/fastapi-features.html
https://fastapi.tiangolo.com/zh/learn/

## 基本使用

pip install fastapi "uvicorn[standard]" sqlalchemy  # 安装依赖

pip install pymysql   # 同步数据库

> 异步支持：将 SQLAlchemy 替换为异步版本（如 databases 或 asyncpg）
pip install aiomysql  # 异步数据库
pip install databases


pip install alembic   # 数据库迁移

注: sqlalchemy只自带create_all(建立全部表)的功能


pip install pydantic

pip install pydantic-settings  # 配置文件

pip install gunicorn  # 部署


source .wsl-venv/bin/activate  # 激活虚拟环境

pip freeze > requirements.txt  # 生成requirements.txt


uvicorn main:app --reload  # 启动服务命令（开发环境）

uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug  # 启动服务命令（生产环境）

## 数据库

### 数据库配置

#### 同步数据库配置

```python
#app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tasks.db"
#DATABASE_URL = "mysql://user:password@localhost:3306/fastapi_db"  # 替换为你的 MySQL 配置
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # check_same_thread 仅适用于 SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据库会话依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 异步数据库配置

- aiomysql

```python
# config.py
class Settings(BaseSettings):
# 构建数据库URL
    @property
    def ASYNC_SQLALCHEMY_DATABASE_URL(self) -> str:
        """异步数据库 URL (用于 FastAPI)"""
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
```

```python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# 创建异步引擎
async_engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 创建基本模型类
Base = declarative_base()

# 异步数据库会话依赖
async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```
- databases

```python
from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/dbname"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

async def get_processed_data():
    query = "SELECT * FROM processed_data"
    return await database.fetch_all(query)
```
#### 数据库迁移

常用 Alembic 命令

初始化迁移环境：alembic init alembic
生成迁移脚本： alembic revision --autogenerate -m "create tasks table"
应用迁移：alembic upgrade head


查看当前版本：alembic current
查看迁移历史：alembic history
回滚到上一版本：alembic downgrade -1
回滚到特定版本：alembic downgrade <revision_id>
升级到最新版本：alembic upgrade head


#### 单数据库配置

#### 多数据库配置


### 模型

#### 字段类型

1、基本类型：

Integer：用于表示整数类型。
String(length)：用于表示字符串类型，length 指定字符串的最大长度。
Text：用于表示没有长度限制的长文本字段。
Float：用于表示浮点数类型。
Boolean：用于表示布尔类型（True 或 False）。
Date：用于表示日期类型（只包含日期，没有时间）。
Time：用于表示时间类型（只包含时间，没有日期）。
DateTime：用于表示日期时间类型，包含日期和时间。

2、数值类型：

Integer：整数类型。
SmallInteger：小整数类型。
BigInteger：大整数类型。
Numeric(precision, scale)：用于表示具有固定精度和小数位数的数值类型。precision 表示总位数，scale 表示小数位数。
Float：浮点数类型。

3、文本类型：

String(length)：短文本字符串，length 参数指定字符串的最大长度。
Text：用于存储不受长度限制的文本。

4、二进制类型：

LargeBinary：用于存储大文件或二进制数据（如图像或文件）。

5、日期和时间类型：

Date：仅表示日期，不包含时间。
Time：仅表示时间，不包含日期。
DateTime：日期和时间类型，通常用于存储精确的日期和时间。

6、JSON 类型：

JSON：用于存储 JSON 格式的数据，这对于存储嵌套数据或灵活的数据结构非常有用。

#### 字段选项

1. primary_key：指定该字段是否为主键，若为主键，则该字段的值必须唯一且不可为空。
```python
id = Column(Integer, primary_key=True)
```

2. nullable：指定字段是否允许为空。默认为 True，表示可以为空。
```python
description = Column(String(200), nullable=False)
```

3. unique：指定字段是否要求唯一，确保字段中的每个值都不重复。
```python
email = Column(String(100), unique=True)
```

4. index：为字段创建索引，提高查询效率。通常对经常查询的字段（如 name）使用索引。
```python
title = Column(String(100), index=True)
```

5. default：设置字段的默认值。当新记录没有为该字段指定值时，会使用默认值。
```python
created_at = Column(DateTime, default=datetime.utcnow)
```

6. server_default：与 default 类似，但该值由数据库服务器生成。
```python
created_at = Column(DateTime, server_default=func.now())
```

7. onupdate：当该记录更新时，字段的值会自动更新为指定的值。
```python
updated_at = Column(DateTime, onupdate=func.now())
```

8. unique=True：用于确保字段中的值是唯一的。
```python
username = Column(String(50), unique=True)
```

#### 关系字段

##### 一对一

- 可以使用 ForeignKey 并在 relationship 中设置 uselist=False 来表示一对一关系。

例如，定义用户和用户资料的一对一关系：

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="profile")
```
解释：

- uselist=False 表示每个 User 实体最多有一个 Profile，即一对一关系。

ondelete 用法：

- CASCADE ：当父表的记录被删除时，子表的相关记录也被删除。
- SET NULL：当父表中的记录被删除时，子表中的外键字段会被设置为 NULL。
- NO ACTION：禁止删除父表的记录，如果存在相关子记录

##### 一对多

- 使用 ForeignKey 定义外键。
- 使用 relationship 来创建模型之间的关系。

例如，定义一个用户和多篇文章的关系（一个用户可以有多篇文章）：

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # 一对多关系
    articles = relationship("Article", back_populates="owner")

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    # 外键
    user_id = Column(Integer, ForeignKey("users.id"))
    # 外键约束，反向引用 "owner" 属性
    owner = relationship("User", back_populates="articles")
```
解释：

- ForeignKey("users.id") 表示 Article 表中的 user_id 字段是外键，指向 User 表的 id 字段。
- relationship("Article", back_populates="owner") 表示 User 模型和 Article 模型之间是一对多的关系。
- back_populates 是 SQLAlchemy 用来设置双向关系的属性。

##### 多对多

- 使用 Table 来定义一个中间表，通常用来表示多对多的关系。
- 使用 relationship 进行关联。

例如，定义学生和课程的多对多关系：

```python
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship

# 定义中间表
student_course = Table(
    "student_course", Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id"))
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    courses = relationship("Course", secondary=student_course, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Student", secondary=student_course, back_populates="courses")
```
解释：

- student_course 是一个中间表，用于连接 students 和 courses 表。
- secondary=student_course 告诉 SQLAlchemy 使用 student_course 作为关联表。

### 预加载

#### joinedload()
连接加载

工作原理：
- 使用 SQL JOIN 语句一次性加载主表和关联表的数据。
- 生成一个较大的结果集，包含主表和关联表的所有字段。

示例查询
```python
session.query(MonitorAccount).options(joinedload(MonitorAccount.account_stats)).all()
```

生成的 SQL 查询
```sql
SELECT monitor_account.*, account_stats.*
FROM monitor_account
LEFT OUTER JOIN account_stats ON monitor_account.id = account_stats.account_id;
```


优点：
- 单次查询：只需 1 次数据库往返。
- 适合小规模数据：如果关联数据量少，性能较好。

缺点：
- 数据冗余：如果主表有 100 条记录，每条记录关联 10 条数据，结果集会有 1000 行，可能包含大量重复数据（主表字段）,需要去重。
- 性能问题：当关联数据量大时，JOIN 会导致结果集膨胀，增加内存和网络开销。

适用场景
- 关联数据量少（如 1:1 或 1:few 关系）。
- 需要严格保证数据一致性（JOIN 是原子的）。

```python
stmt = (
    select(Terminal)
    .where(Terminal.online == True)
    .options(joinedload(Terminal.robots))
)
result = await db.execute(stmt)
online_terminals = result.scalars().unique().all()
```


#### selectinload()

子查询加载

工作原理
- 先查询主表，再用 IN 子查询单独加载关联数据。
- 执行 2 次查询（主查询 + 关联查询）。

示例查询
```python
session.query(MonitorAccount).options(selectinload(MonitorAccount.account_stats)).all()
```

生成的 SQL 查询
```sql
-- 第一次查询：主表
SELECT * FROM monitor_account;

-- 第二次查询：关联表（自动执行）
SELECT * FROM account_stats
WHERE account_stats.account_id IN (1, 2, 3, ...);
```


优点：
- 减少数据冗余：关联表查询结果无重复字段。
- 适合大规模数据：即使主表有 1000 条记录，IN 查询也能高效处理。
- 避免笛卡尔积：不会因 JOIN 导致结果集膨胀。

缺点：
- 多次查询：至少 2 次数据库往返。
- IN 子查询限制：某些数据库对 IN 列表长度有限制（如 Oracle 的 1000 条限制）。**需数据库支持长 IN 列表**

适用场景
- 关联数据量较大（如 1:many 或 many:many 关系）。
- 主表记录多，但关联数据分布稀疏。

## schemas-Pydantic 模型

Pydantic 模型 用于定义请求/响应的数据

```python
# app/schemas/task.py
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True  # 兼容 SQLAlchemy 模型
```
## crud

### SQLAlchemy CRUD 操作 



#### fetchall()

返回查询结果的 所有行，每行是一个 元组（Tuple） 或 Row 对象（类似字典）。
适用于 查询多列 的场景（例如 SELECT id, name FROM users）


返回数据类型
- 多列查询 → 返回 List[Row] 或 List[Tuple]，每行包含所有列的值。
- 单列查询 → 返回 List[Tuple]，但每个元组只有单个值（需要手动解包）。

适用场景
需要同时获取多列数据。
不关心 ORM 对象，只需原始数据。

示例
```python
query = select(User.id, User.name)  # 查询多列
result = await db.execute(query)
data = result.fetchall()  # 返回 List[Row] 或 List[Tuple]

# 输出示例：
# [(1, "Alice"), (2, "Bob")]  # 每行是一个元组
```

#### .scalars().all()

返回 **单列** 的 标量值（Scalar） 或 ORM 对象。

适用场景：适用于 查询单列 或 返回 ORM 模型实例（例如 SELECT id FROM users 或 SELECT * FROM users）。


返回数据类型
单列查询 → 直接返回值的列表 List[Any]（如 List[int]、List[str]）。
ORM 查询 → 返回 List[ORM模型]（如 List[User]）

示例 1：查询单列（返回标量值）：
```python
query = select(MonitorPlatform.id)  # 查询单列
result = await db.execute(query)
platform_ids = result.scalars().all()
# platform_ids 是一个包含整数的列表，例如 [1, 2, 3]
```
示例 2：查询 ORM 对象（返回模型实例）
```python
query = select(User)  # 查询整个 ORM 模型
result = await db.execute(query)
data = result.scalars().all()  # 返回 List[User]

# 输出示例：
# [<User id=1, name="Alice">, <User id=2, name="Bob">]
```


**.all()**
返回值：返回一个包含元组的列表，每个元组代表一行数据。即使查询的是单个列，也会返回元组形式的结果。

适用场景：当需要获取完整的查询结果，并且结果中包含多个列时，可以使用 .all()。

示例：
```python
result = await db.execute(select(MonitorPlatform.id, MonitorPlatform.platform_name))
records = result.all()
# records 是一个包含元组的列表，例如 [(1, 'Platform A'), (2, 'Platform B')]
```

```python
result = await db.execute(select(user_table.c.name))
records = result.all()
# records 是一个包含元组的列表，例如 [('Alice',), ('Bob',), ('Charlie',)]
```

**.scalar()**
返回值：返回查询结果中的第一个值，如果查询结果为空，则返回 None。
适用场景：当查询结果只包含一个列，并且只需要获取该列的值时，可以使用.scalar()。

示例：
```python
result = await db.execute(select(MonitorPlatform.id))
platform_id = result.scalar()
# platform_id 是一个整数，如果查询结果为空，则 platform_id 为 None
```

#### scalar_one_or_none()

返回查询结果中的第一个值，如果查询结果为空，则返回 None。
如果查询结果包含多个值，则会抛出 MultipleResultsFound 异常。

#### scalars().first()

返回单列的第一个值（标量）或 ORM 对象。

#### fetchone()

 返回第一行的元组或 Row 对象。

## 路由

```python
# app/routers/task.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task as TaskModel
from app.schemas.task import Task, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=list[Task])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}
```

```python
from fastapi import FastAPI
from app.routers import task
from app.database import Base, engine

app = FastAPI(
    title="Task Management API",
    description="A simple API to manage tasks",
    version="1.0.0"
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 包含路由
app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Task Management API"}
```

## 并发
### 信号量(Semaphore)
信号量是一种用于控制并发访问的同步原语。它允许指定同时可以访问共享资源的最大并发数。

关键点：
MAX_CONCURRENT_REQUESTS ：允许的最大并发请求数（例如 10）。
async with semaphore: ：进入信号量控制的代码块时，会占用一个“许可”；离开时释放。
如果所有许可已被占用，新任务会 阻塞等待，直到有许可被释放。

工作原理
信号量本质上是一个 计数器：
计数器初始值 = MAX_CONCURRENT_REQUESTS（例如 10）。

- acquire() （通过 async with 触发）：
如果计数器 > 0，减 1 并继续执行。
如果计数器 = 0，阻塞等待其他任务调用 release()。

- release() （离开 async with 块时自动触发）：
计数器加 1，唤醒等待的任务。


（1）初始化信号量
```python
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
```
创建一个信号量，初始值为 MAX_CONCURRENT_REQUESTS（例如 10）。
任何时候最多允许 10 个任务同时执行 send_request_with_retry。

（2）创建异步任务（限制并发）
```python
async with semaphore:
    task = asyncio.create_task(
        send_request_with_retry(...)
    )
    tasks.append(task)
```
- async with semaphore: ：尝试获取一个信号量许可：
    - 如果当前并发数未满（例如已有 9 个任务在运行），立即进入代码块。
    - 如果已达最大值（例如 10 个任务在运行），阻塞等待，直到其他任务完成并释放许可。
- asyncio.create_task ：将任务加入事件循环，但不会立即执行（需等待信号量许可）。
（3）等待所有任务完成
```python
await asyncio.gather(*tasks)
```
如果需要超时控制，可以结合 asyncio.wait_for()

## 认证


使用 fastapi.security 集成 JWT 或 OAuth2。


## 部署步骤
部署参考 
https://blog.csdn.net/qq_51116518/article/details/143870495
https://blog.csdn.net/asd54090/article/details/137783835

# 1. 在服务器上创建部署目录
ssh user@your_server
mkdir -p /path/to/your/app

# 2. 从本地复制文件到服务器
scp -r ./* user@your_server:/path/to/your/app/

# 3. SSH 到服务器
ssh user@your_server

# 4. 进入项目目录
cd /path/to/your/app

# 5. 添加执行权限
chmod +x scripts/*.sh

# 6. 运行安装脚本
./scripts/install.sh

# 7. 配置 supervisor
sudo cp scripts/supervisor.conf /etc/supervisor/conf.d/your_app.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start your_app

配置nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 部署检查清单

## 前置准备
- [ ] 生成最新的 requirements.txt
- [ ] 更新配置文件
- [ ] 确保所有敏感信息已从代码中移除

## 服务器配置
- [ ] Python 3.8+ 已安装
- [ ] pip 已安装
- [ ] 虚拟环境已创建
- [ ] MySQL 客户端已安装
- [ ] Supervisor 已安装
- [ ] Nginx 已安装

## 部署步骤
- [ ] 代码已复制到服务器
- [ ] 依赖已安装
- [ ] 环境变量已配置
- [ ] 数据库已配置
- [ ] Supervisor 配置已更新
- [ ] Nginx 配置已更新
- [ ] 日志目录已创建

## 验证
- [ ] 应用能够启动
- [ ] 数据库连接正常
- [ ] API 端点可访问
- [ ] 日志正常记录