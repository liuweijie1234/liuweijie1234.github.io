---
title: Python3 模块 os
date: 2022-08-15 10:22:00
tags:
- Python module
- os
categories:
- Python
---

## os
os 模块，用于提供系统级别的操作

os.getcwd()         获取当前工作目录，即当前 python 脚本工作的目录路径
os.chdir("dirname") 改变当前脚本工作目录；相当于 shell 下 cd
os.curdir           返回当前目录：('.')
os.pardir           获取当前目录的父目录字符串名：('..')
os.removedir("dirname") 若目录为空，则删除，并递归到上一级目录，如若也为空，则删除，一次类推
os.mkdir('dirname') 生成单级目录；相当于 shell 中 mkdir dirname
os.rmdir('dirname') 删除单级空目录，若目录不为空则无法删除，报错；相当于 shell 中 rmdir dirname
os.remove()         删除一个文件
os.rename("oldname","newname") 重命名文件/目录
os.sep              输出操作系统特定的路径分隔符，win 下为"`\\`",Linux 下为"/"
os.linesep          输出当前平台使用的行终止符，win 下为"`\t\n`"，Linux 下为"`\n`"


## os.path



- os.path.exists()
    判断 文件夹\文件 是否存在


打开文件




删除文件

```bash
import os

# 指定要删除的文件路径
file_path = "path/to/file.txt"

try:
    # 删除文件
    os.remove(file_path)
    print("文件删除成功！")
except FileNotFoundError:
    print("文件未找到！")
except PermissionError:
    print("没有权限删除文件！")
except Exception as e:
    print(f"文件删除失败：{str(e)}")
```
