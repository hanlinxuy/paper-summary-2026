# Evaluating the Ability of Explanations to Disambiguate Models in a Rashomon Set

## 基本信息
- arXiv ID: 2601.08703
- 作者: Kaivalya Rawal, Eoin Delaney, Zihao Fu, Sandra Wachter, Chris Russell

## 核心方法

**研究背景**：对于形成Rashomon集合的相似性能模型，解释提供了一种区分个体模型行为的方式。但解释本身可能因使用的解释器而异，需要评估。

**核心方法**：

1. **三个评估原则**：
   - 局部上下文化(Local Contextualization)：解释应依赖于输入数据点
   - 模型相对主义(Model Relativism)：解释应依赖于特定模型
   - 流形上评估(On-Manifold Evaluation)：解释应仅依赖于流形上的模型行为

2. **AXE框架**：ground-truth Agnostic eXplanation Evaluation
   - 好的解释是正确识别对模型输出最具预测性的特征
   - 满足所有三个评估原则
   - 基于k-NN预测性度量

3. **对抗性公平清洗攻击检测**：
   - 攻击者使用Rashomon集合中的不同模型来掩盖歧视性预测
   - AXE可100%检测这种攻击

## 实验结果

**关键发现**：
- 传统评估指标如PGI、PGU无法检测对抗性公平清洗攻击
- PGI和PGU错误率达50%
- AXE错误率为0%（完全检测攻击）

**表：评估指标比较**

| 指标 | P1(局部) | P2(相对) | P3(流形) |
|------|---------|---------|----------|
| FA/RA/SA/SRA/RC/PRA | ❌ | ❌ | ✅ |
| PGI/PGU | ✅ | ✅ | ❌ |
| **AXE** | ✅ | ✅ | ✅ |

## 关键贡献

1. **三个评估原则**：为特征重要性解释评估提供理论指导

2. **AXE框架**：
   - 首个满足所有三个原则的解释评估方法
   - 可检测对抗性公平清洗攻击
   - 100%检测成功率

3. **揭示现有指标缺陷**：证明基于ground-truth和敏感性的评估指标在Rashomon集合场景下的失效

4. **实践意义**：帮助从Rashomon集合中选择模型时保持相同预测但识别真实使用的特征
