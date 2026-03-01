# DFlash: Block Diffusion for Flash Speculative Decoding

## 基本信息
- arXiv ID: 2602.06036
- 作者: Jian Chen, Yesheng Liang, Zhijian Liu (UC San Diego)
- 来源: ICML 2026

## 核心方法

DFlash是一种新型的推测解码框架，利用轻量级块扩散模型实现并行drafting，显著提升大语言模型推理速度。

**关键技术设计：**

1. **目标模型上下文特征提取**
   - 目标模型执行标准prefill pass生成第一个token时，从浅层到深层均匀采样的隐藏层提取表示
   - 将跨层信息通过轻量级投影层融合为紧凑的"目标上下文特征"

2. **KV注入条件化**
   - 将融合的目标上下文特征直接注入到draft模型每一层的Key和Value投影中
   - 特征存储在draft模型的KV cache中，在drafting迭代中复用
   - 这种设计提供了强一致的条件化，使acceptance length能随draft层数有效扩展

3. **并行扩散drafting**
   - 预测下一个token块使用块级扩散过程
   - 块内的所有masked位置在单次前向传播中并行解码
   - 相比自回归drafting，大幅降低drafting延迟

4. **训练策略**
   - 随机采样anchor tokens，块大小16（Llama为10）
   - 指数衰减损失权重，强调早期token位置
   - 共享embedding和LM head（冻结）

## 实验结果

**Qwen3-8B模型上的加速效果：**
- Greedy decoding: 4.9×加速 (vs baseline), 2.4×加速 (vs EAGLE-3)
- Non-greedy (temp=1): 4.1×加速 (vs baseline), 2.2×加速 (vs EAGLE-3)

**SGLang (FA4 backend) 实测：**
- Qwen3-8B @ Math500: 5.1×加速 (concurrency=1)
- Qwen3-4B @ Math500: 4.8×加速 (concurrency=1)
- Qwen3-Coder-30B-A3B @ LCB: 2.6×加速

**LLaMA-3.1-8B-Instruct对比EAGLE-3：**
- GSM8K: 2.4× vs 1.6× (EAGLE-3)
- HumanEval: 2.8× vs 2.0× (EAGLE-3)

## 关键贡献

1. **首次提出基于扩散模型的轻量级推测解码框架**，实现超过6×的无损加速
2. **创新性地利用目标模型的隐藏特征作为条件**，通过KV注入实现高效的条件化机制
3. **块级并行扩散drafting**，大幅降低drafting延迟，提高GPU利用率
4. **在多种模型和任务上显著超越EAGLE-3**，最高达2.5×加速提升
