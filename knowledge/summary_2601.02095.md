# Metric Distortion with Preference Intensities

## 基本信息
- arXiv ID: 2601.02095
- 作者: Mehrad Abbaszadeh, Ali Ansarifar, Mohamad Latifian, Masoud Seddighin
- 领域: Computer Science and Game Theory (cs.GT)

## 核心方法

### 研究背景
在排名投票中，每个投票者提交严格排名格式 $a \succ b \succ c \succ d$ 的选票。虽然这种投票形式有良好特性，但问题在于它是否足够表达投票者的偏好。Kahng, Latifian和Shah提出在排名中加入强度(inensities)来解决这个问题。

### 主要成果
本文从度量失真(metric distortion)角度分析带偏好强度的投票格式。设计了Positional Scoring Matching规则类，通过求解零和博弈找到问题的最优成员。该规则考虑强度因素，达到小于3的失真度。

### 技术框架
1. **带强度的排名选票**: 允许使用 $\succ\!\succ$ 和 $\succ$ 表达强度偏好和普通偏好
2. **Positional Scoring Matching规则**: 可用于度量设置中不同问题的投票规则类
3. **零和博弈优化**: 找到该类中最优的规则
4. **失真度分析**: 证明忽略强度可能带来的损失下界

### 核心创新
- 将Kahng等人的工作从功利主义失真框架扩展到度量失真框架
- 设计新的投票规则达到小于3的失真度
- 证明忽略偏好强度可能导致严重的失真损失

## 关键贡献

1. **新框架**: 从度量失真角度分析带强度的投票

2. **最优规则设计**: 通过博弈论方法找到最优的Positional Scoring Matching规则

3. **失真界限**: 证明忽略强度可能带来的失真损失

4. **理论贡献**: 为偏好强度在投票中的应用提供理论基础

## 效果评估

- 失真度: < 3 (达到的理论界限)
- 理论分析: 提供忽略强度与考虑强度的失真对比

## 结论

通过在投票中引入偏好强度并从度量失真角度分析，可以显著改善投票结果的质量。忽略偏好强度可能导致严重的性能损失。
