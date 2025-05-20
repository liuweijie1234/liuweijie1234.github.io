# 生产环境部署指南


## 使用 systemd 管理 Celery 服务
创建一个 systemd 服务文件：

```ini
[Unit]
Description=Celery Worker
After=network.target

[Service]
User=celery_user
Group=celery_group
EnvironmentFile=/etc/default/celery
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/celery -A my_app worker --loglevel=info -c 4 -n worker1

[Install]
WantedBy=multi-user.target
```

启动服务

```bash
systemctl start celery-worker
systemctl enable celery-worker
```