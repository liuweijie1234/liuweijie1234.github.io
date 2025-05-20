# 查看版本及版本代号
lsb_release -a
cat /etc/os-release
cat /etc/issue
hostnamectl

# 查看IP
hostname -I

sudo apt-get install python3.10-venv 
sudo apt-get remove python3.10-venv
sudo apt-get purge python3.10-venv
# 查看进程
ps aux | grep uvicorn
ps aux | grep uvicorn | grep -v grep

# 杀死进程
kill -9 PID


# 查看端口是否被监听
sudo netstat -tulpn | grep 8000

# 替代命令（更现代）
sudo ss -tulpn | grep 8000

sudo lsof -i :8000


# 安装 MySQL
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql

sudo service mysql start
sudo service mysql stop
sudo service mysql status

# 安装 Redis
sudo apt install redis-server
sudo nano /etc/redis/redis.conf
```conf
# bind 127.0.0.1 ::1
bind 0.0.0.0
protected-mode no
```
按 Ctrl + X 键。
按 Y 键确认保存。
按 Enter 键确认文件名。

sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo systemctl restart redis-server
sudo systemctl status redis-server



sudo apt install build-essential python3-dev libmysqlclient-dev






## 解决 WSL IP 动态变化问题
```bash
# 管理员 PowerShell 执行
$trigger = New-ScheduledTaskTrigger -AtStartup
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\path\to\wsl-port-forward.ps1"
Register-ScheduledTask -TaskName "WSL Port Forward" -Trigger $trigger -Action $action -RunLevel Highest

```