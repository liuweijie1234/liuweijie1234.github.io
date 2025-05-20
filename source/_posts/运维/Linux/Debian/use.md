---
title: debian 使用
date: 2023-08-17 16:14:00
tags:
- Debian
categories:
- Debian
---

[在 Debian 中打开终端的四种方法](https://digitalixy.com/linux/641990.html)


### 安装Python

切换有权限的用户
su root

确保系统已更新：

sudo apt update && sudo apt upgrade

安装构建Python所需的依赖包和工具：

sudo apt install build-essential libc6-dev libbz2-dev libffi-dev libgdbm-dev libncurses5-dev libnss3-dev libreadline-dev libsqlite3-dev libssl-dev tk-dev wget zlib1g-dev

下载 Python 3.8 的源代码（可以根据需要选择其他对应的版本）：
wget https://www.python.org/ftp/python/3.8.17/Python-3.8.17.tgz
或者
curl -O https://www.python.org/ftp/python/3.8.17/Python-3.8.17.tgz


解压缩下载的源代码文件：
tar -xf Python-3.8.17.tgz

进入解压后的目录：
cd Python-3.8.17

配置编译选项：

./configure --enable-optimizations

编译源代码：

make -j$(nproc)

> 解释：-j 参数用于指定并行编译的线程数，$(nproc) 则是一个 shell 变量，用于获取当前系统上可用的逻辑 CPU 核心数量。


安装 Python：

sudo make altinstall

注意：使用 make altinstall 命令而不是 make install 是为了避免覆盖系统默认的 Python 版本。

验证安装结果：

python3.8 --version


确定已安装python的版本和路径

which python
或
whereis python