# RLAnything: Forge Environment, Policy, and Reward Model in Completely Dynamic RL System

## 基本信息
- arXiv ID: 2602.02488
- 作者: Yinjie Wang, Tianbao Xie, Ke Shen, Mengdi Wang, Ling Yang

## 核心方法

本文提出**RLAnything**，一个完全动态的强化学习框架，通过闭环优化同时锻造（forge）环境、策略和奖励模型三大组件：

### 1. 策略训练 - 集成反馈机制
$$R_{\tau_i} = O_{\tau} + \frac{\lambda}{m}\sum_{j=1}^{m} S_{\tau_i,j}$$

- $O_{\tau}$: 最终结果奖励（-1或1）
- $S_{\tau_i,j}$: 奖励模型对第i步的m次采样评估
- 优势函数通过同一步骤的奖励标准化计算

### 2. 奖励模型训练 - 一致性反馈
$$R_{S_{\tau_i,j}} = R_{\tau_i} \cdot S_{\tau_i,j}$$

- 将策略的轨迹作为奖励模型的训练环境
- 利用结果监督和自一致性信号联合优化奖励模型

### 3. 环境自适应 - 批评反馈
- 根据策略的rollout准确率调整任务难度
- 使用奖励模型的评估信息总结错误模式
- 通过语言模型自动修改任务（变难或变易）

### 理论保证
- **定理1**：当$\mu = p_+ + p_- > 1$时，随着采样次数$m \to \infty$，奖励精度$\mathcal{A} \to 1$
- **定理2**：任务难度过难或过轻会导致重要性采样不平衡，损害奖励模型训练

## 实验结果

### GUI Agent (OSWorld)
| 模型 | In-Domain | OOD | 提升 |
|------|-----------|-----|------|
| 基线 | 40.4% | 16.1% | - |
| Policy | 48.3% | 19.8% | +8.1% |
| Policy + Reward | 49.6% | 20.0% | +9.2% |
| **RLAnything** | **52.8%** | **22.0%** | **+12.4%** |

**Qwen3-VL-8B-Thinking在OSWorld上提升9.1%**

### LLM Agent (AlfWorld)
| 配置 | In-Domain | OOD |
|------|-----------|-----|
| 基线 | 39.0% | 44.9% |
| Policy + Reward + Env | **57.0%** | **64.3%** |

**Qwen2.5-7B-Instruct在AlfWorld上提升18.7%，LiveBench上提升11.9%**

### 奖励模型准确性
- 优化后的奖励模型在step-level正确性评估和outcome预测上均显著提升
- 优于依赖人工标签的结果信号

## 关键贡献

1. **框架创新**：提出RLAnything，通过闭环优化同时锻造环境、策略和奖励模型
2. **理论贡献**：
   - 证明任务难度平衡对奖励模型训练的重要性
   - 建立奖励精度与采样密度的数学关系
3. **方法创新**：
   - 集成反馈：结合step-wise和outcome信号
   - 一致性反馈：联合优化奖励模型
   - 环境自适应：基于批评反馈自动调整任务难度
4. **实证成果**：
   - 在计算机控制、文本游戏、编码等场景取得显著提升
   - 优化的奖励模型信号优于人工标签
