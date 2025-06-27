SELECT
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
FROM
    information_schema.key_column_usage
WHERE
    table_name = 'keyword_trigger_records'
    AND column_name = 'account_id';



ALTER TABLE keyword_trigger_records DROP FOREIGN KEY keyword_trigger_records_ibfk_1;


DROP INDEX account_id ON keyword_trigger_records;


def upgrade():
    # 删除外键约束
    op.drop_constraint('keyword_trigger_records_ibfk_1', 'keyword_trigger_records', type_='foreignkey')
    # 删除索引
    op.drop_index('account_id', table_name='keyword_trigger_records')



-- 查看数据库字符集
SHOW VARIABLES LIKE 'character_set%';

-- 查看表字符集
SHOW CREATE TABLE monitor_account_stats;

-- 查看列字符集
SHOW FULL COLUMNS FROM monitor_account_stats;



ALTER DATABASE your_database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

ALTER DATABASE test CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


ALTER TABLE monitor_accounts CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE monitor_account_stats CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE keyword_trigger_records CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE data_posts CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE data_replies CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE monitor_account_stats MODIFY account_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE data_replies MODIFY account_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;






SELECT CONCAT('ALTER DATABASE ', SCHEMA_NAME, ' CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;')
FROM INFORMATION_SCHEMA.SCHEMATA
WHERE SCHEMA_NAME = '你的数据库名';

SELECT CONCAT('ALTER TABLE ', TABLE_NAME, ' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = '你的数据库名';

SELECT CONCAT('ALTER TABLE ', TABLE_NAME, ' MODIFY ', COLUMN_NAME, ' ', COLUMN_TYPE, ' CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = '你的数据库名'
AND (COLUMN_TYPE LIKE '%varchar%' OR COLUMN_TYPE LIKE '%text%');



SHOW INDEX FROM data_posts;

ALTER TABLE data_posts DROP INDEX url;


-- 查看表的索引和约束
SHOW INDEX FROM data_replies;

-- 查找名为 'unique_url' 的约束
SELECT CONSTRAINT_NAME, COLUMN_NAME 
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
WHERE TABLE_NAME = 'data_replies' 
  AND CONSTRAINT_NAME = 'unique_url';

ALTER TABLE data_replies DROP INDEX unique_url;



SELECT
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
FROM
    information_schema.key_column_usage
WHERE
    table_name = 'data_posts'
    AND column_name = 'url';




SELECT 
    traitor_id,
    account_id,
    COUNT(*) AS duplicate_count,
    MIN(create_time) AS first_occurrence,
    MAX(create_time) AS last_occurrence
FROM traitor_account_association
GROUP BY traitor_id, account_id
HAVING COUNT(*) > 1;


-- 创建临时表存储需要保留的记录
CREATE TEMPORARY TABLE keep_records AS
SELECT 
    traitor_id,
    account_id,
    MIN(create_time) AS min_create_time
FROM traitor_account_association
GROUP BY traitor_id, account_id;

-- 删除不在保留表中的记录
DELETE t
FROM traitor_account_association t
LEFT JOIN keep_records k 
    ON t.traitor_id = k.traitor_id 
    AND t.account_id = k.account_id
    AND t.create_time = k.min_create_time
WHERE k.traitor_id IS NULL;

-- 清理临时表
DROP TEMPORARY TABLE keep_records;