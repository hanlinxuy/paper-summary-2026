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

## 项目结构

```
.
├── scripts/
│   ├── read-paper.sh           # 单论文分析 CLI
│   ├── paper-reader-prompt.md  # 分析流程 Prompt
│   └── batch-runner.sh         # 批量处理脚本
├── templates/
│   └── structured_analysis.md.j2  # 结构化摘要模板
├── knowledge/
│   └── papers/                 # 输出目录
└── README.md                   # 本文档
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
