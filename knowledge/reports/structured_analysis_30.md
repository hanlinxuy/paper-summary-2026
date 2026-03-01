# 2026年2月精选论文结构化摘要汇总

## 目录

1. [2601.22607 - EigenData: 自演化合成数据与可验证奖励RL](#260122607---eigendata)
2. [2601.22966 - GatedNorm: 门控归一化](#260122966---gatednorm)
3. [2602.02488 - RLAnything: 环境-策略-奖励闭环优化](#260202488---rlanything)
4. [2602.02493 - PixelGen: 像素扩散与感知损失](#260202493---pixelgen)
5. [2602.04770 - Drifting Models: 漂移生成范式](#260204770---drifting-models)
6. [2602.04884 - RAL: 强化注意力学习](#260204884---ral)
7. [2602.06028 - Context Forcing: 长上下文视频生成](#260206028---context-forcing)
8. [2602.06036 - DFlash: 块扩散推测解码](#260206036---dflash)
9. [2602.06949 - DreamDojo: 机器人世界模型](#260206949---dreamdojo)
10. [2602.06960 - InftyThink+: 无限视野推理](#260206960---inftythink)
11. [2602.08234 - SkillRL: 递归技能增强RL](#260208234---skillrl)
12. [2602.09024 - BAR: 掩码比特建模](#260209024---bar)
13. [2602.09082 - UI-Venus-1.5: GUI智能体](#260209082---ui-venus)
14. [2602.10090 - Agent World Model: 合成环境](#260210090---agent-world-model)
15. [2602.10560 - GRU-Mem: 门控循环记忆](#260210560---gru-mem)
16. [2602.10815 - DC-SFT: 数据中心SFT](#260210815---dc-sft)
17. [2602.12275 - OPCD: 策略上下文蒸馏](#260212275---opcd)
18. [2602.12276 - CATTS: 置信度感知测试时缩放](#260212276---catts)
19. [2602.12670 - SkillsBench: Agent技能评估](#260212670---skillsbench)
20. [2602.12675 - SLA2: 稀疏线性注意力](#260212675---sla2)
21. [2602.14041 - BitDance: 二进制Token生成](#260214041---bitdance)
22. [2602.15030 - Sphere Encoder: 球面潜在空间](#260215030---sphere-encoder)
23. [2602.15763 - GLM-5: 高效Agent工程](#260215763---glm-5)
24. [2602.15922 - DreamZero: 世界动作模型](#260215922---dreamzero)
25. [2602.17270 - Unified Latents: 统一潜在表示](#260217270---unified-latents)
26. [2602.18308 - JPmHC: 正交超连接](#260218308---jpmhc)
27. [2602.20021 - Agents of Chaos: Agent安全](#260220021---agents-of-chaos)
28. [2602.21193 - Nemotron-Terminal: 终端智能体](#260221193---nemotron-terminal)
29. [2602.22208 - Solaris: 多人视频世界模型](#260222208---solaris)
30. [2602.23330 - Fine-Grained多智能体交易系统](#260223330---trading-system)

---

## 2601.22607 - EigenData

**作者**: Jiaxuan Gao, Jiaao Chen, Chuyi He, Wei-Chen Wang, Shusheng Xu, Hanrui Wang, Di Jin, Yi Wu

**核心方法**: 论文提出EigenData框架，结合自演化数据智能体与基于验证器的RL。系统通过分层多智能体引擎合成工具对话数据，并通过闭环自演化流程提高生成可靠性。RL阶段先进行SFT微调，然后应用GRPO风格训练。

**效果评估**: 在tau^2-bench上，最佳模型在Airline任务达到73.0% pass^1，在Telecom任务达到98.3% pass^1。

**端侧价值**: 8/10 - 为端侧Agent训练提供可扩展的数据生成方案。

---

## 2601.22966 - GatedNorm

**作者**: 智谱AI

**核心方法**: 提出GatedNorm机制，通过引入可学习的门控参数增强模型在量化场景下的鲁棒性。仅增加2%参数量即可显著提升INT8/FP8量化性能。

**效果评估**: 量化误差降低约40%，W8A16推理性能提升显著。

**端侧价值**: 9/10 - 极低的参数开销换取显著的量化鲁棒性提升，对端侧部署价值极高。

---

## 2602.02488 - RLAnything

**作者**: 待补充

**核心方法**: 提出环境-策略-奖励模型闭环优化框架RLAnything，支持在任意环境中通过自博弈提升Agent能力。

**效果评估**: 在多任务场景下相比基线提升15%以上。

**端侧价值**: 7/10 - 通用RL框架对端侧Agent训练有参考价值。

---

## 2602.02493 - PixelGen

**作者**: Zehong Ma, Ruihan Xu, Shiliang Zhang

**核心方法**: 提出PixelGen框架，使用感知损失（LPIPS + DINO）引导像素扩散模型学习更有意义的感知流形。在像素空间直接进行端到端扩散生成，避免VAE引入的 artifacts。

**效果评估**: ImageNet-256上FID达到5.11（80 epochs），GenEval得分0.79。

**端侧价值**: 7/10 - 简化的生成范式，但计算成本仍较高。

---

## 2602.04770 - Drifting Models

**作者**: Mingyang Deng, He Li, Tianhong Li, Yilun Du, Kaiming He (FAIR, MIT)

**核心方法**: 提出漂移生成范式Drifting Models，在训练过程中演化pushforward分布，实现单步推理。引入漂移场控制样本移动，在分布匹配时达到平衡。

**效果评估**: ImageNet 256x256上单步生成FID 1.54（潜在空间）/ 1.61（像素空间），达到SOTA。

**端侧价值**: 8/10 - 单步生成大幅降低推理延迟，对端侧部署意义重大。

---

## 2602.04884 - RAL

**作者**: 待补充

**核心方法**: 提出强化注意力学习（RAL）方法，通过RL优化注意力机制，提升VLM的多模态推理能力。

**效果评估**: 多模态推理基准上显著提升。

**端侧价值**: 7/10 - 注意力优化对端侧VLM有参考价值。

---

## 2602.06028 - Context Forcing

**作者**: Shuo Chen, Cong Wei, Sun Sun, Ping Nie, Kai Zhou, Ge Zhang, Ming-Hsuan Yang, Wenhu Chen

**核心方法**: 提出Context Forcing框架，解决长视频生成中的学生-教师不匹配问题。通过长上下文教师监督长上下文学生，引入Slow-Fast Memory架构管理上下文。

**效果评估**: 支持超过20秒的有效上下文长度，是SOTA的2-10倍。

**端侧价值**: 6/10 - 长视频生成对端侧场景价值有限，但上下文管理技术有参考意义。

---

## 2602.06036 - DFlash

**作者**: Jian Chen, Yesheng Liang, Zhijian Liu (UC San Diego)

**核心方法**: 首次提出基于扩散的轻量级推测解码框架DFlash。利用目标模型的隐藏层特征作为条件，通过KV注入实现高效条件化，采用块级并行扩散drafting。

**效果评估**: Qwen3-8B上4.9x加速（greedy），SGLang实测5.1x加速（Math500）。

**端侧价值**: 9/10 - 显著的推理加速效果，对端侧LLM部署价值极高。

---

## 2602.06949 - DreamDojo

**作者**: 待补充

**核心方法**: 提出基于44k小时egocentric视频的机器人世界模型DreamDojo，通过视频预测实现机器人技能泛化。

**效果评估**: 在真实机器人实验中展现良好的零样本迁移能力。

**端侧价值**: 7/10 - 机器人领域应用潜力大。

---

## 2602.06960 - InftyThink+

**作者**: Yuchen Yan, Liang Jiang, Jin Jiang, Shuaicheng Li, Zujie Wen, Zhiqiang Zhang, Jun Zhou, Jian Shao, Yueting Zhuang, Yongliang Shen (浙江大学)

**核心方法**: 提出端到端RL框架InftyThink+，优化整个迭代推理轨迹。采用两阶段训练：冷启动SFT + 轨迹级RL。引入任务奖励与效率奖励的组合。

**效果评估**: AIME24上准确率提升21.46%，延迟降低32.8%，训练时间缩减18.2%。

**端侧价值**: 9/10 - 同时提升准确率、降低延迟和训练成本，对端侧推理优化价值极高。

---

## 2602.08234 - SkillRL

**作者**: Peng Xia, Jianwen Chen, Hanyang Wang, Jiaqi Liu, Kaide Zeng, Yu Wang, Siwei Han, Yiyang Zhou, Xujiang Zhao, Haifeng Chen, Zeyu Zheng, Cihang Xie, Huaxiu Yao

**核心方法**: 提出SkillRL框架，通过自动技能发现和递归演化弥合原始经验与策略改进之间的差距。引入基于经验的蒸馏机制构建分层技能库SkillBank。

**效果评估**: ALFWorld、WebShop等任务上超越基线15.3%。

**端侧价值**: 8/10 - 技能库机制可减少Token消耗，对端侧Agent有参考价值。

---

## 2602.09024 - BAR

**作者**: Qihang Yu, Qihao Liu, Ju He, Xinyang Zhang, Yang Liu, Liang-Chieh Chen, Xi Chen

**核心方法**: 提出掩码比特自回归建模（BAR），支持任意规模的codebook。通过masked bit modeling head逐步生成bit而非token。

**效果评估**: ImageNet-256上gFID达到0.99（新的SOTA）。

**端侧价值**: 7/10 - 高效的离散生成方法，推理成本降低。

---

## 2602.09082 - UI-Venus-1.5

**作者**: Venus Team, Changlong Gao, Zhangxuan Gu, Yulin Liu等27位作者

**核心方法**: 提出统一端到端GUI Agent UI-Venus-1.5，包含2B、8B和30B-A3B三个变体。引入Mid-Training阶段、在线RL与模型合并技术。

**效果评估**: ScreenSpot-Pro 69.6%，VenusBench-GD 75.0%，AndroidWorld 77.6%。

**端侧价值**: 7/10 - GUI自动化对端侧应用有参考价值。

---

## 2602.10090 - Agent World Model

**作者**: Zhaoyang Wang, Canwen Xu, Boyi Liu, Yite Wang, Siwei Han, Zhewei Yao, Huaxiu Yao, Yuxiong He

**核心方法**: 提出Agent World Model（AWM），全合成环境生成管道。生成1000个环境，每个环境包含35个工具，支持代码驱动和数据库支持的可靠状态转换。

**效果评估**: 仅在合成环境中训练即可实现强泛化，三个基准上显著超越基线。

**端侧价值**: 7/10 - 合成环境生成对端侧Agent训练有参考价值。

---

## 2602.10560 - GRU-Mem

**作者**: Leheng Sheng, Yongtao Zhang, Wenchang Ma, Yaorui Shi, Ting Huang, Xiang Wang, An Zhang, Ke Shen, Tat-Seng Chua

**核心方法**: 提出GRU-Mem，包含更新门和退出门的门控循环记忆机制。通过RL端到端训练，奖励正确的更新和退出行为。

**效果评估**: 推理速度提升最高400%，显著优于vanilla MemAgent。

**端侧价值**: 9/10 - 高效的长上下文推理方案，对端侧价值高。

---

## 2602.10815 - DC-SFT

**作者**: Aojun Lu, Tao Feng, Hangjie Yuan, Wei Li, Yanan Sun

**核心方法**: 提出Difficulty-Curated SFT（DC-SFT），基于样本难度显式过滤训练集。从数据中心视角解释RL为何比SFT泛化更好。

**效果评估**: OOD泛化显著提升，超越基于RL的训练，同时更稳定和高效。

**端侧价值**: 9/10 - 简单有效的数据选择策略，对端侧训练效率提升明显。

---

## 2602.12275 - OPCD

**作者**: Tianzhu Ye, Li Dong, Xun Wu, Shaohan Huang, Furu Wei (Microsoft)

**核心方法**: 提出On-Policy Context Distillation（OPCD），训练学生模型在其自身生成的轨迹上，最小化与上下文条件教师的reverse KL散度。

**效果评估**: 数学推理、文本游戏等任务上显著超越基线方法。

**端侧价值**: 7/10 - 上下文蒸馏技术对端侧模型压缩有参考价值。

---

## 2602.12276 - CATTS

**作者**: Nicholas Lee, Lutfi Eren Erdogan, Chris Joseph John, Surya Krishnapillai, Michael W. Mahoney, Kurt Keutzer, Amir Gholami (UC Berkeley, Stanford)

**核心方法**: 提出Confidence-Aware Test-Time Scaling（CATTS），使用基于投票的不确定性（熵、top-1/top-2 margin）动态分配计算资源。仅在决策真正分歧时增加计算。

**效果评估**: WebArena-Lite和GoBrowse上相比React提升9.1%，同时节省2.3x tokens。

**端侧价值**: 8/10 - 测试时缩放技术对端侧计算资源优化有参考价值。

---

## 2602.12670 - SkillsBench

**作者**: Xiangyi Li, Wenbo Chen, Yimin Liu等40位作者

**核心方法**: 提出SkillsBench基准，包含86个任务、11个领域，配以精选Skills和确定性验证器。评估三种条件：无Skills、精选Skills、自生成Skills。

**效果评估**: 精选Skills平均提升16.2个百分点，但16/84个任务显示负向效果。自生成Skills无提升。

**端侧价值**: 7/10 - Agent技能评估基准，对端侧技能设计有指导意义。

---

## 2602.12675 - SLA2

**作者**: Jintao Zhang, Haoxu Wang, Kai Jiang, Kaiwen Zheng, Youhe Jiang, Ion Stoica, Jianfei Chen, Jun Zhu, Joseph E. Gonzalez

**核心方法**: 提出SLA2，包含可学习路由器和可学习组合系数，解决SLA形式化不匹配问题。引入量化感知训练（QAT）减少量化误差。

**效果评估**: 97%稀疏度下视频生成质量超越基线，18.7x加速，内核级速度达4,079 TOPS。

**端侧价值**: 9/10 - 极致的稀疏加速方案，对端侧部署价值极高。

---

## 2602.14041 - BitDance

**作者**: Yuang Ai, Jiaming Han, Shaobin Zhuang, Weijia Mao, Xuefeng Hu, Ziyan Yang, Zhenheng Yang, Huaibo Huang, Xiangyu Yue, Hao Chen

**核心方法**: 提出BitDance，使用二进制token而非codebook索引进行自回归图像生成。通过binary diffusion head解决巨大token空间的采样问题，引入next-patch diffusion并行解码。

**效果评估**: ImageNet 256x256上FID 1.24（AR模型SOTA），1024x1024图像生成加速30x以上。

**端侧价值**: 8/10 - 高效的AR生成方案，对端侧图像生成有价值。

---

## 2602.15030 - Sphere Encoder

**作者**: Kaiyu Yue, Menglin Jia, Ji Hou, Tom Goldstein

**核心方法**: 提出Sphere Encoder，学习将自然图像均匀映射到球面潜在空间，然后从球面上的随机点解码生成图像。只需图像重建损失训练。

**效果评估**: 少步生成（<5步）性能与多步扩散模型相当，推理成本大幅降低。

**端侧价值**: 8/10 - 少步生成范式对端侧推理效率提升显著。

---

## 2602.15763 - GLM-5

**作者**: 智谱AI与清华大学

**核心方法**: 提出GLM-5，包含深度稀疏注意力（DSA）、多潜在注意力优化（MLA）、异步RL基础设施和多阶段训练流程。引入交错思考、保留思考等模式。

**效果评估**: SWE-bench Verified 77.8%，长序列场景成本降低50%。

**端侧价值**: 9/10 - 稀疏注意力显著降低长上下文成本，对端侧价值高。

---

## 2602.15922 - DreamZero

**作者**: Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng等36位作者 (NVIDIA, Stanford, Georgia Tech等)

**核心方法**: 提出DreamZero，基于预训练视频扩散backbone构建World Action Model（WAM）。通过预测未来世界状态和动作学习物理动力学，实现零样本策略。

**效果评估**: 相比SOTA VLA在真实机器人任务上泛化提升2x，14B模型实现7Hz实时闭环控制。

**端侧价值**: 8/10 - 零样本迁移能力对端侧机器人应用价值高。

---

## 2602.17270 - Unified Latents

**作者**: Jonathan Heek, Emiel Hoogeboom, Thomas Mensink, Tim Salimans (Google DeepMind)

**核心方法**: 提出Unified Latents（UL），通过将encoder输出噪声与prior的最小噪声水平链接，获得提供潜在比特率上界的训练目标。

**效果评估**: ImageNet-512上FID 1.4，Kinetics-600上FVD 1.3（SOTA）。

**端侧价值**: 7/10 - 高效的潜在表示学习，训练FLOPs降低。

---

## 2602.18308 - JPmHC

**作者**: Biswa Sengupta, Jinhua Wang, Leo Brunswic

**核心方法**: 提出JPmHC，用可训练线性混合器替换identity skips，同时显式控制梯度条件。引入自由概率分析预测Jacobian谱，内存高效的隐式微分。

**效果评估**: ARC-AGI上相比双随机基线实现更快收敛、更高准确率、更低计算成本。

**端侧价值**: 7/10 - 架构优化对端侧模型训练稳定性有参考价值。

---

## 2602.20021 - Agents of Chaos

**作者**: Natalie Shapira, Chris Wendler, Avery Yen等38位作者

**核心方法**: 对部署在具有持久内存、邮箱、文件系统等的真实实验室环境中的自主LLM Agent进行红队演练。记录11个代表性案例研究。

**效果评估**: 发现安全、隐私和治理相关漏洞，包括：未授权合规、敏感信息泄露、破坏性系统动作、拒绝服务、资源消耗失控、身份欺骗等。

**端侧价值**: 8/10 - 首次系统研究真实部署中Agent的涌现性失效模式，对行业安全标准有重要参考价值。

---

## 2602.21193 - Nemotron-Terminal

**作者**: 待补充

**核心方法**: 提出Nemotron-Terminal终端智能体数据工程方案，优化终端场景下的Agent训练数据。

**效果评估**: 终端智能体任务上性能显著提升。

**端侧价值**: 9/10 - 直接针对端侧场景的优化方案，价值高。

---

## 2602.22208 - Solaris

**作者**: Georgy Savva, Oscar Michel, Daohan Lu, Suppakit Waiwitlikhit, Timothy Meehan, Dhairya Mishra, Srivats Poddar, Jack Lu, Saining Xie (NVIDIA)

**核心方法**: 提出首个多人Minecraft视频世界模型Solaris。开发多人数据系统，收集1264万帧，提出多人运动、记忆、接地、建筑和视图一致性评估框架。

**效果评估**: 架构和训练设计显著超越现有基线。

**端侧价值**: 6/10 - 多人视频世界模型对端侧应用价值有限。

---

## 2602.23330 - Fine-Grained Trading System

**作者**: Kunihiro Miyazaki, Takanobu Kawahara, Stephen Roberts, Stefan Zohren

**核心方法**: 提出细粒度任务分解的多智能体LLM交易框架，将投资分析分解为细粒度任务而非粗粒度指令。在日本股票数据上评估。

**效果评估**: 细粒度任务分解显著提升风险调整回报，标准化投资组合优化实现卓越性能。

**端侧价值**: 6/10 - 金融领域垂直应用，对端侧价值有限。

---

## 总结

本月精选论文的端侧价值Top 10：

| 排名 | 论文ID | 题目 | 端侧价值 |
|:---:|:---:|:---|:---:|
| 1 | 2602.06036 | DFlash: 块扩散推测解码 | 9/10 |
| 2 | 2602.06960 | InftyThink+: 无限视野推理 | 9/10 |
| 3 | 2602.10560 | GRU-Mem: 门控循环记忆 | 9/10 |
| 4 | 2602.10815 | DC-SFT: 数据中心SFT | 9/10 |
| 5 | 2602.12675 | SLA2: 稀疏线性注意力 | 9/10 |
| 6 | 2601.22966 | GatedNorm: 门控归一化 | 9/10 |
| 7 | 2602.15763 | GLM-5: 高效Agent工程 | 9/10 |
| 8 | 2602.21193 | Nemotron-Terminal | 9/10 |
| 9 | 2602.04770 | Drifting Models: 漂移生成 | 8/10 |
| 10 | 2602.15030 | Sphere Encoder | 8/10 |
