---
title: MySQL 常用命令
date: 2022-08-15 11:42:00
tags:
- MySQL
categories:
- 数据库
---


## 数据类型

[MySQL数据类型和存储引擎](http://c.biancheng.net/mysql/40/)

## 基本命令

MySQL 检查运行状态

```sql
show status;
show status like 'uptime';
```

创建数据库
```sql
CREATE DATABASE `{APP_CODE}` default charset utf8 COLLATE utf8_general_ci;

CREATE DATABASE `test` default charset utf8 COLLATE utf8_general_ci;
```

查看数据库
```sql
show databases;
```

选择数据库
```sql
use databases_name;
```

删除数据库
```sql
drop dababase dababase_name;
```

查看表
```sql
show tables;
```

设置使用的字符集
```sql
set names utf8;
```

读取数据表的信息
```sql
SELECT * FROM table_name;

# 计算该表有多少条数据
SELECT COUNT(*) FROM table_name;
```

查看表结构
```sql
desc table_name;
DESCRIBE table_name;
```

查看表索引
```sql
SHOW INDEX FROM <表名> [ FROM <数据库名>]
```

查看所有键和索引
```sql
SHOW KEYS FROM <表名>;
```



批量插入
```sql
INSERT INTO my_table (id, name, age) VALUES
(1, 'John', 25),
(2, 'Jane', 30),
(3, 'Bob', 40);
```

批量更新

```sql
批量更新 services_bluetooth表 where sn like 'DBW%'的uploaded字段的值为 services_bluetooth SET uploaded = 0 WHERE sn LIKE 'DBW%';


UPDATE services_bluetooth
SET uploaded = 0
WHERE sn LIKE 'P04%'
    AND create_time BETWEEN '2023-07-15 09:00:00' AND '2023-07-15 16:00:00';


UPDATE `tools_telecomdata`
SET 
    sn = NULL,
    unbind_time = NOW(),
    unbind_cause = '解绑13套',
    upload_kds = 0
WHERE sn IN (
    'W5380F2312220DB1559522',
    'W5380F2312220DB1559512',
    'W5380N2401180DB0740730',
    'W5380N2401290DC0845954',
);
```


查询MySQL中当前有多少连接
```sql
SHOW STATUS LIKE 'Threads_connected';
```

MySQL常用命令(基础)
https://bk.tencent.com/s-mart/community/question/919?type=answer


[ORDER BY 排序](https://www.runoob.com/mysql/mysql-order-by.html)

## LEFT JOIN(JOIN) 详解

```sql
SELECT 
    t1.c1,
    t1.c2,
    t2.c1,
    t2.c2
FROM
    t1
        LEFT JOIN
    t2 ON t1.c1 = t2.c1; 
```

```sql
SELECT 
    pro.id,
    pro.file_name,
    pro.module_name,
    pro.version,
    pac.name
FROM 
    deploy_projectpackage_tags AS dpt
        LEFT JOIN
    deploy_projectpackage AS pro ON pro.id=dpt.projectpackage_id
        LEFT JOIN
    deploy_packagetag AS pac ON pac.id=dpt.packagetag_id
WHERE
    dpt.packagetag_id=507;
```


```sql
SELECT
    c.id AS case_id,
    c.name AS case_name,
    c.parent_id_id AS project_id,
    c.spend AS case_spend,
    c.result AS case_result,
    c.desc AS case_desc,
    r.name AS result_name,
    r.desc AS result_desc,
    r.result AS result_result,
    r.standard AS result_standard
FROM 
    survey_testresult AS r
        LEFT JOIN
    survey_testcase AS c ON r.parent_id_id = c.id
```

```sql
SELECT
    *
FROM
    survey_testproject AS p
        LEFT JOIN 
        (
        SELECT
            c.id AS case_id,
            c.name AS case_name,
            c.parent_id_id AS project_id,
            c.spend AS case_spend,
            c.result AS case_result,
            c.desc AS case_desc,
            r.name AS result_name,
            r.desc AS result_desc,
            r.result AS result_result,
            r.standard AS result_standard
        FROM 
            survey_testcase AS c 
                LEFT JOIN
            survey_testresult AS r ON r.parent_id_id = c.id
        ) AS sub ON sub.project_id= p.id
WHERE
    p.name= 'firmware_burn'
    AND
    sub.case_name='burn'
    AND
    p.time>'2022-10-01 00:00:00'
    AND
    p.time<'2022-12-13 23:59:59'
```


```sql
SELECT
    a.barcode,a.name,a.long_name,a.working_line,a.station,a.time,a.spend,
    a.result,a.desc,a.version,u.name,a.case_name,a.case_desc,a.case_result,
    a.case_spend,a.result_name,a.result_result,a.result_desc,a.result_standard 
FROM 
    xtauth_user AS u
        RIGHT JOIN 
    (
        SELECT
            *
        FROM 
            survey_testproject AS p
                LEFT JOIN 
            (
                SELECT 
                    c.id AS case_id,
                    c.name AS case_name,
                    c.parent_id_id AS project_id,
                    c.spend AS case_spend,
                    c.result AS case_result,
                    c.desc AS case_desc,
                    r.name AS result_name,
                    r.desc AS result_desc,
                    r.result AS result_result,
                    r.standard AS result_standard
                FROM 
                    survey_testcase AS c 
                        LEFT JOIN  
                    survey_testresult AS r ON r.parent_id_id = c.id
            ) AS sub ON sub.project_id= p.id
        WHERE
            p.name= 'firmware_burn'
            AND 
            sub.case_name='burn'
            AND 
            p.time>'2022-10-01 00:00:00'
            AND 
            p.time<'2022-12-13 23:59:59'
    ) AS a ON u.uid = a.user_id
```

查询产测指定记录并链接SN展示

```sql
SELECT `time`,`desc` 
FROM survey_testcase 
WHERE parent_id_id 
    IN (SELECT id FROM survey_testproject WHERE `name`='ABWRK-Printer' AND result='Pass') 
    AND `name`='1.9 显示BLE MAC地址';



SELECT t.barcode, tc.time, tc.desc
FROM survey_testcase tc
JOIN survey_testproject t ON t.id = tc.parent_id_id
WHERE t.name = 'ABWRK-Printer' AND t.result = 'Pass' AND tc.name = '1.9 显示BLE MAC地址';
```



## RIGHT JOIN 详解

RIGHT JOIN 类似于 LEFT JOIN 是对表反转的处理。

```sql
SELECT 
    * 
FROM t1
    RIGHT JOIN 
t2 ON t1.pk = t2.fk ; 
```

t1是左表，t2是右表

将左表（t1）上的行与右表（t2）上的行匹配

> 重要：`RIGHT JOIN`与 `LEFT JOIN` 子句在功能上是等效的，只要切换表顺序，它们就可以互相替换。
> 
> 注意：`RIGHT OUTER JOIN`是`RIGHT JOIN`的同义词。


## group by 详解

根据给定数据列的每个成员对查询结果进行分组统计，最终得到一个分组汇总表。

## having 详解

筛选满足条件的组，即在分组之后过滤数据，条件中经常包含聚组函数，使用 having 条件过滤出特定的组，也可以使用多个分组标准进行分组。


[mysql中去重 distinct用法](https://blog.csdn.net/weixin_36210698/article/details/73496673)

[MySQL优化之：explain用法详解](https://juejin.cn/post/6966055143565426696)
[MySQL 性能优化神器 Explain 使用分析](https://segmentfault.com/a/1190000008131735)


## 工作案例

[MySQL慢查询日志总结](https://www.cnblogs.com/kerrycode/p/5593204.html)

### 查询某字段不为空的数据

SELECT * FROM table_dk01mf_packing WHERE Field01 IS NOT NULL;

### 删除单条数据

SELECT id,sn, barcode FROM tools_bluetooth WHERE sn="63Z0224110001";

DELETE FROM tools_bluetooth WHERE sn="63Z0224110001";

### 删除多条数据

DELETE FROM tools_telecomdata WHERE ctei IN (
    '187920850003091',
    '187920850003092',
    '187920850003093'
);


### 修改装备测试工程包标签(单个)

页面第1行的"包名"对应 deploy_projectpackage 的 file_name 
页面第2行的"模块名称"对应 deploy_projectpackage 的 module_name 
页面第3行的"版本号"对应 deploy_projectpackage 的 version 
页面第4行的"适用于"对应 deploy_packagetag 的 name 
页面第5行的"工厂"对应 deploy_projectpackage_factory 
页面第6行的"描述"对应 deploy_projectpackage 的 desc 


找到需要替换 包标签 对应的id
```sql
select * from deploy_packagetag WHERE name LIKE 'DDL501%';

packagetag_id=752 DDL501-M(W131S_DL9)

packagetag_id=693 DDL501-S(W131S_DLS)
```

找到包 对应的id
```sql
select * from deploy_projectpackage where module_name="D56F1_FT";

projectpackage_id=4295
```


### 修改装备测试工程包工厂(单个)

ATE阿里云服务

1、选择对于数据库

```sql
use ate_2021;
```
2、找到自己需要的数据及id

页面第4行的"适用于"对应 deploy_packagetag 的 name 

2.1 找到包标签对应的id

```sql
select * from deploy_packagetag WHERE name LIKE 'WFV01%';

packagetag_id=507

select * from deploy_packagetag WHERE id="507";

```

2.2 根据包标签id找到与其有关系的包id

```sql
select * from deploy_projectpackage_tags where packagetag_id="507";

+------+-------------------+---------------+
| id   | projectpackage_id | packagetag_id |
+------+-------------------+---------------+
| 4938 |              2859 |           507 |
| 4939 |              2860 |           507 |
| 4940 |              2861 |           507 |
| 4950 |              2872 |           507 |
| 4988 |              2901 |           507 |
| 4989 |              2902 |           507 |
| 4990 |              2903 |           507 |
| 5013 |              2924 |           507 |
| 5014 |              2925 |           507 |
| 5015 |              2926 |           507 |
| 5054 |              2956 |           507 |
| 5055 |              2957 |           507 |
| 5056 |              2958 |           507 |
| 5160 |              3043 |           507 |
| 5366 |              3241 |           507 |
| 5367 |              3242 |           507 |
| 5368 |              3243 |           507 |
```

2.3 找到温州工厂及对应id

```sql
select * from tools_factory;

factory_id=1
温州id 是1
factory_id=3
珠海id是3

武汉id是7
```

2.4 找到需要修改包的数据

```sql
select * from deploy_projectpackage where id=3854;
select * from deploy_projectpackage where module_name="D56F1_FT";

select id,file_name,module_name,version from deploy_projectpackage where module_name="S0V01_W02_FT";
select id,file_name,module_name,version from deploy_projectpackage where module_name LIKE "WFV01%";

select id,file_name,version from deploy_projectpackage where module_name="D56F1_FT";


select id,file_name,module_name,version from deploy_projectpackage where id=2859;
select * from deploy_projectpackage_factory where projectpackage_id=2859;
```


更新包的描述
```sql
UPDATE deploy_projectpackage 
SET `desc` = '1、调整测试工艺，增加在FT站写入ESN。'
WHERE module_name="S0V01_W02_FT" and id='4133';

```



新增包的工厂

```sql
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3607,1);
```


### 修改装备测试工程包工厂(多个)

通过多对多关系查询单个标签对于的所有包，并为包插入工厂

```sql
select * from deploy_packagetag WHERE name LIKE 'JC201%';
得到packagetag_id

select projectpackage_id from deploy_projectpackage_tags where packagetag_id="507";

select id,file_name,module_name,version from deploy_projectpackage where id=2859;
```

```sql
SELECT 
pro.id,pro.file_name,pro.module_name,pro.version,pac.name
FROM 
deploy_projectpackage_tags dpt
LEFT JOIN 
deploy_projectpackage pro
on pro.id=dpt.projectpackage_id
LEFT JOIN 
deploy_packagetag pac
on pac.id=dpt.packagetag_id
WHERE dpt.packagetag_id=507;
```
+------+-------------------------+--------------+---------+------------------+
| id   | file_name               | module_name  | version | name             |
+------+-------------------------+--------------+---------+------------------+
| 2859 | S0V01_MBT_V1.0.1.rar    | S0V01_MBT    | V1.0.1  | WFV01(S0V01_W02) |
| 2860 | S0V01_SFT_V1.0.1.rar    | S0V01_SFT    | V1.0.1  | WFV01(S0V01_W02) |
| 2861 | S0V01_W02_FT_V1.0.2.rar | S0V01_W02_FT | V1.0.2  | WFV01(S0V01_W02) |
| 2872 | S0V01_W02_FT_V1.0.3.rar | S0V01_W02_FT | V1.0.3  | WFV01(S0V01_W02) |
| 2924 | S0V01_MBT_V1.0.4.rar    | S0V01_MBT    | V1.0.4  | WFV01(S0V01_W02) |
| 2925 | S0V01_SFT_V1.0.4.rar    | S0V01_SFT    | V1.0.4  | WFV01(S0V01_W02) |
| 2926 | S0V01_W02_FT_V1.0.6.rar | S0V01_W02_FT | V1.0.6  | WFV01(S0V01_W02) |
| 2956 | S0V01_MBT_V1.0.5.rar    | S0V01_MBT    | V1.0.5  | WFV01(S0V01_W02) |
| 2957 | S0V01_SFT_V1.0.5.rar    | S0V01_SFT    | V1.0.5  | WFV01(S0V01_W02) |
| 2958 | S0V01_W02_FT_V1.0.7.rar | S0V01_W02_FT | V1.0.7  | WFV01(S0V01_W02) |
| 3043 | S0V01_W02_FT_V1.0.8.rar | S0V01_W02_FT | V1.0.8  | WFV01(S0V01_W02) |
| 3241 | S0V01_W02_FT_V1.0.9.zip | S0V01_W02_FT | V1.0.9  | WFV01(S0V01_W02) |
| 3242 | S0V01_SFT1_V1.0.4.zip   | S0V01_SFT1   | V1.0.4  | WFV01(S0V01_W02) |
| 3243 | S0V01_SFT_V1.0.5.zip    | S0V01_SFT    | V1.0.5  | WFV01(S0V01_W02) |
+------+-------------------------+--------------+---------+------------------+

INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2859,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2860,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2861,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2872,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2924,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2925,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2926,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2956,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2957,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (2958,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3043,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3241,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3242,1);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3243,1);




select * from deploy_packagetag WHERE name LIKE 'KA211%';
JC201(P0AQ1_J21)  packagetag_id=760

KA202(V0AJ2_R22)  packagetag_id=655

SELECT 
pro.id,pro.file_name,pro.module_name,pro.version,pac.name
FROM 
deploy_projectpackage_tags dpt
LEFT JOIN 
deploy_projectpackage pro
on pro.id=dpt.projectpackage_id
LEFT JOIN 
deploy_packagetag pac
on pac.id=dpt.packagetag_id
WHERE dpt.packagetag_id=655;

id	file_name	module_name	version	name
4518	SIPEVB_ATE_915Mhz_CH25_CW_14dBm_15sec_sleepMode.rar	PowerG 15秒发射测试固件	V	JC201(P0AQ1_J21)
4517	P0AQ1_J21_FT1_V1.0.1.rar	P0AQ1_J21_FT1	V1.0.1	JC201(P0AQ1_J21)
4516	P0AQ1_J21_FT_V1.0.7.rar	P0AQ1_J21_FT	V1.0.7	JC201(P0AQ1_J21)
4515	P0AQ1_SFT_V1.0.4.rar	P0AQ1_SFT	V1.0.4	JC201(P0AQ1_J21)
4514	P0AQ1_MBT_V1.0.4.rar	P0AQ1_MBT	V1.0.4	JC201(P0AQ1_J21)


INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3837,3);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3838,3);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (3839,3);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (4516,3);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (4515,3);
INSERT INTO deploy_projectpackage_factory ( projectpackage_id,factory_id) VALUES (4514,3);




### 导出SN、ESN

查询
SELECT * FROM tools_bluetooth 
where sn LIKE 'K58%' 

排序 （DESC降序）

SELECT * FROM tools_bluetooth 
WHERE sn LIKE 'K58%' 
ORDER BY id DESC


去重

SELECT * FROM tools_bluetooth 
WHERE sn LIKE 'K58%' 
group by barcode
ORDER BY `create_time` DESC;



导出

SELECT * FROM tools_bluetooth 
WHERE sn LIKE 'K58%' 
group by barcode
ORDER BY `create_time`
INTO OUTFILE '/var/lib/mysql-files/K58.txt';

发现排序失败 先抽出排序

```sql
SELECT * FROM
(SELECT DISTINCT * FROM tools_bluetooth ORDER BY id DESC) AS a
WHERE sn LIKE 'K58%'
group by barcode
INTO OUTFILE '/var/lib/mysql-files/K58.txt';


SELECT * FROM
(SELECT DISTINCT * FROM tools_bluetooth ORDER BY id DESC) AS a
WHERE sn LIKE 'K59%'
group by barcode
INTO OUTFILE '/var/lib/mysql-files/K59.txt';
```


### 限制查询结果的条数

SELECT * FROM survey_testresult WHERE `desc`='V124008' LIMIT 0,1000;


### 通过时间范围查询ESN
```sql
SELECT robot_name, COUNT(*) AS count
FROM apischedulers_logs
WHERE create_time BETWEEN '2025-05-07 00:00:00' AND '2025-05-07 23:59:59'
GROUP BY robot_name;
```

select * from services_bluetooth where date_format(create_time,'%Y-%m-%d') between '2022-11-07' and '2022-11-09';

SELECT *
FROM services_bluetooth
WHERE sn LIKE 'P04%' AND create_time BETWEEN '2023-07-15 09:00:00' AND '2023-07-15 16:00:00';

[mysql 根据时间范围查询](https://blog.csdn.net/qq_36189144/article/details/88350390)

[查询字段取前3位，后3位，中间3位，去除前3位，去除后3位](https://blog.csdn.net/happy_jijiawei/article/details/41979631)

select left(sn,3) from services_bluetooth where date_format(create_time,'%Y-%m-%d') between '2022-11-22' and '2022-11-23';

[模糊查询](http://c.biancheng.net/view/7395.html)


select * from services_bluetooth where (create_time between '2022-11-24 22:00:00' and '2022-11-25 16:20:00') AND (sn LIKE 'S2L%');


select * from services_bluetooth where (date_format(create_time,'%Y-%m-%d') between '2022-11-24' and '2022-11-25') AND (sn LIKE 'S2L%');

select * from services_bluetooth where (date_format(create_time,'%Y-%m-%d') between '2022-11-24' and '2022-11-25') AND (sn LIKE 'S2L%');

select * from services_bluetooth where sn LIKE 'K83%';

select * from services_bluetooth where sn LIKE 'D81%'

insert into `services_productmodel` (`id`, `model`, `research`, `sn_head`, `server`, `remark`, `create_user`, `create_time`, `batch_time`, `country`, `country_code`, `product_mark`, `product_sn`, `ptp`, `ptp_num`, `fill_light`, `picture_rotation`, `server_code_id`) values('552','BL1-WiFi','KMWA0','BL1','凯迪仕','博流BL602C（替换乐鑫8266模组）','张泳伦','2022-10-27 16:00:00.255667',NULL,'中国','CN',NULL,NULL,NULL,NULL,NULL,NULL,'1');


django.db.utils.InternalError: (1054, "Unknown column 'tools_telecomdata.profile_id' in 'field list'")


UPDATE `ate_2021`.`services_productmodel` 
SET `model` = 'DDL709-FVP-7HW', `research` = '79FVU', `sn_head` = '79U', `server` = '飞利浦', `remark` = '1.增加云存储需求；2.更新TDK超声波模组', `create_user` = '余国平', `create_time` = '2022-11-08 09:29:45.376362', `country` = '中国', `country_code` = 'CN', `ptp` = '凯迪仕（腾讯云V2.5）', `ptp_num` = 4, `fill_light` = 0, `picture_rotation` = '0', `server_code_id` = 18, `cardgroupnum` = 100, `facegroupnum` = 20, `fingergroupnum` = 100, `fingerveingroupnum` = NULL, `isactivationcode` = 1, `isequipmentdistribution` = 0, `policypwdgroupnum` = 0, `pwdgroupnum` = 20, `pwdtype` = '1,2', `iswanderingsensor` = 1, `logocode` = 18 
WHERE `id` = 977;


### 查询某字段重复的数据

[MYSQL 查找单个字段或者多个字段重复数据，清除重复数据](https://blog.csdn.net/qq_35387940/article/details/108074927)


SELECT id,sn, barcode, COUNT(barcode) as count FROM services_bluetooth GROUP BY barcode;

SELECT barcode FROM services_bluetooth GROUP BY barcode HAVING COUNT(barcode) > 1;


```sql
SELECT id,sn, barcode FROM  services_bluetooth 
WHERE barcode IN
(
SELECT barcode FROM services_bluetooth 
GROUP BY barcode HAVING COUNT(barcode) > 1
)
ORDER BY barcode ASC;
LIMIT 10 OFFSET 20;
```


```sql
SELECT min(id) as id from (


SELECT id,sn, barcode FROM  services_bluetooth WHERE barcode IN
(
SELECT barcode FROM services_bluetooth GROUP BY barcode HAVING COUNT(barcode) > 1
)


) a GROUP BY a.barcode

```

```sql

DELETE FROM services_bluetooth WHERE id IN (

SELECT t1.id 
FROM ( SELECT id FROM services_bluetooth WHERE barcode IN (  SELECT barcode FROM tools_bluetooth GROUP BY barcode HAVING COUNT(barcode) > 1) ) t1 
WHERE t1.id 
NOT IN (
 
SELECT max(id) as id from (

SELECT id,sn, barcode FROM  services_bluetooth WHERE barcode IN
(
SELECT barcode FROM services_bluetooth GROUP BY barcode HAVING COUNT(barcode) > 1
)


) a GROUP BY a.barcode

)
)
```

### 导出产测数据

多表查询


```sql
SELECT * FROM survey_testproject WHERE NAME='P0AQ1_J21_FT1' AND result='Pass'

SELECT * FROM survey_testcase WHERE parent_id_id IN (SELECT id FROM survey_testproject WHERE NAME='P0AQ1_J21_FT1' AND result='Pass');

SELECT * FROM survey_testresult WHERE parent_id_id IN (SELECT id FROM survey_testcase WHERE parent_id_id IN (SELECT id FROM survey_testproject WHERE NAME='P0AQ1_J21_FT1' AND result='Pass'));


SELECT * FROM survey_testproject WHERE NAME='P0AQ1_J21_RF' AND result='Pass'

SELECT * FROM survey_testcase WHERE parent_id_id IN (SELECT id FROM survey_testproject WHERE NAME='P0AQ1_J21_RF' AND result='Pass');

SELECT * FROM survey_testresult WHERE parent_id_id IN (SELECT id FROM survey_testcase WHERE parent_id_id IN (SELECT id FROM survey_testproject WHERE NAME='P0AQ1_J21_RF' AND result='Pass'));


SELECT * FROM survey_testproject WHERE NAME='P0AQ1_SFT' AND result='Pass'

SELECT * FROM survey_testcase WHERE parent_id_id IN (SELECT id FROM survey_testproject WHERE NAME='P0AQ1_SFT' AND result='Pass');

SELECT * FROM survey_testresult WHERE parent_id_id IN (SELECT id FROM survey_testcase WHERE parent_id_id IN (SELECT id FROM survey_testproject WHERE NAME='P0AQ1_SFT' AND result='Pass'));

```

导出产线、箱子和SN关系数据

```sql
SELECT id,name,long_name,station,working_line,time,spend,barcode,count,result,desc,version,upload_ip,upload_user,create_time,user_id FROM survey_testproject WHERE NAME='P0AQ1_J21_RF' AND result='Pass'

user_id是对应着 xtauth_user表的uid,想得到xtauth_user表的name来替换use_id

SELECT stp.id, stp.name, stp.long_name, stp.station, stp.working_line, stp.time, stp.spend, stp.barcode, stp.count, stp.result, stp.desc, stp.version, stp.upload_ip, stp.upload_user, stp.create_time, xtu.name AS user_name
FROM survey_testproject AS stp
JOIN xtauth_user AS xtu ON stp.user_id = xtu.uid
WHERE stp.name = 'P0AQ1_J21_RF' AND stp.result = 'Pass';
```

### 导出产测记录指定版本

```sql
SELECT
  t0.barcode AS `barcode`,
  MAX(t2_wifi.desc) AS `ValidateVersionWiFi`,
  MAX(t2_1.desc) AS `ValidateVersion1`,
  MAX(t2_6.desc) AS `ValidateVersion6`,
  MAX(t2_7.desc) AS `ValidateVersion7`,
  MAX(t2_8.desc) AS `ValidateVersion8`,
  MAX(t2_16.desc) AS `ValidateVersion16`
FROM 
  survey_testcase t1
LEFT JOIN
  survey_testproject t0 ON t0.id = t1.parent_id_id
LEFT JOIN
  survey_testresult t2_wifi ON t1.id = t2_wifi.parent_id_id AND t1.name = 'ValidateVersionWiFi'
LEFT JOIN
  survey_testresult t2_1 ON t1.id = t2_1.parent_id_id AND t1.name = 'ValidateVersion1'
LEFT JOIN
  survey_testresult t2_6 ON t1.id = t2_6.parent_id_id AND t1.name = 'ValidateVersion6'
LEFT JOIN
  survey_testresult t2_7 ON t1.id = t2_7.parent_id_id AND t1.name = 'ValidateVersion7'
LEFT JOIN
  survey_testresult t2_8 ON t1.id = t2_8.parent_id_id AND t1.name = 'ValidateVersion8'
LEFT JOIN
  survey_testresult t2_16 ON t1.id = t2_16.parent_id_id AND t1.name = 'ValidateVersion16'
WHERE 
  t1.parent_id_id IN (
    SELECT id FROM survey_testproject t0 WHERE NAME = 'K8603_K83_FT' AND barcode IN (
      'W9250A2211180DA0122922',
      'W9250A2211180DA0131128',
      'W9250A2211230DA0131140'
    )
  )
GROUP BY t0.barcode;
```



```sql
SELECT
  t0.barcode AS `barcode`,
  MAX(t2.desc) AS `RearVersion`,
  MAX(t3.desc) AS `Version`,
FROM 
  survey_testcase t1
LEFT JOIN
  survey_testproject t0 ON t0.id = t1.parent_id_id
LEFT JOIN
  survey_testresult t2 ON t1.id = t2.parent_id_id AND t1.name = 'RearVersion'
LEFT JOIN
  survey_testresult t3 ON t1.id = t3.parent_id_id AND t1.name = 'Version'
WHERE 
  t1.parent_id_id IN (
    SELECT id FROM survey_testproject t0 WHERE NAME = 'W1AC0_AC0_FT' AND result='Pass' AND barcode IN (
      'K502QBS07E230728A00001',
      'K502QBS07E230728A00002',
      'K502QBS07E230728A00003'
    )
  )
GROUP BY t0.barcode;



```

### 批量根据SN反查ESN信息

```sql
SELECT * FROM services_bluetooth WHERE sn IN (
    'K831233111324',
    'K831233111157',
    'K831225211016'
);
```



### 根据SN导出最新的ESN信息

```sql
SELECT sn, barcode, create_time
FROM services_bluetooth s1
WHERE barcode IN (
'W9257A2302160DB4302942',
'W9257A2302160DB4303212',
'W9257A2035184DG1017052'
)
AND create_time = (
    SELECT MAX(create_time)
    FROM services_bluetooth s2
    WHERE s2.barcode = s1.barcode
);
```

### 导出指定一天的所有ESN信息

```sql
SELECT * FROM services_bluetooth WHERE create_time BETWEEN '2024-04-11 00:00:00' AND '2024-04-11 23:59:59';
```


### 多对多表 查询

阿里云 装备包+标签 多表查询

```sql
SELECT dp.name AS tag_name, dpp.file_name
FROM deploy_packagetag dp
JOIN deploy_projectpackage_tags dpt ON dp.id = dpt.packagetag_id
JOIN deploy_projectpackage dpp ON dpt.projectpackage_id = dpp.id
WHERE dp.create_time BETWEEN '2023-01-01 00:00:00' AND '2024-01-01 00:00:00';
```

```sql
SELECT dp.name AS tag_name, dpp.file_name, dpp.upload_time
FROM deploy_projectpackage dpp
JOIN deploy_projectpackage_tags dpt ON dpt.projectpackage_id = dpp.id
JOIN deploy_packagetag dp ON dp.id = dpt.packagetag_id
WHERE dpp.upload_time BETWEEN '2024-01-01 00:00:00' AND '2024-04-29 00:00:00';
```

```sql
select file_name, tag.name AS tag_name, `desc` , upload_time
from deploy_projectpackage AS pkg
LEFT JOIN
deploy_projectpackage_tags AS pt ON pkg.id=pt.projectpackage_id
LEFT JOIN
deploy_packagetag AS tag ON tag.id=pt.packagetag_id
where pkg.upload_time BETWEEN '2024-01-01 00:00:00' AND '2024-07-03 16:00:00';
```

## 数据库管理

### 启动/停止

### 查看用户

```sql
SELECT user, host FROM mysql.user;
```

### 查看用户权限

```sql
SHOW GRANTS FOR 'root'@'%';
SHOW GRANTS FOR 'root'@'172.16.3.33';
SHOW GRANTS FOR 'root'@'localhost';
SHOW GRANTS FOR 'MySlave12'@'172.16.0.12';
```

### 创建用户

```sql
CREATE USER 'MySlave228'@'172.16.2.228' IDENTIFIED BY '123456';

CREATE USER 'admin'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%';
FLUSH PRIVILEGES;
```
```sql
CREATE USER 'root'@'%' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```


### 删除用户

```sql
DROP USER 'jack'@'localhost';

DROP USER 'MySlave109'@'192.168.0.109';
```

### 修改用户密码

```sql
UPDATE user SET authentication_string = PASSWORD('abcdefg@com') WHERE user = 'root' AND host = 'localhost';
UPDATE mysql.user SET authentication_string = PASSWORD('Ld@Qq123456') WHERE user = 'root' AND host = 'localhost';
UPDATE user SET authentication_string = PASSWORD('Ld@Qq123456') WHERE user = 'root' AND host = 'localhost';

SET PASSWORD FOR 'root'@'localhost' = PASSWORD('new_password');
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('Ld@Qq123456');

GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'abcdefg@com' WITH GRANT OPTION;
GRANT PROXY ON ''@'' TO 'root'@'localhost' IDENTIFIED BY 'abcdefg@com' WITH GRANT OPTION;

flush privileges;
```
https://www.yiibai.com/mysql/changing-password.html



mysql8.0 修改密码

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Ld@Qq123456';
alter user 'root'@'localhost' identified with mysql_native_password by 'Ld@Qq123456';    
```
https://www.cnblogs.com/tangmj/p/16377411.html



### 授权

https://www.sjkjc.com/mysql/grant-privileges/


### 修改用户主机限制

```sql
DELETE FROM mysql.user WHERE user='root' AND host='172.16.3.33';
UPDATE mysql.user SET host='%' WHERE user='root' AND host='172.16.3.33';
FLUSH PRIVILEGES;
```

### 删除表数据

```sql
DELETE FROM <表名> [WHERE 子句] [ORDER BY 子句] [LIMIT 子句]

DELETE FROM tools_bluetooth WHERE barcode='A81710D9B9EA';
```

DELETE FROM survey_testresult WHERE time BETWEEN '2016-01-01 00:00:00' AND '2017-01-01 00:00:00';
DELETE FROM survey_testcase WHERE time BETWEEN '2016-01-01 00:00:00' AND '2017-01-01 00:00:00';
DELETE FROM survey_testproject WHERE time BETWEEN '2016-01-01 00:00:00' AND '2017-01-01 00:00:00';

### 删除表字段



### 删除表

MySQL 删除表的几种情况:

drop table table_name : 删除表全部数据和表结构，会立刻释放磁盘空间，

例子：

```sql
DROP TABLE IF EXISTS `tbl`;
```


### 删除表数据

```sql
truncate table table_name
```
删除表全部数据，并将自动递增列的值重置为 0，保留表结构，立刻释放磁盘空间。（此时可以通过desc tablename来查看表结构依然是存在的，但是使用select * from tablename会发现表内的数据已经删除。）

```sql
delete from table_name : 删除表全部数据，表结构不变，mysql也会立即释放磁盘空间。

delete from table_name where xxx : 加了条件判读where从句，表结构不变，不会释放磁盘空间。
```


注意：Delete可以rollback撤销，truncate不能。



### 删除库

1、在删除数据库之前，请确保对于该数据库的任何操作都已备份并保存到安全位置。因为删除后将无法恢复该数据库及其内容。


2、如果该数据库包含其他对象（如表、视图、存储过程等），则可能需要先删除这些对象才能成功删除数据库。您可以使用 SHOW TABLES 和 DROP TABLE 等命令来查看和删除表，使用 DROP VIEW 命令来删除视图，使用 DROP PROCEDURE 命令来删除存储过程等。


3、使用 DROP DATABASE 语句删除指定的数据库。例如，要删除名为 exampledb 的数据库，可以运行以下命令：

```sql
DROP DATABASE exampledb;
```

需要注意的是，要执行这些操作，您需要具有适当的权限才能访问和修改数据库。在某些情况下，可能需要使用管理员或超级用户帐户来执行这些操作。


### 修改表

[MySQL数据表添加字段（三种方式）](http://c.biancheng.net/view/7201.html)

[MySQL新增、修改字段并添加默认值和备注](https://blog.csdn.net/weixin_44609018/article/details/113942865)

### 查询索引

https://blog.csdn.net/weixin_31861065/article/details/113229676

### 删除索引

DROP INDEX <索引名> ON <表名>


[mySQL中删除unique key的语法](https://blog.csdn.net/jaray/article/details/19820663)

### 导出

导出=备份

> 注意：运算符(>)表示导出。

#### 导出指定数据库

```sql
mysqldump -u [用户名] -p [数据库名] > [输出文件名].sql

mysqldump -u root -p ate > ate_2023.sql

mysqldump -u root -p --databases ate > ate_20240513.sql


```
> 注意：test.sql 默认位于 C:\Program Files\MySQL\MySQL Server 5.7\bin

#### 导出指定数据库指定表

```sql

mysqldump -u username -p database_name  table1 table2 table3 > filename.sql

mysqldump -u root -p mysql db event > /backup/mysqldump/tables.sql

mysqldump -u root -p ate_2021 survey_testcase survey_testproject survey_testresult > dump.sql

mysqldump -u root -p ate2022 survey_testproject survey_testcase survey_testresult > ate_ytl20231010.sql

mysqldump -u root -p ate2022 services_bluetooth > ate_esn.sql
```
mysqldump -u your_username -p your_password --where="create_time < '2022-01-01'" ate ProductModel > backup.sql


其中 db 、event 为 mysql 库 的表

> 注意：多个表用空格间隔

#### 导出指定数据库排除某些表

```sql
mysqldump -uroot -p ate_2022 --ignore-table=ate_2022.django_migrations > ate_2023.sql

mysqldump -uroot -p ate_2022 --ignore-table=ate_2022.django_migrations --ignore-table=ate_2022.authtoken_token > ate_2023.sql
```

#### 导出特定表内容

```sql
SELECT * FROM tools_bluetooth 
WHERE sn LIKE 'K58%' 
group by barcode
ORDER BY `create_time`
INTO OUTFILE '/var/lib/mysql-files/K58.txt';
```

#### 示例


1、在目标机器上安装MySQL服务器，并确保它已启动和运行。

2、创建一个新的MySQL用户，并授予适当的权限以备份和恢复数据库。例如，可以使用如下命令创建一个名为backup_user的新用户：

```sql
CREATE USER 'backup_user'@'localhost' IDENTIFIED BY 'your_password';

GRANT SELECT, RELOAD, SHUTDOWN, PROCESS, SUPER, LOCK TABLES, REPLICATION CLIENT ON . TO 'backup_user'@'localhost';
```

3、在源MySQL服务器上执行备份操作，例如使用mysqldump工具执行备份。例如，以下命令将在本地生成一个名为mydatabase.sql的备份文件：
```sql
mysqldump -u root -p mydatabase > mydatabase.sql
```

4、通过SCP命令将备份文件传输到目标机器上。例如，以下命令将备份文件从本地复制到目标机器的/var/backups目录下：

```bash
scp mydatabase.sql backup_user@target_machine:/var/backups/
```

5、在目标MySQL服务器上执行还原操作。例如，以下命令将备份文件中的数据还原到名为mydatabase的数据库中：

```bash
mysql -u root -p mydatabase < /var/backups/mydatabase.sql
```

```bash
# 依靠工具备份
[root@localhost tmp]# mysqldump -u'root' -p'123456' --all-databases --single-transaction --master-data=2 --flush-logs --default-character-set=utf8 > /tmp/mysqlbackup/`date +%F_%H-%M-%S`-mysql-all.sql   # 备份数据库

# 下面的命令是发送数据备份文件到从服务器的/tmp/目录下
[root@localhost tmp]# scp /tmp/mysqlbackup/2020-12-09_13-18-55-mysql-all.sql 192.168.137.101:/tmp/

The authenticity of host '192.168.137.101 (192.168.137.101)' can't be established.
ECDSA key fingerprint is SHA256:XGNB4Tf/YmQOhuzY8BXxSIEbRbKli30IAJLfR5UM4VI.
ECDSA key fingerprint is MD5:96:ef:27:6c:35:16:f0:99:5c:4b:1d:4c:27:b1:56:bf.
Are you sure you want to continue connecting (yes/no)? yes        # 这里输入yes表示需要连接
Warning: Permanently added '192.168.137.101' (ECDSA) to the list of known hosts.
root@192.168.137.101's password:    # 这里输入从服务器密码
2020-12-09_13-18-55-mysql-all.sql         100%  777KB  89.1MB/s   00:00    # 看到100%说明传输成功
```

6、确认还原是否成功。可以登录目标MySQL服务器并检查数据库是否包括所有预期的表和数据。

这些步骤可以帮助您将MySQL数据库备份到另一台机器的MySQL数据库中。请注意，备份和还原过程可能需要比较长时间，取决于数据库的大小和网络速度等因素。

#### 参数详解

| 参数名 | 缩写 | 含义 |
| -- | -- | -- |
| –host | -h | 服务器IP地址 |
| –port | -P | 服务器端口号 |
| –user | -u | MySQL 用户名 |
| –pasword | -p | MySQL 密码 |
| --databases | | 指定要备份的数据库 |
| --all-databases | | 备份mysql服务器上的所有数据库 |
| –compact | | 压缩模式，产生更少的输出 |
| –comments | | 添加注释信息 |
| –complete-insert | | 输出完成的插入语句 |
| –lock-tables | | 备份前，锁定所有数据库表 |
| –no-create-db/–no-create-info | | 禁止生成创建数据库语句 |
| –force | | 当出现错误时仍然继续备份操作 |
| --default-character-set |  | 指定默认字符集 |
| –add-locks | | 备份数据库表时锁定数据库表 |
| --single-transaction | | 一致性服务可用性，锁表机制 , 热备份 |
| --master-data=2 | | 该选项将会记录binlog的日志位置与文件名，可以选择1或者2，效果一样 |
| --max_allowed_pa​​cket=512M | | 数据库包含大数据字段，则应使用--max_allowed_pa​​cket参数|
| --flush-logs | | 自动刷新日志 |
| --ignore-table | | 排除指定表 |


### 导入（还原）

MySQL导入sql文件的三种方法 https://blog.csdn.net/m0_67390788/article/details/126803325


#### source 方法

将需要导入的文件 test.sql 放到bin文件下 （windows默认C:\Program Files\MySQL\MySQL Server 5.7\bin）

命令行导入数据库：

1，将要导入的.sql文件移至bin文件下，这样的路径比较方便
2，同上面导出的第1步
3，进入MySQL：`mysql -u root -p`
4，在MySQL-Front中新建你要建的数据库，这时是空数据库，如新建一个名为news的目标数据库
5，**输入：mysql > `use 目标数据库名`**
6，**导入文件：mysql > `source 导入的文件名;`**

比如我输入的命令行：mysql > source test.sql;

导入路径不能有中文

如果您希望在出现冲突时执行一些特定的操作，可以使用以下方式：

使用--replace选项，它将自动替换掉所有具有相同键的记录。具体来说，在插入新行之前，MySQL会先删除具有相同键的任何现有行，然后再插入新行。
mysql> source d:/path/to/sql/file.sql --force

使用--ignore选项，它将忽略所有具有相同键的记录。具体来说，在插入新行时，如果该行具有与现有行相同的唯一索引或主键，则MySQL将跳过该行而不进行插入。
mysql> source d:/path/to/sql/file.sql --ignore

#### 系统行命令

```sql
mysql -u [用户名] -p [数据库名] < [输入文件名].sql 2>&1 | tee [输出文件名].txt

mysql -u root -p db_name < d:\Download\ate_2023.sql
```

> 注意：
> 1、导入备份数据库前，需要存在 db_name 库； 而且与db_name.sql中数据库名是一样的才可以导入。
> 2、导入时加上 **--skip-replace** 参数，则不覆盖已经存在的数据库对象
> 3、运算符(<)表示导入。

2>&1将错误输出重定向到标准输出，tee [输出文件名].txt将标准输出同时输出到终端和指定的输出文件中。

这样，当你执行SQL文件时，会在终端上看到类似source命令的输出，并将其保存到指定的输出文件中。


## 日志

查看日志
SHOW GLOBAL VARIABLES LIKE '%log%';

日志文件路径
mysql> show variables like 'general_log_file';

错误日志文件路径
mysql> show variables like 'log_error';

慢查询日志文件路径
mysql> show variables like 'slow_query_log_file';

## 变量

[MySQL中全局变量、会话变量、用户变量和局部变量的区别](https://blog.csdn.net/albertsh/article/details/103421646)



## 报错


[django.db.utils.InternalError: (1153, "Got a packet bigger than 'max_allowed_packet' bytes")](https://blog.csdn.net/zhouzhiwengang/article/details/118192674)



[mysql登录报错：ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)](https://www.cnblogs.com/zhongyehai/p/10695334.html)



## 配置文件解读

查看mysql服务器的所有全局配置信息：

show global variables;


showglobal variables like "%max_connections%";

- max_connections：允许的最大连接数

MySQL默认允许的最大连接数取决于所使用的MySQL版本和配置。在MySQL 5.7及更高版本中，默认的最大连接数是150。

这个值可以通过在MySQL配置文件中设置 max_connections 参数来修改。此参数的值可以根据您的特定需求进行修改。如果需要更多的连接，可以将此参数的值增加到适当的水平，但需要注意系统资源的限制和性能问题。

- wait_timeout：连接超时时间

默认情况下，MySQL服务器会在8小时后关闭空闲连接，此超时时间由wait_timeout参数控制。

wait_timeout参数定义了一个客户端连接在没有任何活动（即没有发送任何查询）的情况下可以保持打开状态的时间量。

如果在这段时间内没有任何活动，则服务器将断开与客户端的连接。在MySQL中，连接的超时时间取决于wait_timeout参数的值和MySQL服务器上当前的负载情况。

除此之外，还有一些其他的MySQL配置选项可以影响连接的超时时间，比如 interactive_timeout 参数。需要根据实际情况来设置这些参数以达到最佳性能。



- interactive_timeout：交互超时时间

interactive_timeout参数是MySQL服务器的一个系统变量，它控制了一个交互式客户端连接可以保持打开状态的最长时间。

当一个MySQL客户端连接被标记为“交互式”时，此参数就会生效。在默认情况下，MySQL客户端连接被认为是交互式的，并且此参数的默认值为28800秒（8小时）。

如果在此时间段内没有任何活动，则MySQL服务器将关闭连接。这个活动可以是发送一个查询、接收一个响应、发送一个提示符或者任何其他的交互式操作。

通过调整interactive_timeout参数的值，可以根据实际需求来控制连接的超时时间。如果您需要更短的超时时间，可以减少此参数的值；如果您希望延长连接保持打开的时间，可以增加此参数的值。

需要注意的是，修改interactive_timeout参数的值可能会对MySQL服务器的性能产生影响，因此需要谨慎设置。



- Max_used_connections

显示已连接数
show global status like 'Max_used_connections';

显示最大连接数
show variables like '%max_connections%';


mysql> show status like 'Threads%';

+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Threads_cached    | 58    |
| Threads_connected | 57    |   ###这个数值指的是打开的连接数
| Threads_created   | 3676  |
| Threads_running   | 4     |   ###这个数值指的是激活的连接数，这个数值一般远低于connected数值
+-------------------+--

mysql> show status like '%connect%';  
+-----------------------------------------------+---------+  
| Variable_name                                 | Value   |  
+-----------------------------------------------+---------+  
| Aborted_connects                              | 45643   |  
| Connection_errors_accept                      | 0       |  
| Connection_errors_internal                    | 0       |  
| Connection_errors_max_connections             | 2275689 |  
| Connection_errors_peer_address                | 15      |  
| Connection_errors_select                      | 0       |  
| Connection_errors_tcpwrap                     | 0       |  
| Connections                                   | 145379  |  
| Max_used_connections                          | 152     |  
| Performance_schema_session_connect_attrs_lost | 0       |  
| Ssl_client_connects                           | 0       |  
| Ssl_connect_renegotiates                      | 0       |  
| Ssl_finished_connects                         | 0       |  
| Threads_connected                             | 7       |  
+-----------------------------------------------+---------+ 

mysql> show variables like '%connect%'; 


计算每个表有多少行数据
```sql
SELECT table_name, table_rows
FROM information_schema.tables
WHERE table_schema = 'your_database_name';

```

SELECT COUNT(*) FROM 表名;



## UNION

```sql
//基础查询
SELECT `time`,`desc` 
FROM survey_testcase 
WHERE parent_id_id 
    IN (SELECT id FROM survey_testproject WHERE `name`='ABWRK-Printer' AND result='Pass') 
    AND `name`='1.9 显示BLE MAC地址';

//链表查询
SELECT t.barcode, tc.time, tc.desc as mac
FROM survey_testcase tc
JOIN survey_testproject t ON t.id = tc.parent_id_id
WHERE t.name = 'ABWR-Printer' AND t.result = 'Pass' AND tc.name = '1.9 显示BLE MAC地址';

SELECT t.barcode, tc.time, tc.desc as esn
FROM survey_testcase tc
JOIN survey_testproject t ON t.id = tc.parent_id_id
WHERE t.name = 'ABWR-Printer' AND t.result = 'Pass' AND tc.name = '1.b 显示ESN';

//合并后

SELECT t.barcode, tc.time, tc.desc AS mac_or_esn
FROM survey_testcase tc
JOIN survey_testproject t ON t.id = tc.parent_id_id
WHERE t.name = 'ABWR-Printer' AND t.result = 'Pass' 
AND (tc.name = '1.9 显示BLE MAC地址' OR tc.name = '1.b 显示ESN');


SELECT t.barcode, tc.time, NULL AS esn, tc.desc AS mac
FROM survey_testcase tc
JOIN survey_testproject t ON t.id = tc.parent_id_id
WHERE t.name = 'ABWR-Printer' AND t.result = 'Pass' AND tc.name = '1.9 显示BLE MAC地址'
UNION ALL
SELECT t.barcode, tc.time, tc.desc AS esn, NULL AS mac
FROM survey_testcase tc
JOIN survey_testproject t ON t.id = tc.parent_id_id
WHERE t.name = 'ABWR-Printer' AND t.result = 'Pass' AND tc.name = '1.b 显示ESN';

```

在合并后的命令中，使用了一个新的列别名mac_or_esn用于表示mac和esn两个不同的列。

通过在WHERE子句中使用OR运算符，可以选择具有名称为 '1.9 显示BLE MAC地址' 或 '1.b 显示ESN' 的行。

[MySQL查出所有的主外键关系、级联关系,并记录起来，删除所有的外键关系，根据记录重新建立外键关系](https://www.cnblogs.com/SuperSuperWang/p/17374495.html)

```sql
SELECT
    kcu.constraint_name,
    kcu.column_name,
    kcu.referenced_table_name,
    kcu.referenced_column_name,
    rc.UPDATE_RULE,
    rc.delete_rule
FROM
    information_schema.KEY_COLUMN_USAGE AS kcu
    JOIN information_schema.REFERENTIAL_CONSTRAINTS AS rc ON kcu.CONSTRAINT_NAME  = rc.CONSTRAINT_NAME 
WHERE
    kcu.table_schema = 'test' AND kcu.table_name = 'survey_testproject';

```
[MySql 外键约束 之CASCADE、SET NULL、RESTRICT、NO ACTION分析和作用](https://www.cnblogs.com/yzuzhang/p/5174720.html)

### 优化查询逻辑

1. 避免使用函数在 WHERE 子句中

在 WHERE 子句中使用 DATE(time) 会导致 MySQL 不能使用索引，可以通过其他方式来优化查询。例如，使用 BETWEEN 或直接比较时间范围

```sql
SELECT
    `name`,
    COUNT(*) AS total_count,
    SUM(CASE WHEN result = 'Pass' THEN 1 ELSE 0 END) AS success_count,
    SUM(CASE WHEN result = 'Fail' THEN 1 ELSE 0 END) AS fail_count
FROM
    survey_testproject
WHERE
    `time` >= CURDATE() AND `time` < CURDATE() + INTERVAL 1 DAY
GROUP BY `name`;
```

