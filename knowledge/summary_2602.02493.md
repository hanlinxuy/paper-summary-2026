# PixelGen: Pixel Diffusion Beats Latent Diffusion with Perceptual Loss

## 基本信息
- arXiv ID: 2602.02493
- 作者: 待确认

## 核心方法

**研究背景**：像素扩散模型在高维像素空间中直接生成图像时优化困难、生成质量落后于潜在扩散模型（LDM）。

**核心方法**：

1. **简化预测目标**：沿用JiT的x-prediction范式，网络直接输出干净图像，再转为速度保持流匹配采样优势

2. **引入互补感知损失，引导模型聚焦"感知流形"**：
   - 局部纹理损失：利用冻结VGG特征的LPIPS损失，强化边缘与细粒度细节
   - 全局语义损失：提出P-DINO损失，在冻结DINOv2-B的patch特征上计算余弦距离，保证物体布局与语义一致
   - 两项损失仅在去噪后期（低噪声阶段）启用，避免早期高噪声阶段过度约束导致多样性下降

3. **端到端训练目标**：
   $$\mathcal{L}= \mathcal{L}_{\mathrm{FM}}+\lambda_1\mathcal{L}_{\mathrm{LPIPS}}+\lambda_2\mathcal{L}_{\mathrm{P\text{-}DINO}}+\mathcal{L}_{\mathrm{REPA}}$$

## 实验结果

**ImageNet-256基准对比**：
| 方法 | FID |
|------|-----|
| JiT (像素扩散) | 23.67 |
| PixelGen (本文) | **7.53** |
| DDT-L/2 (潜在扩散) | 10.00 |

- 端到端像素扩散首次击败两阶段潜在扩散

**完整训练结果**：
- 无CFG：80 epoch FID **5.11**，低于REPA-XL/2（800 epoch，5.90）
- 有CFG：160 epoch FID **1.83**，优于同期像素扩散方法

**文本到图像**：
- GenEval整体分：**0.79**，与FLUX.1-dev、OmniGen2等8B-12B模型持平，参数量仅1.1B

## 关键贡献

1. 首次将**LPIPS局部感知损失 + DINOv2全局感知损失**同时引入像素扩散训练
2. 配合噪声门控策略，实现端到端、无VAE的图像生成
3. 首次证明**像素扩散+感知监督**可在同等训练预算下**击败两阶段潜在扩散**
