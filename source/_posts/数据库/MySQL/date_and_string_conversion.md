---
title: MySQL 日期和字符串转换、日期查询
date: 2022-08-15 11:42:00
tags:
- MySQL
categories:
- 数据库
---


[mysql 日期和字符串相互转化](https://blog.csdn.net/qq_33157666/article/details/78385115)

[sql 语句查询今天、昨天、近 7 天、近 30 天、一个月内、上一月 数据](https://blog.csdn.net/allWords/article/details/78357307)

[SQL 计算一个月的第一天和最后一天](https://geek-docs.com/sql/sql-examples/sql-calculation-on-the-first-day-of-a-month-and-the-last-day.html)

[【Mysql-3】条件判断函数-CASE WHEN、IF、IFNULL 详解](https://cloud.tencent.com/developer/article/1698429)

[MySQL 通过 sql 语句获取当前日期|时间|时间戳](https://blog.csdn.net/llwan/article/details/40345349)

[mysql 时间戳格式化函数 from_unixtime 使用说明](https://blog.csdn.net/fdipzone/article/details/51018930)

[SQL Date 函数](https://www.w3school.com.cn/sql/sql_dates.asp)
[MySQL DATE_SUB() 函数](https://www.w3school.com.cn/sql/func_date_sub.asp)

[DATE_FORMAT(date,format) 函数](https://www.w3school.com.cn/sql/func_date_format.asp)


```sql
NOW()	返回当前的日期和时间
CURDATE()	返回当前的日期
CURTIME()	返回当前的时间
DATE()	提取日期或日期/时间表达式的日期部分
EXTRACT()	返回日期/时间按的单独部分
DATE_ADD()	给日期添加指定的时间间隔
DATE_SUB()	从日期减去指定的时间间隔
DATEDIFF()	返回两个日期之间的天数
DATE_FORMAT(date,format)	用不同的格式显示日期/时间,
PERIOD_DIFF()   函数返回两日期之间的差异。结果以月份计算。

SELECT NOW();
SELECT CURDATE();
SELECT CURTIME();

SELECT DATE_SUB(NOW(), INTERVAL 30 DAY);
SELECT DATE_SUB(CURDATE(), INTERVAL 0 DAY);
SELECT DATE_SUB(CURDATE(), INTERVAL 7 DAY);
SELECT DATE_SUB(CURDATE(), INTERVAL 30 DAY);
SELECT DATE_SUB(now(),INTERVAL 1 MONTH);
SELECT DATE_SUB(now(),INTERVAL 2 MONTH);

SELECT PERIOD_DIFF( date_format( now( ) , '%Y%m%d' ) , date_format( '2022-05-13 19:26:29', '%Y%m' ) ) =1;

where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date();
```
```sql
# 近30天时间返回

# 当前一个月时间范围
select DATE_FORMAT(date_add(current_date, interval -day(current_date)+1 day ), '%Y-%m-%d %H:%i:%S') firstday, CONCAT (last_day(current_date), ' 23:59:59') lastday;

# 上一个月的时间范围
select DATE_FORMAT(date_add(date_sub(current_date, interval 1 month), interval -day(current_date)+1 day), '%Y-%m-%d %H:%i:%S') firstday, CONCAT (last_day(date_sub(current_date, interval 1 month)), ' 23:59:59') lastday;

# 近一月的单据
SELECT title,module,created,status,version_report FROM static_tapd_bug_tapdbug WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') AND workspace_id=20415412;
SELECT title,module,created,status,version_report FROM static_tapd_bug_tapdbug WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') AND status in ('new','in_progress','reopened')  AND workspace_id=20415412;

# 近一个月各产品出现的次数
SELECT module,COUNT(module) FROM static_tapd_bug_tapdbug WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') AND workspace_id=20415412 group by module;

# 上个月的单据
SELECT bug_id,title,module,created FROM static_tapd_bug_tapdbug WHERE PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 AND workspace_id=20415412 group by module;

# 上个月各产品出现的次数
SELECT module,COUNT(module) FROM static_tapd_bug_tapdbug WHERE PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 AND workspace_id=20415412 group by module;
```

[mysql 之 any，in，some，all 的区别](https://blog.csdn.net/LY_Dengle/article/details/78027398)


[SQL CONCAT 函数](https://wiki.jikexueyuan.com/project/sql/useful-functions/concat-function.html)
[SQL CONCAT 函数-w3school](https://www.w3school.com.cn/sql/sql_func_count.asp)
```sql
SELECT module,30days_count,30days_news_count,last_month_count,last_month_news_count,now,30days,last_month_firstday,last_month_lastday
FROM (
    SELECT module,
    sum(case when DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') then 1 else 0 end) as 30days_count,
    sum(case when DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') AND status in ('new','in_progress','reopened') then 1 else 0 end) as 30days_news_count,
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%S') as now,
    DATE_FORMAT(DATE_SUB(now(), INTERVAL 30 DAY), '%Y-%m-%d %H:%i:%S') as 30days,
    sum(case when PERIOD_DIFF( DATE_FORMAT( now( ) , '%Y%m' ) , DATE_FORMAT( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 then 1 else 0 end) as last_month_count,
    sum(case when PERIOD_DIFF( DATE_FORMAT( now( ) , '%Y%m' ) , DATE_FORMAT( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 AND status in ('new','in_progress','reopened') then 1 else 0 end) as last_month_news_count,
    DATE_FORMAT(date_add(date_sub(current_date, interval 1 month), interval -day(current_date)+1 day), '%Y-%m-%d %H:%i:%S') last_month_firstday,
    CONCAT (last_day(date_sub(current_date, interval 1 month)), ' 23:59:59') last_month_lastday
    FROM static_tapd_bug_tapdbug 
    WHERE version_report like '%社区版%' AND workspace_id=20415412
    group by module
) a
group by module
order by 30days_count desc
```
```sql
SELECT module,30days_count,30days_news_count,last_month_count,last_month_news_count 
FROM ( 
    SELECT 
    module, sum(case when DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') then 1 else 0 end) as 30days_count, sum(case when DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') AND status in ('new','in_progress','reopened') then 1 else 0 end) as 30days_news_count, sum(case when PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 then 1 else 0 end) as last_month_count, sum(case when PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 AND status in ('new','in_progress','reopened') then 1 else 0 end) as last_month_news_count 
    FROM static_tapd_bug_tapdbug  
    WHERE version_report like '%社区版%' AND workspace_id=20415412 group by module
    ) a 
    group by module 
    order by 30days_count desc;
```


[SQL HAVING 子句](https://www.runoob.com/sql/sql-having.html)
```sql
SELECT module,30days_count,30days_news_count,30days_solved_count,last_month_count,last_month_news_count,last_month_solved_count
FROM (
    SELECT module,
    sum(case when DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') then 1 else 0 end) as 30days_count,
    sum(case when DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') AND status in ('new','in_progress','reopened') then 1 else 0 end) as 30days_news_count,
    sum(case when DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= str_to_date(created, '%Y-%m-%d %H:%i:%S') AND status in ('resolved','assigned','verified') then 1 else 0 end) as 30days_solved_count,
    sum(case when PERIOD_DIFF( DATE_FORMAT( now( ) , '%Y%m' ) , DATE_FORMAT( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 then 1 else 0 end) as last_month_count,
    sum(case when PERIOD_DIFF( DATE_FORMAT( now( ) , '%Y%m' ) , DATE_FORMAT( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 AND status in ('new','in_progress','reopened') then 1 else 0 end) as last_month_news_count,
    sum(case when PERIOD_DIFF( DATE_FORMAT( now( ) , '%Y%m' ) , DATE_FORMAT( str_to_date(created, '%Y-%m-%d %H:%i:%S'), '%Y%m' ) ) =1 AND status in ('resolved','assigned','verified') then 1 else 0 end) as last_month_solved_count
    FROM static_tapd_bug_tapdbug 
    WHERE version_report like '%社区版%' AND workspace_id=20415412
    group by module
) a
group by module
having (30days_count > 0) or (30days_news_count > 0) or (30days_solved_count > 0) or (last_month_count > 0) or (last_month_news_count > 0) or (last_month_solved_count > 0)
order by 30days_count desc 
```

```sql
SELECT module, 7days_count, 30days_count, 7days_news_count, 30days_news_count
FROM (
    SELECT module, 
    sum(case when status='new' then 1 else 0 end) as 7days_count,
    sum(case when status='in_progress' then 1 else 0 end) as 30days_count,
    sum(case when status='reopened' then 1 else 0 end) as 7days_news_count,
    sum(case when status in ('resolved', 'assigned') then 1 else 0 end) as 30days_news_count
    FROM static_tapd_bug_tapdbug
    WHERE version_report like '%社区版%' AND workspace_id=20415412 
    group by module
) a
group by module
order by 30days_count desc
```

## 具体案例

[MySQL 统计过去12个月每个月的数据信息](https://blog.csdn.net/liudachu/article/details/109258858)

工厂查询

计算每月产测平均耗时+产测数量
```sql
SELECT DATE_FORMAT(TIME, '%Y-%m') AS TIME, ROUND(AVG(spend),2) AS spend , count(id) AS count 
FROM survey_testproject
GROUP BY DATE_FORMAT(TIME,'%Y-%m')
ORDER BY TIME DESC
LIMIT 24;
```


计算每个月ESN数量
```sql
SELECT DATE_FORMAT(create_time, '%Y-%m') AS TIME, count(id) AS count 
FROM services_bluetooth
GROUP BY DATE_FORMAT(create_time,'%Y-%m')
ORDER BY TIME DESC
LIMIT 24;
```

阿里云查询


计算每月装备包数量
select DATE_FORMAT(upload_time, '%Y-%m') AS TIME, count(id) AS count 
from deploy_projectpackage
GROUP BY DATE_FORMAT(upload_time,'%Y-%m')
ORDER BY upload_time DESC
LIMIT 12;


计算每月FT装备包数量 FT

select DATE_FORMAT(upload_time, '%Y-%m') AS TIME, count(id) AS count 
from deploy_projectpackage
WHERE file_name LIKE '%FT%'
AND file_name not LIKE '%SFT%'
GROUP BY DATE_FORMAT(upload_time,'%Y-%m')
ORDER BY upload_time DESC
LIMIT 12;


计算每月SFT装备包数量 SFT
select DATE_FORMAT(upload_time, '%Y-%m') AS TIME, count(id) AS count 
from deploy_projectpackage
WHERE file_name LIKE '%SFT%'
GROUP BY DATE_FORMAT(upload_time,'%Y-%m')
ORDER BY upload_time DESC
LIMIT 12;


计算每月MBT装备包数量
select DATE_FORMAT(upload_time, '%Y-%m') AS TIME, count(id) AS count 
from deploy_projectpackage
WHERE file_name LIKE '%MBT%'
GROUP BY DATE_FORMAT(upload_time,'%Y-%m')
ORDER BY upload_time DESC
LIMIT 12;

```sql
SELECT
    DATE_FORMAT(upload_time, '%Y-%m') AS TIME,
    COUNT(id) AS total_count,
    SUM(CASE WHEN file_name LIKE '%FT%' AND file_name NOT LIKE '%SFT%' THEN 1 ELSE 0 END) AS ft_count,
    SUM(CASE WHEN file_name LIKE '%SFT%' THEN 1 ELSE 0 END) AS sft_count,
    SUM(CASE WHEN file_name LIKE '%MBT%' THEN 1 ELSE 0 END) AS mbt_count
FROM deploy_projectpackage
GROUP BY DATE_FORMAT(upload_time, '%Y-%m')
ORDER BY upload_time DESC
LIMIT 12;
```

# 性能

不要使用子查询，尽量使用链表查询

[SQL 多表查询：SQL JOIN 连接查询各种用法总结](https://zhuanlan.zhihu.com/p/68136613)