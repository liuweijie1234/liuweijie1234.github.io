

Flask 教程-菜鸟教程
https://www.runoob.com/flask/flask-tutorial.html



## 启动 API 服务

flask run --host 0.0.0.0 --port=5001 --debug



## 启动 Worker 服务

用于消费异步队列任务，如知识库文件导入、更新知识库文档等异步操作。 Linux / MacOS 启动：

celery -A app.celery worker -P gevent -c 1 -Q dataset,generation,mail,ops_trace --loglevel INFO

如果使用 Windows 系统启动，请替换为该命令：

celery -A app.celery worker -P solo --without-gossip --without-mingle -Q dataset,generation,

## 数据库迁移命令


flask db stamp base # 删除所有迁移记录

flask db init # 重新初始化迁移

flask db upgrade d3f6769a94a3
flask db upgrade 93ad8c19c40b
flask db upgrade f4d7ce70a7ca
flask db upgrade d07474999927
flask db upgrade 09a8d1878d9b
flask db upgrade 01d6889832f7
flask db upgrade 479e8b0342f7
flask db upgrade head


01d6889832f7


flask db downgrade d07474999927 # 回滚到指定版本

flask db upgrade d3f6769a94a3  # 升级指定版本

flask db stamp d3f6769a94a3  # 标记起始版本

flask db upgrade head  # 升级到最新

flask db history  # 检查迁移历史
flask db current  # 查看当前状态版本

flask db migrate -m "add account field to source"


flask db upgrade # 应用迁移