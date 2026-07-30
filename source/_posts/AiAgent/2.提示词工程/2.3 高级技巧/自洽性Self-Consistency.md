## 2.3 高级技巧：自洽性（Self-Consistency）

### 核心思想

同一个问题，让模型**用不同的推理路径采样多次**（高 temperature），再对最终答案**投票取多数**。直觉：正确推理往往殊途同归，错误推理则各说各话。

> 它是思维链（CoT）的升级版：CoT 只跑一次，Self-Consistency 跑多次再汇总。

### 流程

1. 把问题 + 「请一步步思考」给模型，temperature 调高（如 0.7~0.9）；
2. 采样 N 次（如 5~10 次），拿到 N 条带推理过程的回答；
3. 用正则/解析从每条里抽出「最终答案」；
4. 统计答案出现频次，选最多的那个作为输出。

### 代码示例

```python
import re
from collections import Counter
from openai import OpenAI
client = OpenAI()

def self_consistency(question: str, n: int = 7):
    answers = []
    for _ in range(n):
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.8,
            messages=[
                {"role": "system", "content": "请逐步推理，最后用『答案：X』给出结论。"},
                {"role": "user", "content": question}
            ]
        )
        text = r.choices[0].message.content
        m = re.search(r"答案[:：]\s*(.+)", text)
        if m:
            answers.append(m.group(1).strip())
    return Counter(answers).most_common(1)[0][0]  # 多数票

print(self_consistency("一个农场有鸡和兔共35只，脚共94只，鸡几只？"))
```

### 效果与代价

- 在数学推理、常识题、逻辑题上，准确率通常比单次 CoT 提升 5%~15%；
- 代价是 **N 倍 Token 和延迟**，不适合对实时性要求高的在线场景；
- 常作为「离线精算 / 关键决策」的增强手段，而非每条消息都用。

### 适用边界

- 适合**有唯一正确答案**的任务（数学、选择题、分类）；
- 不适合开放式创作（写诗、写文案没有「多数票」概念）；
- 可和结构化输出结合：每条都要求输出 JSON，再对关键字段投票。
