
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
source test_env/bin/activate
```

在Windows环境下，打开PowerShell，执行下面的命令:

```bash
test_env\Scripts\Activate
```

可以看到，命令行的提示符前面会出现括号，里面是虚拟环境名称。

### 4. 安装包

虚拟环境启用后，就可以使用pip命令来安装需要的包：

```bash
# 安装一个包
pip install requests
# 升级一个包
pip install --upgrade requests
# 升级一个包
pip install --upgrade requests
# 列出虚拟环境中已安装的包
pip list
# 将虚拟环境中已安装的包及其版本号导出到 requirements.txt 文件
pip freeze > requirements.txt
# 从 requirements.txt 文件安装依赖
pip install -r requirements.txt
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

### 7. 删除虚拟环境

```bash
rm -rf myenv
```