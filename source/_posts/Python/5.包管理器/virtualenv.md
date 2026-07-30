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

