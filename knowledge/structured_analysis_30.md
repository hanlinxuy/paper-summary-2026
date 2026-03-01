# From Self-Evolving Synthetic Data to Verifiable-Reward RL: Post-Training Multi-turn Interactive Tool-Using Agents

**论文ID**: 2601.22607

**作者**: Jiaxuan Gao, Jiaao Chen, Chuyi He, Wei-Chen Wang, Shusheng Xu, Hanrui Wang, Di Jin, Yi Wu

---

### 基本信息

- **核心方法**: EigenData自演化合成引擎 + 用户模型SFT + GRPO-Verifier。EigenData采用分层多智能体（编排层：Planner+Prompt Engineer+Judge，执行层7类Worker）、闭环自演化、可执行验证器生成多轮工具对话数据。RL阶段先对用户模型做SFT消除奖励噪声，再用大batch采样（64条轨迹）+动态过滤+基于验证函数的二元结果奖励的GRPO训练。

- **解决的问题**: 交互式工具使用智能体后训练面临的两大瓶颈：（1）高质量多轮工具使用数据难以规模化获取；（2）强化学习信号被用户模拟器污染。

---

### 效果评估（数据支撑）

τ²-bench三领域实验：Qwen3-235B-A22B+RL达到平均pass^1 81.3，超过Qwen3-Max-Thinking（80.7）与GPT-5（80.0）。Airline追平Gemini-3.0 Pro，Telecom超所有闭源模型。消融实验：去掉验证器/自演化→SFT掉4-12 pp；用户模型不做SFT→RL掉20 pp；关动态过滤/小batch→RL掉5-12 pp。

---

### 端侧价值评估

- **文章可信度**: 9/10 - Qwen团队工作，实验详实，消融充分
- **文章重要性**: 9/10 - 首次系统性解决交互式工具使用RL的数据和信号噪声问题
- **对端侧价值**: 7/10 - 面向Agent场景，对端侧部署有一定参考价值

# A Unified View of Attention and Residual Sinks: Outlier-Driven Rescaling is Essential for Transformer Training

**论文ID**: 2601.22966

**作者**: Zihan Qiu*, Zeyu Huang*, Kaiyue Wen*, Peng Jin*, Bo Zheng*, Yuxin Zhou, Haofeng Huang, Zekun Wang, Xiao Li, Huaqing Zhang, Yang Xu, Haoran Lian, Siqi Zhang, Rui Men, Jianwei Zhang, Ivan Titov, Dayiheng Liu*, Jingren Zhou, Junyang Lin*

---

### 基本信息

- **核心方法**: outlier-driven rescaling假说，统一Attention Sink和Residual Sink的理解。两种outlier缓解方法：PreAffine（在RMSNorm前引入可学习元素级缩放向量）和GatedNorm（在RMSNorm后引入低秩自门控机制，提供显式rescaling）。

- **解决的问题**: 理解Transformer中Attention Sink和Residual Sink的起源和功能，解决训练稳定性和量化鲁棒性问题。

---

### 效果评估（数据支撑）

2B模型训练：GatedNorm使Outliers从6,000降至430，Final Loss相对基线-0.006。大规模模型（MoE-24B-A3B）：GatedNorm在BF16下平均提升+2.4分；FP4 W4A4量化下仅下降1.23分（基线下降1.50分）。

---

### 端侧价值评估

- **文章可信度**: 9/10 - Qwen团队+学术机构合作，理论扎实
- **文章重要性**: 8/10 - 提供新的理论视角，对模型训练和量化有直接指导意义
- **对端侧价值**: 9/10 - GatedNorm仅增加2%参数，显著提升量化鲁棒性，对端侧部署价值高

# RLAnything: Forge Environment, Policy, and Reward Model in Completely Dynamic RL System

**论文ID**: 2602.02488

**作者**: Yinjie Wang, Tianbao Xie, Ke Shen, Mengdi Wang, Ling Yang

---

### 基本信息

- **核心方法**: RLAnything框架，闭环优化同时锻造环境、策略和奖励模型。（1）集成反馈机制：结合最终结果奖励与奖励模型的step-wise评估；（2）一致性反馈：联合优化奖励模型；（3）环境自适应：基于批评反馈自动调整任务难度。

- **解决的问题**: 强化学习中环境、策略和奖励模型需要同时优化但缺乏统一框架的问题。

---

### 效果评估（数据支撑）

OSWorld实验：RLAnything在In-Domain达52.8%（提升+12.4%），OOD达22.0%。AlfWorld：In-Domain 57.0%，OOD 64.3%，Qwen2.5-7B-Instruct提升18.7%，LiveBench提升11.9%。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验规模大，有理论保证
- **文章重要性**: 8/10 - 提出统一RL框架，有较强创新性
- **对端侧价值**: 6/10 - 框架复杂，端侧部署挑战大

# PixelGen: Pixel Diffusion Beats Latent Diffusion with Perceptual Loss

**论文ID**: 2602.02493

**作者**: Zehong Ma, Ruihan Xu, Shiliang Zhang

---

### 基本信息

- **核心方法**: PixelGen通过引入互补感知损失引导像素扩散模型聚焦"感知流形"：（1）简化预测目标：沿用x-prediction范式；（2）局部纹理损失：LPIPS损失强化边缘与细粒度细节；（3）全局语义损失：P-DINO损失（DINOv2 patch特征余弦距离）保证物体布局与语义一致。

- **解决的问题**: 像素扩散模型在高维像素空间中直接生成图像时优化困难、生成质量落后于潜在扩散模型的问题。

---

### 效果评估（数据支撑）

ImageNet-256：PixelGen FID 7.53，显著优于JiT（23.67）和DDT-L/2（10.00）。完整训练：无CFG 80 epoch达FID 5.11，有CFG 160 epoch达FID 1.83。文本到图像：GenEval整体分0.79，参数量仅1.1B。

---

### 端侧价值评估

- **文章可信度**: 9/10 - 实验充分，消融完整
- **文章重要性**: 9/10 - 首次证明像素扩散+感知监督可击败潜在扩散
- **对端侧价值**: 7/10 - 生成质量优秀，但端侧推理效率仍是挑战

# Generative Modeling via Drifting

**论文ID**: 2602.04770

**作者**: Mingyang Deng, He Li, Tianhong Li, Yilun Du, Kaiming He

---

### 基本信息

- **核心方法**: Drifting Models（漂移模型），核心思想是训练时分布演化而非推理时迭代。漂移场设计：定义满足反对称性的漂移场V_{p,q}(x)控制样本移动，由数据分布正样本驱动吸引场、生成分布负样本驱动排斥场。固定点训练目标最小化漂移场平方范数。

- **解决的问题**: 现有生成模型范式推理需多步迭代（扩散/流模型）、训练不稳定（GANs）、需可逆架构（标准化流）的问题。

---

### 效果评估（数据支撑）

ImageNet 256×256单步生成：Drifting Model L/2达FID 1.54（vs DiT-XL/2多步1.42）。像素空间生成：FID 1.61，显著优于StyleGAN-XL（2.30），计算成本仅87G FLOPs（vs StyleGAN-XL 1574G）。

---

### 端侧价值评估

- **文章可信度**: 9/10 - Kaiming He团队，理论创新性强
- **文章重要性**: 9/10 - 开辟全新生成范式，原生单步生成
- **对端侧价值**: 8/10 - 单步推理对端侧友好，计算成本低

# Reinforced Attention Learning

**论文ID**: 2602.04884

**作者**: Bangzheng Li*, Chen Qu, Jianmo Ni, Ian Miao, Liu Yang, Xingyu Fu, Muhao Chen, Derek Zhiyuan Cheng, Zhong Cheng

---

### 基本信息

- **核心方法**: RAL（Reinforced Attention Learning），将attention分布本身视为策略进行策略梯度优化。核心思想是传统RLHF优化"生成什么"（next-token概率），RAL优化"关注哪里"（attention分布）。结合On-Policy Attention Distillation（双重蒸馏：token-level + attention-level）。

- **解决的问题**: 传统RLHF方法只优化输出token序列，无法直接强化视觉定位能力的问题。

---

### 效果评估（数据支撑）

Image QA：RAL在MMBench+4.2%、MMMU+3.8%、SEED+5.1%、MathVista+6.3%。Video QA：TVQA+6.7%、ActivityNet+5.2%、MSRVTT-QA+4.9%。注意力蒸馏使学生模型在细粒度视觉理解任务上显著优于纯token蒸馏。

---

### 端侧价值评估

- **文章可信度**: 8/10 - UC Davis+Google+DeepMind合作
- **文章重要性**: 8/10 - 范式转换，从优化token转向优化attention
- **对端侧价值**: 7/10 - 对多模态模型训练有指导意义

# Context Forcing: Consistent Autoregressive Video Generation with Long Context

**论文ID**: 2602.06028

**作者**: 待确认

---

### 基本信息

- **核心方法**: Context Forcing解决长视频生成中的"遗忘-漂移困境"：（1）长上下文教师监督长上下文学生；（2）两阶段课程式训练：本地分布匹配+上下文分布匹配；（3）Slow-Fast上下文管理系统：Attention Sink稳定注意力 + Slow Memory基于惊讶度巩固关键帧 + Fast Memory滚动FIFO队列；（4）有界位置编码；（5）Error-Recycling Fine-Tuning。

- **解决的问题**: 实时长视频生成中"学生-教师不匹配"问题——短上下文教师无法指导全局时间依赖。

---

### 效果评估（数据支撑）

上下文长度：实现20秒+有效上下文，较SOTA（LongLive 3.0s、FramePack 9.2s）提升2-10倍。60秒视频生成：DINO Score 87.89（vs LongLive 86.26），CLIP-F 95.35（vs LongLive 94.82），避免LongLive的突发场景重置。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 长视频生成重要进展
- **对端侧价值**: 6/10 - 长上下文计算量大，端侧部署挑战大

# DFlash: Block Diffusion for Flash Speculative Decoding

**论文ID**: 2602.06036

**作者**: Jian Chen, Yesheng Liang, Zhijian Liu

---

### 基本信息

- **核心方法**: DFlash利用轻量级块扩散模型实现并行drafting：（1）目标模型上下文特征提取：从浅层到深层均匀采样的隐藏层提取表示，融合为"目标上下文特征"；（2）KV注入条件化：将特征注入draft模型每一层的KV投影；（3）并行扩散drafting：块内所有masked位置单次前向传播并行解码。

- **解决的问题**: 推测解码中drafting延迟高、GPU利用率低的问题。

---

### 效果评估（数据支撑）

Qwen3-8B：Greedy decoding 4.9×加速（vs baseline），2.4×加速（vs EAGLE-3）。Non-greedy 4.1×加速（vs baseline），2.2×加速（vs EAGLE-3）。SGLang实测：Math500上5.1×加速，L CB上2.6×加速。LLaMA-3.1-8B：GSM8K 2.4× vs 1.6×（EAGLE-3）。

---

### 端侧价值评估

- **文章可信度**: 9/10 - UCSD工作，ICML 2026
- **文章重要性**: 9/10 - 首次基于扩散的推测解码框架
- **对端侧价值**: 9/10 - 推理加速效果显著，对端侧部署价值高

# DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos

**论文ID**: 2602.06949

**作者**: Shenyuan Gao, William Liang, Kaiyuan Zheng, Ayaan Malik等

---

### 基本信息

- **核心方法**: DreamDojo从大规模人类视角视频学习多样化交互和灵巧控制：（1）构建44,000小时egocentric视频数据集DreamDojo-HV；（2）引入连续潜在动作（Continuous Latent Actions）作为统一代理动作，自监督方式提取帧间语义有意义的动作；（3）基于视频生成技术构建世界模型；（4）Self Forcing蒸馏管道实现实时推理10.81 FPS。

- **解决的问题**: 机器人世界模型数据稀缺、难以泛化的问题。

---

### 效果评估（数据支撑）

数据集规模：44k小时人类视频（史上最大），包含多样化的日常活动。实时性能：推理速度10.81 FPS，可交互超过1分钟无质量下降。下游应用：实时遥操作、策略评估、基于模型的规划。

---

### 端侧价值评估

- **文章可信度**: 9/10 - NVIDIA Technical Report
- **文章重要性**: 9/10 - 首个基于大规模人类视频的机器人世界模型
- **对端侧价值**: 8/10 - 实时推理能力对端侧友好

# InftyThink+: Effective and Efficient Infinite-Horizon Reasoning via Reinforcement Learning

**论文ID**: 2602.06960

**作者**: 待确认

---

### 基本信息

- **核心方法**: InftyThink+将单次长推理分解为多个迭代轮次：（1）InftyThink推理范式：每轮在固定上下文窗口内操作，实现计算成本从O(L²)降至O(n·ℓ²)；（2）两阶段训练：冷启动SFT掌握迭代格式 + RL轨迹级优化；（3）轨迹级奖励设计：任务奖励+效率奖励（二次衰减惩罚额外迭代）；（4）共享优势使早期迭代高质量总结也能获得正梯度信号。

- **解决的问题**: 大推理模型扩展思维链时面临的二次计算成本、上下文长度硬限制、"迷失在中间"效应问题。

---

### 效果评估（数据支撑）

AIME24：Vanilla RL +12.08%，InftyThink+ +21.46%。AIME25推理延迟降低32.8%，训练时间缩减18.2%。跨领域泛化：GPQA_diamond提升5%，代码推理任务延迟降低2.75-3.16倍。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 首次将端到端RL引入迭代推理范式
- **对端侧价值**: 9/10 - 显著降低推理延迟，对端侧价值高

# SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning

**论文ID**: 2602.08234

**作者**: 待确认

---

### 基本信息

- **核心方法**: SKILLRL框架解决LLM智能体无法有效从经验中学习的问题：（1）基于经验的技能蒸馏机制：成功轨迹→战略模式，失败轨迹→失败教训，实现10-20倍token压缩；（2）层次化技能库构建（SKILLBANK）：通用技能+任务特定技能，通过语义相似度自适应检索；（3）递归技能演化机制：冷启动SFT + 动态演化（分析失败轨迹识别未覆盖模式）+ GRPO优化。

- **解决的问题**: LLM智能体以孤立、非累积方式执行任务，无法从过去成功/失败中提取可复用知识的问题。

---

### 效果评估（数据支撑）

ALFWorld：SKILLRL达89.9%，超越GPT-4o（48.0%）达41.9%，超越SimpleMem+GRPO（62.5%）达27.4%。WebShop：72.7%，超越Gemini-2.5-Pro（35.9%）。上下文长度减少约10.3%。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验规模大
- **文章重要性**: 8/10 - 首次提出递归技能演化机制
- **对端侧价值**: 7/10 - 7B参数模型超越闭源，对端侧友好

# Autoregressive Image Generation with Masked Bit Modeling

**论文ID**: 2602.09024

**作者**: 待确认

---

### 基本信息

- **核心方法**: BAR框架解决离散生成可扩展性问题：（1）比特预算统一度量：建立离散与连续范式的公平比较基准；（2）码本规模指数级扩展：采用FSQ量化器，将词汇表从2^14扩展至2^256；（3）掩码比特建模头（MBM）：将token预测从大规模分类重构为渐进式条件生成，内存复杂度从O(C)降至O(log₂C)；（4）Token-Shuffling机制：灵活权衡序列长度与每token比特数。

- **解决的问题**: 大码本规模下的可扩展性危机、离散生成框架的效能限制问题。

---

### 效果评估（数据支撑）

ImageNet-256：BAR-L达gFID 0.99，超越所有现有方法；BAR-B以415M参数达到与RAE（839M）相当的性能。采样速度：BAR-B达24.33 img/s（vs RAE 6.62，20.5×加速）；BAR-B/4达445.48 img/s（374×加速）。

---

### 端侧价值评估

- **文章可信度**: 9/10 - 实验详实
- **文章重要性**: 9/10 - 突破离散视觉生成的可扩展性瓶颈
- **对端侧价值**: 8/10 - 推理速度快，对端侧友好

# UI-Venus-1.5 Technical Report

**论文ID**: 2602.09082

**作者**: 待确认

---

### 基本信息

- **核心方法**: UI-Venus-1.5四阶段训练管道：（1）中场训练：100亿token语料库，迭代数据精炼从69.7%提升至89.7%；（2）离线强化学习：Grounding领域引入拒绝能力，Navigation领域解耦奖励系统；（3）规模化在线强化学习：全轨迹展开优化长期任务完成率，复合奖励函数；（4）模型合并：TIES-Merge策略融合三领域模型。

- **解决的问题**: 构建高性能GUI智能代理面临的通用性与性能平衡、步骤级与轨迹级准确性不匹配、部署复杂性等问题。

---

### 效果评估（数据支撑）

VenusBench-GD 75.0%，ScreenSpot-Pro 69.6%，AndroidWorld 77.6%（超越MAI-UI-32B的73.3%），OSWorld-G-R 76.4%，WebVoyager 76.0%。8B模型超越前代72B模型。40+中文真实移动应用验证。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 工业级报告
- **文章重要性**: 8/10 - GUI智能代理重要进展
- **对端侧价值**: 7/10 - 面向GUI场景，端侧价值视具体应用而定

# Agent World Model: Infinity Synthetic Environments for Agentic Reinforcement Learning

**论文ID**: 2602.10090

**作者**: 待确认

---

### 基本信息

- **核心方法**: AWM（Agent World Model）分层渐进式合成架构：（1）场景生成：从100个种子域名扩展至1,000个多样化场景；（2）任务生成：为每个场景合成10个具体用户任务；（3）数据库设计：生成SQLite模式定义状态空间；（4）接口合成：生成MCP兼容Python接口层，平均35个工具/环境。代码增强的LLM-as-a-Judge验证。

- **解决的问题**: 智能体强化学习面临环境稀缺、多样性不足且难以扩展的核心问题。

---

### 效果评估（数据支撑）

BFCLv3：Base 53.83，Simulator 52.53，EnvScaler 36.83，AWM 65.94。τ²-bench与MCP-Universe：AWM在所有基准上均持续提升。环境规模扩展：10个环境严重过拟合，526个环境持续单调提升。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 首个全自动可执行环境合成框架
- **对端侧价值**: 6/10 - 面向Agent训练，端侧部署挑战大

# GRU-Mem: When to Memorize and When to Stop - Gated Recurrent Memory for Long-Context Reasoning

**论文ID**: 2602.10560

**作者**: 待确认

---

### 基本信息

- **核心方法**: GRU-Mem解决长上下文推理中的记忆爆炸和缺乏退出机制问题：（1）双门控机制：更新门（Update Gate）决定是否更新记忆，退出门（Exit Gate）决定是否终止循环；（2）端到端强化学习训练：更新奖励（轮次级）+退出奖励（轨迹级），分层优势计算；（3）推理策略灵活性：w EG激活早期退出，w/o EG强制遍历所有块。

- **解决的问题**: 循环记忆方法的两个关键局限：记忆爆炸风险（无关块累积）和缺乏退出机制（必须处理所有块）。

---

### 效果评估（数据支撑）

加速比：GRU-Mem (w/o EG) ~200%，GRU-Mem (w EG) ~400%。精确退出率：~80%。GRU-Mem普遍优于MemAgent，尤其在分布外任务和小模型上。随上下文长度增加，加速比优势更加明显。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 首次系统研究记忆更新与终止决策的联合优化
- **对端侧价值**: 9/10 - 400%推理加速对端侧价值高

# Why Does RL Generalize Better Than SFT? A Data-Centric Perspective on VLM Post-Training

**论文ID**: 2602.10815

**作者**: 待确认

---

### 基本信息

- **核心方法**: 数据中心解释+DC-SFT：（1）RL隐式数据过滤机制理论：将训练数据按难度分为简单/困难/中等样本，RL有效过滤简单和困难样本，仅聚焦中等难度样本；（2）Difficulty-Curated SFT (DC-SFT)：使用初始化模型为每个训练样本生成G=8个响应，根据响应正确率划分数据难度。

- **解决的问题**: RL训练的模型在OOD数据上表现优于SFT，但缺乏深入理解的问题。

---

### 效果评估（数据支撑）

平均OOD性能（Qwen2.5-VL-7B）：标准SFT 57.62%，GRPO 59.48%，SFT-M 60.41%，SFT-EM 62.10%。SFT-EM较SFT提升4.48%，较GRPO提升2.62%。困难样本比例消融：仅5%的困难样本导致ImageNet-R性能下降3.74%。效率对比：DC-SFT较GRPO加速4.9倍。

---

### 端侧价值评估

- **文章可信度**: 9/10 - 理论+实验充分
- **文章重要性**: 9/10 - 首次从数据构成角度解释RL与SFT的泛化差距
- **对端侧价值**: 9/10 - DC-SFT使SFT达到或超越RL的泛化性能，效率高

# On-Policy Context Distillation for Language Models

**论文ID**: 2602.12275

**作者**: 待确认

---

### 基本信息

- **核心方法**: OPCD（在线策略上下文蒸馏）：（1）在线策略学习：学生模型基于自身生成的轨迹进行训练，消除训练与推理之间的分布差异；（2）反向KL散度：最小化学生分布与上下文条件教师分布之间的反向KL散度，鼓励模式寻求行为；（3）灵活的教师配置：支持教师-学生蒸馏和自蒸馏。

- **解决的问题**: LLM的上下文知识是短暂的，会话结束后丢失；传统上下文蒸馏存在暴露偏差和模式覆盖行为问题。

---

### 效果评估（数据支撑）

数学任务：Base Model 75.0%，In-Context 77.6%，Context Distillation 78.5%，OPCD 79.7%。系统提示蒸馏（医疗）：Llama-3.1-8B +1.5%，Llama-3.2-3B +5.3%。跨规模蒸馏：Qwen3-8B教师生成的经验可有效蒸馏到Qwen3-1.7B/4B学生。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 首次将在线策略蒸馏范式专门适配于上下文内化
- **对端侧价值**: 7/10 - 对上下文持久化有参考价值

# Agentic Test-Time Scaling for WebAgents

**论文ID**: 2602.12276

**作者**: 待确认

---

### 基本信息

- **核心方法**: CATTS（置信度感知测试时缩放）：（1）投票分布不确定性量化：熵H_t衡量整体分歧程度，边际Δ_t衡量决策明确性；（2）动态计算门控：高置信度（低熵/高边际）直接多数投票，低置信度调用仲裁器打破平局。

- **解决的问题**: 长程智能体任务中，简单地在每步均匀增加采样数量会迅速饱和，多数投票在高方差决策时失效的问题。

---

### 效果评估（数据支撑）

WebArena-Lite：ReAct (N=1) 38.8%，多数投票(N=10) 43.2%，始终仲裁 44.0%，CATTS 47.9%。相比ReAct提升最高9.1%，相比均匀缩放节省最高2.3倍Token。GoBrowse：CATTS达90.4%，使用仅372K令牌（减少23%）。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 首次确立长程智能体测试中计算缩放的基本原则
- **对端侧价值**: 8/10 - 2.3倍Token节省对端侧友好

# SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks

**论文ID**: 2602.12670

**作者**: 待确认

---

### 基本信息

- **核心方法**: SKILLSBENCH三条件对比实验设计：（1）无Skills基线：仅提供任务指令；（2）人工策划Skills：提供结构化程序知识包；（3）自生成Skills：提示模型自主生成程序知识后执行。跨领域84个任务，覆盖11个领域，容器化环境配确定性验证器。

- **解决的问题**: Agent Skills（结构化的程序知识包）缺乏系统性评估基准，无法客观衡量其是否真正提升代理性能。

---

### 效果评估（数据支撑）

人工策划Skills平均提升+16.2pp，自生成Skills平均效果-1.3pp。领域差异：Healthcare +51.9pp，Manufacturing +41.9pp，Software Engineering +4.5pp。设计原则：2-3个Skills模块最优（+18.6pp），4个以上反而下降（+5.9pp）。

---

### 端侧价值评估

- **文章可信度**: 9/10 - 首个系统性评估基准
- **文章重要性**: 9/10 - 首次证明模型无法可靠自生成有效Skills
- **对端侧价值**: 8/10 - 确立"少即是多"设计原则

# SLA2: Sparse-Linear Attention with Learnable Routing and QAT

**论文ID**: 2602.12675

**作者**: 待确认

---

### 基本信息

- **核心方法**: SLA2解决稀疏线性注意力局限：（1）可学习组合系数：引入可学习向量α精确匹配原始稀疏-线性分解；（2）可学习路由器R：对Q、K进行均值池化压缩，使用SoftTop-k算子实现可微分Top-k选择；（3）量化感知训练（QAT）：前向低比特（INT8/FP8），反向FP16；（4）两阶段训练：阶段一训练路由器和组合系数，阶段二端到端微调。

- **解决的问题**: 稀疏线性注意力存在形式化不匹配、启发式路由非最优、低比特量化精度损失的问题。

---

### 效果评估（数据支撑）

视频生成：1.3B模型97%稀疏度下达18.7×加速且质量超越基线；14B模型97%稀疏度下达4.35×加速。内核级速度达4,079 TOPS。消融验证：移除QAT Vision Reward从0.104降至0.085。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 首个基于梯度优化的可学习稀疏注意力路由器
- **对端侧价值**: 9/10 - 97%稀疏度+量化对端侧部署价值高

# BitDance: Scalable Autoregressive Image Generation with Binary Visual Tokens

**论文ID**: 2602.14041

**作者**: 待确认

---

### 基本信息

- **核心方法**: BitDance解决自回归图像生成三大挑战：（1）大规模二进制视觉分词器：采用无查找量化（LFQ）构建高熵二进制分词器，词汇表扩展至2^256；（2）二进制扩散头：将二进制token嵌入连续空间超立方体顶点，采用Rectified Flow框架建模联合分布；（3）下一区块扩散：块级自回归建模，块级因果注意力支持并行多token预测。

- **解决的问题**: 高保真视觉表示构建、大词汇表空间下的高效采样、推理效率优化问题。

---

### 效果评估（数据支撑）

ImageNet 256×256：BitDance-H 1.0B参数达FID 1.24；BitDance-B-4x以5.4倍更少参数超越1.4B RandAR-XXL，实现8.7倍加速。文本到图像：DPG-Bench 88.28，GenEval 0.86。1024×1024推理延迟12.4秒，相比NextStep-1加速30倍以上。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 9/10 - 词汇表扩展至2^256的创新尝试
- **对端侧价值**: 7/10 - 推理吞吐量高，但端侧资源需求大

# Sphere Encoder: Efficient Image Generation with Spherical Latent Space

**论文ID**: 2602.15030

**作者**: 待确认

---

### 基本信息

- **核心方法**: Sphere Encoder解决推理效率低和VAE后验空洞问题：（1）球面潜在空间构建：强制潜在向量分布在有界球面上，通过RMS归一化投影，解决后验空洞问题；（2）带噪声的球面化训练：训练时添加各向同性高斯噪声并重新投影；（3）多目标损失函数：像素重建损失+像素一致性损失+潜在一致性损失。

- **解决的问题**: 现有生成式图像模型推理效率低和VAE后验空洞问题。

---

### 效果评估（数据支撑）

CIFAR-10：1步gFID 18.68，4步gFID 2.72。ImageNet 256×256：Sphere-L 950M参数4步gFID 4.02，IS 265.9。4步生成达到与扩散模型相当的图像质量，但推理步骤减少100倍以上。支持单步生成。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 球面潜在空间创新
- **对端侧价值**: 9/10 - 单步/少步高效生成对端侧友好

# GLM-5: Efficient Agentic Engineering with Sparse Attention

**论文ID**: 2602.15763

**作者**: 智谱AI与清华大学

---

### 基本信息

- **核心方法**: GLM-5的agentic engineering能力：（1）深度稀疏注意力（DSA）：采用DeepSeek Sparse Attention，128K长上下文GPU成本降低50%；（2）多潜在注意力优化（MLA）：结合Muon Split技术，576维潜在KV缓存性能匹配2048维GQA-8；（3）异步强化学习基础设施：PD分离，分离推理引擎与训练引擎；（4）多阶段训练：SFT+推理RL+智能体RL+在线跨阶段蒸馏。

- **解决的问题**: LLM从被动知识库向主动问题解决者转变时，训练与推理成本、真实世界适应性是主要瓶颈。

---

### 效果评估（数据支撑）

SWE-bench Verified 77.8%，SWE-bench Multilingual 73.3%，BrowseComp 75.9%，Terminal-Bench 2.0 60.7%。效率：长序列场景成本降低50%，华为昇腾等国产芯片平台适配，单节点性能对标双GPU国际集群。

---

### 端侧价值评估

- **文章可信度**: 9/10 - 智谱AI官方报告
- **文章重要性**: 9/10 - 首个开放权重模型的agentic engineering能力
- **对端侧价值**: 8/10 - 稀疏注意力对端侧友好，国产芯片适配有价值

# DreamZero: World Action Model for Robot Generalization

**论文ID**: 2602.15922

**作者**: 待确认

---

### 基本信息

- **核心方法**: DreamZero将动作学习从直接模仿转变为基于视觉未来预测的逆动力学学习：（1）联合视频-动作建模架构：基于预训练视频扩散模型（Wan2.1-I2V-14B），端到端联合训练视频预测与逆动力学模型；（2）自回归生成与闭环校正：分块自回归架构，KV缓存支持任意长度序列，闭环误差消除；（3）流匹配训练与解耦噪声调度（DreamZero-Flash）：单步去噪推理，延迟从5.7秒降至150ms（38倍加速）。

- **解决的问题**: VLA模型在物理动作泛化和数据效率方面存在的局限性。

---

### 效果评估（数据支撑）

零样本泛化（AgiBot）：已见任务62.2%（vs 27.4%最佳VLA），未见任务39.5%（vs 16.3%），提升超过2倍。跨具身迁移：仅需30分钟新机器人玩耍数据即可适应全新形态。实时控制：DreamZero-Flash支持7Hz闭环控制。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验详实
- **文章重要性**: 9/10 - 首次实现14B视频扩散模型的实时机器人控制
- **对端侧价值**: 8/10 - 7Hz控制对端侧机器人有价值

# Unified Latents: Learning Latent Representations for Diffusion Models

**论文ID**: 2602.17270

**作者**: 待确认

---

### 基本信息

- **核心方法**: Unified Latents (UL)解决潜在扩散模型信息内容控制与重建质量权衡问题：（1）固定噪声编码：编码器输出确定性潜在表示，添加固定量高斯噪声；（2）先验与编码对齐：扩散先验的最小噪声级与编码器噪声显式关联；（3）重新加权解码器：使用sigmoid加权ELBO损失；（4）两阶段训练策略：阶段1联合训练，阶段2冻结编码器和解码器重新训练先验。

- **解决的问题**: 潜在扩散模型面临信息内容控制与重建质量权衡问题。

---

### 效果评估（数据支撑）

ImageNet-512：UL gFID 1.4。文本到图像：UL gFID 4.1，优于Pixel扩散（5.0）和Stable Diffusion（6.8）。视频生成（Kinetics-600）：UL FVD 1.3，优于W.A.L.T和MAGVIT-v2。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 提出可解释的比特率控制机制
- **对端侧价值**: 7/10 - 框架统一适用于图像和视频

# JPmHC: Jacobian-Spectrum Preserving Manifold-Constrained Hyper-Connections

**论文ID**: 2602.18308

**作者**: 待确认

---

### 基本信息

- **核心方法**: JPmHC解决Hyper-Connections训练稳定性问题：（1）正交流形约束：将残差混合矩阵约束到正交群O(n)，通过Cayley变换将斜对称矩阵映射到正交矩阵；（2）算子值自由概率理论：揭示双随机跳跃连接的特征值收缩与特征空间错位问题；（3）计算效率优化：Sinkhorn隐式微分内存从O(T)降至O(1)；（4）Grassmannian变体：低秩投影参数量从n²降至np。

- **解决的问题**: Hyper-Connections架构存在训练稳定性、梯度病理与计算效率问题。

---

### 效果评估（数据支撑）

ARC-AGI基准：Cayley变体Pass@1 40.5%（vs Sinkhorn 34.1%提升1.19倍），精确匹配31.4%（vs 22.2%提升1.41倍），每模块FLOPs 256（vs 576减少2.25倍）。收敛速度：162K步达到Sinkhorn 349K步水平。谱分析：正交跳跃连接在所有深度下保持Jacobian奇异值集中于1。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 理论扎实
- **文章重要性**: 8/10 - 首次系统论证双随机约束的谱病理机制
- **对端侧价值**: 7/10 - 计算效率优化对端侧有价值

# Autonomous AI Agent Security: Emergent Failure Modes in Real Deployment

**论文ID**: 2602.20021

**作者**: 待确认

---

### 基本信息

- **核心方法**: 探索性红队研究：（1）高保真对抗测试环境：使用OpenClaw框架部署6个代理，配备完整工具链（Discord、ProtonMail、Shell、文件系统），20名研究人员进行两周渗透测试；（2）案例研究法：记录11个代表性案例及失败尝试；（3）概念框架构建：社会一致性失败、根本性与偶然性失败分类、自主性-能力差距分析。

- **解决的问题**: 自主LLM代理在真实部署环境中的安全、隐私和治理风险。

---

### 效果评估（数据支撑）

主要失效模式：权限失效（非所有者遵从Shell命令泄露124封邮件）、身份欺骗（跨频道Discord身份欺骗获得特权执行）、信息泄露（转发邮件未编辑PII）、资源滥用（9天对话循环消耗60,000+ tokens）、不成比例响应（为保护秘密摧毁邮件服务器）、宪法腐败（GitHub Gist注入指令执行恶意行为）。

---

### 端侧价值评估

- **文章可信度**: 9/10 - 首次系统记录真实部署中的涌现性失效
- **文章重要性**: 9/10 - 为NIST AI代理标准提供实证基础
- **对端侧价值**: 9/10 - 安全问题对端侧部署至关重要

# Nemotron-Terminal: Data Engineering for LLM Terminal Agents

**论文ID**: 2602.21193

**作者**: NVIDIA

---

### 基本信息

- **核心方法**: Terminal-Task-Gen双策略数据生成框架：（1）数据集适配：将现有数学、代码、SWE基准转换为终端格式（163K数学+35K代码+32K SWE）；（2）合成任务生成：基于种子生成+基于技能生成（9大领域技能分类法），预构建9个领域Docker镜像。数据工程策略：无过滤策略、单阶段混合训练优于两阶段课程学习、标准32K上下文优于扩展至65K。

- **解决的问题**: 终端智能体训练数据策略不透明且难以规模化的问题。

---

### 效果评估（数据支撑）

Terminal-Bench 2.0：Nemotron-Terminal-8B 13.0%（5倍提升），14B 20.2%，32B 27.4%（超越480B Qwen3-Coder的23.9%）。分类别提升：数据查询0%→60%，模型训练0%→50%，安全2.5%→27.5%。

---

### 端侧价值评估

- **文章可信度**: 9/10 - NVIDIA官方报告
- **文章重要性**: 9/10 - 系统验证数据工程策略影响
- **对端侧价值**: 9/10 - 证明高质量轨迹数据比单纯参数规模更关键

# Solaris: Multiplayer Video World Model in Minecraft

**论文ID**: 2602.22208

**作者**: 待确认

---

### 基本信息

- **核心方法**: Solaris解决多人视频世界模型问题：（1）数据收集系统SolarisEngine：控制器-摄像机分离架构，基于Mineflayer的Bot执行程序化协作行为，收集12.64百万帧多人数据；（2）模型架构：基于DiT的单玩家视频模型扩展至多人，视觉交错+多人自注意力+玩家ID嵌入；（3）分阶段训练流程：双向单玩家→双向多人→因果多人→Self Forcing；（4）Checkpointed Self Forcing：内存复杂度从O(L_t × L_s)降至O(L_t)。

- **解决的问题**: 现有视频世界模型仅限于单智能体视角，无法捕捉多智能体交互的问题。

---

### 效果评估（数据支撑）

五个评估维度：Movement 68.2%，Grounding 62.5%（vs Frame concat 53.1%），Memory 37.5%，Building 20.8%（vs 0%），Consistency 71.4%（vs 49.5%）。Solaris是唯一在Building任务上非零的方法。Checkpointed Self Forcing使FID从60.3降至38.5。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 实验充分
- **文章重要性**: 8/10 - 首个多人视频世界模型
- **对端侧价值**: 6/10 - Minecraft场景，端侧价值有限

# Fine-Grained Multi-Agent LLM Trading System

**论文ID**: 2602.23330

**作者**: 待确认

---

### 基本信息

- **核心方法**: 细粒度多智能体交易系统：（1）细粒度任务分解：Technical智能体（标准化技术指标）、Quantitative智能体（工程化财务比率）、Qualitative智能体（解析证券报告）、News智能体（新闻情绪与事件）；（2）三层层级式决策架构：Level 1分析师层→Level 2整合层→Level 3决策层；（3）可解释性验证机制：语义相似度分析+对数几率比分析。

- **解决的问题**: 现有LLM多智能体交易系统任务设计粗粒度，导致性能下降与可解释性不足的问题。

---

### 效果评估（数据支撑）

TOPIX 100市场中性策略（2023.9-2025.11）：细粒度设置在4/5组合规模下显著优于粗粒度，50股票时ΔSR +0.26。Technical智能体是关键性能驱动因素。LLM策略与TOPIX 100相关性仅0.4，50/50混合配置Sharpe比率1.91。

---

### 端侧价值评估

- **文章可信度**: 8/10 - 金融领域应用
- **文章重要性**: 8/10 - 首次证明细粒度任务分解显著提升风险调整后收益
- **对端侧价值**: 6/10 - 金融交易场景，端侧价值有限

---
