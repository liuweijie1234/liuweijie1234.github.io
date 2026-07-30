requests_go 是一个支持 tls 指纹修改（如ja3）和 http2 的 http 请求库，它基于 requests（python 版） (opens new window)和 requests（go 版） (opens new window)，使用 requests 做为上层请求参数处理库，requests（go版）作为底层进行网络请求。
requests_go 使用方法跟 requests 一模一样，与之唯一不同的就是多了一个 tls_config 参数，此参数是用于修改 tls 指纹信息的。



https://spiderapi.cn/net/requests_go/