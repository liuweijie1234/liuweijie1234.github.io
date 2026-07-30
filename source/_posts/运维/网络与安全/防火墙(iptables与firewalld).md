---
title: 防火墙（iptables 与 firewalld）
date: 2026-07-30 10:00:00
tags:
- 运维
- 网络
- 安全
- 防火墙
- iptables
categories:
- 运维
- 网络与安全
---

# 防火墙（iptables 与 firewalld）

Linux 防火墙主流方案有 `iptables`（底层 Netfilter 规则）与 `firewalld`（RHEL 7+ 默认的动态管理前端）。理解二者关系与规则链，是服务器网络安全的基础。

## iptables 表链结构

iptables 包含多个**表（table）**，每个表包含若干**链（chain）**：

| 表 | 用途 |
| --- | --- |
| `filter` | 过滤（默认表），控制放行/拒绝 |
| `nat` | 网络地址转换（端口转发、SNAT/DNAT） |
| `mangle` | 修改报文（TTL、TOS 等） |
| `raw` | 连接跟踪前处理 |

`filter` 表常用链：`INPUT`（入站）、`OUTPUT`（出站）、`FORWARD`（转发）。

**数据包匹配流程**：路由判断 → PREROUTING → INPUT/FORWARD/OUTPUT → POSTROUTING。规则按顺序匹配，命中即执行动作（`ACCEPT`/`DROP`/`REJECT`）。

## 常用规则（filter）

```bash
# 查看规则（-n 数字显示，-L 列出，-v 详细）
iptables -nvL

# 放行 SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 放行已建立的连接（务必先加，否则会断自己的回包）
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 拒绝某 IP（DROP 静默丢弃，REJECT 返回拒绝）
iptables -A INPUT -s 10.0.0.5 -j DROP

# 限制 ping 频率（防洪水）
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# 默认策略：入站拒绝、转发拒绝、出站放行
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```

## NAT 与端口转发

```bash
# 开启 IP 转发
sysctl -w net.ipv4.ip_forward=1

# SNAT（内网机器共享公网出口）
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT（端口转发：公网 8080 -> 内网 192.168.1.10:80）
iptables -t nat -A PREROUTING -p tcp --dport 8080 \
  -j DNAT --to-destination 192.168.1.10:80
```

## 规则持久化

```bash
# Debian/Ubuntu
iptables-save > /etc/iptables/rules.v4
# 开机恢复：安装 iptables-persistent，或加入 /etc/rc.local

# RHEL/CentOS 7
service iptables save        # 写入 /etc/sysconfig/iptables
```

> 注意：直接用 `iptables` 命令添加的规则重启会丢失，必须保存。

## firewalld 区域与服务

firewalld 以**区域（zone）**管理信任级别，默认 zone 通常为 `public`。

```bash
# 查看状态与默认 zone
firewall-cmd --state
firewall-cmd --get-default-zone

# 放行端口（--permanent 持久化，需 reload 生效）
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --add-service=http --permanent

# 端口转发
firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80:toaddr=192.168.1.10 --permanent

# 富规则：仅允许特定 IP 访问 3306
firewall-cmd --add-rich-rule='rule family=ipv4 source address=10.0.0.0/8 port port=3306 protocol=tcp accept' --permanent

firewall-cmd --reload
```

## iptables 与 firewalld 的区别

- firewalld 是 iptables/nftables 的**上层管理工具**，动态增删规则无需重启服务。
- 二者底层都会写 Netfilter；不要混用 `iptables` 命令与 `firewall-cmd` 管理同一台机器，避免规则冲突。
- CentOS 7/8 默认 firewalld；Ubuntu 默认 `ufw`（也是 iptables 前端）。统一管理建议选其一。

## 与云安全组的关系

- 云厂商的**安全组**是虚拟网络的 ACL，在流量到达实例前已过滤，相当于外层的 iptables。
- 主机 iptables/firewalld 是实例内的第二道防线。两者配合：安全组做粗粒度（允许某网段），主机防火墙做细粒度。
- 排障时若访问不通，先确认安全组是否放行，再查本地防火墙。
