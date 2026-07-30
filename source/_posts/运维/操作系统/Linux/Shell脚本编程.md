---
title: Shell 脚本编程
date: 2026-07-30 10:00:00
tags:
- 运维
- Linux
- Shell
- 脚本
categories:
- 运维
- 操作系统
- Linux
---

# Shell 脚本编程

Shell 脚本是自动化运维的核心能力，用于批量操作、定时任务、部署与健康检查等。本文以 `bash` 为主。

## 脚本基础

```bash
#!/usr/bin/env bash
set -euo pipefail     # 出错即停、未定义变量报错、管道失败捕获

echo "Hello, $USER"
var="value"
readonly PI=3.14      # 只读变量
```

- `set -e`：命令非零退出即终止；`set -u`：引用未定义变量报错；`set -o pipefail`：管道任一环节失败则整体失败。强烈建议脚本开头都加。
- 执行方式：`./script.sh`（需可执行）、`bash script.sh`、`source script.sh`（在当前 shell 执行，影响环境变量）。

## 变量与字符串

```bash
name="world"
greeting="hello $name"          # 双引号内可展开变量
echo ${name:0:3}                # 子串：wor
echo ${name:-default}           # 为空则用默认值
len=${#name}                    # 长度

# 字符串判断
[[ "$name" == "world" ]]
[[ "$name" =~ ^a.* ]]           # 正则
```

数组：

```bash
arr=(a b c)
arr+=("d")
echo ${arr[0]}                  # a
echo ${arr[@]}                  # 全部元素
echo ${#arr[@]}                 # 元素个数
```

## 条件判断

```bash
if [[ -f "$file" ]]; then
  echo "是普通文件"
elif [[ -d "$dir" ]]; then
  echo "是目录"
else
  echo "其他"
fi

# 常用测试：-f 文件 -d 目录 -e 存在 -z 空串 -n 非空 -eq 数值等
# case 多分支
case "$env" in
  prod)  echo "生产" ;;
  test)  echo "测试" ;;
  *)     echo "未知" ;;
esac
```

## 循环

```bash
for f in *.log; do
  echo "处理 $f"
done

for i in {1..5}; do echo $i; done

while read -r line; do
  echo "$line"
done < file.txt

while true; do
  check_health || break
  sleep 5
done
```

## 函数与参数

```bash
backup() {
  local src="$1"; local dst="$2"     # 局部变量
  tar czf "$dst" "$src"
  echo "备份完成: $dst"
}
backup /data /backup/data.tar.gz

# 位置参数
echo "脚本名: $0, 参数个数: $#, 全部: $@"
shift                                    # 左移参数
```

## 输入输出与重定向

```bash
cmd > out.log 2>&1          # 标准输出与错误都进文件
cmd >> out.log              # 追加
cmd 2>/dev/null             # 丢弃错误
read -p "输入: " var        # 交互读入
cat <<'EOF'                 # heredoc（变量不展开）
line1
line2
EOF
```

## 信号处理（trap）

```bash
trap 'echo "收到中断，清理中..."; rm -f /tmp/lock; exit 1' INT TERM
# 退出时清理
trap 'cleanup' EXIT
```

## 定时任务（crontab）

```bash
crontab -e                   # 编辑当前用户任务
crontab -l                   # 列出
# 格式：分 时 日 月 周  命令
0 3 * * *  /opt/scripts/backup.sh >> /var/log/backup.log 2>&1   # 每天 3 点
*/5 * * * * /opt/check.sh                                       # 每 5 分钟
0 2 * * 1  /opt/weekly.sh                                         # 每周一 2 点
```

- 建议使用绝对路径；输出重定向避免产生邮件堆积。
- 系统级任务放 `/etc/cron.d/` 或 `/etc/cron.daily/`。
- 容器/K8s 环境多用 `cronjob` 或调度器替代系统 crontab。

## 实战：健康检查脚本

```bash
#!/usr/bin/env bash
set -euo pipefail
URL="http://localhost:8080/healthz"
if curl -fsS --max-time 3 "$URL" >/dev/null; then
  echo "$(date) OK"
else
  echo "$(date) FAIL" | tee -a /var/log/health.log
  # 可选：systemctl restart myapp
fi
```

## 实战：日志清理

```bash
#!/usr/bin/env bash
set -euo pipefail
LOG_DIR="/var/log/myapp"
DAYS=7
find "$LOG_DIR" -name '*.log' -mtime +"$DAYS" -delete
echo "清理了 $DAYS 天前的日志"
```

写脚本的好习惯：加 `set -euo pipefail`、用双引号包裹变量、关键操作前打印日志、提供 `--help`、对输入做校验。
