# Paper Summary - 单论文独立总结工作流

AI/CS论文总结项目。**完全本地方案**，零全局配置，上下文隔离。

## 核心特性

- **完全本地**: 所有配置在项目目录内，不修改 `~/.config/opencode/`
- **上下文隔离**: 每个论文使用独立 `opencode run` 进程，LLM 上下文完全隔离
- **Model 可配置**: 默认 `minimax-cn-coding-plan/MiniMax-M2.5-highspeed`，可覆盖
- **批量处理**: 安全并发控制，避免文件冲突

## 快速开始

### 单论文分析

```bash
# 基本用法
./scripts/read-paper.sh 2602.21221 /tmp/paper-2602.21221

# 指定模型
./scripts/read-paper.sh 2602.21221 /tmp/paper-2602.21221 --model anthropic/claude-3-5-sonnet
```

**输出**: `knowledge/papers/2602.21221.md`

### 批量处理

```bash
# 基本用法（默认4并发）
./scripts/batch-runner.sh "2602.21221 2310.06825 2401.15884"

# 指定并发数和模型
./scripts/batch-runner.sh --max-concurrent 8 --model anthropic/claude-3-5-sonnet "2602.21221 2310.06825"
```

### 生成最终报告

批量处理完成后，生成包含所有论文完整内容的综合报告：

```bash
./scripts/generate-final-report.sh
```

**输出**: `knowledge/reports/final_report_feb-2026.md`
- 可点击目录（30篇论文导航）
- 每篇论文的完整结构化分析
- 端侧设备影响分析（手机/移动PC/机器人）

## 项目结构

```
.
├── scripts/
│   ├── read-paper.sh              # 单论文分析 CLI
│   ├── batch-runner.sh            # 批量处理脚本
│   ├── generate-final-report.sh   # 生成最终综合报告
│   ├── generate-final-report-v2.sh # 生成按新排名排序的报告
│   ├── rank_existing_papers.py    # 重新排序论文（热度+端侧）
│   ├── paper-reader-prompt.md     # 分析流程 Prompt (v1)
│   └── paper-reader-prompt-v2.md  # 分析流程 Prompt (v2 - 含端侧分析)
├── templates/
│   ├── structured_analysis.md.j2  # 结构化摘要模板（含端侧设备影响）
│   └── academic_summary.md.j2     # 学术摘要模板
├── knowledge/
│   ├── papers/                    # 单论文输出目录
│   ├── reports/                   # 报告输出目录
│   │   ├── structured_papers/     # 结构化论文摘要
│   │   └── final_report_*.md      # 最终综合报告
│   ├── selected_papers_*.json     # 筛选结果
│   └── selected_*_ids.txt         # 排序后的论文ID列表
└── README.md                      # 本文档
```

## 工作原理

### 为什么能避免上下文污染？

| 机制 | 说明 |
|------|------|
| **独立进程** | 每个 `./scripts/read-paper.sh` 调用启动全新 `opencode run` 进程 |
| **独立上下文** | 每个进程有独立的 LLM conversation history |
| **独立工作目录** | 每个论文使用不同的 `--workdir`，缓存互不影响 |
| **进程销毁** | 完成后进程完全退出，无残留 |

### 工作流程

每个论文处理包含6个步骤：

1. **解析参数**: 提取 paper_id 和 workdir
2. **获取 Kimi 摘要**: 调用 `kimi-summary-extractor` skill（重试3次）
3. **下载论文**: 调用 `read-arxiv-paper` skill（TeX优先，PDF回退）
4. **生成摘要**: 使用 `paper-summary-template` skill 和结构化模板
5. **原子写入**: 保存到 `knowledge/papers/{paper_id}.md`
6. **立即退出**: 不进入交互模式

### 完整工作流程示例

```bash
# 1. 批量分析论文（输出到 knowledge/papers/）
./scripts/batch-runner.sh "2602.21221 2602.21224 2602.22273"

# 2. （可选）移动结构化文件到 reports
mkdir -p knowledge/reports/structured_papers
cp knowledge/papers/*.md knowledge/reports/structured_papers/

# 3. 生成最终报告
./scripts/generate-final-report.sh

# 4. 查看报告
cat knowledge/reports/final_report_feb-2026.md
```

### 月度完整工作流程

每月执行一次完整流程：

```bash
# Step 1: 新建分支
git checkout main && git pull
git checkout -b refactor/{月份}-full-pipeline

# Step 2: 批量分析论文
./scripts/batch-runner.sh "论文ID列表"

# Step 3: 移动结构化文件
mkdir -p knowledge/reports/structured_papers
cp knowledge/papers/*.md knowledge/reports/structured_papers/

# Step 4: 重新排序（热度70% + 端侧30%）
python3 scripts/rank_existing_papers.py

# Step 5: 生成按新排名的报告
./scripts/generate-final-report-v2.sh

# Step 6: 提交并推送
git add -A && git commit -m "feat: {月份}论文完整分析"
git push -u origin refactor/{月份}-full-pipeline

# Step 7: 合并到main
gh pr create --title "{月份}论文完整分析" --body "筛选方式: 热度70% + 端侧30%"
gh pr merge --squash
```

### 结构化摘要内容

每篇论文的摘要包含：

- **基本信息**: 作者、机构（简化中文）、arXiv ID
- **论文内容分析**: 核心方法、解决的问题
- **效果评估**: 关键实验数据、性能指标
- **价值评估**: 可信度、重要性（1-10分）
- **端侧设备实用价值**: 评分/X - 手机：相关性+场景+可行性。移动PC：相关性+场景+可行性。机器人：相关性+场景+可行性。优先级：高/中/低。挑战：关键难点

### 筛选维度

论文筛选采用多维度综合评分：

| 维度 | 权重 | 说明 |
|------|------|------|
| 热度 | 70% | papers.cool 点击排名 |
| 端侧相关性 | 30% | 对手机/移动PC/机器人的潜在价值 |
| 架构判断 | 标注 | Transformer/MoE/Diffusion/RNN/CNN/VLA等 |

#### 端侧相关性关键词

```python
EDGE_KEYWORDS = [
    "edge", "mobile", "on-device", "efficient", "tiny", "lightweight",
    "quantization", "pruning", "distillation", "compression",
    "inference", "latency", "real-time", "low-power", "acceleration",
    "optimization", "compact", "sparse", "hardware", "deploy",
    "attention", "flash", "memory", "cache", "kv", "fast", "speed"
]
```

#### 模型架构检测

自动识别的架构类型：
- Transformer, MoE, Diffusion, Mamba/SSM
- RNN, CNN, ViT, VLA/Robot
- Agent, Reasoning, Memory, Video, 3D

## Model 配置

### 默认模型
`minimax-cn-coding-plan/MiniMax-M2.5-highspeed`

### 支持的模型
- `minimax-cn-coding-plan/MiniMax-M2.5-highspeed` (默认)
- `myprovider/deepseek-v3.2`
- `myprovider/kimi-k2.5`
- `anthropic/claude-3-5-sonnet-20241022`

## 对比

| 方案 | 上下文隔离 | 全局配置 | 适用场景 |
|------|-----------|---------|---------|
| **本地方案** | ✅ 完全隔离 | ❌ 零修改 | **推荐** |
| 旧批量方案 | ❌ 污染 | ❌ 零修改 | 草稿 |

## 技术栈

- opencode CLI
- papers.cool API
- arXiv TeX/PDF
- Minimax/Anthropic 模型

## 旧技能命令（仍然可用）

```bash
# 筛选论文
papers-cool-filter

# 获取摘要
kimi-summary-extractor

# 深度分析
read-arxiv-paper

# 结构化输出
paper-summary-template
```

## License

MIT
