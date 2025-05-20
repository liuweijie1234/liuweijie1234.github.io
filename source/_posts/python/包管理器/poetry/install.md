
## 安装

pipx 安装
https://pipx.pypa.io/stable/installation/

pipx install poetry==1.8.4


https://python-poetry.org/docs/

windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -


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
