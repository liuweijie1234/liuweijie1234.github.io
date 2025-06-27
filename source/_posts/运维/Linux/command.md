---
title: linux 常用命令
date: 2022-08-15 15:11:00
tags:
- linux
categories:
- linux
---

### 系统时间时区设置

查看服务器时间
date
sudo date -s "2025-06-23 13:18:00"

查看系统时区
timedatectl
sudo timedatectl set-timezone Asia/Shanghai
sudo timedatectl set-time "2025-06-20 14:30:00"

### 查看系统资源
top ：查看系统资源占用情况，显示当前进程信息
uptime：查看报告系统运行时长及平均负载


查看端口情况
netstat -tunlp | grep 端口号：查看端口号占用情况
lsof -i:端口号：查看端口号占用情况

磁盘 
df -hl：查看磁盘剩余空间
df -h：查看每个根路径的分区大小 (如果出现磁盘报警和实际有出入，可能因为文件操作符或者文件句柄未释放导致)
du -sh [目录名]：返回该目录的大小
du -sh * 当前目录下所有目录的大小
du -sm [文件夹]：返回该文件夹总M数
du -h [目录名]：查看指定文件夹下的所有文件大小（包含子文件夹）


查看内存交换区
free -m -h

cpu
sar -u 1 5

IO
iotop：查看IO读写（yum install iotop安装）
iotop -o：直接查看比较高的磁盘读写程序


查看进程
ps aux | grep uwsgi


压缩zip
zip -q -r html.zip *

### 基础命令

1、查看目录与文件：ls

ls -la：显示当前目录下所有文件的详细信息

2、切换目录：cd

cd /home 进入 ‘/ home’ 目录

cd … 返回上一级目录

cd …/… 返回上两级目录

3、显示当前目录：pwd

pwd

4、创建空文件：touch

touch desc.txt：在当前目录下创建文件desc.txt

5、创建目录：mkdir

mkdir test：在当前目录下创建test目录

mkdir -p /opt/test/img：在/opt/test目录下创建目录img，若无test目录，先创建test目录

6、查看文件内容：cat

cat desc.txt：查看desc.txt的内容



7、分页查看文件内容：more

more desc.txt：分页查看desc.txt的内容

8、查看文件尾内容：tail

tail -100 desc.txt：查看desc.txt的最后100行内容
tail -n 2000 /var/log/messages/error.log： 查看日志

9、拷贝：cp

cp desc.txt /mnt/：拷贝desc.txt到/mnt目录下

cp -r test /mnt/：拷贝test目录到/mnt目录下

10、剪切或改名：

mv desc.txt /mnt/：剪切文件desc.txt到目录/mnt下

mv 原名 新名

11、删除：rm

rm -rf test：删除test目录，-r递归删除，-f强制删除。危险操作，务必小心，切记！

12、搜索文件：find

find /opt -name ‘*.txt’：在opt目录下查找以.txt结尾的文件

13、显示或配置网络设备：ifconfig

ifconfig：显示网络设备情况

14、显示网络相关信息：netstat

netstat -a：列出所有端口

netstat -tunlp | grep 端口号：查看进程端口号

15、显示进程状态：ps

ps -ef：显示当前所有进程

ps-ef | grep java：显示当前所有java相关进程

16、查看目录使用情况：du

du -h /opt/test：查看/opt/test目录的磁盘使用情况

17、查看磁盘空间使用情况：df

df -h：查看磁盘空间使用情况

18、显示系统当前进程信息：top

top：显示系统当前进程信息

19、杀死进程：kill

kill -s 9 27810：杀死进程号为27810的进程，强制终止，系统资源无法回收

20、压缩和解压：tar

tar -zcvf test.tar.gz ./test：打包test目录为test.tar.gz文件，-z表示用gzip压缩

tar -zxvf test.tar.gz：解压test.tar.gz文件

21、改变文件或目录的拥有者和组：chown

chown nginx:nginx desc.txt：变更文件desc.txt的拥有者为nginx，用户组为nginx

chown -R nginx:nginx test：变更test及目录下所有文件的拥有者为nginx，用户组为nginx 22、改变文件或目录的访问权限：chmod

chmod u+x test.sh：权限范围：u(拥有者)g(郡组)o(其它用户)， 权限代号：r(读权限/4)w(写权限/2)x(执行权限/1)#给文件拥有者增加test.sh的执行权限

chmod u+x -R test：给文件拥有者增加test目录及其下所有文件的执行权限

23、文本编辑：vim

vim三种模式：命令模式，插入模式，编辑模式。使用ESC或i或：来切换模式。

命令模式下:q退出 :q!强制退出 :wq!保存退出 :set number显示行号 /java在文档中查找java yy复制 p粘贴

vim desc.txt：编辑desc.txt文件

24、关机或重启：shutdown

shutdown -h now：立刻关机

shutdown -r -t 60：60秒后重启

shutdown -r now：重启(1)

reboot：重启(2)

25、帮助命令：man

man ls：查看ls命令的帮助文档

help

### 快捷键

Ctrl + a 光标到开头

Ctrl + c 中断当前程序

Ctrl + d 退出当前窗口或当前用户

Ctrl + e 光标到结尾

Ctrl + l 清屏 相当与clear

Ctrl + u 剪切、删除（光标以前的）内容- - Ctrl + k 剪切、删除（光标以后的）内容- - Ctrl + r 查找（最近用过的命令）

tab 所有路径以及补全命令

Ctrl+shift+c 命令行复制内容

Ctrl+shift+v 命令行粘贴内容

Ctrl + q 取消屏幕锁定

Ctrl + s 执行屏幕锁定

#### 清空日志文件

```bash
echo " ">filename.log
```

#### 按照文件名搜索

```bash
find / -name yum.conf
find / -name nginx.conf
find / -name supervisord.service
```

#### 提取当前所有文件内容带有相关 ip 的行

```bash
grep -n -ri "10.0.0.1" ./  >> ../10.0.0.1.txt
```

-n: 显示匹配行在文件中的行号。
-r: 递归搜索当前目录及其所有子目录。
-i: 忽略大小写，即搜索时不区分大小写。

./: 表示当前目录。
>>: 追加重定向，将搜索结果追加到指定文件。
../10.0.0.1.txt: 要保存搜索结果的文件路径，即上一级目录的 "10.0.0.1.txt" 文件。

```bash
grep '10.3.2.61' access.log > 10.3.2.61.txt
```

#### 批量给当前目录下的日志文件增加前缀

```bash
for name in `ls *.log`;do mv $name 10.0.0.1_${name%.html};done
```

#### **/etc/profile 和 /root/.bashrc 的区别**

/etc/profile 和 /root/.bashrc 是用于配置用户环境的文件，但它们有以下区别：

1、/etc/profile：

- /etc/profile 是系统级别的配置文件，适用于所有用户。
- 它是在用户登录时执行的脚本文件，用于设置全局的环境变量和默认的系统环境。
- 通常用于定义系统范围的环境变量、全局的路径和命令别名等。
- 所做的更改会影响到所有登录到系统的用户。

2、/root/.bashrc：

- /root/.bashrc 是特定用户（以 root 用户为例）的个人配置文件。
- 它是在用户每次打开新的终端或登录时执行的脚本文件，用于设置个人的环境变量和用户级别的配置。
- 每个用户都可以有自己的 .bashrc 文件，并且这些文件只适用于对应的用户。
- 通常用于定义个人化的环境变量、路径和命令别名等。
- 所做的更改只会影响到某个特定用户。

总结起来，/etc/profile 是系统级别的全局配置文件，会影响所有用户。
而 /root/.bashrc 是特定用户的个人配置文件，只会影响到对应的用户。
在设置环境变量和配置文件时，应根据需要选择合适的文件进行修改

### 统计 Apache日志中访问IP地址数量

```bash
grep -Eo 'client ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})' error.log | sort | uniq -c | sort -nr
```
grep 命令用于在文件中搜索匹配模式的字符串。
-Eo 选项指定仅输出匹配的子字符串，而不输出整行。
'client ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})' 是正则表达式，用于匹配 "client " 后面的 IP 地址。

sort 命令用于对提取的 IP 地址进行排序。
uniq -c 命令用于统计每个 IP 地址出现的次数。
sort -nr 命令用于将结果按照出现次数降序排序。

```bash
awk '{print $1, $9}' access.log | sort | uniq -c | sort -nr
```
awk 命令是一种强大的文本处理工具，可以根据特定模式对文本进行操作
$1 表示第一列，即 IP 地址。
$9 表示第九列，即状态码。
sort 命令用于对输出结果进行排序，方便后续统计。
uniq -c 命令用于统计每个排序后的行出现的次数。
sort -nr 命令用于按计数降序排序，方便查看出现次数最多的 IP 和状态码组合。


###  更换 apt 源


### 设置环境变量

```bash
export PATH=$PATH:/usr/local/mysql/bin/
```
export 命令用于设置环境变量。

```bash
echo 'export DB_PASSWORD=Aa1237456' >> ~/.bashrc
echo 'export DB_HOST=mysql' >> ~/.bashrc
echo 'export DB_PORT=3306' >> ~/.bashrc
echo 'export DB_NAME=test' >> ~/.bashrc
source ~/.bashrc
```
