

poetry --version # 查看poetry版本

pipx upgrade poetry # 更新poetry

poetry env use 3.11

poetry install

poetry shell

## 配置

poetry config --list # 查看配置

poetry config virtualenvs.in-project true # 在项目目录下创建虚拟环境

https://cloud.tencent.com/developer/article/2174333

```toml
# Poetry 缓存目录位置
cache-dir = "C:\\Users\\zy\\AppData\\Local\\pypoetry\\Cache"

# 安装器配置
installer.max-workers = null        # 安装时的最大工作进程数
installer.parallel = true          # 是否启用并行安装
installer.re-resolve = true       # 是否在更新依赖时重新解析依赖关系
installer.no-binary = null        # 指定哪些包不使用二进制分发
installer.only-binary = null      # 指定哪些包只使用二进制分发

# 是否启用系统密钥环存储凭证
keyring.enabled = true

# HTTP 请求重试次数
requests.max-retries = 0

# 依赖解析器配置
solver.lazy-wheel = true

# 是否使用系统的 git 客户端
system-git-client = false
# 是否自动创建虚拟环境
virtualenvs.create = true

# 是否在项目目录下创建虚拟环境（而不是全局目录）
virtualenvs.in-project = true

# 虚拟环境选项
virtualenvs.options.always-copy = false      # 是否总是复制而不是链接 Python 可执行文件
virtualenvs.options.no-pip = false          # 是否不安装 pip
virtualenvs.options.system-site-packages = false  # 是否允许访问系统的 site-packages

# 虚拟环境存放路径
virtualenvs.path = "{cache-dir}\\virtualenvs"

# 是否优先使用当前激活的 Python 解释器
virtualenvs.prefer-active-python = true

# 虚拟环境提示符格式
virtualenvs.prompt = "{project_name}-py{python_version}"

# 是否使用 Poetry 自带的 Python 解释器
virtualenvs.use-poetry-python = false
```



## 依赖管理

通过 pyproject.toml 文件管理依赖


poetry add requests # 添加依赖

poetry remove requests # 移除依赖

poetry update requests # 更新依赖

poetry show requests # 查看依赖


## 管理Python版本

通过在 pyproject.toml 中设置 python 字段

```toml
[tool.poetry.dependencies]
python = "^3.8"
```


## 虚拟环境

poetry env use 3.8.12 # 使用指定版本

poetry install # 安装依赖并创建虚拟环境

poetry env list # 查看虚拟环境



poetry shell # 进入虚拟环境 source .venv/Scripts/activate 替代命令

poetry deactivate # 退出虚拟环境


poetry env remove myenv # 删除虚拟环境

poetry env remove python3.11.9 # 删除指定版本

poetry env remove python3.11.9 --all # 删除指定版本并删除所有虚拟环境

poetry env info # 查看虚拟环境信息



## 打包发布

poetry build # 打包

poetry publish --build # 发布


## 自动生成锁文件

Poetry 会生成 poetry.lock 文件，这个文件记录了所有的依赖项和它们的版本信息，确保在不同环境中安装时，所有依赖的一致性。









