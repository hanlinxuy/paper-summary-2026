# Safe-FedLLM: Delving into the Safety of Federated Large Language Models

## 基本信息
- arXiv ID: 2601.07177
- 作者: Mingxiang Tao, Yu Tian, Wenxuan Tu, Yue Yang, Xue Yang, Xiangyan Tang

## 核心方法

**研究背景**：联邦学习(FL)解决了大语言模型(LLM)中的数据隐私和数据孤岛问题，但安全防御研究不足。

**核心发现**：
1. LLM在联邦学习中容易受到恶意客户端攻击
2. LoRA权重表现出可区分的行为模式，可以通过简单分类器过滤

**Safe-FedLLM框架**：

1. **Step-Level Defense**：在每个训练步骤中检测异常
2. **Client-Level Defense**：对每个客户端的LoRA权重进行探测分类
3. **Shadow-Level Defense**：使用影子模型进行安全探测

**核心思想**：将LoRA权重视为高维行为特征，使用轻量级分类模型判断其是否具有恶意属性。

## 实验结果

**主要结果**：Llama3.1-8B在不同恶意客户端比例下的安全变化

| 方法 | Rule | MD-Judge | RM | MT-1 |
|------|------|----------|-----|-------|
| FedAvg(10:0) | 90.77 | 75.77 | -1.55 | 2.72 |
| FedAvg(8:2) | 60.77 | 20.77 | -3.70 | 3.18 |
| FedAvg(5:5) | 45.77 | 7.69 | -4.33 | 3.34 |

- 随着恶意客户端比例增加，安全指标显著下降
- LoRA权重可视化(LDA+PCA)显示良性/恶意客户端权重可分离

## 关键贡献

1. **安全性分析**：首次从LoRA权重角度分析FedLLM的安全漏洞，揭示其对恶意攻击的高度敏感性

2. **可区分特性**：发现不同类型客户端的LoRA权重具有可区分的内在特性，可作为有效的内生安全信号

3. **Safe-FedLLM框架**：
   - 基于探测的轻量级防御
   - 三层防御设计(Step/Client/Shadow)
   - 低开销、高效率的恶意客户端识别

4. **性能保持**：有效过滤恶意数据，同时保持良性数据的训练效率
