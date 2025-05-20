---
title: docker 安装
date: 2022-08-15 15:11:00
tags:
- docker
categories:
- docker
---

## 定义

Docker 是一个开源的应用容器引擎，它可以让开发者打包他们的应用以及依赖包到一个可移植的镜像中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）,更重要的是容器性能开销极低。


## 安装

### windows 安装

https://zhuanlan.zhihu.com/p/441965046


在 Windows 上安装 Hyper-V
https://learn.microsoft.com/zh-cn/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v


### ubuntu 安装 Docker


1. 更新系统并安装依赖
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release # 安装必要的工具
```

2. 添加Docker官方GPG密钥 (验证 Docker 软件包的来源和完整性)
```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

添加阿里云 Docker GPG 密钥
```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker-aliyun.gpg
sudo chmod a+r /etc/apt/keyrings/docker-aliyun.gpg
```

3. 添加Docker的 APT 仓库(安装和更新 Docker 软件包本身)

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
$(lsb_release -cs)  和  $(. /etc/os-release && echo "$VERSION_CODENAME")  是一样的


配置阿里云 Docker 的 APT 仓库

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker-aliyun.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker-aliyun.list > /dev/null
```

4. 安装Docker Engine 引擎
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin  
```

5. 启动Docker并设置开机自启
```bash
sudo systemctl enable docker --now
```

6. 将当前用户加入docker组（避免每次使用sudo）

```bash
sudo usermod -aG docker $USER
# 退出当前会话重新登录后生效
newgrp docker
```

7. 验证Docker是否安装成功

```bash
docker version       # 查看版本信息
docker run hello-world  # 运行测试容器
```

### 安装 Docker Compose

方法一：默认已安装

```bash
sudo apt-get install docker-compose-plugin -y
```

方法二： 使用pip安装

```bash
sudo apt install python3 python3-pip
python --version
pip --version

pip install docker-compose
```

方法三： 下载二进制文件安装（推荐最新稳定版）

1. 下载Docker Compose二进制文件（推荐v2版本）

```bash
# 自动获取最新稳定版
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 或手动指定版本（例如v2.26.1）
# sudo curl -L https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

2. 赋予执行权限

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

#### 验证安装

```bash
docker compose version  # 查看版本信息  V2
```

验证 Docker Compose

创建一个测试docker-compose.yml

```bash
mkdir ~/test-compose && cd ~/test-compose
cat <<EOF > docker-compose.yml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
EOF
```

启动服务并验证
```bash
docker compose up -d
curl http://localhost:80  # 应返回Nginx欢迎页面
docker compose down       # 停止服务
```

### 切换镜像源

Docker 中国区官方镜像：https://registry.docker-cn.com

腾讯云：https://mirror.ccs.tencentyun.com

网易云：https://hub-mirror.c.163.com

ustc：https://docker.mirrors.ustc.edu.cn


1. 修改 Docker 配置文件

```bash
sudo mkdir -p /etc/docker

sudo tee /etc/docker/daemon.json <<-'EOF'
{ 
  "registry-mirrors" : 
    [ 
      "https://docker.domys.cc",
      "https://hub.domys.cc",
      "https://docker.m.daocloud.io",
      "https://docker.xuanyuan.me", 
      "https://docker.1ms.run"
    ] 
}
EOF
```
其中<你的ID>需替换为阿里云容器镜像服务控制台获取的专属加速地址。

2. 重启 Docker 服务

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

3. 运行命令 docker info，在输出中查找 Registry Mirrors，确认包含配置的镜像地址，则说明加速器配置成功。

```bash
docker info
```

## 代理

```bash
"docker.io":
    endpoint:
    - "https://docker.m.daocloud.io"
    - "https://docker.amingg.com"
    - "https://docker.1ms.run"
    - "https://docker.1panel.dev"
```


## 卸载

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

