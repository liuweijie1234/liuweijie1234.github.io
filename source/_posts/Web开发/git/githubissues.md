---
title: github issues 管理
date: 2022-08-15 14:47:00
tags:
- github
categories:
- 开发工具
---


## 一、背景及需求

当公司的开源项目比较多，公司需要一个 label 系统来管理 issues。

若开源项目人气高，也会有外部开发者的参与建设

## 二、思考

1、怎样才能达到最好 管理 issue 效果 (完善的 label)
2、怎样让用户提出高质量的 issue （个人想法是 通过 issue 模板）

## 三、个人思路

### 3.1 创建 Label 分组

在 label 分组上，除了项目进度和功能优先级的标识，还需要有适用于外部开发者的 label，以及项目组回应 label。

ps: 不确定标签是要 全英文、全中文 还是 中英文


- 具体 label

分类 | 具体 label |
---|--------|
功能分类 | 新功能(new function)，功能增强(function enhancement)，漏洞缺陷(BUG)，文档改进(Documentation improvements)，用法疑问(Usage Questions) | 
外部 label | 第三方开发(third-party dev) | 
项目组回复 | 项目组:需求 get(get requirement)，项目组:已加入计划(join plan)，项目组:忽略此需求(neglect requirement) | 
优先级 | 优先级:低(low priority)，优先级:高(high priority)，优先级:紧急(urgent priority) |
项目进度 | 开发中(in dev)，测试中(testing)，已上线(online) | 

- 新建 label


![](/images/image2022-7-14_10-46-41.png)

![](/images/image2022-7-14_10-47-6.png)


### 3.2 配置 Issues 模板

普通用户提 issue 是不能选择 label，所以可以根据 issue 模板绑定 label 来解决最初的接入

[https://docs.github.com/cn/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository](https://docs.github.com/cn/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)

- BUG 模板例子

```markdown

<--创建 Issues 时需要检查已经存在的 Issues 列表中是否有类似的问题，如果有则不需要重新创建新的 Issue，请在已有的 Issue 下加入讨论，详细描述您出现的问题，Issue 的状态更改后会收到邮件通知。-->

<--Whether there is a similar problem in the existing problem when creating the problem, there is no need to create a new problem, if you need to check the description of the existing problem and add it to the list, detail the problem you have, and the status of the problem will be changed. to email notification-->

**发生了什么(What happened)**:

**你希望发生什么事情(What you expected to happen)**:

**如何复现这个问题,尽可能描述下相关信息(How to reproduce it ,as minimally and precisely as possible)**:

**还有什么需要让我们了解的(Anything else we need to know?)**:

```

- 配置模板

步骤一：找到配置 issues 模板入口


![](/images/image2022-7-14_11-17-47.png)

![](/images/image2022-7-14_11-18-10.png)

步骤二：新增模板

![](/images/image2022-7-14_11-18-31.png)

步骤三：编辑模板，将模板标题、关于、内容、标题前缀、标签 填写完成

![](/images/image2022-7-14_11-19-8.png)

![](/images/image2022-7-14_11-22-24.png)

步骤四：提交 commit changes

![](/images/image2022-7-14_11-38-5.png)

步骤五：验证

![](/images/image2022-7-14_11-35-15.png)


## 四、看板


### 4.1 单产品看板

通过 github 的 projects 来实现单个仓库的看板

[https://docs.github.com/cn/issues/trying-out-the-new-projects-experience](https://docs.github.com/cn/issues/trying-out-the-new-projects-experience)

![](/images/image2022-7-14_10-50-6.png)

### 4.2 多产品看板

需要开发将数据存入数据库，然后在展示

# github 接口调用说明

[参考官方文档](https://docs.github.com/cn/rest/overview/resources-in-the-rest-api#authentication)

- url
```bash
https://api.github.com
```

[一篇文章搞定 Github API 调用 (v3）](https://segmentfault.com/a/1190000015144126)