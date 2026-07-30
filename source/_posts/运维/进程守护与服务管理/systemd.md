---
title: systemd 服务管理
date: 2026-07-30 10:00:00
tags:
- 运维
- systemd
- 服务管理
categories:
- 运维
- 进程守护与服务管理
---

# systemd 服务管理

systemd 是现代 Linux 发行版（RHEL 7+、Ubuntu 16.04+、Debian 8+）默认的初始化系统与和服务管理器，负责系统启动、服务生命周期、日志收集（journald）与资源管控。

## unit 文件结构

unit 文件通常位于 `/etc/systemd/system/<服务名>.service`，由若干段落组成：

```ini
[Unit]
Description=My App
After=network.target mysql.service
Requires=mysql.service

[Service]
Type=simple
ExecStart=/opt/myapp/bin/server
WorkingDirectory=/opt/myapp
User=app
Group=app
Restart=on-failure
RestartSec=5
Environment=ENV=production
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

### 关键字段

- `[Unit]`：`Description` 描述；`After`/`Before` 控制启动顺序；`Requires` 强依赖；`Wants` 弱依赖。
- `[Service]`：
  - `Type`：`simple`（默认，ExecStart 即主进程）、`forking`（后台 fork）、`notify`（就绪后发信号）、`oneshot`（一次性）。
  - `ExecStart`：启动命令；`ExecReload`：重载命令；`ExecStop`：停止命令。
  - `Restart`：退出后是否重启（`no`/`on-success`/`on-failure`/`always`）。
  - `User`/`Group`：运行身份，避免 root。
  - `Environment`/`EnvironmentFile`：环境变量。
- `[Install]`：`WantedBy` 指定启用后挂到哪个 target（多用户模式为 `multi-user.target`）。

## 编写自定义服务

```bash
# 创建服务文件
cat > /etc/systemd/system/myapp.service <<'EOF'
[Unit]
Description=My App
After=network.target

[Service]
Type=simple
ExecStart=/opt/myapp/bin/server
User=app
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 重载配置并启动
systemctl daemon-reload
systemctl enable --now myapp
```

## 常用命令

```bash
systemctl daemon-reload          # 修改 unit 后重载
systemctl start|stop|restart <svc>
systemctl enable|disable <svc>   # 开机自启/取消
systemctl status <svc>           # 状态与最近日志
systemctl is-active <svc>        # 是否运行中
systemctl list-units --type=service  # 列出服务
systemctl cat <svc>              # 查看 unit 文件内容
```

## 日志查看（journalctl）

```bash
journalctl -u myapp -f           # 跟踪（类似 tail -f）
journalctl -u myapp -n 200       # 最近 200 行
journalctl -u myapp --since "2026-07-30 10:00" --until "11:00"
journalctl -p err -u myapp       # 仅错误级别
journalctl -b                    # 本次启动后的日志
```

> journald 默认日志在内存/磁盘循环，长期归档建议接入 rsyslog 或 ELK。

## 依赖与启动顺序

- `After=network.target` 表示在网络就绪后启动（仅顺序，不保证依赖存在）。
- `Requires=network.target` + `After=network.target` 表示强依赖且顺序启动；依赖不存在则本服务也失败。
- 使用 `Wants` 表达"最好一起启动但不强依赖"。

## 资源限制

```ini
[Service]
# 限制内存 512M，超限被杀（OOM）
MemoryLimit=512M
# CPU 配额（μs/周期），如 50% 单核
CPUQuota=50%
# 文件描述符上限
LimitNOFILE=65535
```

## 与 Supervisor 的取舍

- **systemd**：系统级、无额外依赖、与发行版深度集成，适合把服务纳入系统管理。
- **Supervisor**：纯 Python、跨发行版一致、Web 管理界面友好，适合无 systemd 的环境或需要细粒度进程组管理（详见 [Supervisor](../进程守护与服务管理/Supervisor/安装部署.md)）。
- 一般新项目优先用 systemd；多进程、需统一 Web 管控时考虑 Supervisor。
