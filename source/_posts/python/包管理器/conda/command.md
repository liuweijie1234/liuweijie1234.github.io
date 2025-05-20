## 命令

conda --version      # 查看conda版本

conda upgrade --all  # 升级所有包

conda update conda   # 更新conda

conda update python  # 更新python

conda install gatk
conda install gatk=3.7					# 安装特定的版本:
conda install -n env_name gatk  # 将 gatk 安装都 指定env_name中

## 管理虚拟环境

conda create -n env_name python=3.8  # 创建虚拟环境

conda env list           # 查看虚拟环境

conda info --envs        # 查看虚拟环境

activate                 # 进入base环境

conda activate env_name  # 激活虚拟环境

conda deactivate         # 退出虚拟环境

conda remove --name env_name --all  # 删除虚拟环境

conda env remove -n env_name        # 删除虚拟环境

conda create -n torch --clone py3  	# 将 py3 重命名为 torch

## 管理依赖包

虚拟环境下安装包
> 注！安装特定版本的包，conda用“=”，pip用“==”

conda install numpy=1.93
pip install numpy==1.93

conda list           # 查看已安装包

conda update numpy   # 更新包

conda remove numpy   # 删除包

pip uninstall numpy  # 删除包

## 管理镜像源

conda config --show-sources  # 查看镜像源

conda config --get channels  # 查看镜像源

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/

目前国内提供conda镜像的大学
  清华大学: https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/
  北京外国语大学: https://mirrors.bfsu.edu.cn/help/anaconda/
  南京邮电大学: https://mirrors.njupt.edu.cn/
  南京大学: http://mirrors.nju.edu.cn/
  重庆邮电大学: http://mirror.cqupt.edu.cn/
  上海交通大学: https://mirror.sjtu.edu.cn/
  哈尔滨工业大学: http://mirrors.hit.edu.cn/#/home
```

conda config --remove channels defaults  # 删除默认镜像源

conda config --remove-key channels # 恢复默认镜像源

conda config --set show_channel_urls yes  # 显示镜像源

conda config --set show_channel_urls no  # 隐藏镜像源

## 其他

升级base 的python版本
https://www.cnblogs.com/ruhai/p/12684838.html


防止打开终端Conda默认激活基本环境
conda config --set auto_activate_base false
https://blog.csdn.net/Edisonleeee/article/details/95089524


## 编辑器配置 conda 运行环境

确定当前激活Conda环境所在路径.

conda env list 

然后在File-->Preferences-->Settings-->Extensions-->Python-->setting.json添加下面的 Python 路径，这个路径和你设置的环境名称有关。

"python.pythonPath": "D:\\anaconda3\\envs\\python310\\python.exe"


选择编辑器模式
 方法一：点击vscode左下角然后选择相应的Anaconda环境
 方法二：点击vscode左下角选择扩展，搜索Anaconda，点击安装，然后点击设置，选择Anaconda路径，选择相应的Anaconda环境




