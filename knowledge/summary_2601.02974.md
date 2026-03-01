# K-stability of Fano weighted hypersurfaces via plt flags and convex geometry

## 基本信息
- arXiv ID: 2601.02974
- 作者: Livia Campo, Kento Fujita, Taro Sano, Luca Tasin
- 机构: Institut für Mathematik, Universität Wien; Osaka University; Kobe University; Università degli Studi di Milano

## 核心方法

### 研究背景
K-稳定性已成为Fano簇研究的核心概念，作为Kähler-Einstein度量存在的代数几何对应物。它在双有理几何、模理论 和复微分几何之间架起了桥梁，在Fano簇的分类及其退化中起着关键作用。

### 主要成果
本文系统地研究了准光滑加权Fano超曲面的K-稳定性，结合了双有理几何和凸几何技术。

### 技术框架
1. **Abban-Zhuang方法**: 建立稳定性阈值下界，将问题归约到低维情况
2. **plt flags (Purely Log Terminal Flags)**: 使用不一定可接受的plt flags，这是方法的关键特征
3. **凸几何技术**: 用于估计稳定性阈值

### 核心定理

**定理1** (索引1，最多两个权重大于1的情况):
设$a>1$和$n\geq3$为整数。设$X=X_d\subset\mathbb{P}(1^{n+1},a)$是次数$d$、维数$n$、索引$1$的准光滑Fano加权超曲面。则：
$$\delta\left(X; \mathcal{O}_X(1)\right) \ge \frac{n+1}{n} > 1$$
特别地，$X$是K-稳定的。

**定理2** (恰好两个权重大于1的情况):
设$2\leq a\leq b$和$n\geq3$为整数。设$X=X_d\subset\mathbb{P}(1^n,a,b)$是次数$d$、维数$n$、索引$1$的准光滑Fano加权超曲面。则：
$$\delta\left(X; \mathcal{O}_X(1)\right) \ge \frac{n+1}{n+\frac{1}{a}} > 1$$
特别地，$X$是K-稳定的。

### 关键概念
- **广义Eckardt点**: 点$P=[0:\cdots:0:1]$是$X$的广义Eckardt点
- **稳定性阈值($\delta$)**: klt Fano簇$X$是K-稳定的当且仅当$\delta(X; -K_X) > 1$
- **准光滑(Quasi-smooth)**: 加权超曲面的一种特殊光滑性概念

## 关键贡献

1. **系统性框架**: 建立了研究加权Fano超曲面K-稳定性的系统框架，结合双有理和凸几何技术

2. **K-稳定性证明**: 证明了所有索引为1、至多两个权重大于1的准光滑加权Fano超曲面是K-稳定的

3. **K-不稳定实例**: 构建了多个低索引的K-不稳定准光滑加权Fano超曲面例子，这些是已知首批具有此性质的高维例子

4. **方法创新**: 使用不一定可接受的plt flags，这是方法的关键创新点

5. **sharp估计**: 对于广义Eckardt点的情况，获得了尖锐估计：
$$\delta_P\left(X; \mathcal{O}_X(1)\right)=\frac{n(n+1)}{ak+n}$$

6. **与光滑情形对比**: 发现了与标准投影空间中光滑超曲面的显著差异——构造了索引小于维数的K-不稳定例子
