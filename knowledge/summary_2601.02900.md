# SPO-CLAPScore: Enhancing CLAP-based alignment prediction system with Standardize Preference Optimization, for the first XACLE Challenge

## 基本信息
- arXiv ID: 2601.02900
- 作者: Taisei Takano, Ryoya Yoshida
- 机构: The University of Tokyo, Japan
- 领域: Sound (cs.SD); Audio and Speech Processing (eess.AS)

## 核心方法

### 研究背景
Text-to-audio (TTA) 生成是重要研究领域，评估生成音频与文本语义对齐的关键指标是人类主观评估。目前常用的CLAPScore与人类主观评估相关性较低。XACLE Challenge旨在开发与人类主观评估高度相关的自动评估模型。

### 主要成果
本文提出SPO-CLAPScore系统，结合CLAPScore架构和标准化偏好优化(SPO)方法，在XACLE挑战赛中获得第6名，SRCC达到0.6142。

### 技术框架
1. **CLAPScore基础架构**: 使用CLAP模型的音频和文本编码器，计算余弦相似度作为对齐分数
2. **Listener筛选**: 过滤评分不一致的听众数据
3. **标准化偏好优化(SPO)**: 将原始分数标准化为相对偏好分数，缓解个体评分偏差
4. **模型集成**: 组合多种训练设置的模型提高鲁棒性

### 核心公式
$$\hat{x}=\frac{\textbf{e}^{\textsf{audio}}\cdot \textbf{e}^{\textsf{text}}}{\|\textbf{e}^{\textsf{audio}}\| \|\textbf{e}^{\textsf{text}}\|} \times 10$$

$$x_{\text{spo}}=\frac{x-\mu_{\text{listener}}}{\sigma_{\text{listener}}}$$

### 损失函数
$$L = L_{\text{reg}}\left(x_{\text{spo}}, \frac{\hat{x}-\mu_{\text{train}}}{\sigma_{\text{train}}}\right) + \lambda L_{\text{con}}\left(x_{\text{spo}}, \frac{\hat{x}-\mu_{\text{train}}}{\sigma_{\text{train}}}\right)$$

## 关键贡献

1. **新优化方法**: 提出标准化偏好优化(SPO)，将原始分数转换为相对偏好指示

2. **Listener筛选**: 设计算法过滤评分异常的听众，减少噪声影响

3. **模型集成**: 通过集成不同训练条件的模型提高预测稳定性

4. **性能提升**: 相比基线模型，SRCC提升超过0.27

## 效果评估

### 测试集结果
| 模型 | SRCC ↑ | LCC ↑ | KTAU ↑ | MSE ↓ |
|------|--------|--------|--------|-------|
| 基线 | 0.3345 | 0.3420 | 0.229 | 4.811 |
| SPO-CLAPScore | **0.6142** | **0.6542** | **0.4407** | 2.985 |

- SRCC提升: 0.2797 (从0.3345到0.6142)
- 排名: 第6名
- 代码开源: https://github.com/ttakano398/SPO-CLAPScore

## 结论

SPO-CLAPScore通过引入标准化偏好优化方法，有效解决了人类评估中的个体偏差问题，在音频-文本语义对齐预测任务上取得了显著性能提升。
