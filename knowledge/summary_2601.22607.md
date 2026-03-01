# From Self-Evolving Synthetic Data to Verifiable-Reward RL: Post-Training Multi-turn Interactive Tool-Using Agents

## 基本信息
- arXiv ID: 2601.22607
- 作者: 待确认

## 核心方法

**研究背景**：交互式工具使用智能体在后训练阶段面临两大核心瓶颈：高质量多轮工具使用数据难以规模化获取、强化学习信号被用户模拟器污染。

**核心方法 - 统一框架EigenData + 可验证奖励RL**：

1. **EigenData自演化合成引擎**：
   - 分层多智能体：编排层（Planner + Prompt Engineer + Judge）+ 执行层7类专业Worker
   - 闭环自演化：Judge输出结构化critique → 更新prompt & workflow
   - 可执行验证器：为每个样本生成Python脚本，对比终态与关键函数调用
   - 三阶段扩量：64组多样化prompt初始化 → 小批量pilot迭代16轮 → 大规模在线监控回滚

2. **用户模型SFT + GRPO-Verifier**：
   - 先对用户模型做SFT消除奖励噪声
   - 大batch采样（64条完整轨迹）降低用户方方差
   - 动态过滤：若G条轨迹奖励全相同则丢弃该任务
   - 可验证奖励：用验证函数比对终态，给出二元R∈{0,1}

## 实验结果

**主要性能对比（τ²-bench三领域）**：
| 训练方式 | 模型 | 平均pass^1 |
|---------|------|-----------|
| Separate | Qwen3-235B-A22B+RL | 81.9 |
| Mix | Qwen3-235B-A22B+RL | **81.3** |

- Airline追平Gemini-3.0 Pro，Telecom超所有闭源模型
- 超过Qwen3-Max-Thinking（80.7）与GPT-5（80.0）

**消融实验**：
- 去掉验证器/自演化 → SFT掉4-12 pp
- 用户模型不做SFT → RL掉20 pp
- 关动态过滤/小batch → RL掉5-12 pp

## 关键贡献

1. **EigenData**：首个把"自演化闭环+可执行验证器"引入多轮工具对话合成的数据引擎
2. **用户模型SFT + 大batch GRPO-Verifier**：解决交互式RL信号噪声问题
3. **零人工标注**：实现无需昂贵人工标注即可规模化提升多轮工具使用能力
