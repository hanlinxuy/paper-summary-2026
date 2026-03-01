# Solaris: Multiplayer Video World Model in Minecraft

## 基本信息
- arXiv ID: 2602.22208
- 作者: 待确认

## 核心方法

**研究背景**：现有视频世界模型仅限于单智能体视角，无法捕捉多智能体交互。

**核心方法 - Solaris**：

1. **数据收集系统SolarisEngine**：
   - 控制器-摄像机分离架构
   - 基于Mineflayer的Bot执行程序化协作行为
   - 官方Minecraft客户端GPU加速渲染
   - 收集12.64百万帧（每玩家6.32M）多人数据

2. **模型架构**：
   - 基于DiT的单玩家视频模型扩展至多人
   - 视觉交错：多玩家token沿序列维度交错排列
   - 多人自注意力：通过共享自注意力层实现跨玩家信息交换
   - 玩家ID嵌入区分不同视角

3. **分阶段训练流程**：
   - Stage 1：双向单玩家（VPT数据集）
   - Stage 2：双向多人
   - Stage 3：因果多人（Diffusion Forcing）
   - Stage 4：Self Forcing

4. **Checkpointed Self Forcing**：
   - 前向阶段：缓存干净估计帧，停止梯度
   - 重计算阶段：拼接干净帧和噪声帧，启用梯度
   - 内存复杂度从O(L_t × L_s)降至O(L_t)

## 实验结果

**五个评估维度**：
| 任务 | Solaris | Frame concat | 无预训练 |
|------|---------|--------------|----------|
| Movement | 68.2% | - | - |
| Grounding | 62.5% | 53.1% | 29.2% |
| Memory | 37.5% | - | - |
| Building | 20.8% | 0% | 0% |
| Consistency | 71.4% | 49.5% | 49.5% |

- Solaris是唯一在Building任务上非零的方法
- Checkpointed Self Forcing使FID从60.3降至38.5

## 关键贡献

1. 首个能够模拟多人一致视角的视频世界模型
2. 开发SolarisEngine解决多人游戏数据缺失问题
3. 提出Checkpointed Self Forcing突破长时程训练内存瓶颈
4. 建立五人评估基准涵盖Movement、Grounding、Memory、Building、Consistency
