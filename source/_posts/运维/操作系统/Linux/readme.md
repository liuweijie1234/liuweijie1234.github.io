---
title: 运维 · Linux
date: 2026-07-30 10:00:00
tags:
- 运维
- 操作系统
- Linux
- 导航
categories:
- 运维
- 操作系统
- Linux
---

# Linux

Linux 是服务器运维的绝对主力。本页汇总 Linux 常用操作、系统管理、权限与 Shell 编程，以及主流发行版实践。

## 常用操作

- [常用命令](常用命令.md) 合并自 `Linux/command.md`，覆盖文件、文本处理、网络、进程等基础命令
- [系统管理（进程/内存/磁盘/网络）](系统管理.md)
- [用户与权限](用户与权限.md) 用户组、sudo、chmod/chown、ACL、SELinux 基础

## 性能排查（实战）

- 线上 CPU 飙到 100%：如何用 `py-spy` 或 `gdb` 快速定位阻塞线程？
- 排查 `/proc` 目录下哪些文件（如 `/proc/<pid>/status`、`/proc/loadavg`、`/proc/meminfo`）？
- 配套工具：`top` / `htop` / `perf` / `strace` / `netstat` / `ss`

## Shell 编程

- [Shell 脚本编程](Shell脚本编程.md) 变量、条件判断、循环、函数、定时任务（crontab）、实战脚本

## 发行版

- [Debian](发行版/Debian.md) 合并自 `Linux/Debian/*`
- [Ubuntu](发行版/Ubuntu.md) 合并自 `Linux/Ubuntu/*`（apt 源、常用操作）
