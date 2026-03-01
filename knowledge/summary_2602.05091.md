# Evaluating Robustness and Adaptability in Learning-Based Mission Planning for Active Debris Removal

## 基本信息
- arXiv ID: 2602.05091
- 作者: Agni Bandyopadhyay, Günther Waxenegger-Wilfing (Julius-Maximilians-Universität Würzburg)
- 来源: IEEE Conference

## 核心方法

本文比较了三种主动碎片移除(ADR)任务规划器：标准PPO、域随机化PPO和蒙特卡洛树搜索(MCTS)。

**任务定义：**
- 低地球轨道(LEO) 700-800km高度带的碎片收集
- 服务航天器从700km轨道上的燃料站出发
- 每回合50个碎片对象，7天任务时间，3 km/s Δv预算

**三种规划器：**

1. **标准Masked PPO**
   - 使用Stable-Baselines3的MaskablePPO
   - 训练于固定任务参数
   - 2层隐藏层，每层256单元
   - 训练100万步

2. **域随机化Masked PPO**
   - 任务参数在每回合随机化：
     - Δv_max: [1, 3.5] km/s
     - 任务时间: [1, 7] 天
   - 训练550万步
   - 暴露于约束和非约束环境

3. **蒙特卡洛树搜索 (MCTS)**
   - 使用UCT选择规则
   - 每步200次模拟
   - 探索常数c_uct = 1.5
   - Rollout深度限制为15
   - 统一随机策略

**动作空间与约束：**
- 动作：转移到未访问碎片或燃料站
- 约束：剩余Δv、剩余任务时间、访问状态
- 使用动作掩码确保可行性

## 实验结果

**三种场景测试：**
- Nominal: 7天，3 km/s Δv
- Time-limited: 3天，3 km/s Δv  
- Δv-limited: 7天，1 km/s Δv

**性能对比（平均碎片访问数）：**

| 场景 | PPO(标准) | PPO(随机化) | MCTS |
|------|-----------|-------------|------|
| Nominal | 29.1 | 28.2 | 27.1 |
| Time-limited | 12.6 | 14.1 | 11.9 |
| Δv-limited | 3.2 | 8.1 | 15.0 |

**计算时间：**
- PPO: < 1秒/回合
- MCTS: > 4分钟/回合

## 关键贡献

1. **系统评估了三种ADR任务规划策略**，在名义、燃料受限和时间受限场景下进行对比
2. **展示域随机化可有效缓解分布偏移问题**，提高策略在未见约束下的适应性
3. **揭示学习策略与搜索方法的根本权衡**：快速推理 vs 高度适应性
4. **量化MCTS的计算成本**：比PPO慢约240倍
5. **为未来混合学习-规划方法奠定基础**，结合训练时多样性与在线规划能力
