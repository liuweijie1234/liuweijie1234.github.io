---
title: Windows MySQL 主从复制
date: 2023-05-15 09:00:00
tags:
- MySQL
categories:
- MySQL
---



要配置 Django 以使用 MySQL 主从复制或主备复制，您需要执行以下步骤：

1、首先，在 MySQL 中设置主从/主备复制关系。这可能涉及到安装另一个 MySQL 实例，并确保复制正常工作。

2、 在 Django 中配置数据库连接。在 settings.py 文件中，您可以指定多个数据库连接，用于读取和写入操作。例如，您可以将主数据库配置为用于写入操作，而从数据库则用于读取操作。

```Python
DATABASES = {
    'default': {
        'NAME': 'main',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'main_user',
        'PASSWORD': 'main_password',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'read_replica': {
        'NAME': 'replica',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'replica_user',
        'PASSWORD': 'replica_password',
        'HOST': 'localhost',
        'PORT': '3307',
    }
}
```

在这个例子中，我们定义了两个数据库：'default' 是主数据库，用于写入操作；'read_replica' 是从数据库，用于读取操作。请注意，这些连接的端口号不同，因此它们使用不同的 MySQL 实例。

3、配置 Django 使用读取从数据库进行读取操作。

如果您想强制 Django 对从数据库进行读取操作，可以使用 django.db.router.DBRouter 类来实现此目的。这个类可以让你根据请求类型（读/写）将请求路由到不同的数据库。

```Python
class DBRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return 'read_replica'

    def db_for_write(self, model, **hints):
        """
        Writes always go to the master database.
        """
        return 'default'
```

在这个例子中，我们使用 DBRouter 类将所有读取操作路由到名为 'read_replica' 的数据库，而将所有写入操作路由到名为 'default' 的数据库。请注意，这个类只是一个示例实现，您需要根据自己的需求来定制它。

在 Django 项目中使用读取从数据库进行查询。最后，在您的 Django 项目代码中，您可以指定查询应该使用哪个数据库连接。例如，如果您想从从数据库中读取数据，您可以使用以下代码：

```Python
from django.db import router
from myapp.models import MyModel

# Explicitly route this query to the read replica.
with router.route_context(DBRouter(), 'read_replica'):
    MyModel.objects.all()
```
在这个例子中，我们使用 router.route_context() 方法指定了要使用的数据库连接。


在这个示例中，我们使用 using 参数指定了要使用的数据库连接。对于 ModelA，我们将其映射到 default 数据库，即主库；而对于 ModelB，我们将其映射到 read_replica 数据库，即从库。

```Python
from django.db import models

class ModelA(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        app_label = 'myapp'
        db_table = 'model_a'
        managed = False
        using = 'default'

class ModelB(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        app_label = 'myapp'
        db_table = 'model_b'
        managed = False
        using = 'read_replica'
```

现在，当您使用 Django 的 ORM 进行写入操作时，它会自动同步数据到从库中的 modelB 表中。例如：

```Python
from myapp.models import ModelA

# Create a new object in the main database.
obj_a = ModelA(name='Object A', description='This is object A')
obj_a.save()

# The object should now be automatically synchronized to the replica database.
from myapp.models import ModelB
obj_b = ModelB.objects.get(name='Object A')
print(obj_b.description)  # This should print "This is object A".
```
在这个示例中，我们创建了一个新的 ModelA 对象，并将其保存到主数据库中。由于我们已经将 ModelA 和 ModelB 映射到不同的数据库，因此 Django 将自动同步数据到从数据库中的 ModelB 表中。最后，我们从从数据库中读取同步后的数据，并验证它是否正确。