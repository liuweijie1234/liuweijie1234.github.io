---
title: Python 虚拟环境工具
date: 2023-08-18 16:14:00
tags:
- Python
categories:
- Python
---

## 优缺点分析

虚拟环境工具 virtualenvwrapper、venv和virtualenv的优势和缺点的分析：

1、**virtualenvwrapper**:

优势：

- 简化了创建、使用和管理虚拟环境的过程，提供了一组易用的命令。
- 支持在不同的项目中切换虚拟环境，方便管理多个项目。
- 提供了扩展功能，如预定义钩子，可以在环境创建和销毁时执行自定义命令。

缺点：

- 依赖于在系统上全局安装的 virtualenv 包，需要额外安装该包。
- 只能与 bash 或 zsh 终端兼容。

2、**venv (Python 3.3+ 内置)**:

优势：

- 是 Python 官方推荐的用于创建虚拟环境的工具，无需额外安装。
- 可以通过 venv 模块轻松创建和管理虚拟环境。
- 提供了用于激活和停用虚拟环境的命令。

缺点：

- 相比于 virtualenvwrapper 缺少一些高级功能，例如自动执行脚本或命令。
- 不支持直接切换虚拟环境，在不同的项目间切换时需要手动激活不同的环境。

3、**virtualenv**:

优势：

- 是最早发布的 Python 虚拟环境工具，被广泛使用。
- 兼容性强，支持多个版本的 Python。
- 提供了一些高级功能，例如在创建虚拟环境时指定 Python 解释器版本。

缺点：

- 安装和使用较为繁琐，需要手动安装 virtualenv 包。
- 不提供像 virtualenvwrapper 那样的额外工具和便利功能。

总体来说，这些工具都有其优点和缺点。
如果你希望一个功能丰富的工具，并且只关注于 bash 或 zsh 终端的兼容性，那么 virtualenvwrapper 可能更适合你。
如果你更倾向于使用官方推荐的工具以及较为简洁的方式创建和管理虚拟环境，venv 是个不错的选择。
而 virtualenv 则是一个稳定且具有广泛支持的选项，尤其在需要支持多个 Python 版本的情况下较为有用。
根据你的具体需求和喜好，选择适合自己的虚拟环境工具。


## venv 教程

官方文档： https://docs.python.org/3/library/venv.html


### 1. 安装venv(默认跳过)

python3.6及以上已经默认安装，python3.5需要通过系统的包管理工具安装，例如在Ubuntu上，可以这么安装:

```bash
sudo apt install python3-venv
```

### 2. 创建虚拟环境

假设我们要在当前目录的 `test_env` 目录下创建虚拟环境，那么执行下面的命令就可以了：

```bash
python3 -m venv test_env
```

指定Python 版本为 3.9

```bash
python3.9 -m venv myproj2
```

### 3. **启用虚拟环境**

在Linux和Mac环境下，打开终端，执行下面的命令：

```bash
source ./test_env/bin/activate
```

在Windows环境下，打开PowerShell，执行下面的命令:

```bash
.\test_env\Scripts\Activate.ps1
```

可以看到，命令行的提示符前面会出现括号，里面是虚拟环境名称。

### 4. 安装包

虚拟环境启用后，就可以使用pip命令来安装需要的包：

```bash
pip install easydict
```

注意这里不需要root权限，因此无需添加sudo。

在Linux和Mac系统上，安装的包放在 `./test_env/lib/pythonx.x/site-packages` 目录下，

在Windows系统上，是在`./test_env/Lib/site-packages` 目录下。

### 5. 使用包

安装后，可以在命令行执行 python 命令，进入 Python 交互式环境，然后 import 安装的包，如果不报错，就说明安装成功了

```bash
$ python
Python 3.9.6 (default, Sep 26 2022, 11:37:49)
[Clang 14.0.0 (clang-1400.0.29.202)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import easydict
>>>
```

或者也可以用一条命令 `python -c "import <package-name>"`来验证是否安装，没有报错就说明安装成功

然后就可以编写你的Python代码了，写完后用 python my-code.py 来执行Python代码。

### 6. **退出虚拟环境**

退出虚拟的python环境，在命令行执行下面的命令即可：

```bash
deactivate
```

## virtualenv 教程

### 1. 安装 virtualenv

```bash
pip3 install virtualenv
```

- 查看版本

```bash
virtualenv --version
```

### 2. 创建虚拟环境

```bash
virtualenv myenv5
```

- 指定Python 版本为 3.9

```bash
virtualenv myvenv6 -p python3.9
```

bin：存放一些python、pip命令的目录

virtualenv的软件包管理目录在 `lib/python3.6/site-packages/` 下。

- 继承父环境的包

```bash
#创建一个专门放虚拟环境的文件夹，并cd进去
virtualenv --system-site-packages myvenv7
```

- 删除虚拟环境，只需要将这个虚拟环境目录删除即可。

```bash
rm -rf myenv5
```

### 3. **启用虚拟环境**

```bash
source /myenv5/bin/activate
```


### 4. **退出虚拟环境**

```bash
deactivate
```


## virtualenvwrapper 教程(推荐)

### 1. 安装 virtualenvwrapper

- 依赖

```bash
pip3 install virtualenv 
```

- linux 安装

```bash
pip3 install virtualenvwrapper
```

- Windows 安装

```bash
pip3 install virtualenvwrapper-win
```

### 2. 修改虚拟环境保存目录(可选)

virtualenvwrapper 默认将所有的虚拟环境放在 `～/.virtualenvs` 目录下管理，可以修改环境变量 `WORKON_HOME`` 来指定虚拟环境的保存目录。

```bash
mkdir -p /data/virtualenvs/ # 可选，我们这里安装在默认的 

vim /etc/profile
# virtualenvwrapper 
export WORKON_HOME=$HOME/.virtualenvs 
export PROJECT_HOME=$HOME/Devel
```

```bash
source /etc/profile  # source加载环境变量使生效
```

### 3. 激活 virtualenvwrapper


- 找到virtualenvwrapper.sh

一般在 `/usr/local/bin/virtualenvwrapper.sh`

- 激活virtualenvwrapper

```bash
source /usr/local/bin/virtualenvwrapper.sh
```

更新环境变量
```bash
vim /root/.bashrc
​
# virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3.8
source /usr/local/bin/virtualenvwrapper.sh
```

注意：如果你安装的virtualenv不在系统默认的python解释器上，就需要单独指定virtualenvwrapper使用的python路径：VIRTUALENVWRAPPER_PYTHON，否则激活的时候，会报错，如下：

No module named virtualenvwrapper

如下报错，因为它默认使用系统的python路径了。
添加VIRTUALENVWRAPPER_PYTHON 变量即可。

```bash
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3.8
```

### 2. 创建虚拟环境

```bash
mkvirtualenv venv8
```
注意： 创建的同时，还默认激活（启用）了虚拟环境

指定python版本
```bash
mkvirtualenv --python=/usr/local/python3.9/bin/python3 venv9 
# 有环境变量可以简化 
mkvirtualenv --python=python3.9 venv9
```

### 3. **进入虚拟环境**

查看当前的虚拟环境目录

```bash
workon
```

切换虚拟环境

```bash
workon venv8
```

### 4. **退出虚拟环境**


```bash
deactivate
```


### 5. 删除虚拟环境

```bash
rmvirtualenv venv8
```