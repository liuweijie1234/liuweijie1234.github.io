---
title: Prometheus windows 安装
date: 2024-03-18 09:00:00
tags:
- Prometheus
categories:
- [Prometheus]
---

## 文档

https://prometheus.io/docs/introduction/overview/

Prometheus+Grafana环境搭建（window）https://blog.csdn.net/qq_41316955/article/details/131078463
Windows下Grafana+Promethus+node_export监控Windows系统资源详细教程(我没装go) https://blog.csdn.net/qq_14945475/article/details/120062779
生产环境安装配置Prometheus+Grafana（windows版）https://blog.csdn.net/csdn_chenhao/article/details/128034399
Prometheus(普罗米修斯)部署方案 https://www.bilibili.com/read/cv22077599/
---

prometheus之自动发现自动注册（consul）https://blog.csdn.net/qq_25934401/article/details/127450266

## 安装

### 下载安装包

https://prometheus.io/download/
https://github.com/prometheus/prometheus/releases

找到对应的windows版本的安装包下载，本文以下载 prometheus-2.51.0-rc.0.windows-amd64.zip

解压到指定目录，例如：`D:\prometheus`


### 下载采集器并配置

下载 windows_exporter 采集器
https://github.com/prometheus-community/windows_exporter/releases

其他系统采集器：https://prometheus.io/download/#node_exporter

- 推荐下载 `windows_exporter-0.25.1-amd64.msi`
1、下载完成后以管理员身份运行
2、默认安装到 `C:\Program Files\windows_exporter` 目录下。
3、安装成功后，会自动创建文件夹 `C:\Program Files\windows_exporter\textfile_inputs`,并将 windows_exporter.exe 放入该文件夹，自动创建服务 widows_exporter，并启动。
4、将服务状态改为“自动（延迟启动）”
5、采集服务默认端口为9182，可通过浏览器访问`http://localhost:9182/`,查看采集到的指标等信息。

- 若下载 `windows_exporter-0.25.1-amd64.exe`，
1、下载完成后，将需要手动创建文件夹 `C:\Program Files\windows_exporter` 并将 windows_exporter.exe 放入该文件夹，
2、在windows_exporter 文件夹下还需要手动创建 textfile_inputs 文件夹。
（避免错误 level=error msg="Error reading textfile collector directory \"C:\\\\Program Files\\\\windows_exporter\\\\textfile_inputs\": open C:\\Program Files\\windows_exporter\\textfile_inputs: The system cannot find the file specified." source="textfile.go:222）
3、需要手动创建服务
```bash
sc create windows_exporter binpath= "C:\Program Files\windows_exporter\windows_exporter-0.25.1-amd64.exe" type= own start= auto displayname= windows_exporter
```
其他参数
```bash
"C:\Program Files\windows_exporter\windows_exporter.exe" --log.file eventlog  --web.listen-address 0.0.0.0:9182
```

4、启动服务。
```bash
sc start windows_exporter
```
5、采集服务默认端口为9182，可通过浏览器访问`http://localhost:9182/`,查看采集到的指标等信息。


Prometheus 监控Windows机器 https://www.cnblogs.com/gered/p/13523379.html


wmi_export 参数解析 https://blog.csdn.net/qq_38311845/article/details/105279963

## Prometheus 注册服务并启动

默认端口9090

手动执行exe文件

双击prometheus.exe启动prometheus，任务栏会新增一个黑窗口（不要关闭），但是这个不是后台服务，不能随着系统关闭而关闭，需要手动关闭。


推荐 nssm 注册服务

下载 nssm https://nssm.cc/download

解压到指定目录，例如：`D:\nssm`

> 推荐：将 nssm 路径添加到环境变量中，方便使用。

```bash
nssm install prometheus
```

![](/images/微信图片_20240319193843.png)

注意：

Application 
path：就是选择你 exe 文件的路径。例如：`D:\prometheus\prometheus.exe`

Startup directory：会自动加载exe所对应目录，不需改动

Service name ：自定义服务名称，可在服务列表找到。

Arguments：启动参数，默认即可。

**prometheus 启动参数**有：

可通过 -h 查看帮助信息。

配置文件路径：
```bash 
--config.file=D:\prometheus\prometheus.yml
```
指定端口启动：
```bash
--web.listen-address=127.0.0.1:9090
```
指定数据存储路径：
```bash        
--storage.tsdb.path=D:\prometheus\data
```


![](/images/微信截图_20240319194108.png)


![](/images/微信截图_20240319194248.png)

命令行启动服务
```bash
nssm start prometheus
```
或者手动启动服务


启动成功后，访问 prometheus 本地地址 http://localhost:9090/

![](/images/微信截图_20240319200900.png)

进入Prometheus后台：

点击 Status --> Targets (http://localhost:9090/targets)便可以找到对应的节点信息

![](/images/微信截图_20240319200939.png)

## 配置文件


配置文件 `prometheus.yml` 示例：

```yaml
# 全局配置
global:
  scrape_interval:     15s # 数据拉取间隔: 将抓取间隔设置为每 15 秒一次。 默认为每 1 分钟一次。
  evaluation_interval: 15s # 报警规则拉取间隔: 每 15 秒评估一次规则。 默认为每 1 分钟一次。
  # scrape_timeout 单次数据拉取超时, 设置为全局默认值（10 秒）。当报context deadline exceeded错误时需要在特定的job下配置该字段。

# 告警插件配置
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093 # 单实例配置,等同于 targets: ['127.0.0.1:9093']
      #- targets: ['172.31.10.167:19093','172.31.10.167:29093','172.31.10.167:39093'] # 集群配置


# 告警规则, 加载规则一次并根据全局“evaluation_interval”定期评估它们。
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"


# 采集配置，配置数据源，包含分组job_name以及具体target。又分为静态配置和服务发现
scrape_configs:
  # 作业名称作为标签“job=<job_name>”添加到从此配置中抓取的任何时间序列中。
  # job_name 需要监控的对象名称
  - job_name: 'prometheus'
    # metrics_path 默认为“/metrics”
    # 方案默认为“http”。
    static_configs:
    # targets 对应需要监控的地址端口
    - targets: ['localhost:9090']

  - job_name: 'windows_exporter'
    static_configs:
    - targets: ['localhost:9182']
    - targets: ['localhost:8080']
```

Prometheus配置文件详解https://www.jianshu.com/p/872bafe8d85e

Prometheus 监控Linux Windows主机 https://cloud.tencent.com/developer/article/2221574

## Grafana 对接 Prometheus

### Grafana 安装

Grafana 下载地址：https://grafana.com/grafana/download

![](/images/微信截图_20240319203756.png)

推荐下载 grafana-enterprise-10.4.0.windows-amd64.msi ，一键安装，自动注册服务Grafana。

默认url是http://localhost:3000/，默认用户名密码是admin/admin。

Grafana 安装配置文档：https://grafana.com/docs/grafana/latest/installation/windows/ 

### 导入 Prometheus 数据源

Grafana 导入 Prometheus 数据源：
https://grafana.com/docs/grafana/latest/datasources/add-a-data-source/

Home -> Connections -> Data sources

![](/images/微信截图_20240320101234.png)

填写好 Name 和 Prometheus server URL，点击 Save & Test。

![](/images/微信截图_20240320101622.png)


### 导入 Prometheus 模板

Grafana 导入 Prometheus 模板：
https://grafana.com/grafana/dashboards/?dataSource=prometheus

Grafana 导入 Prometheus window Exporter模板：

https://grafana.com/grafana/dashboards/10467-windows-exporter-for-prometheus-dashboard-cn-v20230531/


Copy ID to clipboard

![](/images/微信截图_20240320103645.png)

进入导入模板页面

![](/images/微信截图_20240320104212.png)

将复制的仪表盘模板ID粘贴到输入框中，点击 Load

![](/images/微信截图_20240320104341.png)

选择自己的 Prometheus 数据源，点击 Import

![](/images/微信截图_20240320105220.png)

基本仪表盘就导入成功了。

![](/images/微信截图_20240320104532.png)




一台grafana监控多台Windows server的操作配置 https://blog.csdn.net/Nightwish5/article/details/118224088




### Prometheus启动参数配置及释义

```bash
-h, --[no-]help             显示上下文相关的帮助（也可以尝试--help-long 和 --help-man)。
--[no-]version              显示应用程序版本。
--config.file="prometheus.yml"  启动时，指定 Prometheus 读取配置文件的路径。
--web.listen-address="0.0.0.0:9090"  用于侦听 UI、API 和遥测的地址。
--auto-gomemlimit.ratio=0.9  保留的 GOMEMLIMIT 内存与检测到最大容器或系统内存
--web.config.file=""        [实验] 可以启用 TLS 或身份验证的配置文件的路径。
--web.read-timeout=5m       页面读取请求最大超时时间。
--web.max-connections=512   同时访问Prometheus页面的最大连接数。
--web.external-url=<URL>    Prometheus 对外的 URL可到达（例如，如果 Prometheus 通过反向代理提供服务）。
                            用于生成一个相对和绝对链接返回 Prometheus 本身。
                            如果 URL 有路径部分，它将用于 Prometheus 所有 HTTP 端点的前缀。
                            如果省略，则相关 URL 组件会自动派生。
--web.route-prefix=<path>   Web 端点内部路由的前缀。默认为 --web.external-url 的路径。
--web.user-assets=<path>    静态资源路径，位于 /user 下。
--[no-]web.enable-lifecycle 通过 HTTP 请求启用关闭和重新加载。
--[no-]web.enable-admin-api 启用管理控制操作的 api 端点。
--[no-]web.enable-remote-write-receiver  启用 API 端点接受远程写入请求。
--web.console.templates="consoles"  到控制台模板目录的路径，位于 /consoles 下。
--web.console.libraries="console_libraries"  控制台库目录的路径。
--web.page-title="Prometheus Time Series Collection and Processing Server"  Prometheus 实例的文档标题。
--web.cors.origin=".*"      CORS 起源的正则表达式。 它已完全锚定。
                            示例：'https?://(domain1|domain2)\.com'
--storage.tsdb.path="data/"  指标存储的基本路径。 仅与服务器模式一起使用。

--storage.tsdb.retention=STORAGE.TSDB.RETENTION  [已弃用] 存储采样的保存时间。 该标志已被弃用，请改用“storage.tsdb.retention.time”。 仅与服务器模式一起使用。
                            
--storage.tsdb.retention.time=STORAGE.TSDB.RETENTION.TIME  存储采样的保存时间。 
                                                           当设置此标志时，它将覆盖“storage.tsdb.retention”。 
                                                           如果此标志、“storage.tsdb.retention”和“storage.tsdb.retention.size”均未设置，则保留时间默认为 15 天。 
                                                           支持的单位：y、w、d、h、m、s、ms。 
                                                           仅与服务器模式一起使用。
                            
--storage.tsdb.retention.size=STORAGE.TSDB.RETENTION.SIZE  块可以存储的最大字节数。 
                                                           单位为必填项，支持的单位：B、KB、MB、GB、TB、PB、EB。 
                                                           例如：“512MB”。 基于2的幂，所以1KB就是1024B。 
                                                           仅与服务器模式一起使用。
--[no-]storage.tsdb.no-lockfile 不要在数据目录中创建锁定文件。仅与服务器模式一起使用。
--storage.tsdb.head-chunks-write-queue-size=0  将头块写入要进行 m 映射的磁盘的队列大小，0 完全禁用队列。 实验性的。仅与服务器模式一起使用。
--storage.agent.path="data-agent/"  指标存储的基本路径。仅与代理模式一起使用。
--[no-]storage.agent.wal-compression 压缩代理 WAL。 仅与代理模式一起使用。
--storage.agent.retention.min-time=STORAGE.AGENT.RETENTION.MIN-TIME
--storage.agent.retention.max-time=STORAGE.AGENT.RETENTION.MAX-TIME  当 WAL 被截断时，最小年龄样本可能会在被考虑删除之前。仅与代理模式一起使用。
--[no-]storage.agent.no-lockfile  不要在数据目录中创建锁定文件。仅与代理模式一起使用。
--storage.remote.flush-deadline=<duration>  关闭或重新加载配置时等待刷新示例的时间。
--storage.remote.read-sample-limit=5e7 在单个查询中通过远程读取接口返回的最大样本总数。0 表示没有限制。 对于流式响应类型，此限制将被忽略。仅与服务器模式一起使用。
--storage.remote.read-concurrent-limit=10  并发远程读取调用的最大数量。 0 表示没有限制。仅与服务器模式一起使用。
--storage.remote.read-max-bytes-in-frame=1048576
                            在编组之前流式传输远程读取响应类型的单帧中的最大字节数。 
                            请注意，客户端也可能对帧大小有限制。 默认情况下 protobuf 建议 1MB。
                            仅与服务器模式一起使用。
--rules.alert.for-outage-tolerance=1h  恢复“for”警报状态时允许普罗米修斯中断的最大时间。仅与服务器模式一起使用。
--rules.alert.for-grace-period=10m  警报和恢复“for”状态之间的最短持续时间。 仅针对配置的“for”时间大于宽限期的警报保留此设置。仅与服务器模式一起使用。
--rules.alert.resend-delay=1m  向 Alertmanager 重新发送警报之前等待的最短时间。仅与服务器模式一起使用。
--rules.max-concurrent-evals=4  可同时运行的独立规则的全局并发限制。仅与服务器模式一起使用。
--alertmanager.notification-queue-capacity=10000  等待报警通知队列的大小。仅与服务器模式一起使用。
--query.lookback-delta=5m  在表达式求值和联合期间检索指标的最大回溯持续时间。仅与服务器模式一起使用。
--query.timeout=2m         一个查询在终止之前可以执行的最长时间(如果超过2min，就会自动kill掉) 仅与服务器模式一起使用。
--query.max-samples=50000000  单个查询可以加载到内存中的最大样本数。 
                              请注意，如果尝试加载比这更多的样本，查询将会失败到内存中，因此这也限制了查询可以返回的样本数量。
                              仅与服务器模式一起使用。
--enable-feature= ...      要启用的以逗号分隔的功能名称。有效选项： 
                            agent, auto-gomemlimit, exemplar-storage, expand-external-labels, 
                            memory-snapshot-on-shutdown, promql-at-modifier, promql-negative-offset, 
                            promql-per-step-stats, promql-experimental-functions, remote-write-receiver (DEPRECATED),
                            extra-scrape-metrics, new-service-discovery-manager, auto-gomaxprocs, 
                            no-default-scrape-port, native-histograms, otlp-write-receiver. 
                            参考 https://prometheus.io/docs/prometheus/latest/feature_flags/
--log.level=info           开启打印日志级别(debug,info,warn,error,fatal)。默认为info。
--log.format=logfmt        日志消息的输出格式。 其中之一：[logfmt,json]
```


curl -X POST http://localhost:9090/-/reload 重新加载配置文件,需要开启配置文件中的 web.enable-lifecycle



详细学习资料 https://yunlzheng.gitbook.io/prometheus-book




部署 influxdb, 持久化 prometheus metrics 存储， influxdb学习

Prometheus 基础知识脑图
https://developer.aliyun.com/article/1277296

Prometheus全面学习教程（精心整理，看这一篇就足够）
https://blog.csdn.net/qq_55723966/article/details/134976679