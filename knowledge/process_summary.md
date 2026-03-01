# 论文筛选与结构化摘要生成 - 过程总结

## 任务目标
筛选2026年2月20日至28日的AI/ML论文，选出20篇高质量论文并生成结构化摘要。

---

## 工作流程

### 1. 数据获取
- **数据源**: papers.cool (按热度排序的arXiv论文)
- **日期范围**: 2026-02-20 至 2026-02-27 (6个工作日，周末无更新)
- **分类**: cs.CL, cs.LG, cs.AI, cs.CV
- **排序**: sort=1 (按点击量)

### 2. 筛选策略
- 每天取前25篇 (已按热度排序)
- 总候选: 6天 × 25篇 = 150篇
- 获取Kimi 7-Q&A摘要 (146/150 成功, 97.3%)
- 综合评分: 热度分60% + 质量分40%
- 选出Top 20

### 3. 评分算法
```
综合分 = 0.6 × 热度分 + 0.4 × 质量分
热度分 = max(0, 100 - (index-1) × 3)
质量分 = Q1-Q6非空且>30字各+15分, Q7非空+5分
```

### 4. 结构化摘要
使用 structured_analysis.md.j2 模板:
- 基本信息 (核心方法、解决的问题)
- 效果评估 (数据支撑、关键数据点)
- 端侧价值评估 (可信度/重要性/端侧价值 1-10分)
- 端侧落地分析 (技术可行性、未来影响、落地挑战)

---

## 输出文件

| 文件 | 说明 |
|------|------|
| `knowledge/papers_2026-02-20_to_2026-02-28_filtering.md` | 筛选报告 + Kimi 7-Q&A |
| `knowledge/selected_papers_2026-02.json` | 选中20篇论文元数据 |
| `knowledge/summary_2602.XXXXX.md` | 20篇深入阅读报告 (TeX分析) |
| `knowledge/structured_analysis_20.md` | 结构化摘要 (分点格式) |

---

## 技术要点

### curl 代替 Playwright
- papers.cool HTML可直接用curl获取
- 更稳定、更快速

### Kimi API 调用
```bash
curl -s -X POST "https://papers.cool/arxiv/kimi?paper={arxiv_id}"
```
- 返回HTML格式的7个Q&A
- 解析 `<p class="faq-q">` + `<div class="faq-a">` 结构

### 周末无数据
- arXiv周末不更新
- 2026-02-21(周六)、2026-02-22(周日) 无论文

---

## 端侧价值评分 Top 5

| 排名 | 论文 | 端侧价值 |
|------|------|----------|
| 1 | Mobile-Agent-v3.5 | 10/10 |
| 2 | Mobile-O | 10/10 |
| 3 | Going Down Memory Lane | 9/10 |
| 4 | On Data Engineering | 9/10 |
| 5 | Sink-Aware Pruning | 8/10 |

---

## 模板文件
- 位置: `.agents/skills/paper-summary-template/templates/`
- `structured_analysis.md.j2` - 结构化分析模板
- `academic_summary.md.j2` - 学术摘要模板

---

*Generated: 2026-03-01*
