---
title: Python pip工具配置与使用
date: 2023-08-18 16:14:00
tags:
- Python
categories:
- Python
---

## 参考

https://blog.csdn.net/JineD/article/details/125090904
https://blog.csdn.net/qq_19922839/article/details/117294102

## pip 源

| 来源 | URL |
| -- | -- |
| 清华大学 | https://pypi.tuna.tsinghua.edu.cn/simple/ |
| 阿里云 | http://mirrors.aliyun.com/pypi/simple/ |
| 中国科技大学 | https://pypi.mirrors.ustc.edu.cn/simple/ |
| 豆瓣 | http://pypi.douban.com/simple |
| Python官方 | https://pypi.python.org/simple/ |
| 网易 | https://mirrors.163.com/pypi/simple/ |
| 华为云 | https://repo.huaweicloud.com/repository/pypi/simple |


## 配置

### pip.ini配置文件

```ini
[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

```bash
cat > ~/.pip/pip.conf << EOF
[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```


### 临时指定源

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
```

### 升级 pip

```bash
python -m pip install --upgrade pip
或者
pip install --upgrade pip
pip install pip -U
```

### 获取到配置文件地址

```bash
pip config debug 
```


- Debian/Linux
```bash
liuweijie@debian:~$ pip3.8 config debug
env_var:
env:
global:
  /etc/xdg/pip/pip.conf, exists: False
  /etc/pip.conf, exists: False
site:
  /usr/local/pip.conf, exists: False
user:
  /home/liuweijie/.pip/pip.conf, exists: True
    global.timeout: 6000
    global.index-url: https://pypi.tuna.tsinghua.edu.cn/simple
    install.trusted-host: pypi.tuna.tsinghua.edu.cn
  /home/liuweijie/.config/pip/pip.conf, exists: False
```

- windows

```bash
(venv) E:\liuweijie1234\xxxxxx>pip config debug
env_var:
env:
global:
  C:\ProgramData\pip\pip.ini, exists: False
site:
  d:\python\python_setup\pip.ini, exists: False
user:
  C:\Users\win10\pip\pip.ini, exists: False
  C:\Users\win10\AppData\Roaming\pip\pip.ini, exists: True
    global.timeout: 6000
    global.index-url: https://pypi.tuna.tsinghua.edu.cn/simple
    global.trusted-host: pypi.tuna.tsinghua.edu.cn
```

- 查看当前环境pip源

```bash
pip config list
```

### 更新pip源配置

- 命令行更新

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

- 编辑文件更新

```ini
[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```


更新配置文件后更新pip

```bash
pip install update
```


C:\Users\win10\AppData\Roaming\pip

C:\Users\你的帐户名\pip


## 常用命令

```bash
pip freeze > requirements.txt # 导出已安装的包到requirements.txt文件

pip install requests # 安装requests包
pip install requests -i https://mirrors.aliyun.com/pypi/simple/

pip uninstall requests # 卸载requests包
pip list # 查看已安装的包
pip show requests # 查看requests包的详细信息
pip search requests # 搜索requests包
pip install -r requirements.txt # 根据requirements.txt文件安装包
```


