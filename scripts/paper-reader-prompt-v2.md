# 单论文完整分析闭环任务

你收到一个命令：`{paper_id} {workdir}`

你的任务是：**零交互地自动完成论文的全部6个步骤分析**，完成后立即退出。

## 执行步骤

### 第1步：解析参数
从用户输入中提取：
- paper_id: arXiv 论文 ID
- workdir: 工作目录路径（用于临时缓存）

### 第2步：获取 Kimi 摘要
执行（最多重试3次）：
```bash
curl -s -X POST "https://papers.cool/arxiv/kimi?paper={paper_id}" > {workdir}/kimi_summary.html
```

解析 HTML 提取 Q1-Q7 的纯文本内容，保存到变量 kimi_summary。

### 第3步：下载 arXiv 论文
执行：
```bash
# 尝试 TeX 源码
curl -s -L "https://arxiv.org/e-print/{paper_id}" -o {workdir}/paper.tar.gz

# 如果是 tar.gz，解压到 {workdir}/source/
cd {workdir} && tar -xzf paper.tar.gz -C source/ 2>/dev/null || mv paper.tar.gz source/paper.pdf
```

找到入口 .tex 文件（通常是 main.tex 或包含 \documentclass 的文件）。

### 第4步：提取论文内容
从 TeX 文件中提取：
- **title**: 从 \icmltitle 或 \title 命令提取
- **authors**: 从 \icmlauthorlist 或 \author 提取
- **original_abstract**: 从 \begin{abstract}...\end{abstract} 提取
- **pdf_summary**: 读取 TeX 正文内容（Introduction, Method, Experiments 等章节）
- **results**: 提取实验结果、性能数据、表格等

### 第5步：使用 paper-summary-template skill 生成结构化输出

**必须使用模板**: `templates/structured_analysis.md.j2`

填充以下模板变量：
- `paper_id`: arXiv ID
- `title`: 论文标题
- `authors`: 作者列表
- `original_abstract`: 原文摘要（清理 LaTeX 格式）
- `kimi_summary`: Kimi Q1-Q7 摘要（已获取）
- `method`: 从 TeX 提取的核心方法描述
- `problem`: 论文解决的问题
- `pdf_summary`: 论文详细内容分析
- `results`: 实验结果和关键数据
- `credibility_score`: 1-10 评分（基于实验设计严谨性）
- `credibility_comment`: 可信度评价
- `importance_score`: 1-10 评分（学术/工业界影响力）
- `importance_comment`: 重要性评价
- `edge_devices_impact`: 端侧设备实用价值分析（综合描述，重点分析该技术对以下三类设备的影响）：
  - **智能手机**: 技术相关性、具体应用场景、在移动SoC/手机端落地的可行性（功耗/算力/存储限制）
  - **移动PC/笔记本电脑**: 技术相关性、在笔记本/平板上的应用潜力、移动端落地的可行性
  - **机器人/边缘AI设备**: 技术相关性、在机器人/IoT/边缘设备上的应用场景、在资源受限设备落地的可行性
  - 包含综合评估：端侧落地优先级（高/中/低）、关键挑战

**使用 skill**: 调用 `paper-summary-template` skill，传入上述变量和模板路径 `templates/structured_analysis.md.j2`，生成最终 Markdown。

### 第6步：原子写入并退出
- 临时文件: `knowledge/papers/{paper_id}.md.tmp`
- 重命名为: `knowledge/papers/{paper_id}.md`
- 输出文件路径和大小
- **立即退出**（不进入交互模式）

## 关键约束

1. **禁止询问用户** - 所有参数从命令获取
2. **禁止交互模式** - 执行完成后必须退出
3. **必须使用指定模板** - structured_analysis.md.j2
4. **原子写入** - 使用临时文件+重命名
5. **错误处理** - 任何步骤失败时记录错误并退出

## 输出位置

最终文件: `knowledge/papers/{paper_id}.md`

现在开始执行分析流程。
