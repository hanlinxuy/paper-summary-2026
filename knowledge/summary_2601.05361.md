# Noise sensitivity in last-passage percolation

## 基本信息
- arXiv ID: 2601.05361
- 作者: Daniel Ahlberg, Malo Hillairet, Ekaterina Toropova
- 机构: Department of Mathematics, Stockholm University; Institut Fourier, Université Grenoble Alpes

## 核心方法

### 问题背景
噪声敏感性（Noise Sensitivity）最初由Benjamini、Kalai和Schramm在1999年提出，描述了临界Bernoulli渗流的一个显著现象：小随机扰动足以完全去相关其连接性质。

### 主要结果
本文证明了与KPZ（Kardar-Parisi-Zhang）普适类相关的空间生长过程的第一个噪声敏感性实例。具体而言，证明了在几何最后通道渗透（geometric last-passage percolation）中，旅行时间相对于作用于几何权重的Bernoulli编码的扰动是噪声敏感的。

### 技术贡献
1. **BKS定理的推广**：将著名的Benjamini-Kalai-Schramm噪声敏感性/影响力定理从布尔函数推广到实值函数

2. **影响上界**：给出了任意顶点位于两点间测地线上概率的精确上界，这本身具有独立价值

3. **形式化定义**：
   - 在$\Z^2$的整数点上赋予参数为$p\in(0,1)$的几何分布权重
   - 从$u$到$v$的最后通过时间定义为：$T(u,v)=\max\{T(\gamma):\gamma\text{是从}u\text{到}v\text{的有向路径}\}$
   - 扰动通过独立重采样每个比特实现，概率为$\varepsilon=1-e^{-t}$

### 证明思路
根据BKS定理的推广，定理证明归约为证明：
$$\sum_{v\in\Z^2}\sum_{i\in\N} I_{v,i}(T_n)^2 = o(n^{2/3})$$

其中$I_{v,i}(T_n)$是用于编码顶点$v$权重的第$i$个比特对旅行时间$T_n$的影响。

## 关键贡献

1. **首个KPZ类模型的噪声敏感性证明**：这是首次在KPZ普适类的空间生长模型中建立噪声敏感性

2. **BKS定理的广义化**：将BKS噪声敏感性/影响力定理从布尔函数扩展到实值函数，提供了定量版本

3. **几何影响边界**：给出了顶点位于测地线上概率的精确边界

4. **一般化噪声定义**：证明了两种自然的噪声定义方式大致等价

5. **与黑噪声的联系**：表明从稳定性到噪声敏感性的转变预计在$t\asymp n^{-1/3}$处发生
