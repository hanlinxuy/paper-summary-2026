# Generative Modeling via Drifting

## 基本信息
- arXiv ID: 2602.04770
- 作者: 待确认

## 核心方法

**研究背景**：现有生成模型范式存在局限：扩散/流模型推理需多步迭代计算开销大；GANs依赖对抗优化训练不稳定；标准化流需可逆架构。

**核心方法 - Drifting Models（漂移模型）**：

1. **训练时前推分布演化**：利用神经网络优化的迭代性（如SGD），将每次参数更新视为对前推分布q的演化，而非在推理时进行多步迭代

2. **漂移场（Drifting Field）设计**：
   - 定义漂移场V_{p,q}(x)控制样本移动方向
   - 满足**反对称性**：V_{p,q}(x) = -V_{q,p}(x)，保证平衡条件（q=p时V=0）
   - 采用吸引-排斥机制：
     - 吸引场V_p^+(x)：由数据分布p的正样本驱动
     - 排斥场V_q^-(x)：由生成分布q的负样本驱动

3. **固定点训练目标**：
   $$\mathcal{L} = \mathbb{E}_\epsilon \left[ \left\| f_\theta(\epsilon) - \text{stopgrad}\left( f_\theta(\epsilon) + V_{p,q_\theta}(f_\theta(\epsilon)) \right) \right\|^2 \right]$$

4. **特征空间扩展**：将漂移损失计算在预训练自监督特征空间（如MAE、MoCo）中

5. **分类器自由引导（CFG）**：CFG作为训练时行为实现，通过混合生成分布与无条件数据分布构造负样本

## 实验结果

**ImageNet 256×256单步生成**：
| 方法 | FID |
|------|-----|
| DiT-XL/2 (多步) | 1.42 |
| iMeanFlow (单步) | 1.72 |
| **Drifting Model L/2 (本文)** | **1.54** |

- 像素空间生成：FID **1.61**，显著优于StyleGAN-XL（2.30）
- 计算成本仅87G FLOPs，远低于StyleGAN-XL（1574G）

**跨域应用（机器人控制）**：
- 单步Drifting Policy在1-NFE下匹配或超越100-NFE Diffusion Policy

## 关键贡献

1. 首次提出**训练时漂移场**实现分布演化，完全摒弃SDE/ODE框架
2. 实现**原生单步（1-NFE）生成**，无需蒸馏
3. 开辟了不依赖微分方程、对抗训练或可逆约束的高质量生成新范式
