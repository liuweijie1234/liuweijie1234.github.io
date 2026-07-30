---
title: 在 shell 脚本中对 python 传递带有空格的字符串参数
date: 2022-08-10 16:14:00
tags:
- Python
- Shell
categories:
- Python
---

## 发现问题(linux)

linux 机器使用 shell 调用一个 python 脚本，并向 shell 中传入带有空格参数，导致脚本不能实现原有的功能，并报错参数不对

```shell
parameter='IEG straget test' 

python3 xxx.py ${xxx} ${parameter} ${xxx} ${xxx} ${xxx} ${xxx}
```


## 本地复现(windows)

![](/images/20220810_python_script.png)

发现双引号不会导致参数移位

## 解决办法

对于`有空格的变量`加上双引号，如果为了省事，可以全部都加上双引号

```shell
python3 xxx.py ${xxx} "${parameter}" "${xxx}" ${xxx} ${xxx} ${xxx}
```

## argparse 和 Fire 的区别和优缺点

argparse库和Fire库是两种用于处理命令行参数的Python库，它们有不同的特点和适用场景。

### argparse

- 优点：

是Python标准库的一部分，无需额外安装。
功能强大，支持定义命令行参数、子命令、帮助信息等。
提供了丰富的参数类型验证和帮助信息生成功能。

- 缺点：

使用起来相对繁琐，需要编写较多的代码来定义和解析命令行参数。
对于简单的命令行参数处理，可能显得过于复杂。

### Fire

- 优点：

简单易用，无需编写大量代码即可实现命令行参数的处理。
支持将任何Python对象转换为命令行接口，提供了更灵活的使用方式。
自动生成帮助信息，减少了编写文档的工作量。

- 缺点：

功能相对较简单，不如argparse提供的功能丰富。
对于复杂的命令行参数处理，可能需要额外的处理逻辑。

- 参考使用文档:

https://cuiqingcai.com/36050.html

### 区别

argparse是Python标准库中的模块，提供了丰富的功能和灵活性，适用于复杂的命令行参数处理。
Fire是一个由Google开发的库，设计简洁易用，适用于快速创建命令行接口。

根据具体的需求和项目复杂度，可以选择适合的库来处理命令行参数。
如果需要更多的功能和灵活性，可以选择使用argparse库；
如果希望快速实现简单的命令行接口，可以考虑使用Fire库。