# A Unified Attention U-Net Framework for Cross-Modality Tumor Segmentation in MRI and CT

## 基本信息
- arXiv ID: 2601.06187
- 作者: Nishan Rai, Pushpa R. Dahal

## 核心方法

**研究背景**：医学图像分割中通常使用单模态和单器官范式，但临床实践中涉及异构模态（如MRI用于脑部，CT用于肺部）。

**核心方法**：

1. **统一Attention U-Net架构**：
   - 联合训练MRI (BraTS 2021) 和 CT (LIDC-IDRI) 数据集
   - 不依赖特定模态编码器或域适应
   - 约189万可训练参数，~7.3G乘加运算

2. **模态协调预处理**：
   - 统一输入尺寸128×128像素
   - 强度归一化到[0,1]
   - CT图像复制通道形成4通道张量

3. **注意力门控跳跃连接**：
   - 选择性抑制无关编码器特征
   - 突出解码器中的显著区域
   - 公式：$\alpha = \sigma(\psi^T(W_x x + W_g g + b))$

4. **Focal Tversky Loss**：
   - 处理类别不平衡问题
   - 强调难以分割的区域

## 实验结果

**数据集**：
- BraTS 2021：多参数MRI (T1, T1ce, T2, FLAIR)
- LIDC-IDRI：肺部CT扫描

**评估指标**：Dice系数、IoU、AUC

## 关键贡献

1. **首个统一模型**：首个在MRI (BraTS) 和 CT (LIDC) 肿瘤数据集上联合训练的Attention U-Net

2. **模态协调策略**：使用注意力门控跳跃连接和Focal Tversky损失的模态协调训练策略

3. **泛化性证明**：单一模型可泛化到异构成像领域，建立稳健基线

4. **轻量级方法**：与复杂的域适应方法相比，提供简单、资源友好的基线
