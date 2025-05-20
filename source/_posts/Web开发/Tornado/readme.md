tornado异步非阻塞:
什么是异步非阻塞，什么是同步阻塞，select poll epoll网络模型，举例子：育婴室。
强调tornado单线程，由此引出，线程 进程 协程，tornado的异步写法，引出开发人员综合素质问题，
引出原生协程：async和await，怎么使用关键字来实现真正的异步非阻塞特性，再由协程的io多路复用和状态保持与切换引出迭代器和生成器，
点出生成器是python协程的底层实现，再由生成器引出性能问题，生成器对象和list对象的区别（range），由线程可以引申出线程安全问题，
io密集型任务，由tornado+supervisor配合cpu核心起进程来引出cpu密集型任务。

Tornado的异步原理： 
单线程的torndo打开一个IO事件循环， 当碰到IO请求（新链接进来 或者 调用api获取数据），
由于这些IO请求都是非阻塞的IO，都会把这些非阻塞的IO socket 扔到一个socket管理器，
所以，这里单线程的CPU只要发起一个网络IO请求，就不用挂起线程等待IO结果，这个单线程的事件继续循环，接受其他请求或者IO操作，如此循环。


![](/images/tornado.gif)

### IOLoop模块

IOLoop是Tornado的核心，负责服务器的异步非阻塞机制。
IOLoop是一个基于level-triggered的I/O事件循环，它使用I/O多路复用模型(select,poll,epoll)监视每个I/O的事件，当指定的事件发生时调用对用的handler处理。



### IOStream模块

IOStream模块封装了file-like(file or socket)的一系列非阻塞读写操作。
IOStream对file-like的非阻塞读写进行了缓存，提供了读&写Buffer。当读写操作结束时通过callback通知上层调用者从缓存中读写数据。


### HttpServer模块
服务器模块


### Application模块
实现 URI 转发，将 Application 的实例传递给 httpserver ，当监听到请求时，把服务器传回来的请求进行转发，通过调用 call ，处理请求。


### RequestHandeler模块
实现控制器业务的模块



### autoreload模块
实时监测代码修改，也就是debug模式的开关