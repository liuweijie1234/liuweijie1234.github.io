## 3.3 检索策略：重排序（Reranker）

### 为什么需要 Reranker

向量检索（召回）追求「快且广」，但第一关召回的 Top-K 里，**真正相关的不一定排在最前**。Reranker 就是「多路召回后用 BGE-Reranker 做精排」——目前 RAG 提效的标配技术。

一句话：**召回（Retrieval）负责把候选拉进来，重排（Rerank）负责把对的顶上去。**

### 工作原理

Reranker 是一个 Cross-Encoder 模型：把「查询 + 文档」**拼在一起**喂给模型，直接输出一个相关性分数。因为能看到 query 和 doc 的全局交互，比单纯的向量内积准得多。

```
召回 Top-20（快但粗）
   ↓ 全部送 Reranker 打分
精排 Top-5（准且相关）
   ↓ 喂给 LLM 生成
```

### 代码示例（用 FlagEmbedding / BGE）

```python
from FlagEmbedding import FlagReranker

reranker = FlagReranker("BAAI/bge-reranker-v2-m3", use_fp16=True)

pairs = [
    ("用户问题", "候选文档1内容"),
    ("用户问题", "候选文档2内容"),
    # ...
]
scores = reranker.compute_score(pairs)
# 按分数降序取前 N
```

### 选型

- 中文首选 **BGE-Reranker**（BAAI 出品，中英文都强）；
- 也可用 Cohere Rerank（API 托管）、Jina Reranker；
- 本地部署用 `bge-reranker-base/large`，注意显存占用。

### 使用建议

- 召回 `top_k=20~50`，Rerank 后取 `top_k=3~8` 给模型，效果与成本最均衡；
- Reranker 比向量检索慢，别在召回阶段用，只用在「已缩小的候选集」上；
- 是小成本、大收益的典型优化点，RAG 上线前强烈建议加一层。

### 经验

很多 RAG「答非所问」的根源不是模型弱，而是**最相关的块排在第 8 位被截断了**。加 Reranker，往往立竿见影。
