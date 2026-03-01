# PRISMA: Reinforcement Learning Guided Two-Stage Policy Optimization in Multi-Agent Architecture for Open-Domain Multi-Hop Question Answering

## 基本信息
- arXiv ID: 2601.05465
- 作者: Yu Liu, Wenxiao Zhang, Cong Cao, Wenxuan Lu, Fangfang Yuan, Diandian Guo, Kun Peng, Qiang Sun, Kaiyan Zhang, Yanbing Liu, Jin B. Hong, Bowen Zhou, Zhiyuan Ma
- 机构: Institute of Information Engineering, Chinese Academy of Sciences; The University of Western Australia; Huazhong University of Science and Technology; Tsinghua University; Shanghai AI Laboratory

## 核心方法

### 问题定义
将开放域多跳问答形式化为：给定问题q和语料库C={d_1,...,d_N}（N=21M Wikipedia段落），生成答案a和支撑事实F⊂C。系统需要：(i)将q分解为依赖感知的子问题；(ii)基于中间答案检索证据；(iii)验证证据和答案，必要时重试；(iv)合成最终答案并标注来源。

### PRISMA架构
提出Plan-Retrieve-Inspect-Solve-Memoize (PRISMA)架构，包含：
- **Planner**: 将问题分解为带有答案占位符（如[ANSWER_1]）的依赖感知子问题
- **Memoizer**: 检查语义缓存避免冗余处理
- **Retriever**: 三级联检索——密集检索、混合重排序、交叉编码器评分
- **Context Inspector**: 验证子问题质量和文档充分性，触发重写或检索扩展
- **Solver**: 生成带引用的答案
- **Reasoning Inspector**: 验证推理 grounding，启用带反馈的重试
- **Memoize**: 缓存验证答案以供重用

### 两阶段训练：GRPO + OARPO
**Stage I - 专家校准**：独立优化Planner和Solver，使用GRPO分别训练
- Planner专门负责依赖感知分解
- Solver专门负责基于检索证据的 grounding 推理

**Stage II - OARPO**：冻结专家后训练Inspector
- 使用观察增强状态 s_aug = (x, τ_{P,S})
- Inspector学习残差失败模式，触发针对性恢复动作（pass/rewrite/expand/retry）

## 实验结果

### 主实验结果（In-distribution）
| Benchmark | EM | F1 |
|-----------|-----|-----|
| MuSiQue | **30.6** | **39.5** |
| HotpotQA | **50.2** | **55.8** |
| 2WikiMHQA | **57.0** | **60.1** |

### Out-of-distribution
| Benchmark | EM | F1 |
|-----------|-----|-----|
| NaturalQ | **38.6** | **53.7** |
| Bamboogle | **46.4** | **59.2** |
| Chemistry | **75.3** | **78.5** |
| Game | **73.3** | **77.1** |

### 与基线对比
- 超越最强训练基线TIRESRAG-R1：在MuSiQue上提升+11.2/+9.5点
- 超越API模型IRCoT(GPT-5-Medium)：在MuSiQue上提升+7.2/+4.5点
- 在10个基准数据集上达到SOTA

## 关键贡献

1. **解耦的多智能体架构**：提出PRISMA架构，将规划、检索、检查、解决、记忆功能解耦，灵感来自研究人员的解决问题工作流程

2. **两阶段GRPO训练**：Stage I校准Planner和Solver为专门专家，Stage II使用OARPO训练Inspector进行残差审计和恢复

3. **观察感知的残差策略优化(OARPO)**：Inspector基于专家轨迹学习残差失败模式，触发针对性恢复动作

4. **推理引导的合作**：Inspector为Planner提供基于推理的反馈以改进分解和细粒度检索，同时在Solver中强制执行基于证据的推理

5. **高效部署**：可在真实场景中高效部署，在10个开放域基准上达到SOTA
