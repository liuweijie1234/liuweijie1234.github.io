
推荐使用 redis Desktop Manager，可以方便的安装和管理redis。

## 安装

### windwos 安装

下载地址：https://github.com/tporadowski/redis/releases

参考：https://blog.csdn.net/m0_63230155/article/details/131951639


### WSL 使用 windows 安装的 redis

查看版本
```bash
redis-cli info | grep redis_version
```

1. 修改 Redis 配置文件
```bash
# redis.windows-service.conf
bind 0.0.0.0      # 允许所有 IP 连接
protected-mode no # 关闭保护模式（重要！）
```

2. 重启 Redis 服务
```bash
# 以管理员身份运行 PowerShell
Stop-Service redis
Start-Service redis
```

3. 配置 Windows 防火墙

4. 获取 Windows 主机 IP（WSL2 专用）
```bash
# 在 WSL 终端中执行
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
# 输出示例：172.28.112.1（这是 WSL2 访问 Windows 的专用 IP）
```

5. 测试连接
```bash
# 在 WSL 中安装 redis-cli
sudo apt install redis-tools

# 使用 Windows 主机 IP 连接
redis-cli -h 172.28.112.1 -p 6379

telnet 172.28.112.1 6379
```


### macOS 安装 redis

#### 方法一：使用 Homebrew 安装

```bash
brew install redis
```

启动 Redis

临时启动（关闭终端后停止）：

```bash
redis-server
```
后台服务并开机自启（推荐）：

```bash
brew services start redis
```

验证 Redis 是否运行
```bash
redis-cli ping
```
如果返回 PONG，说明 Redis 已正常运行。

#### 方法二：使用Docker安装（适合开发隔离）

启动 Redis
```bash
docker run --name my-redis -p 6379:6379 -d redis
```

验证 Redis
```bash
docker exec -it my-redis redis-cli ping
```


## 常见问题

Redis 连接问题

### 错误：Connection refused

检查 Redis 是否运行：

```bash
brew services list | grep redis
```
检查端口：

```bash
lsof -i :6379
```

## 卸载

```bash
brew uninstall redis
brew cleanup
```