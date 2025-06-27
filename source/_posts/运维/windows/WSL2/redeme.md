


[Windows 11 安装 WSL2](https://zhuanlan.zhihu.com/p/475462241)

[WSL2安装Debian(Ubuntu)并配置国内apt源](https://zhuanlan.zhihu.com/p/99938831)

https://blog.csdn.net/tianjuewudi/article/details/122564815

debian系统

```powershell
wsl --install
```

wsl -l -v


<3>WSL (14)ERRoR: createProcesscomon:559: execvpe(/bin/bash) failed: No such file or directory

## 常用命令


wsl --set-default Ubuntu # 设置 Ubuntu 为默认发行版


一、安装与配置
命令/操作	说明	示例
wsl --install	一键安装默认 Linux 发行版	wsl --install (需 Windows 11 或最新版本)
wsl --install -d <发行版名>	安装指定发行版	wsl --install -d Ubuntu-22.04
wsl --list --online	查看可安装的发行版列表	wsl --list --online
wsl --set-default-version 2	设置默认使用 WSL2	wsl --set-default-version 2


二、系统管理
命令	说明	示例
wsl -d Ubuntu    启动指定的WSL
wsl --shutdown	强制关闭所有 WSL 实例	wsl --shutdown
wsl --terminate <发行版名>	终止指定发行版	wsl --terminate Ubuntu-20.04
wsl --list --verbose	查看已安装发行版及状态	wsl --list -v
wsl --update	手动更新 WSL 内核	wsl --update


三、文件系统操作
命令	说明	示例
explorer.exe .	在 Windows 资源管理器中打开当前目录	(在 WSL 终端中执行)
\\wsl$\<发行版名>	在 Windows 中直接访问 WSL 文件系统	在资源管理器地址栏输入 \\wsl$\Ubuntu-22.04
wsl --export <发行版> <文件名>.tar	导出系统镜像	wsl --export Ubuntu-22.04 backup.tar
wsl --import <新发行版名> <安装路径> <文件名>.tar	导入系统镜像	wsl --import Ubuntu-backup C:\wsl\backup backup.tar


四、网络相关
命令	说明	示例
ip addr show eth0	查看 WSL2 的 IP 地址	ip a show eth0 | grep inet
curl http://localhost:<端口>	从 WSL 访问 Windows 服务	curl http://localhost:8080
netsh interface portproxy add v4tov4 listenport=<端口> listenaddress=0.0.0.0 connectport=<端口> connectaddress=<WSL_IP>	配置 Windows 端口转发到 WSL	(需管理员 PowerShell 执行)


五、服务管理
命令	说明	示例
sudo service <服务名> start	启动 Linux 服务	sudo service nginx start
sudo systemctl enable <服务名>	设置服务开机自启	sudo systemctl enable postgresql
sudo journalctl -u <服务名>	查看服务日志	sudo journalctl -u docker


六、开发环境常用
命令	说明	示例
code .	在 WSL 中启动 VSCode（需安装 Remote-WSL 扩展）	(在项目目录执行)
python3 -m venv .venv	创建 Python 虚拟环境	python3 -m venv .venv
sudo apt-get install build-essential	安装开发工具链	(Ubuntu/Debian)


七、Windows ↔ WSL 交互
场景	Windows 端	WSL 端
执行 Linux 命令	wsl <命令>	wsl ls -l
执行 Windows 命令	-	cmd.exe /c dir 或 powershell.exe Get-Process
共享环境变量	设置 WSLENV=VAR_NAME/p	在 WSL 中直接访问 $VAR_NAME


八、高级用法
命令	说明	场景
wsl --mount <物理磁盘>	挂载物理磁盘到 WSL	wsl --mount \\.\PHYSICALDRIVE1
wsl --user root	以 root 身份启动	修改系统级配置时使用
wsl --exec <命令>	不进入 shell 直接执行命令	wsl --exec python3 script.py


