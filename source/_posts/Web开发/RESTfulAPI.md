


## RESTful API 的概念

RESTful API 是一种基于 HTTP 协议的网络应用程序设计风格和开发方式。它以资源为中心，通过统一的接口（如 HTTP 方法 GET、POST、PUT、DELETE 等）对资源进行操作。

## 设计原则


### 资源导向 ：
将系统中的数据和功能抽象为资源，每个资源都有一个唯一的 URI（Uniform Resource Identifier）来标识。例如，/api/users/1 表示用户 ID 为 1 的资源。

### 无状态（Stateless） ：
服务器端不存储客户端请求的上下文信息，每次请求都包含所有必要的信息来完成操作。例如，客户端在每次请求时都需要提供认证信息（如令牌）。

### 统一接口 ：
使用标准的 HTTP 方法（GET 用于获取资源、POST 用于创建资源、PUT 用于更新资源、DELETE 用于删除资源）和 HTTP 状态码来操作资源。
例如，使用 GET /api/books 获取所有书籍，使用 POST /api/books 创建一本新书，使用 PUT /api/books/1 更新 ID 为 1 的书籍信息，使用 DELETE /api/books/1 删除 ID 为 1 的书籍。

### 分层系统 ：
客户端和服务器之间可以有中间层（如代理、缓存等），简化了客户端和服务器的实现。