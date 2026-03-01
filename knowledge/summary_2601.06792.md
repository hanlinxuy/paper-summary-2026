# Cross-Modal Computational Model of Brain-Heart Interactions via HRV and EEG Features

## 基本信息
- arXiv ID: 2601.06792
- 作者: Malavika Pradeep, Akshay Sasi, Nusaibah Farrukh, Rahul Venugopal, Elizabeth Sherly

## 核心方法

**研究背景**：EEG是量化心理负荷的金标准，但复杂且不便携；ECG可通过可穿戴设备获取，有望作为EEG的替代方案。

**核心方法**：

1. **特征提取**：
   - ECG：HRV指标（时域：MeanNN, SDNN, RMSSD, Poincaré descriptors）和Catch22时间序列特征
   - EEG：频带功率和Catch22特征

2. **跨模态回归框架**：
   - 使用XGBoost将ECG衍生的HRV特征映射到EEG衍生的认知特征
   - 桥接自主神经系统和中枢神经系统的表征

3. **PSV-SDG合成数据生成**：
   - Poincaré交感-副交感合成数据生成模型
   - 基于EEG活动调节生成HRV信号
   - 增强模型在稀疏数据情况下的鲁棒性

## 实验结果

**数据集**：OpenNeuro ds003838，86名健康成人被试，执行数字跨度记忆任务

**实验设计**：
- 5、9、13位数字的记忆负荷任务
- 被动聆听条件

**实验发现**：
- ECG提取的特征可预测EEG表征
- 合成HRV数据增强了模型鲁棒性
- 自主信号编码部分心理负荷标记

## 关键贡献

1. **跨模态学习**：首次使用XGBoost回归模型将HRV特征映射到EEG认知特征空间

2. **合成数据增强**：PSV-SDG模型生成逼真的HRV信号，增强模型在噪声数据和有限数据情况下的表现

3. **证据贡献**：提供自主信号编码心理负荷标记的定量证据

4. **实际应用**：为可穿戴设备在非实验室环境中实现轻量级、可解释的认知监测系统奠定基础
