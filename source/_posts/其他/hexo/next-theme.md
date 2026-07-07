---
title: hexo next-theme 配置
date: 2022-07-03 16:44:15
tags: 
- hexo
- next
categories: hexo
---
## next-theme 配置


根目录下的 `_config.yml`，简称【站点配置文件】，例 `liuweijie1234.github.io\_config.yml`
主题下的 `_config.yml`，简称【主题配置文件】，例 `liuweijie1234.github.io\themes\next-theme\_config.yml`

[主题代码](https://github.com/next-theme/hexo-theme-next)
[主题官方文档](https://theme-next.js.org/)

## 站点配置

### 主题配置

站点配置文件的主题配置，配置项 `theme`

```yaml
# Extensions
## Plugins: https://hexo.io/plugins/
## Themes: https://hexo.io/themes/
# git clone https://github.com/next-theme/hexo-theme-next themes/next-theme
theme: next-theme
# theme_config: 
```

### 基本配置

```yaml
# Site/网站
title: 刘伟杰的个人博客
subtitle: ''
description: '刘伟杰的个人博客'
keywords: 个人博客
author: liuweijie1234
language: zh-CN
timezone: Asia/Shanghai
```

### 网址/URL 配置

```yaml
# URL
## Set your site url here. For example, if you use GitHub Page, set url as 'https://username.github.io/project'
url: http://liuweijie1234.github.io
permalink: :title/
permalink_defaults:
pretty_urls:
  trailing_index: true # Set to false to remove trailing 'index.html' from permalinks
  trailing_html: true # Set to false to remove trailing '.html' from permalinks
```

### 部署配置

```yaml
# Deployment/部署
## Docs: https://hexo.io/docs/one-command-deployment
deploy:
  type: git
  repo: https://github.com/liuweijie1234/liuweijie1234.github.io
  branch: main
  token: xxxxxxxxxxxxxxxxxxxxxx
  name: liuweijie1234
```

## 主题配置

### 选择布局方案

修改 Next 主题配置文件，配置项 `scheme`

ps: 这两个方案对个人来说，感觉挺不错的

```yaml
# Scheme Settings
scheme: Pisces
# scheme: Gemini
```
### 菜单配置

- 修改 Next 主题配置文件 ，配置项 `menu`
```yaml
menu:
  home: / || fa fa-home
  about: /about/ || fa fa-user
  tags: /tags/ || fa fa-tags
  categories: /categories/ || fa fa-th
  archives: /archives/ || fa fa-archive
  # schedule: /schedule/ || fa fa-calendar
  # sitemap: /sitemap.xml || fa fa-sitemap
  # commonweal: /404/ || fa fa-heartbeat
```

- 新建相关页面
```bash
hexo new page "about"
hexo new page "tags"
hexo new page "categories"
hexo new page "archives"
```

- 页面顶部配置
source\about\index.md
```text
---
title: 关于我
date: 2022-06-28 16:35:11
type: "about"
comments: false
---
```

source\tags\index.md
```text
---
title: 标签页
date: 2022-06-28 16:35:22
type: "tags"
comments: false
---
```

source\categories\index.md
```text
---
title: 分类页
date: 2022-06-28 16:35:31
type: "categories"
comments: false
---
```

source\archives\index.md
```text
---
title: archives
date: 2022-06-28 16:35:49
type: "archives"
---
```

### 配置头像

修改 Next 主题配置文件 ，配置项 `avatar`

```yaml
# Sidebar Avatar
avatar:
  # Replace the default image and set the url here.
  url: /images/QQ头像.jpg
  # If true, the avatar will be displayed in circle.
  rounded: false
  # If true, the avatar will be rotated with the cursor.
  rotated: false
```
[官方文档：配置头像](https://theme-next.js.org/docs/theme-settings/sidebar.html#Configuring-Avatar)

### 侧边栏社交链接

```yaml
# Social Links
# Usage: `Key: permalink || icon`
# Key is the link label showing to end users.
# Value before `||` delimiter is the target permalink, value after `||` delimiter is the name of Font Awesome icon.
social:
  GitHub: https://github.com/liuweijie1234 || fab fa-github
  E-Mail: mailto:2496234829@qq.com || fa fa-envelope
  #Weibo: https://weibo.com/yourname || fab fa-weibo
  #Google: https://plus.google.com/yourname || fab fa-google
  #Twitter: https://twitter.com/yourname || fab fa-twitter
  #FB Page: https://www.facebook.com/yourname || fab fa-facebook
  #StackOverflow: https://stackoverflow.com/yourname || fab fa-stack-overflow
  #YouTube: https://youtube.com/yourname || fab fa-youtube
  #Instagram: https://instagram.com/yourname || fab fa-instagram
  #Skype: skype:yourname?call|chat || fab fa-skype
```

[官方文档：侧边栏社交链接](https://theme-next.js.org/docs/theme-settings/sidebar.html#Sidebar-Social-Links)

### 本地搜索

启用 `hexo-generator-searchdb` ，[参考 Github 链接](https://github.com/next-theme/hexo-generator-searchdb)

- 安装

```bash
npm install hexo-generator-searchdb
```

- 配置

```yaml
# 站点配置文件新增
search:
  path: search.xml
  field: post
  content: true
  format: html
```

```yaml
# 主题配置文件修改
local_search:
  enable: true
  # If auto, trigger search by changing input.
  # If manual, trigger search by pressing enter key or search button.
  trigger: auto
  # Show top n results per article, show all results by setting to -1
  top_n_per_article: 1
  # Unescape html strings to the readable one.
  unescape: false
  # Preload the search data when the page loads.
  preload: false
```

### 网页音乐

- 登陆网页版网易云音乐，然后找到自己喜欢的歌，点击歌曲下面的「生成外链播放器」
- 修改 next 主题下 `iuweijie1234.github.io\themes\next-theme\layout\_macro\sidebar.njk` 文件，在`<div class="sidebar-inner">`中添加

```html
    <div id="music">
        <iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=1394963332&auto=1&height=66"></iframe>
    </div>
```

### 右上角增加 GitHub

修改 Next 主题配置文件，配置项 `github_banner`
```yaml
# `Follow me on GitHub` banner in the top-right corner.
github_banner:
  enable: true
  permalink: https://github.com/liuweijie1234
  title: Follow me on GitHub
```

### 黑暗模式

[参考 hexo-next-darkmode github 链接](https://github.com/rqh656418510/hexo-next-darkmode)

- 安装

```bash
npm install hexo-next-darkmode --save
```
- 配置

修改 Next 主题配置文件
```yaml
# Dark Mode
darkmode: false
```
```yaml
darkmode_js:
  enable: true
  bottom: '64px' # default: '32px'
  right: 'unset' # default: '32px'
  left: '32px' # default: 'unset'
  time: '0.5s' # default: '0.3s'
  mixColor: 'transparent' # default: '#fff'
  backgroundColor: 'transparent' # default: '#fff'
  buttonColorDark: '#100f2c' # default: '#100f2c'
  buttonColorLight: '#fff' # default: '#fff'
  isActivated: false # 默认激活暗模式
  saveInCookies: true # default: true
  label: '🌓' # default: ''
  autoMatchOsTheme: true # default: true
  libUrl: # Set custom library cdn url for Darkmode.js
```

### 返回顶部

修改 Next 主题配置文件 ，配置项 `back2top`

```yaml
back2top:
  enable: true
  # Back to top in sidebar.
  sidebar: false
  # Scroll percent label in b2t button.
  scrollpercent: true
```

### 增加文章结束语

修改 next 主题文件夹下的 `layout\_macro\post.njk` 文件，在文章结束 END POST BODY 位置增加

```html
<div>
    {% if not is_index %}
        <div style="text-align:center;color: #ccc;font-size:14px;">
            ------------- 本文结束 <i class="fa fa-heart-o"></i> 感谢您的阅读-------------
     </div>
    {% endif %}
</div>
```


### 计数工具：阅读次数/浏览量/访客数

主题已集成[不蒜子站点访客、文章阅读量](http://ibruce.info/2015/04/04/busuanzi/)

修改 Next 主题配置文件，配置项 `busuanzi_count`


```yaml
busuanzi_count:
  enable: true
  total_visitors: true
  total_visitors_icon: fa fa-user
  total_views: true
  total_views_icon: fa fa-eye
  post_views: true
  post_views_icon: far fa-eye
```
ps: 个人喜欢这个服务，如果不喜欢可以使用其他的，可以参考[计数工具](https://theme-next.js.org/docs/third-party-services/statistics-and-analytics.html#Counting-Tools)、[hexo-leancloud-counter-security](https://github.com/theme-next/hexo-leancloud-counter-security)

ps： leancloud 我一直就没弄好过，有人弄好，可以 call 我

### 字数统计/阅读时间

启用 `hexo-symbols-count-time` ，[参考 Github 链接](https://github.com/theme-next/hexo-symbols-count-time)

类似 `hexo-word-counter`,[参考 Github 链接](https://github.com/next-theme/hexo-word-counter)

- 安装

```bash
npm install hexo-symbols-count-time
```

- 配置

```yaml
# 站点配置文件新增
symbols_count_time:
  symbols: true                # 文章字数统计
  time: true                   # 文章阅读时长
  total_symbols: true          # 站点总字数统计
  total_time: true             # 站点总阅读时长
  exclude_codeblock: false     # 排除代码字数统计
```

```yaml
# 主题配置文件修改
symbols_count_time:
  separated_meta: true
  item_text_total: true
  symbols: true
  time: true
  total_symbols: true
  total_time: true
  exclude_codeblock: false
  awl: 4
  wpm: 275
  suffix: "mins."
```

- 中文翻译

在`liuweijie1234.github.io\themes\next-theme\languages\zh-CN.yml`中加入
```yaml
post:
  views: 阅读次数
symbols_count_time:
  time: 阅读时长
  count: 本文字数
  count_total: 站点总字数
  time_total: 站点阅读时长
```

[字数统计 参考](https://juejin.cn/post/7000547315756826638) 

### 评论系统

[官方文档：评论系统](https://theme-next.js.org/docs/third-party-services/comments)

ps: 这个我也没弄好...


#### 关闭评论

文章顶部添加

```md
comments: false
```

[本文参考](https://www.mdnice.com/writing/382af676baff4ed4ad5511074fb736da)

其他优化可以参考大佬的文章 
[https://yuumiy.github.io/posts/2789.html](https://yuumiy.github.io/posts/2789.html)
[https://blog.csdn.net/awt_fudonglai/category_10191857.html?spm=1001.2014.3001.5482](https://blog.csdn.net/awt_fudonglai/category_10191857.html?spm=1001.2014.3001.5482)
[https://blog.csdn.net/tuckEnough/article/details/107383201](https://blog.csdn.net/tuckEnough/article/details/107383201)
