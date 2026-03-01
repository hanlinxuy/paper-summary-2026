# DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos

## 基本信息
- arXiv ID: 2602.06949
- 作者: Shenyuan Gao, William Liang, Kaiyuan Zheng, Ayaan Malik等 (NVIDIA, UC Berkeley, HKUST等)
- 来源: NVIDIA Technical Report

## 核心方法

DreamDojo是一个基础世界模型，从大规模人类视角视频中学习多样化的交互和灵巧控制。

**关键技术设计：**

1. **大规模人类视频数据集 (DreamDojo-HV)**
   - 收集44,000小时 egocentric视频序列
   - 涵盖广泛的日常场景、对象和技能
   - 包含约96倍于之前最多样性公共机器人学习数据集的技能
   - 2000倍于之前数据集的场景数量

2. **连续潜在动作 (Continuous Latent Actions)**
   - 引入潜在动作作为统一代理动作
   - 解决动作标签稀缺的问题
   - 以自监督方式提取帧间语义有意义的动作
   - 确保物理知识和可控性有效迁移

3. **模型架构**
   - 基于视频生成技术构建世界模型
   - 能够理解物理和精确动作可控性
   - 展示对 unseen objects 和 novel environments 的零样本泛化

4. **蒸馏管道 (Distillation Pipeline)**
   - 采用 Self Forcing 范式
   - 加速到实时速度 10.81 FPS
   - 增强长程一致性
   - 可在640×480分辨率下任意horizon自回归预测

## 实验结果

**数据集规模：**
- 44k小时人类视频（史上最大）
- 包含多样化的日常活动

**实时性能：**
- 推理速度: 10.81 FPS
- 可交互超过1分钟无质量下降

**下游应用：**
- 实时遥操作 (Live Teleoperation)
- 策略评估 (Policy Evaluation)
- 基于模型的规划 (Model-based Planning)

## 关键贡献

1. **构建了迄今为止最大、最多样的机器人学习视频数据集**，共44,000小时
2. **提出首个基于大规模人类视频的基础世界模型**，展示对未见对象和新环境的零样本泛化能力
3. **引入连续潜在动作机制**，有效解决大规模视频中动作标签稀缺的问题
4. **开发高效蒸馏管道**，实现实时推理并增强上下文一致性
5. **展示多种下游应用潜力**，包括实时遥操作、策略评估和基于模型的规划
