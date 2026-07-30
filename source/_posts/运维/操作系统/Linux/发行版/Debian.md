---
title: Debian 发行版实践
date: 2023-08-17 16:14:00
tags:
- 运维
- Debian
- Linux
categories:
- 运维
- 操作系统
- Linux
- 发行版
---

# Debian 发行版实践

> 本页由 `Debian/command.md`、`Debian/install.md`、`Debian/use.md` 合并整理而来。

## 安装与下载

[最新下载](https://www.debian.org/CD/)

[Debian 11.7 下载](https://www.debian.org/releases/bullseye/debian-installer/)

[手把手教你 VMware 虚拟机详细安装 Debian 11 图文教程](https://blog.csdn.net/networkTalent/article/details/123375048)

> 注意：使用清华源 mirrors.tuna.tsinghua.edu.cn

## 基本命令

- 查看安装系统版本

```bash
cat /etc/os-release 
```

- 安装包

```bash
sudo apt install vim
```

## 使用

### 安装 Python

切换有权限的用户

```bash
su root
```

确保系统已更新：

```bash
sudo apt update && sudo apt upgrade
```

安装构建 Python 所需的依赖包和工具：

```bash
sudo apt install build-essential libc6-dev libbz2-dev libffi-dev libgdbm-dev libncurses5-dev libnss3-dev libreadline-dev libsqlite3-dev libssl-dev tk-dev wget zlib1g-dev
```

下载 Python 3.8 的源代码（可以根据需要选择其他对应的版本）：

```bash
wget https://www.python.org/ftp/python/3.8.17/Python-3.8.17.tgz
```

或者

```bash
curl -O https://www.python.org/ftp/python/3.8.17/Python-3.8.17.tgz
```

解压缩下载的源代码文件：

```bash
tar -xf Python-3.8.17.tgz
```

进入解压后的目录：

```bash
cd Python-3.8.17
```

配置编译选项：

```bash
./configure --enable-optimizations
```

编译源代码：

```bash
make -j$(nproc)
```

> 解释：`-j` 参数用于指定并行编译的线程数，`$(nproc)` 则是一个 shell 变量，用于获取当前系统上可用的逻辑 CPU 核心数量。

安装 Python：

```bash
sudo make altinstall
```

注意：使用 `make altinstall` 命令而不是 `make install` 是为了避免覆盖系统默认的 Python 版本。

验证安装结果：

```bash
python3.8 --version
```

确定已安装 python 的版本和路径：

```bash
which python
```

或

```bash
whereis python
```
