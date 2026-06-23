新前端系统：(new-freight)(OMP端)
0. 云效拉取new-freight项目,然后使用vscode或者pycharm打开new-freight项目
1. 安装 nvm 
2. 执行 nvm install 22.14.0 安装node环境，
3. 然后输入 nvm use 22.14.0 使用刚才下载的node版本    
tips：必须要安装18以上版本的node环境，否则无法运行vite项目
4. 执行 npm install -g pnpm 安装pnpm
5. 执行 pnpm install 或者yarn install安装node插件依赖
6. 执行 pnpm dev --mode  环境名称  即可运行指定环境的前端    
如 pnpm dev --mode hanjinTest  则运行的是hanjinTest 的环境
pnpm dev --mode developmentHJ