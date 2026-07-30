Agent 的 “外部知识库”，解决知识时效性和私有数据问题

基础原理：Embedding 嵌入原理、完整 RAG 全流程（解析→分块→向量化→检索→生成）
文档处理：多格式解析（PDF/Word/ 表格 / 图片）、固定分块、语义分块、分块策略对比
向量数据库：选型对比（Chroma/Milvus/Pinecone 等）、索引创建、检索语法、性能优化
进阶优化：多路召回、BGE/Reranker 重排序、父文档检索、HyDE、Graph RAG
效果调优：召回率 / 准确率评估、Bad Case 优化思路


03_RAG检索增强生成
├── 3.1 数据预处理管道
│   ├── 文档解析（PDF, Markdown, HTML）
│   ├── 智能分割策略（递归分割、语义分割）
│   └── 元数据提取与维护
├── 3.2 嵌入与向量存储
│   ├── Embedding模型选型（text-embedding-3, bge-large）
│   ├── 向量数据库对比（Chroma, Milvus, Pinecone, Weaviate）
│   └── 索引与更新策略
├── 3.3 检索策略
│   ├── 稠密检索 vs 稀疏检索（BM25）
│   ├── 混合检索与重排序（Rerank）
│   └── 多路召回与融合
├── 3.4 生成增强
│   ├── 上下文注入与引用来源标注
│   └── 防止幻觉的约束提示词
└── 3.5 高级RAG范式
    ├── 自我反思RAG（Self-RAG）
    ├── 图RAG（Graph RAG）
    └── Agent驱动的主动RAG