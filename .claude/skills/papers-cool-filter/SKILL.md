---
name: papers-cool-filter
description: |
  从 papers.cool 网站筛选高价值论文，生成推荐报告。
  
  **触发场景**:
  - "帮我找今天的AI论文"
  - "筛选本周热门论文"
  - "找关于MoE的论文"
  - "发现高价值论文"
  - "papers.cool 筛选"
  - "论文推荐"
  - "paper filter", "filter papers"
---

# Papers.cool 论文筛选器

从 papers.cool 自动筛选高价值论文，生成结构化Markdown报告。

## 核心功能

1. **多维度筛选**: 按日期、分类、关键词排序
2. **智能评估**: AI评估论文相关性 + 关键词匹配 + 手动标记
3. **中文报告**: 摘要翻译成中文，生成推荐理由
4. **并发处理**: 摘要翻译、AI评估等任务并发后台执行，大幅提升效率

## URL 参数说明

```
https://papers.cool/arxiv/{categories}?date={date}&sort={sort}
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `categories` | arXiv分类，逗号分隔 | `cs.CL,cs.LG,cs.AI,cs.CV` |
| `date` | 日期筛选 | `2026-02-26` |
| `sort` | 排序方式 | `1`(点击量) 或 `moe,memory,llm`(关键词) |

## 默认配置

```yaml
categories: cs.CL,cs.LG,cs.AI,cs.CV
output_dir: ./knowledge/
report_format: markdown
```

## 执行流程

### Step 1: 解析用户请求

从自然语言中提取：
- **日期范围**: "今天"、"本周"、"最近3天" → 具体日期
- **分类**: "NLP"、"CV"、"ML" → arXiv分类代码
- **关键词**: "MoE"、"推理"、"量化" → sort参数
- **数量限制**: "前10篇"、"top 5" → 最多返回数量

### Step 2: 构建URL并获取论文列表

使用 Playwright MCP 访问 papers.cool：

```python
# 示例URL构建
base_url = "https://papers.cool/arxiv"
categories = "cs.CL,cs.LG,cs.AI,cs.CV"
date = "2026-02-26"
sort_keywords = "moe,memory,reasoning,llm,inference"

url = f"{base_url}/{categories}?date={date}&sort={sort_keywords}"
```

### Step 3: 解析页面提取论文信息

每篇论文提取：
- **arXiv ID**: 从链接中提取 (如 2401.12345)
- **标题**: 论文标题
- **作者**: 作者列表
- **摘要原文**: 英文摘要
- **分类标签**: Subjects
- **发布日期**: Publish date
- **链接**: arXiv链接、PDF链接

### Step 4: 并发处理 - AI评估与翻译

**关键优化**: 使用 `task()` 启动多个后台subagent并发处理，避免串行等待。

对每篇论文启动独立的后台任务：

```python
# 并发启动所有论文的评估和翻译任务
for paper in papers:
    task(
        subagent_type="quick",  # 轻量任务
        run_in_background=true,  # 后台执行
        description=f"评估论文: {paper.arxiv_id}",
        prompt=f"""
        评估以下论文：
        
        标题: {paper.title}
        摘要: {paper.abstract}
        关注关键词: {keywords}
        
        任务：
        1. 相关性评分 (1-10)
        2. 端侧相关性评分 (1-10): 该技术对手机/移动PC/机器人的潜在价值
        3. 模型架构判断: Transformer/MoE/RNN/CNN/Diffusion/其他
        4. 推荐理由 (一句话中文)
        5. 摘要翻译成中文 (保留专业术语)
        
        返回JSON格式：
        {{
            "score": int,
            "edge_relevance": int,
            "architecture": str,
            "reason": str,
            "abstract_cn": str
        }}
        """
    )
```

**并发策略**:
- 所有论文的评估任务**同时启动**，不等待
- 使用 `background_output()` 收集结果
- 评估包含：
  1. **关键词匹配分数**: 标题/摘要中包含关键词的数量
  2. **AI相关性评分**: 使用LLM评估论文与用户关注领域的相关性(1-10分)
  3. **端侧相关性评分**: 评估对手机/移动PC/机器人的潜在价值(1-10分)
  4. **模型架构判断**: Transformer/MoE/RNN/CNN/Diffusion/其他
  5. **推荐理由生成**: 用一句话说明为什么推荐这篇论文
  6. **摘要翻译**: 同步完成中文翻译

### Step 5: 收集并发结果并筛选

等待所有后台任务完成，收集评估结果：

```python
# 收集所有后台任务结果
results = []
for task_id in task_ids:
    result = background_output(task_id=task_id, block=true)
    results.append(result)

# 筛选高价值论文
high_value_papers = [
    paper for paper, result in zip(papers, results)
    if result["score"] >= 6 or result["edge_relevance"] >= 7
]
```

筛选标准（满足任一）：
- AI相关性评分 >= 6
- 端侧相关性评分 >= 7（优先关注端侧落地价值）
- 关键词匹配数 >= 2
- 或用户手动标记为感兴趣

按综合分数排序后取 Top N。

**综合分数计算**:
```
综合分 = 0.7 × 热度 + 0.3 × 端侧相关性
```

### Step 6: 生成Markdown报告

保存到 `./knowledge/papers_{date}.md`：

```markdown
# 论文推荐报告 - {date}

> 筛选条件: {categories}
> 排序关键词: {keywords}
> 共筛选 {total} 篇，推荐 {recommended} 篇

---

## 1. {title}

**arXiv**: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})
**作者**: {authors}
**分类**: {subjects}
**推荐理由**: {recommendation_reason}

### 摘要 (中文)
{abstract_cn}

<details>
<summary>原文摘要</summary>

{abstract_en}

</details>

---
```

## 使用示例

### 示例1: 获取今天的热门论文
```
用户: 帮我找今天的AI热门论文
```
执行:
- 日期: 今天
- 分类: cs.CL,cs.LG,cs.AI,cs.CV (默认)
- 排序: sort=1 (点击量)

### 示例2: 按关键词筛选
```
用户: 找最近关于MoE和推理的论文
```
执行:
- 日期: 最近7天
- 分类: 默认
- 排序: sort=moe,inference,reasoning,experts

### 示例3: 指定分类和日期
```
用户: 2026-02-20的NLP论文有哪些值得看的？
```
执行:
- 日期: 2026-02-20
- 分类: cs.CL
- 排序: 默认(sort=1)

### 示例4: 自定义关键词
```
用户: 帮我找关于long context和attention的论文，最近3天的
```
执行:
- 日期: 最近3天
- 分类: 默认
- 排序: sort=long,context,attention

## 关键词映射表

常见研究领域对应的关键词：

| 研究方向 | 推荐关键词 |
|---------|-----------|
| MoE/混合专家 | moe, mixture, experts, expert, routing |
| 推理/Reasoning | reasoning, inference, chain, thought |
| 长文本/Context | long, context, window, length |
| 量化/压缩 | quantization, bit, compression, prune |
| 注意力机制 | attention, flash, sparse |
| 训练优化 | training, efficient, acceleration |
| 记忆/缓存 | memory, cache, kv |
| LLM通用 | llm, llms, language, model |
| **端侧相关** | edge, mobile, on-device, efficient, tiny, lightweight |
| **模型架构** | transformer, diffusion, mamba, rnn, cnn, vit |
| **机器人/VLA** | robot, vla, embodied, manipulation, navigation |

## 注意事项

1. **Playwright必需**: 必须使用 Playwright MCP 访问网站
2. **并发执行**: 评估和翻译任务使用后台subagent并发执行，大幅提升效率
3. **rate limit**: 避免频繁请求papers.cool，每次筛选间隔至少2秒
4. **摘要翻译**: 在并发任务中完成，使用当前LLM进行翻译，保留专业术语
5. **手动确认**: 对于AI评分在5-6分的论文，可以询问用户是否感兴趣
6. **增量更新**: 如果报告已存在，询问是追加还是覆盖
7. **资源管理**: 完成后使用 `background_cancel(all=true)` 清理后台任务

## 输出文件

- 位置: `./knowledge/papers_{date}.md`
- 格式: Markdown
- 编码: UTF-8
