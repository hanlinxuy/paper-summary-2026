# A Unified View of Attention and Residual Sinks: Outlier-Driven Rescaling is Essential for Transformer Training

## 基本信息
- arXiv ID: 2601.22966
- 作者: Zihan Qiu*, Zeyu Huang*, Kaiyue Wen*, Peng Jin*, Bo Zheng*, Yuxin Zhou, Haofeng Huang, Zekun Wang, Xiao Li, Huaqing Zhang, Yang Xu, Haoran Lian, Siqi Zhang, Rui Men, Jianwei Zhang, Ivan Titov, Dayiheng Liu*, Jingren Zhou, Junyang Lin* (Qwen团队 + 爱丁堡大学 + 斯坦福大学 + 清华大学)

## 核心方法

本文提出**outlier-driven rescaling假说**，统一了对Attention Sink和Residual Sink的理解：

1. **Attention Sink（注意力汇）**：少数特殊token（如首token）持续接收较大的attention logits，出现在softmax归一化环节
2. **Residual Sink（残差汇）**：多数token在固定维度上出现持续的大激活值，出现在RMSNorm归一化环节

核心观点：这些outliers与归一化机制（softmax和RMSNorm）协同工作，起到**rescaling**作用——通过放大outlier维度来调整非outlier特征的尺度。

### 两种outlier缓解方法：
- **PreAffine**：在RMSNorm前引入可学习的元素级缩放向量，将outlier吸收到参数中
- **GatedNorm**：在RMSNorm后引入低秩自门控机制，提供显式的rescaling

## 实验结果

### 训练稳定性与性能（2B模型，120B tokens）
| 配置 | Outliers | Final Loss | 相对基线 |
|------|----------|------------|----------|
| 基线 (Full Attention) | 6,000 | 1.964 | - |
| + Gated Attention (GA) | 2,800 | 1.957 | -0.007 |
| + GA, PreAffine | 640 | 1.954 | -0.003 |
| + GA, GatedNorm | 430 | 1.951 | **-0.006** |

### 大规模模型结果（MoE-24B-A3B, 500B tokens）
- GatedNorm在BF16下平均提升**+2.4分**
- FP4 W4A4量化下，GatedNorm仅下降1.23分（基线下降1.50分，PreAffine下降2.76分）

## 关键贡献

1. **理论贡献**：提出outlier-driven rescaling假说，统一了Attention Sink和Residual Sink的起源和功能
2. **实验发现**：
   - 移除归一化会消除outlier但损害训练稳定性
   - 直接clipping outliers会破坏rescaling机制导致性能下降
   - Outlier更多作为rescale因子而非直接贡献者
3. **方法贡献**：
   - PreAffine：将outlier吸收到可学习参数
   - GatedNorm：显式门控rescaling，仅增加2%参数
4. **工程价值**：GatedNorm显著提升量化鲁棒性，在W4A4量化下仅损失1.23分
