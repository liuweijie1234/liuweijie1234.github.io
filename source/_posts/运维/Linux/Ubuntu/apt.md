## 更改 Ubuntu 的 apt 源为国内源的步骤如下：

### 备份默认源 ：
先备份原始的 sources.list 文件，以便在需要时可以恢复。
```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```
### 编辑 sources.list 文件 ：
使用文本编辑器打开 /etc/apt/sources.list 文件。
```bash
sudo nano /etc/apt/sources.list
```
或者使用 vi 编辑器：
```bash
sudo vi /etc/apt/sources.list
```

### 替换为国内源 ：

在打开的文件中，将默认的源地址替换为国内镜像源地址。以下是一些常见的国内源配置示例：
阿里云 ：
```bash
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

清华大学 ：
```bash
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
```

中科大 ：
```bash
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
```

华为云 ：
```bash
deb https://mirrors.huaweicloud.com/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.huaweicloud.com/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.huaweicloud.com/ubuntu/ bionic-security main restricted universe multiverse
deb https://mirrors.huaweicloud.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.huaweicloud.com/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.huaweicloud.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.huaweicloud.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.huaweicloud.com/ubuntu/ bionic-backports main restricted universe multiverse
```
请根据你使用的 Ubuntu 版本替换上面的 bionic 为相应的版本代号（如 focal、jammy 等）。

### 保存并退出 ：

如果使用 nano，按 Ctrl + O 保存，然后按 Enter 确认，最后按 Ctrl + X 退出。
如果使用 vi，按 Esc 键，然后输入 :wq 并按 Enter 保存并退出。

### 更新软件包列表 ：

运行以下命令使新的源配置生效，并更新软件包列表。
```bash
sudo apt-get update
```