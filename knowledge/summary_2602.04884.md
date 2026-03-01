# Reinforced Attention Learning

## 基本信息
- arXiv ID: 2602.04884
- 作者: Bangzheng Li*, Chen Qu, Jianmo Ni, Ian Miao, Liu Yang, Xingyu Fu, Muhao Chen, Derek Zhiyuan Cheng, Zhong Cheng (UC Davis + Princeton + Google + Google DeepMind)

## 核心方法

本文提出**Reinforced Attention Learning (RAL)**，一个直接优化Transformer内部attention分布而非输出token序列的策略梯度框架。

### 核心思想
传统RLHF方法优化"生成什么"（next-token概率），RAL优化"关注哪里"（attention分布）。

### 1. Attention作为策略
- 将attention分布本身视为策略$\pi(a|h)$
- 当响应获得高奖励时，通过最小化当前策略与参考策略的KL散度来强化该attention分布
- 当响应获得低奖励时，增大与次优模式的KL散度进行惩罚

### 2. On-Policy Attention Distillation
结合标准知识蒸馏和attention蒸馏的**双重蒸馏**方法：
- Token-level distillation: 匹配输出token概率
- Attention-level distillation: 匹配教师模型的attention分布

这种方法使学生模型能够继承教师模型的细粒度感知和视觉定位能力。

## 实验结果

### Image QA Benchmarks
| 方法 | MMBench | MMMU | SEED | MathVista |
|------|---------|------|------|-----------|
| GRPO | 基线 | 基线 | 基线 | 基线 |
| **RAL** | +4.2% | +3.8% | +5.1% | +6.3% |

### Video QA Benchmarks
| 方法 | TVQA | ActivityNet | MSRVTT-QA |
|------|------|-------------|-----------|
| GRPO | 基线 | 基线 | 基线 |
| **RAL** | +6.7% | +5.2% | +4.9% |

### On-Policy Distillation
- 加入attention distillation后，学生模型在细粒度视觉理解任务上显著优于纯token蒸馏
- 证明attention behaviors的迁移对跨模态对齐有重要价值

## 关键贡献

1. **范式转换**：从优化token序列转向优化attention分布，直接强化视觉定位能力
2. **方法创新**：
   - 将attention分布形式化为策略
   - 设计针对attention的策略梯度更新规则
   - 提出On-Policy Attention Distillation
3. **实证验证**：
   - 在多样化的image和video benchmarks上持续超越GRPO
   - 特别在感知密集型任务上效果显著
4. **理论意义**：证明attention policy是一种原则性强且通用的多模态后训练替代方案
