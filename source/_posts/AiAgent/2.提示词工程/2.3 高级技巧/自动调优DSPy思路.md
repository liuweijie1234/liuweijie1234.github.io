## 2.3 高级技巧：自动调优（DSPy 思路）

### 痛点

手写提示词像「调参炼丹」：改一句话、换几个示例，效果时好时坏，全靠人工试。DSPy 想做的事是——**把提示词当成可优化程序，用数据自动搜出最优版本**。

### DSPy 的核心抽象

- **Signature（签名）**：声明「输入是什么、输出是什么」，不管提示词怎么写。
  `question -> answer` 或 `context, question -> answer`
- **Module（模块）**：把 Signature 套进某种推理模式（ChainOfThought、ReAct 等）。
- **Teleprompter（提示优化器）**：用一批标注样本，自动调整提示词里的指令和 few-shot 示例。

### 极简示意

```python
import dspy

dspy.settings.configure(lm=dspy.OpenAI(model="gpt-4o-mini"))

class QA(dspy.Signature):
    """回答用户问题。"""
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()

qa = dspy.ChainOfThought(QA)

# 用少量样本自动优化提示词（BootstrapFewShot 会搜出最好的 few-shot 组合）
from dspy.teleprompt import BootstrapFewShot
optimizer = BootstrapFewShot(metric=your_accuracy_metric)
optimized = optimizer.compile(qa, trainset=your_samples)
```

### 和传统写提示词的区别

| 方式 | 提示词来源 | 优化手段 |
| -- | -- | -- |
| 手写提示词 | 人脑构思 + 试错 | 手动改字 |
| DSPy | 声明式 Signature + 自动编译 | 用数据驱动搜索 few-shot / 指令 |

### 价值与门槛

- 价值：当样本多、提示词频繁变时，DSPy 能稳定产出优于手调的版本，且可复现。
- 门槛：需要一批标注数据（trainset）和评价指标；对简单任务有点「杀鸡用牛刀」。
- 思路可迁移：即使不引入 DSPy，也可以借鉴「准备样本集 + 自动 A/B 评估」的方式迭代提示词，而不是盲调。

### 小白建议

- 先把手写提示词打磨到「能用」；
- 当任务变复杂、要维护多套提示词时，再引入 DSPy 这类框架做自动优化；
- 日常可用「固定测试集 + 自动跑分脚本」模拟它的核心思想，成本低很多。
