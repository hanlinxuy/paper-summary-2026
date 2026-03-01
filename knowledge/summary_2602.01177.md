# Equivalence of Privacy and Stability with Generalization Guarantees in Quantum Learning

## 基本信息
- arXiv ID: 2602.01177
- 作者: Ayanava Dasgupta, Naqueeb Ahmad Warsi, Masahito Hayashi

## 核心方法

本文提出统一的信息论框架，阐明稳定性、隐私与量子学习算法泛化性能之间的相互作用。

**1. 经典-量子次高斯性（Classical-Quantum Sub-Gaussianity）**
- 引入损失算子集合的次高斯性定义，统一经典数据和量子测量涨落
- 在此假设下，期望泛化误差被界定为 mutual information 的平方根：$\overline{\text{gen}}_{\rho}(\cN) \leq \sqrt{2\alpha^2 I[S\Te;WB']}$

**2. 概率泛化界**
- 使用 Sandwiched Rényi 散度证明概率意义上的泛化界
- 假设 i.i.d. 数据结构和损失算子分解，获得 $O(1/\sqrt{n})$ 收敛率

**3. 1-邻域(ε,δ)-差分隐私**
- 提出量子差分隐私的"1-neighbor"框架
- 包含三个条件：置换不变性、隐私性、支集一致性
- 推导机制无关的 mutual information 上界

**4. 信息论可容许性（ITA）**
- 针对不诚实数据处理器的场景
- 定义算法在特定训练集合上的信息论最优性
- 揭示量子非交换性允许同时满足ITA和差分隐私

## 实验结果

**理论结果（无具体数值实验）**：
- 期望泛化界：$\overline{\text{gen}}_{\rho}(\cN) \leq \sqrt{2\alpha^2 I[S\Te;WB']}$
- 概率界：使用 Rényi 散度的泛化界
- 隐私稳定性界：$I[S;WB'] \leq (|\mathcal{Z}| - 1) \ln(n e\eps) + h_{\abs{\cZ}}(\eps,\delta)$

## 关键贡献

1. **稳定性⇒可泛化性**：证明稳定的量子算法固有泛化能力，建立信息泄漏与泛化误差的直接联系

2. **隐私⇒可泛化性**：建立 (ε,δ)-量子差分隐私 ⇒ 稳定性 ⇒ 泛化的逻辑链条

3. **量子优势**：经典情形下ITA意味着完全数据恢复（无隐私），而量子情形允许同时满足ITA和隐私保护，体现量子力学的基本优势

4. **双向界**：不仅给出泛化上界，还给出期望真实损失的下界，形成"夹心"结构
