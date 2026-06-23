

## 安装 Homebrew

```bash
xcode-select --install
```


```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew -v

brew update

brew services list
```

## MySQL

### 启动

```bash
brew install mysql
brew services start mysql
```

方法一：通过系统偏好设置启动

打开 macOS 的系统偏好设置。

找到底部出现的 MySQL 图标，点击进入。

点击 Start MySQL Server 按钮启动服务。

方法二：通过命令行启动

使用 mysql.server 脚本（需管理员权限）：

```bash
sudo /usr/local/mysql/support-files/mysql.server start
sudo /usr/local/mysql/support-files/mysql.server status
sudo /usr/local/mysql/support-files/mysql.server restart
sudo /usr/local/mysql/support-files/mysql.server stop
```

命令未找到

将 MySQL 添加到 PATH：
```bash
echo 'export PATH="/usr/local/mysql/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
### 检查

```bash
# 检查服务状态和版本（如果正在运行）
brew services list | grep mysql
sudo launchctl list | grep mysql

mysql --version
# 查找 MySQL 的安装路径
# 检查 Homebrew 是否安装了 MySQL
brew list | grep mysql

# 使用 which 命令查找可执行文件路径
which mysql
which mysqld

ps aux | grep mysql
lsof -i :3306
netstat -an | grep 3306

/usr/local/mysql/bin/mysql -u root
```

## redis
### 启动 redis
```bash
nano /usr/local/etc/redis.conf


brew services start redis

brew services stop redis

brew services restart redis

brew services info redis

```


ps aux | grep redis
lsof -i :6379
netstat -an | grep 6379