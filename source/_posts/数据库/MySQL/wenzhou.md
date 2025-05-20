
## 查询指定项目产测记录总数

```sql
SELECT `name`, COUNT(*) AS `count`
FROM survey_testproject 
WHERE `name` LIKE 'K5929%'
GROUP BY `name`;
```

```sql
SELECT 
  `name`, 
  SUM(result = 'Pass') AS `Pass`,
  SUM(result = 'Fail') AS `Fail`
FROM 
  survey_testproject 
WHERE 
  `name` REGEXP '_FT[0-9]?$' 
  AND LENGTH(barcode) >= 10 
  AND upload_user NOT IN ('admin', '打印专用')
  AND `time` BETWEEN '2024-01-01 00:00:00' AND '2024-07-01 00:00:00'
GROUP BY `name`;
```

## 取出最近一千条数据的id

珠海SN长度不等于22

```sql
SELECT id
FROM survey_testproject 
WHERE `name` LIKE 'K3AWZ_RK3%' 
AND `result` != 'Exce' 
AND LENGTH(barcode) >= 10 
AND upload_user NOT IN ('admin', '打印专用')
ORDER BY `id` DESC
LIMIT 1000;
```



## 计算最近一千条数据的整体通过数量、异常数量
```sql
SELECT 
  SUM(result = 'Pass') AS `Pass`,
  SUM(result = 'Fail') AS `Fail`,
FROM survey_testproject 
WHERE id IN (

)
```


# 查询1000条产测记录的产测测试项的通过数量、异常数量、取消数量

```sql
SELECT
  t1.`name` AS `name`,
  MAX(t1.`desc`) AS `desc`,
  SUM(t1.result = 'Fail') AS `Fail`
FROM 
  survey_testcase t1
WHERE 
  t1.parent_id_id IN (

  ) AND t1.result = 'Fail'
GROUP BY
  t1.name;
```


## 查询近一千条数据错误的SN和测试项


```sql
SELECT
  t0.`id` AS `ID`,
  t0.`barcode` AS `SN`,
  t0.`time` AS `time`,
  t0.`desc` AS `desc`,
  t1.name AS `name`,
  t1.desc AS `case_desc`,
  t1.result AS `result`,
  t2.`long_name` AS `long_name`,
  t2.`standard` AS `standard`,
  t2.`desc` AS `result_desc`
FROM 
  survey_testproject t0
LEFT JOIN
  survey_testcase t1 ON t0.id = t1.parent_id_id
LEFT JOIN
  survey_testresult t2 ON t1.id = t2.parent_id_id
WHERE 
  t1.parent_id_id IN (
  SELECT id
  FROM survey_testproject 
  WHERE `name` LIKE 'K3AWZ_RK3%' 
  AND `result` != 'Exce' 
  AND LENGTH(barcode) >= 10 
  AND upload_user NOT IN ('admin', '打印专用')
  ORDER BY `id` DESC
  LIMIT 1000;
  ) 
  AND t1.result = 'Fail'
  AND t2.time = (
    SELECT MAX(time) FROM survey_testresult WHERE parent_id_id = t1.id
  )
```

## 取出近一千条中 状态是Pass 或者 Fail 的数据

```sql
SELECT
id,barcode,`time`,result,`desc`,`name`
FROM 
survey_testproject
WHERE
id IN(

  )
ORDER BY `barcode` DESC
```






