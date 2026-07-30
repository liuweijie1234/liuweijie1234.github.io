介绍如何实现高可用性和故障转移。


# 高可用性和故障转移

## 配置多个 Broker

使用多个 Broker 实现故障转移：

```python
app.conf.broker_list = [
    'redis://broker1:6379/0',
    'redis://broker2:6379/0',
]

app.conf.broker_failover_strategy = 'round-robin'
```

## 使用结果后端的高可用性配置

```python
app.conf.result_backend = 'redis://broker1:6379/0'
app.conf.result_backend_transport_options = {
    'master_name': 'broker1',
    'sentinel_kwargs': {
        'password': 'password'
    }
}
```

