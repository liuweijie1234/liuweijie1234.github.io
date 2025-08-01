
## 安装

pipx 安装
https://pipx.pypa.io/stable/installation/

pipx install poetry


https://python-poetry.org/docs/

windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

注意需要添加环境变量到Path,后重启PowerShell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\liuwe\AppData\Roaming\Python\Scripts", "User")

## 常用命令

poetry --version # 查看poetry版本

pipx upgrade poetry # 更新poetry

poetry new myproject  # 创建新项目

poetry add requests  # 添加依赖

poetry env use 3.11
poetry env use C:\Python38\python.exe   # 明确指定 Python 3.8 路径

poetry install # 安装依赖

poetry shell  # 进入虚拟环境

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

poetry show # 检查已安装包

poetry show requests # 查看依赖


```powershell
# 逐行安装 requirements.txt 中的依赖
Get-Content requirements.txt | ForEach-Object { poetry add $_ }
```

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




## 卸载

windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -  --uninstall

https://juejin.cn/post/7224036517140103226

C:\Users\{用户名}\AppData\Roaming\pypoetry\




## cursor 和 poetry 虚拟环境的使用问题

這是因為 VSCode 的 Python 擴展可能沒有正確識別到 Poetry 的虛擬環境。讓我們來解決這個問題：

1. 首先確認 Poetry 虛擬環境的位置：
```bash
# 在終端執行
poetry env info --path
```

2. 在 VSCode 中設置 Python 解釋器：

- 按 Cmd/Ctrl + Shift + P 打開命令面板
- 輸入 Python: Select Interpreter
- 點擊 Enter interpreter path...
- 輸入或瀏覽到 Poetry 虛擬環境的 Python 解釋器路徑
  - Windows: {poetry_env_path}\Scripts\python.exe
  - Mac/Linux: {poetry_env_path}/bin/python

3. 或者在 VSCode 的 settings.json 中直接設置：

```json
{
    "python.defaultInterpreterPath": "/path/to/poetry/venv/bin/python",
    "python.analysis.extraPaths": [
        "/path/to/poetry/venv/lib/python3.11/site-packages"
    ]
}
```

4. 如果還是無法識別，可以在項目根目錄創建 .vscode/settings.json：
```json
{
    "python.analysis.extraPaths": [
        "${workspaceFolder}/.venv/lib/python3.11/site-packages"
    ],
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

5. 確保 Poetry 配置正確：
```bash
# 查看當前配置
poetry config --list

# 設置虛擬環境在項目目錄下
poetry config virtualenvs.in-project true
```


6. 重新創建虛擬環境：

```bash
# 刪除舊的虛擬環境
poetry env remove python3.11

# 創建新的虛擬環境
poetry env use python3.11

# 安裝依賴
poetry install
```

7. 重啟 VSCode：
- 完全關閉 VSCode
- 重新打開項目
- 檢查 Python 解釋器是否正確設置

8. 如果使用的是 WSL，確保路徑正確：

```bash
{
    "python.defaultInterpreterPath": "\\\\wsl$/Ubuntu/home/user/project/.venv/bin/python"
}
```

9. 檢查 import 是否正常：

```python
from authlib.integrations.flask_oauth2 import current_token
# 如果還是報錯，可以嘗試重新安裝
# poetry add authlib
```

這些步驟應該能解決編輯器的環境問題。如果還有問題，可以：

- 檢查 poetry.lock 文件是否包含 authlib
- 確認虛擬環境中確實安裝了該庫
- 使用 poetry show authlib 查看包信息
