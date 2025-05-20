---
title: Vue 安装基本命令
date: 2022-08-15 11:42:00
tags:
- Vue
categories:
- Vue
---


## 创建项目




### 使用 create-vue 创建

```bash
#依赖
npm install -g @vue/cli
#创建命令
npm init vue@latest  #最新的 Vue 版本（即目前为止官方发布的最新版本）
# 相当于
npx create-vue@latest

npm init vue@next  #最新的 Vue 版本上个版本
# 相当于
npx create-vue@next

# 直接指定版本
npm init vue@3.7.3


```


```bash
E:\liuweijie1234\request_test_plus> npm init vue@latest
Need to install the following packages:
  create-vue@3.7.3
Ok to proceed? (y) y

Vue.js - The Progressive JavaScript Framework

√ Project name: ... request_test_vue
√ Add TypeScript? ... No / Yes
√ Add JSX Support? ... No / Yes
√ Add Vue Router for Single Page Application development? ... No / Yes
√ Add Pinia for state management? ... No / Yes
√ Add Vitest for Unit Testing? ... No / Yes
√ Add an End-to-End Testing Solution? » No
√ Add ESLint for code quality? ... No / Yes

Scaffolding project in E:\liuweijie1234\request_test_plus\request_test_vue...

Done. Now run:

  cd request_test_vue
  npm install
  npm run dev
```

```bash
E:\liuweijie1234\request_test_plus> npm init vue@next

Need to install the following packages:
  create-vue@3.7.2
Ok to proceed? (y)
```

### 使用 create-vite 创建

```bash
npm create vite@latest
# 相当于
npm init vite@latest
```

[npm create vite@latest 与 npm init vue@latest之间的区别](https://blog.csdn.net/2301_76979068/article/details/131867881)

### 使用 vue-cli 创建

- CL3

```bash
# 查看@vue/cli版本，确保@vue/cli版本在4.5.0以上
vue --version
#依赖
npm install -g @vue/cli
#创建命令
vue create <project-name>
## 启动
cd <project-name>
npm run serve
```

- CL2 （不使用）

```bash
npm install -g @vue/cli-init

vue init vite-app <project-name>
```

## 初始化

cd vue_test/

npm install 

## 运行启动

npm run dev


安装依赖
npm install --save axios vue-axios



https://segmentfault.com/q/1010000010570125