---
title: Kibana 常用命令
date: 2022-08-15 15:11:00
tags:
- Kibana
categories:
- 运维工具
---

# Kibana 详细入门教程

https://www.cnblogs.com/chenqionghe/p/12503181.html

# Lucene 查询语法汇总

https://www.cnblogs.com/chenqionghe/p/12501218.html



board
req_system_name
req_app_code 
req_component_name 接口名
request_id
req_client_ip


board: ieod 

AND req_system_name: CC
AND req_system_name: JOB
AND req_system_name: IJOBS
AND req_system_name: IJOBS2
AND req_system_name: GCLOUD 

board: ieod_clouds

AND req_system_name: CC
AND req_system_name: JOB
AND req_system_name: JOBV3
AND req_system_name: SOPS

AND req_app_code: octopus

AND req_client_ip: 9.140.128.13

AND req_component_name: execute_job


board: ieod AND req_system_name: JOB

board: ieod AND req_system_name: CC AND req_app_code: icm AND req_client_ip: 10.0.0.1


board: ieod_clouds AND req_system_name: CC AND req_app_code: bksops AND req_component_name: get_query_info

Field req_app_code

order by  metirc: Count

Descending 降序


trust_advisor


board: ieod_clouds AND req_system_name: CC AND req_app_code: icm AND req_component_name: get_biz_location 

board: ieod_clouds AND req_system_name: CC AND req_component_name: get_host_location AND req_app_code: icm

get_biz_location
get_host_location






