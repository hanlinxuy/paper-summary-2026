# BitDance: Scalable Autoregressive Image Generation with Binary Visual Tokens

## 基本信息
- arXiv ID: 2602.14041
- 作者: 待确认

## 核心方法

**研究背景**：自回归（AR）图像生成面临三个核心挑战：高保真视觉表示构建、大词汇表空间下的高效采样、推理效率优化。

**核心方法 - BitDance**：

1. **大规模二进制视觉分词器**：
   - 采用无查找量化（Lookup-Free Quantization, LFQ）构建高熵二进制分词器
   - 词汇表扩展至2^256，使离散表示达到连续VAE的重建保真度
   - 分组LFQ策略平衡内存与精度，PSNR达25.29，SSIM达0.74

2. **二进制扩散头（Binary Diffusion Head）**：
   - 将二进制token嵌入连续空间超立方体顶点
   - 采用Rectified Flow框架建模联合分布
   - 避免传统分类头参数爆炸问题（h×2^d）

3. **下一区块扩散（Next-Patch Diffusion）**：
   - 将图像划分为空间区块（patch），实现块级自回归建模
   - 块级因果注意力机制允许同区块token相互可见
   - 支持并行多token预测，显著提升推理吞吐量

## 实验结果

**类别条件生成（ImageNet 256×256）**：
| 模型 | 参数量 | FID | 吞吐量 |
|------|--------|-----|--------|
| BitDance-H | 1.0B | 1.24 | - |
| BitDance-B-4x | 260M | - | 24.18 img/s |
| BitDance-B-16x | 260M | 1.91 | 90.26 img/s |
| RandAR-XXL | 1.4B | 1.69 | 2.78 img/s |

- BitDance-B-4x以5.4倍更少参数超越1.4B RandAR-XXL，实现8.7倍加速
- 97%稀疏度下生成质量超越全注意力基线

**文本到图像生成**：
- DPG-Bench: 88.28
- GenEval: 0.86
- 1024×1024分辨率下推理延迟12.4秒，相比NextStep-1加速30倍以上

## 关键贡献

1. 首次将视觉分词器词汇表扩展至2^256，证明高熵离散表示可兼顾重建保真度与生成正则化
2. 提出二进制扩散头，以可控参数规模实现超大词汇表的精确联合采样
3. 建立Next-Patch Diffusion范式，通过显式联合分布建模实现高效并行AR生成
