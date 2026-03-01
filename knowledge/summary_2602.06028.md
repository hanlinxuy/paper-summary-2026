# Context Forcing: Consistent Autoregressive Video Generation with Long Context

## 基本信息
- arXiv ID: 2602.06028
- 作者: 待确认

## 核心方法

**研究背景**：现有实时长视频生成方法存在"学生-教师不匹配"问题——短上下文教师监督长上下文学生，导致教师无法指导全局时间依赖。

**核心问题 - 遗忘-漂移困境**：
- 遗忘：短记忆窗口导致长距离生成中丢失先前主题与场景
- 漂移：长上下文窗口虽保留历史，但缺乏能纠正长期误差的教师监督

**核心方法 - Context Forcing**：

1. **长上下文教师监督长上下文学生**：
   - Context Teacher：预训练于视频续写任务，具备处理长上下文输入能力
   - 消除监督鸿沟：教师能够评估学生生成历史的全局一致性

2. **两阶段课程式训练**：
   - Stage 1（本地分布匹配）：对齐短窗口分布，学习局部动态
   - Stage 2（上下文分布匹配，Contextual DMD）：在学生自身生成分布上取值，强制学生适应自生成上下文

3. **Slow-Fast上下文管理系统**：
   - Attention Sink：保留初始token，稳定注意力
   - Slow Memory：基于惊讶度巩固策略动态存储高信息量关键帧
   - Fast Memory：滚动FIFO队列，捕获即时局部上下文

4. **有界位置编码**：约束RoPE索引于固定范围，防止长序列分布偏移

5. **Error-Recycling Fine-Tuning (ERFT)**：向教师注入历史模型残差，训练教师从含噪上下文中恢复正确输出

## 实验结果

**上下文长度**：
- 实现**20秒+有效上下文**，较SOTA（LongLive 3.0s、FramePack 9.2s）提升**2-10倍**

**60秒视频生成**：
| 指标 | Context Forcing | LongLive | FramePack |
|------|----------------|----------|-----------|
| DINO Score | **87.89** | 86.26 | 68.50 |
| CLIP-F | **95.35** | 94.82 | - |
| VBench总分 | 82.45 | 83.64 | - |

- 避免LongLive的突发场景重置（flashback artifacts）

## 关键贡献

1. 首次提出长上下文教师监督长上下文学生的训练范式
2. 设计Slow-Fast Memory与有界位置编码，使20秒+上下文实时推断计算可行
3. 在分钟级视频生成中实现SOTA长程一致性，同时缓解遗忘与漂移
