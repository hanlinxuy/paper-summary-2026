# Video-OPD: Efficient Post-Training of MLLMs for Temporal Video Grounding via On-Policy Distillation

## 基本信息
- arXiv ID: 2602.02994
- 作者: Jiaze Li, Hao Yin等 (多机构)
- 来源: ICML 2026

## 核心方法

Video-OPD是一种基于严格on-policy强化学习的时间视频定位(TVG)框架，将策略优化与密集的基于蒸馏的监督紧密结合。

**关键技术设计：**

1. **On-Policy蒸馏框架 (Video-OPD)**
   - 每个训练迭代只从当前student策略采样轨迹
   - 固定teacher模型仅用于提供细粒度的token级学习信号
   - 保持训练-推理分布对齐

   **训练流程四步：**
   - Step 1: On-Policy轨迹采样 - 记录token级log概率
   - Step 2: 学生轨迹评估 - teacher评估学生生成token的条件log概率
   - Step 3: 密集Token级监督 - 使用反向KL散度定义per-token学习信号
   - Step 4: 策略更新 - 将teacher信号作为token级奖励

2. **Teacher-Validated Disagreement Focusing (TVDF)**
   - 轻量级训练课程，使用标注数据作为验证信号
   - 两个组件：
     - Teacher可靠性预验证(TRPV): 过滤teacher不可靠的样本
     - 基于分歧的轨迹优先(DBTP): 优先处理高信息量样本

   **原则**：只使用ground-truth时间标注作为验证信号，而非直接监督目标

**核心优势：**
- 保持训练-推理对齐，避免分布不匹配
- 密集token级监督实现精确信用分配
- 单次rollout即可完成训练，显著降低计算开销

## 实验结果

**数据集表现：**
- 在多个TVG基准数据集上验证
- 相比GRPO具有更高效的训练动态

**TVDF效果：**
- 使用标注数据作为验证信号提升样本效率
- 加速收敛

## 关键贡献

1. **提出Video-OPD框架**，首个严格on-policy的TVG强化学习方法
2. **引入密集token级监督**，将稀疏episode级奖励转换为细粒度学习信号
3. **设计TVDF训练课程**，利用标注数据作为验证信号识别可靠且信息丰富的样本
4. **实现精确的时间信用分配**，在长程视频理解中避免复合误差
5. **显著降低计算开销**，每个训练样本只需一次rollout
