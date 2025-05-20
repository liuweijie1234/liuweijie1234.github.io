
pyenv --version # 查看pyenv版本

## 安装不同版本的Python

pyenv versions # 查看已安装python版本

pyenv install 3.8.12 # 安装指定版本
pyenv install --list # 查看可安装版本

pyenv uninstall 3.8.12 # 卸载指定版本

## 设置Python版本

- 全局版本
pyenv global 3.8.12 # 设置全局版本
pyenv global # 查看全局版本

- 本地版本
pyenv local 3.8.12 # 设置本地版本

- shell版本
pyenv shell 3.8.12 # 设置shell版本

## 管理虚拟环境

pyenv virtualenv 3.8.12 myenv # 创建虚拟环境

pyenv activate myenv  # 激活虚拟环境

pyenv deactivate # 退出虚拟环境











