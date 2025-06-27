

Flask 教程-菜鸟教程
https://www.runoob.com/flask/flask-tutorial.html



## 启动 API 服务

flask run --host 0.0.0.0 --port=5001 --debug


## 启动 Worker 服务

用于消费异步队列任务，如知识库文件导入、更新知识库文档等异步操作。 Linux / MacOS 启动：

celery -A app.celery worker -P gevent -c 1 -Q dataset,generation,mail,ops_trace --loglevel INFO

如果使用 Windows 系统启动，请替换为该命令：

celery -A app.celery worker -P solo --without-gossip --without-mingle -Q dataset,generation,

## 数据库迁移命令


flask db stamp base # 删除所有迁移记录

flask db init # 重新初始化迁移


flask db downgrade d07474999927 # 回滚到指定版本

flask db upgrade d3f6769a94a3  # 升级指定版本

flask db stamp d3f6769a94a3  # 标记起始版本

flask db upgrade head  # 升级到最新

flask db history  # 检查迁移历史
flask db current  # 查看当前状态版本

flask db migrate -m "add account field to source"

flask db upgrade # 应用迁移


### 路由和视图函数的绑定

 Flask 中，使用 @app.route() 装饰器来绑定路由和视图函数
 
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the homepage!'

@app.route('/about')
def about():
    return 'About page'

if __name__ == '__main__':
    app.run()
```


### 实现用户认证

#### 登录和会话管理 ：

可以使用 Flask - Login 扩展来实现用户认证。首先，安装 Flask - Login：
```bash
pip install flask-login
```

```python
from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于保持会话安全

login_manager = LoginManager()
login_manager.init_app(app)

# 用户类
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 这里应该进行实际的用户验证逻辑
        # 假设验证通过
        user = User(id=username)
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

# 需要登录才能访问的路由
@app.route('/home')
@login_required
def home():
    return 'Welcome to the home page'

# 登出路由
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```
在这个例子中，用户登录时，通过 login_user() 函数将用户登录状态保存到会话中。
@login_required 装饰器用于保护需要用户登录的路由。
logout_user() 函数用于处理用户登出。


#### 会话管理：

Flask 使用会话（Session）来存储用户的相关信息，默认情况下会话数据存储在客户端的 cookie 中。
可以通过 session 对象来访问和修改会话数据。例如：
```python
from flask import session

@app.route('/set_session')
def set_session():
    session['user_name'] = 'John'
    return 'Session set'

@app.route('/get_session')
def get_session():
    user_name = session.get('user_name')
    return f'User name: {user_name}'
```
在这个例子中，set_session() 函数设置了一个名为 user_name 的会话变量，get_session() 函数读取并返回该变量的值。