---
title: OpenVPN 部署
date: 2023-11-28 09:30:00
tags:
- OpenVPN
categories:
- OpenVPN
---

openvpn是开源VPN软件，只需要简单的配置，就可以在企业搭建安全虚拟网络中使用，满足日常远程办公的需求。

本篇文档为在 windows 服务器安装搭建 openvpn记录，仅供参考。

参考：https://blog.eyyyye.com/article/39


## 部署服务端

### windows 部署

#### 1、软件下载

下载最新版本的OpenVPN包（服务端客户端公用一个包）

根据自己机器架构下载相应的包

下载的文件名为：OpenVPN-2.6.8-I001-amd64.msi

[OpenVPN 社区版官网 Web 下载地址](https://openvpn.net/community-downloads/)

[OpenVPN 社区版 Github 下载地址](https://github.com/OpenVPN/openvpn)

根据需要下载
[OpenVPN Connect 客户端 下载地址](https://openvpn.net/client/)

#### 2、服务端安装

双击安装，选择“Customize”

![](/images/微信截图_20231128165316.png)

> 注意：服务端是选择“Customize”，容易点错，服务端需要额外选择服务

默认情况下不会安装的两个特性，我们需要在安装过程中进行选择。

- OpenVPN Service
- OpenSSL Utilities -> EasyRSA 3

![](/images/QQ截图20231128165939.png)

![](/images/QQ截图20231128170032.png)

按需修改安装路径后

点击 Install Now 开始安装

安装成功后，点击 Close

弹出一个提醒框，提示没有找到可连接的配置文件，无视，点击确认即可。

![](/images/微信截图_20231128170405.png)

这个时候 服务端软件 已经安装好了。（客户端开局直接点击 Install Now，不用点击 Customize）

#### 3、证书密匙生成

##### 配置 Easy-RSA 配置文件

默认安装路径是 `C:\Program Files\OpenVPN\`，根据本身情况进行修改，推荐放在 `D:\OpenVPN`

找到目录 `OpenVPN\easy-rsa`，将 vars.example 文件复制并重名为 vars。

“vars”文件包含内置的 Easy-RSA 配置，本文不做配置解释。建议保持默认设置，也可以自定义更改。

##### 生成 证书

以管理员身份打开CMD,切换到 easy-rsa 目录下

```bash
D:

cd D:\OpenVPN\easy-rsa

EasyRSA-Start.bat
```

输入EasyRSA-Start.bat回车后，进入到easy-rsa3的shell会话

![](/images/微信截图_20231128175006.png)

执行 init-pki 来创建 pki 目录

```bash
./easyrsa init-pki
```

- 生成 CA 根证书

生成无密码 CA 证书

```bash
./easyrsa build-ca nopass
```

生成过程中会要求输入证书名称，随意输入即可，本次使用Open_CA作为名称，

生成结束后会打印出证书所在目录 OpenVPN\easy-rsa\pki\ca.crt

![](/images/微信截图_20231128192702.png)

- 生成 服务端 证书

生成无密码服务端证书，其中 server 可以替换服务器名

```bash
./easyrsa build-server-full server nopass
```

生成后证书文件在 OpenVPN\easy-rsa\pki\issued\server.crt

生成后key文件在 OpenVPN\easy-rsa\pki\private\server.key

![](/images/微信截图_20231128193342.png)

验证证书

```bash
openssl verify -CAfile pki/ca.crt pki/issued/server.crt
```

- 生成 客户端 证书

生成无密码客户端证书，其中 client 可以替换服务器名

```bash
./easyrsa build-client-full client nopass
```

生成后证书在 OpenVPN\easy-rsa\pki\issued\client.crt

生成后证书key文件在 OpenVPN\easy-rsa\pki\private\client.key

![](/images/微信截图_20231128194114.png)


验证证书

```bash
openssl verify -CAfile pki/ca.crt pki/issued/client.crt
```

- 生成 DH 密钥

```bash
./easyrsa gen-dh
```

生成文件在 OpenVPN\easy-rsa\pki\dh.pem

![](/images/微信截图_20231128200019.png)

> OpenVPN服务器必须要生成 Diffie Hellman (DH) 参数
>
> 这些参数定义了OpenSSL如何执行Diffie-Hellman (DH)密钥交换。Diffie-Hellman密钥交换是一种通过公共信道安全地交换密码密钥的方法

- 生成 tls-auth 秘钥

使用这个密钥，我们启用TLS -auth指令，它添加一个额外的HMAC签名到所有SSL/TLS握手包的完整性验证。

任何不带有正确HMAC签名的UDP包可以被丢弃而无需进一步处理。

启用tls-auth可以保护我们免受：

- OpenVPN UDP端口上的DoS攻击或端口泛洪。
- 端口扫描，以确定哪些服务器UDP端口处于侦听状态。
- SSL/TLS实现中的缓冲区溢出漏洞。
- 从未经授权的机器发起SSL/TLS握手。

首先[下载Easy-TLS](https://github.com/TinCanTech/easy-tls)。
它是一个Easy-RSA扩展工具，我们正在使用它来生成tls-auth密钥。
单击code选项卡下的Download zip选项。
请参考下面的截图。

这里要注意一下，在最新的版本中，没有了这两个文件，如果有需要的话，可以查看它的前期的版本进行下载使用。

若坚持使用最新版本，没有找到 easytls-openssl.cnf 文件，[issues解决方案](https://github.com/TinCanTech/easy-tls/issues/301)

旧版有easytls-openssl.cnf [旧版下载地址](https://github.com/TinCanTech/easy-tls/tree/v2.6.0)

然后解压“easy-tls-master”文件夹，将“easytls”和“easytls-openssl.cnf”文件拷贝到“manm\OpenVPN\easy-rsa”目录下。

查看下面的截图作为参考。

![](/images/微信截图_20231129140420.png)

![](/images/微信截图_20231129143158.png)

现在回到EasyRSA shell提示符并输入下面的命令。初始化easy-tls脚本程序。

```bash
./easytls init-tls
```

若出现如图的报错,则需要指定 OpenVPN 路径，

![](/images/微信截图_20231129144541.png)

```bash
./easytls -b='D:\OpenVPN' init-tls
```

现在，使用下面的命令生成tls-auth密钥。

```bash
./easytls build-tls-auth
```

该命令将生成名为“tls-auth”的密钥文件。在“OpenVPN\easy-rsa\pki\easytls”文件夹下。请参考下面的截图。

![](/images/image-20220120182604157.png)

#### 4、创建服务器配置文件

进入 `OpenVPN\sample-config`文件夹，将 server.ovpn 文件复制一份到 `OpenVPN\config` 目录下。

同时将以下文件一并复制到`OpenVPN\config`目录下

- ca.crt
- dh.pem
- server.crt
- server.key
- tls-auth.key

编辑 server.ovpn 文件，修改以下地方，其他保持默认即可

```bash
local x.x.x.x  # 这个是服务器的内网IP地址，或者保持默认
ca ca.crt
cert SERVER.crt
key SERVER.key
dh dh.pem

push "route 192.168.0.0 255.255.255.0"  # 用于IP转发，服务端的子网推送到客户端，允许客户端访问服务器的内网
route 192.168.0.0 255.255.255.0  # 用于IP转发

push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 114.114.114.114" # 可以改成其他的DNS服务器
push "dhcp-option DNS 8.8.8.8"
tls-auth tls-auth.key 0 # This file is secret
cipher AES-256-GCM
```


点击连接，图标变绿就正常。

![](/images/image-20220120190423076.png)

假设服务器的内网子网为192.168.1.0/24，而OpenVPN服务器在该内网中的IP地址为192.168.1.10。

在Windows服务器上，需要执行以下步骤添加路由：

打开命令提示符（以管理员身份运行）。

输入以下命令来添加路由：

```bash
route -p add 192.168.0.0 mask 255.255.255.0 192.168.1.10
```

其中，-p参数是指路由将被永久添加到路由表中，192.168.1.0是内网子网的IP地址，255.255.255.0是子网掩码，192.168.1.10是OpenVPN服务器的IP地址。

这样，当客户端连接到OpenVPN服务器后，服务器会自动将访问请求转发到内网子网，从而实现客户端访问服务器端内网其他主机。

参考：[在Windows上配置OpenVPN，使客户端能够访问服务器端内网其他主机](https://blog.csdn.net/wangpwcsdn/article/details/133936962)

#### 5、防火墙端口配置

<font color="red">切记：客户端 和服务端，还有局域网的总路由防火墙 也要放开TCP 和 UDP 1194端口(可根据需要修改) </font>

#### 6、客户端安装

双击安装，选择“Customize” ，可以参考服务端安装，共用一个安装包

#### 6、客户端配置

复制以下文件到你的客户端，并且在同一目录`OpenVPN\config`下

- ca.crt
- CLIENT.crt
- CLIENT.key
- tls-auth.key
- client.ovpn（“\OpenVPN\sample-config”）

编辑client.ovpn，修改以下参数，其他保持默认

```bash
remote *.*.*.* 1194 # 服务器公网IP地址
ca ca.crt
cert CLIENT.crt
key CLIENT.key
tls-auth tls-auth.key 1
cipher AES-256-GCM
```

点击连接，图标变绿就正常。

![](/images/20220727120509885.png)

## 报错、疑问

[TLS Error: TLS key negotiation failed to occur within 60 seconds (check your network connectivity)官方解决方法](https://openvpn.net/faq/tls-error-tls-key-negotiation-failed-to-occur-within-60-seconds-check-your-network-connectivity/)


