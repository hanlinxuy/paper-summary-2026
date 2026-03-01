# SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks

## 基本信息
- arXiv ID: 2602.12670
- 作者: 待确认

## 核心方法

**研究背景**：Agent Skills（结构化的程序知识包）缺乏系统性评估基准，无法客观衡量其是否真正提升代理性能。

**核心方法 - SKILLSBENCH**：

1. **三条件对比实验设计**：
   - 无Skills基线：仅提供任务指令
   - 人工策划Skills：提供结构化程序知识包
   - 自生成Skills：提示模型自主生成程序知识后执行

2. **跨领域任务集**：
   - 84个任务，覆盖11个领域（软件工程、医疗、制造、金融等）
   - 容器化环境，配备确定性验证器
   - 防泄漏审计确保Skills不直接提供答案

3. **大规模多配置评估**：
   - 7种模型-代理配置（Claude Code、Gemini CLI、Codex CLI）
   - 7,308条有效轨迹
   - 标准化增益指标：g = (pass_skill - pass_vanilla)/(1 - pass_vanilla)

## 实验结果

**Skills效用统计**：
| 指标 | 数值 |
|------|------|
| 人工策划Skills平均提升 | **+16.2pp** |
| 自生成Skills平均效果 | **-1.3pp** |
| 标准化增益 | 21.5% |

**领域差异**：
| 领域 | 提升幅度 |
|------|----------|
| Healthcare | +51.9pp |
| Manufacturing | +41.9pp |
| Software Engineering | +4.5pp |

**设计原则**：
- 2-3个Skills模块最优（+18.6pp），4个以上反而下降（+5.9pp）
- 简洁聚焦的指导优于详尽文档（Comprehensive Skills -2.9pp）

## 关键贡献

1. 首个系统性评估Agent Skills效用的基准测试
2. 证明模型无法可靠自生成有效Skills
3. 确立"少即是多"的设计原则
4. 证明Skills可部分替代模型规模（Haiku+Skills超越Opus无Skills）
