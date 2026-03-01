# G-KdVNet: ANN-ADM Surrogate for Geophysical KdV Equation

## 基本信息
- arXiv ID: 2601.04408
- 作者: Mrutyunjaya Sahoo, Arup Kumar Sahoo, Snehashish Chakraverty
- 领域: Dynamical Systems (math.DS)

## 核心方法

### 研究背景
Korteweg-de Vries (KdV) 方程是描述非线性色散波的重要数学模型，在流体动力学、等离子体物理等领域有广泛应用。Coriolis常数（地理物理参数）对KdV方程的解有重要影响，但传统数值方法计算成本高。

### 主要成果
本文提出G-KdVNet，一种基于神经网络的代理模型，用于近似求解地理物理KdV方程。该方法结合了Adomian分解方法(ADM)生成训练数据。

### 技术框架
1. **Adomian分解方法(ADM)**: 用于生成高质量训练数据
2. **神经网络近似**: 使用ANN学习KdV方程的解
3. **Coriolis参数分析**: 探索Coriolis常数对解的影响

### 核心创新
- 将ADM与深度学习结合，创建混合求解方法
- 分析Coriolis参数对波传播特性的影响
- 实现最高0.001量级的绝对误差

## 关键贡献

1. **新方法**: 提出G-KdVNet智能计算框架

2. **训练数据**: 使用Adomian分解方法生成训练数据，保证解的准确性

3. **参数分析**: 系统研究Coriolis常数对KdV方程解的影响

4. **性能验证**: 在未见数据上达到0.001级别的绝对误差

## 效果评估

- 绝对误差: 最高达到0.001（未见数据）
- 方法对比: 与基准方法相比表现优异
- 可视化: 提供表格和图形深入分析Coriolis参数效应

## 结论

G-KdVNet为地理物理KdV方程的求解提供了一种高效的智能计算方法，结合了传统ADM方法的准确性和神经网络的计算效率。
