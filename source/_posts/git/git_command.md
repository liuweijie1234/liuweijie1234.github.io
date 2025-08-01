---
title: git 常用命令
date: 2022-08-15 11:42:00
tags:
- git
categories:
- 开发工具
---

[猴子都能懂git](https://backlog.com/git-tutorial/cn/)
[菜鸟教程-git](https://www.runoob.com/git/git-tutorial.html)
[他人博客-git](https://www.yiibai.com/git)


推荐使用可视化软件 SourceTree，可以直观地看到仓库的状态，以及提交记录。

## 安装

### windows 安装

页面下载安装
https://git-scm.com/downloads/win

### ubuntu 安装 git

```bash
sudo apt-get install git -y
```

### macOS 安装 git

```bash
brew install git
```

https://git-scm.com/downloads/mac

### 基本命令

- 查看配置信息


```bash
git config --list  # 查看当前配置, 在当前项目下面查看的配置是全局配置+当前项目的配置, 使用的时候会优先使用当前项目的配置
```

- 用户配置

```bash
# local 局部设置
git config user.name "gitlab's Name"
git config user.email "gitlab@xx.com"
# global 全局设置
git config --global user.name  "xxx"  
git config --global user.email "xxxx@tencent.com"
# SSL 验证
git config --global http.sslVerify false #  关闭 SSL 验证（临时）
git config --global http.sslVerify true  # 恢复 SSL 验证
# 示例
git clone -c http.sslVerify=false https://10.20.1.22:3000/Shenzhen_SD/513-API.git
```

- 代理配置

```bash
# 取消 Git 的全局代理配置
git config --global --unset http.proxy
git config --global --unset https.proxy

# 设置代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```





- 创建仓库命令

`git clone https://github.com/xxxxx/xxxx.git` 克隆远程数据库到本地

`git init` 在现有目录中初始化仓库

- 提交与修改

`git add .` 添加文件到暂存区
`git status` 查看仓库当前的状态，显示有变更的文件。 `git status -s` 只显示有变更的文件。
`git diff` 比较文件的不同，即暂存区和工作区的差异。 `git diff --cached` 比较暂存区和上一次提交之间的差异。
`git commit -m 'demogit'` 提交暂存区到本地仓库。
`git commit --amend -m 'demogit'` 修改上一次提交错误的提交信息。
git commit --amend  # 修改最近一次提交
`git reset` 回退版本
`git rm` 将文件从暂存区和工作区中删除。
`git mv` 移动或重命名工作区文件。

git push --force origin main 强制推送到远程仓库，覆盖远程仓库的内容。

- 忽略文件

.gitignore 文件格式规范如下：

所有空行或者以 ＃ 开头的行都会被 Git 忽略。
可以使用标准的 glob 模式匹配。
匹配模式可以以(/)开头防止递归。
匹配模式可以以(/)结尾指定目录。
要忽略指定模式以外的文件或目录，可以在模式前加上惊叹号(!)取反。

例子：

```txt
# no .a files
*.a

# but do track lib.a, even though you're ignoring .a files above
!lib.a

# only ignore the TODO file in the current directory, not subdir/TODO
/TODO

# ignore all files in the build/ directory
build/

# ignore doc/notes.txt, but not doc/server/arch.txt
doc/*.txt

# ignore all .pdf files in the doc/ directory
doc/**/*.pdf

```


- 提交日志

`git log` 查看历史提交记录
`git blame <file>` 以列表形式查看指定文件的历史修改记录

- 远程操作

`git remote -v`  列出当前仓库中已配置的远程仓库，并显示它们的 URL。
`git remote add <remote_name> <remote_url>` 添加一个新的远程仓库。指定一个远程仓库的名称和 URL，将其添加到当前仓库中。
`git push -u origin master` 将本地分支推到远程数据库 origin 的 master

`git pull origin master:brantest` 将远程主机 origin 的 master 分支拉取过来，与本地的 brantest 分支合并。



创建一个新的版本库

```bash
git clone https://github.com/xxxxx/xxxx.git
cd xxxx
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

现有的文件夹或Git版本库

```bash
cd existing_folder
git init
git remote add origin https://github.com/xxxxx/xxxx.git
git add .
git commit -m "init"
git push -u origin master
```
#### commit 规范

feat - 新功能 feature
fix - 修复 bug
docs - 文档注释
style - 代码格式(不影响代码运行的变动)
refactor - 重构、优化(既不增加新功能，也不是修复bug)
perf - 性能优化
test - 增加测试
chore - 构建过程或辅助工具的变动
revert - 回退
build - 打包




### 分支操作

#### git fetch

git fetch 命令用于从远程获取代码库。

```bash
git fetch --all
git fetch origin master  # 从远程仓库获取最新的 master 分支
```

[git fetch 命令](https://www.yiibai.com/git/git_fetch.html)

#### 查看分支

- 查看本地分支

```bash
$ git branch   # 查看本地分支
  issue1
* master  # 前面有*的就是现在的分支。
```

- 查看远程分支

```bash
git branch -r  # 查看远程分支 ,若无法看到所有分支，则需要使用 git fetch --all 命令
git branch -a  # 查看本地和远程分支
```

#### 创建分支

```bash
git branch <分支名称>  仅创建分支
git branch issue1 创建名为issue1的分支
```

#### 切换分支

```bash
git checkout <分支名称>  # 切换到指定分支
git checkout issue1     # 切换到issue1分支

git checkout -b <branch>  # 创建并切换到指定分支


git switch <branch> 切换到指定分支
git switch -c <branch> 创建并切换到指定分支
```

本地创建并切换到 deploy-test 分支，可以按照以下步骤操作：

拉取远程的 deploy-test 分支并切换到它：

运行以下命令：

```bash
git checkout -b deploy-test origin/deploy-test
```
或者，使用 git switch 命令：

```bash
git switch -c deploy-test origin/deploy-test
```
这两条命令会执行以下操作：

在本地创建一个名为 deploy-test 的新分支。
将它设置为跟踪远程的 origin/deploy-test 分支。
切换到这个新分支。

#### 删除分支

```bash
git branch -D <branchname>   # 删除本地分支
git push origin --delete <branchname>  # 删除远程分支

```

#### 重命名分支

```bash
git branch -m <old_name> <new_name>  # 重命名分支
```
推送到远程仓库（可选）
```bash
git push -u origin lwj_test
```
-u 表示设置上游分支

#### 合并分支

- git merge 命令

```bash
git merge <commit>   # 将指定分支合并到当前分支
```

该命令将指定分支导入到HEAD指定的分支。先切换 master 分支，然后把issue1分支导入到master分支。

`$ git checkout master` 切换到 master 分支

打开myfile.txt档案以确认内容，然后提交。

已经在issue1分支进行了编辑上一页的档案，所以master分支的myfile.txt的内容没有更改。

```bash
$ git merge issue1
Updating 1257027..b2b23c4
Fast-forward
 myfile.txt |    1 +
 1 files changed, 1 insertions(+), 0 deletions(-)
```

- git rebase 命令

git rebase 命令在另一个分支基础之上重新应用，用于把一个分支的修改合并到当前分支。

[git rebase命令](https://www.yiibai.com/git/git_rebase.html)


- git checkout

git checkout 将 lwj-deploy-dev 分支上的特定文件更新到当前的 lwj-deploy-test 分支。

```bash
git checkout lwj-deploy-dev -- path/to/your/file
```

- git cherry-pick

git cherry-pick 命令用于将特定的提交（commit）从一个分支应用到当前分支，而无需合并整个分支的更改。简单来说，它可以把你指定的一个或多个特定提交“挑选”出来，并将它们应用到当前分支。

```bash
git cherry-pick <commit_id>
```

#### 回退版本

[参考 git reset 回退命令](https://www.runoob.com/git/git-reset.html)

```bash
git reset [--soft | --mixed | --hard] [HEAD]
```

`--mixed` 为默认，可以不用带该参数，用于重置暂存区的文件与上一次的提交(commit)保持一致，工作区文件内容保持不变

```bash
git reset  [HEAD] 
```

```bash
$ git reset HEAD^            # 回退所有内容到上一个版本  
$ git reset HEAD^ hello.php  # 回退 hello.php 文件的版本到上一个版本  
$ git reset  052e           # 回退到指定版本
```


`--soft` 参数用于回退到某个版本：

```bash
git reset --soft HEAD
```

```bash
$ git reset --soft HEAD~3   # 回退上上上一个版本 
```

`--hard` 参数撤销工作区中所有未提交的修改内容，将暂存区与工作区都回到上一次版本，并删除之前的所有信息提交：

```bash
git reset --hard HEAD  # 
git reset --hard origin/master  # 回退到远程仓库的最新版本
```

> 注意：谨慎使用 –-hard 参数，它会删除回退点之前的所有信息。

```bash
$ git reset --hard HEAD~3  # 回退上上上一个版本  
$ git reset –hard bae128  # 回退到某个版本回退点之前的所有信息。 
$ git reset --hard origin/dev1  # 将本地的状态回退到和远程的一样
```

HEAD 说明：

- HEAD 表示当前版本
- HEAD^ 上一个版本
- HEAD^^ 上上一个版本
- HEAD^^^ 上上上一个版本
- 以此类推...

可以使用 ～数字表示

- HEAD~0 表示当前版本
- HEAD~1 上一个版本
- HEAD^2 上上一个版本
- HEAD^3 上上上一个版本
- 以此类推...

`git reset HEAD` 命令用于取消已缓存的内容

#### git remote 命令

git remote：列出当前仓库中已配置的远程仓库。
git remote -v：列出当前仓库中已配置的远程仓库，并显示它们的 URL。
git remote add <remote_name> <remote_url>：添加一个新的远程仓库。指定一个远程仓库的名称和 URL，将其添加到当前仓库中。
git remote rename <old_name> <new_name>：将已配置的远程仓库重命名。
git remote remove <remote_name>：从当前仓库中删除指定的远程仓库。
git remote set-url <remote_name> <new_url>：修改指定远程仓库的 URL。
git remote show <remote_name>：显示指定远程仓库的详细信息，包括 URL 和跟踪分支。
git remote prune <remote_name>：删除远程仓库中已经删除的分支。

### 恢复文件

- 若 无add 过的文件恢复

需要用 `git status` 命令查看文件变更信息

```bash
git checkout <file_path>
``` 

- 若 有add ，但无 commit 过 的文件恢复

`git log` 命令查看 commit id

```bash
git checkout <commit_id> -- <file_path>
``` 

- 已经 commit 过的文件恢复

```bash
git checkout <commit_id>^ -- <file_path>
``` 

### git 日志

git log -{n} 显示最近的 n 条提交记录。

git log --oneline 显示提交记录的简短哈希和提交信息。

git log --graph 显示提交记录的 ASCII 图形表示。

git log --decorate 显示各个分支、标签的最新提交。

git log --stat 显示每次提交的变更统计信息。

git log --pretty=oneline 显示提交记录的单行形式。
git log --pretty=format:"%h - %an, %ar : %s" 显示自定义格式的提交记录。
git log --pretty=format:"%h - %an, %ar : %s" --graph 显示提交记录的 ASCII 图形表示。

git log --author="name" 显示指定作者的提交记录。

git log --grep="text" 显示包含指定文本的提交记录。

git log --all 显示所有分支的提交记录。

git log --since="2022-01-01" 显示指定日期之后的提交记录。

git log --after="2022-01-01" 显示指定日期之后的提交记录。

git log --until="2022-01-01" 显示指定日期之前的提交记录。

git log --before="2022-01-01" 显示指定日期之前的提交记录。

git log --reverse 显示提交记录的逆序。

git log --patch 显示每个提交的详细修改内容。

git log --follow 显示文件的历史记录，包括重命名、复制、删除。

git log --abbrev-commit 显示简短的提交哈希值。

git log --abbrev=n 显示简短的提交哈希值。


### git 标签


#### 查看标签

git tag：列出所有标签

git log --oneline ：列出所有标签

git tag -l "v1.0.*" ：列出所有 v1.0 版本的标签

git show <tag_name> ：显示指定标签的详细信息。

#### 创建标签

git tag <tag_name> ：创建轻量标签。

git tag -a <tag_name> -m <标签描述信息> ：创建带有描述信息的标签。

git tag -a <tag_name> -m <标签描述信息> <commit_id> ：创建指定提交的标签。

#### 删除标签

git tag -d <tag_name> ：删除本地标签。

git push origin -d tag <tag1_name> <tagN_name>：删除远程标签。 

#### 推送标签/共享标签

git push origin <tag_name> ：推送本地标签到远程仓库。

git push origin --tags ：推送所有本地标签到远程仓库。


### git 报错及处理


#### git 警告

- 文件格式不一致

```bash
$ git add .
warning: LF will be replaced by CRLF in static/survey/css/select2.min.css.
The file will have its original line endings in your working directory
warning: LF will be replaced by CRLF in static/survey/js/jquery.min.js.
The file will have its original line endings in your working directory
warning: LF will be replaced by CRLF in static/survey/js/select2.min.js.
The file will have its original line endings in your working directory
```

- Git报错： Failed to connect to github.com port 443 解决方案

https://blog.csdn.net/zpf1813763637/article/details/128340109


git config --global http.proxy 127.0.0.1:7897
git config --global https.proxy 127.0.0.1:7897

- Git报错：SSL certificate problem: self signed certificate

```bash
ldmac@ldmac2deMacBook-Pro Projects % git clone https://39.129.90.146:29923/Shenzhen_SD/513-API.git
Cloning into '513-API'...
fatal: unable to access 'https://39.129.90.146:29923/Shenzhen_SD/513-API.git/': SSL certificate problem: self signed certificate
```
1、临时禁用SSL验证

git clone -c http.sslVerify=false https://39.129.90.146:29923/Shenzhen_SD/513-API.git

2、全局禁用SSL验证

git config --global http.sslVerify false

### 提交冲突

error: Your local changes to the following files would be overwritten by merge:
        apps/order/tasks.py
Please commit your changes or stash them before you merge.
Aborting
Merge with strategy ort failed.


方法一：保存本地修改

```bash
# 暂存修改（创建临时存档点）
git stash

# 拉取远程更新
git pull origin test

# 恢复暂存的修改（自动尝试合并）
git stash pop
```

如果恢复后文件出现 <<<<<<< 冲突标记，需要手动编辑文件解决冲突

解决后执行 git add <文件> 和 git commit