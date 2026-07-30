## 10.4 数据分析 Agent

### 项目定位

用户用自然语言问业务问题（如「上个月各渠道转化率多少？画个图」），Agent 自动生成并执行 SQL、做分析、出图表和结论。是「Text-to-SQL + 代码执行 + 可视化」的典型应用。

### 核心能力

- **自然语言 → SQL**：把用户问题翻译成查数据库的 SQL；
- **安全执行**：SQL 经校验（只读、限表）后在内网数据库执行，绝不裸跑；
- **图表生成**：用 Python（matplotlib / plotly）画图；
- **结论总结**：基于查询结果和图表，用 LLM 输出业务结论与建议。

### 技术要点

1. **Schema 注入**：把表结构（表名、字段、类型、注释）作为上下文注入，模型才知道怎么写 SQL；
2. **SQL 安全防护**：
   - 只允许 `SELECT`，拦截 `DROP/UPDATE/DELETE`；
   - 白名单限制可访问的表；
   - 参数化查询防注入；
3. **代码沙箱**：图表代码在受限沙箱（限时、限资源、禁网络）执行；
4. **多步规划**：复杂问题先拆成「取数→计算→可视化→解读」子任务。

### 关键代码片段（SQL 安全校验）

```python
def safe_sql(sql: str) -> bool:
    forbidden = ["drop", "delete", "update", "insert", "alter", ";"]
    low = sql.lower()
    return low.strip().startswith("select") and not any(w in low for w in forbidden)
```

### 难点与解法

- 复杂 join 写错 → 给模型表关系图 + few-shot 示例；
- 幻觉字段名 → 严格用真实 schema，禁止编造列；
- 大结果集 → 聚合/分页后再进模型，控 token。

### 收获

融合 Text-to-SQL、权限安全、代码沙箱、数据可视化，是「Agent 落地业务」的高价值作品，尤其受数据/分析岗青睐。
