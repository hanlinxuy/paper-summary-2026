#!/usr/bin/env python3
"""
Phase 6: 生成最终综合报告
整合所有分析，生成高层次的洞察和总结
"""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime


def load_data():
    """加载所有数据"""
    # Top 30论文
    with open(
        "knowledge/reports/structured_analysis_mar_2026_top30.json",
        "r",
        encoding="utf-8",
    ) as f:
        top30 = json.load(f)

    # 所有评估论文
    with open(
        "knowledge/papers/2026-03/candidates/all_papers_evaluated.json",
        "r",
        encoding="utf-8",
    ) as f:
        all_papers = json.load(f)

    return top30, all_papers


def generate_executive_summary(top30):
    """生成执行摘要"""

    # 统计
    total_score_avg = sum(p["total_score"] for p in top30) / len(top30)
    architectures = Counter(p.get("architecture", "Other") for p in top30)

    # 高价值论文（前10）
    top10 = top30[:10]

    summary = f"""# 2026年3月AI论文精选报告

## 执行摘要

本报告基于arXiv 2026年3月4日至13日发布的3000篇AI论文，通过**热度评分（70%）+ 端侧关键词匹配（30%）**的综合评估方法，精选出**30篇高价值论文**进行深入分析。

### 核心发现

- **总候选池**: 3,000篇论文（cs.CL/cs.LG/cs.AI/cs.CV）
- **时间跨度**: 2026年3月4日 - 3月13日（10天）
- **精选数量**: 30篇（Top 1%）
- **平均评分**: {total_score_avg:.1f}/100
- **主要趋势**: VLA/机器人、扩散模型、推理优化、端侧效率

### Top 10 核心论文

"""

    for i, paper in enumerate(top10, 1):
        title = paper["title"]
        arch = paper.get("architecture", "Other")
        score = paper["total_score"]
        arxiv_id = paper["arxiv_id"].split("/")[-1].replace("v1", "")
        summary += f"{i}. **[{arch}]** {title[:60]}{'...' if len(title) > 60 else ''} (Score: {score:.1f})\n"

    return summary


def generate_trend_analysis(top30, all_papers):
    """生成趋势分析"""

    # 架构分布
    arch_counts = Counter(p.get("architecture", "Other") for p in top30)

    # 关键词分布
    all_keywords = []
    for p in top30:
        all_keywords.extend(p.get("matched_keywords", []))
    keyword_counts = Counter(all_keywords).most_common(10)

    analysis = f"""
## 趋势分析

### 热门研究方向

| 排名 | 架构/方向 | 论文数量 | 占比 |
|------|----------|---------|------|
"""

    for i, (arch, count) in enumerate(arch_counts.most_common(8), 1):
        pct = count / len(top30) * 100
        analysis += f"| {i} | {arch} | {count} | {pct:.1f}% |\n"

    analysis += f"""
### 高频关键词

| 排名 | 关键词 | 出现次数 |
|------|--------|---------|
"""

    for i, (kw, count) in enumerate(keyword_counts, 1):
        analysis += f"| {i} | {kw} | {count} |\n"

    analysis += """
### 关键洞察

1. **VLA与机器人技术崛起**: Vision-Language-Action模型在Top 30中占据重要位置，显示出多模态大模型在具身智能领域的快速进展。

2. **扩散模型持续演进**: 扩散模型不仅在图像生成，还在策略学习、特征去噪等领域展现潜力。

3. **推理与效率并重**: 推理优化（Reasoning）和端侧效率（Efficient）关键词高频出现，反映了对实用性的追求。

4. **多模态成为主流**: 纯文本模型减少，Vision、Video、3D等多模态论文显著增加。

"""

    return analysis


def generate_edge_device_analysis(top30):
    """生成端侧设备分析"""

    # 端侧高相关性论文
    high_edge = [
        p for p in top30 if p.get("evaluation", {}).get("edge_potential", 0) >= 7
    ]

    analysis = f"""
## 端侧设备价值分析

### 高价值论文（端侧相关性≥7）

共 {len(high_edge)} 篇论文具有较高的端侧部署价值：

"""

    for p in high_edge[:10]:
        title = p["title"]
        arxiv_id = p["arxiv_id"].split("/")[-1].replace("v1", "")
        edge_score = p.get("evaluation", {}).get("edge_potential", 5)
        keywords = ", ".join(p.get("matched_keywords", [])[:5])
        analysis += f"- **{arxiv_id}** | {title[:50]}{'...' if len(title) > 50 else ''} | 端侧评分: {edge_score}/10\n"

    analysis += f"""
### 端侧部署建议

**手机端优先关注**:
- 视觉-语言模型（VLM）的小型化版本
- 高效推理优化技术（如KV Cache优化）
- 端侧Agent框架

**移动PC优先关注**:
- 大模型推理加速技术
- 多模态理解模型
- 代码生成与推理模型

**机器人优先关注**:
- VLA（Vision-Language-Action）模型
- 具身智能算法
- 实时控制策略

"""

    return analysis


def generate_recommendations(top30):
    """生成推荐阅读"""

    # 按类别推荐
    by_category = {}
    for p in top30:
        arch = p.get("architecture", "Other").split("+")[0]
        if arch not in by_category:
            by_category[arch] = []
        by_category[arch].append(p)

    rec = """
## 推荐阅读清单

### 必读论文（Top 5）

"""

    for i, p in enumerate(top30[:5], 1):
        arxiv_id = p["arxiv_id"].split("/")[-1].replace("v1", "")
        title = p["title"]
        abstract = p.get("abstract", "")[:200]
        rec += f"""
**{i}. {title}**
- arXiv: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})
- 架构: {p.get("architecture", "Other")}
- 评分: {p["total_score"]:.1f}
- 摘要: {abstract}...
"""

    rec += """
### 按方向推荐

**推理优化方向**:
"""

    reasoning_papers = [p for p in top30 if "Reasoning" in p.get("architecture", "")]
    for p in reasoning_papers[:3]:
        arxiv_id = p["arxiv_id"].split("/")[-1].replace("v1", "")
        rec += (
            f"- {p['title'][:50]}... ([{arxiv_id}](https://arxiv.org/abs/{arxiv_id}))\n"
        )

    rec += """
**VLA/机器人方向**:
"""

    vla_papers = [p for p in top30 if "VLA" in p.get("architecture", "")]
    for p in vla_papers[:3]:
        arxiv_id = p["arxiv_id"].split("/")[-1].replace("v1", "")
        rec += (
            f"- {p['title'][:50]}... ([{arxiv_id}](https://arxiv.org/abs/{arxiv_id}))\n"
        )

    return rec


def generate_full_report():
    """生成完整报告"""
    print("加载数据...")
    top30, all_papers = load_data()

    print("生成各部分...")

    # 各部分内容
    executive_summary = generate_executive_summary(top30)
    trend_analysis = generate_trend_analysis(top30, all_papers)
    edge_analysis = generate_edge_device_analysis(top30)
    recommendations = generate_recommendations(top30)

    # 合并
    full_report = f"""{executive_summary}

---

{trend_analysis}

---

{edge_analysis}

---

{recommendations}

---

## 完整论文列表

详见: [structured_analysis_mar_2026_top30.md](structured_analysis_mar_2026_top30.md)

---

*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*  
*数据来源: arXiv API*  
*分析模型: Kimi k2.5*
"""

    return full_report


def main():
    print("=" * 60)
    print("Phase 6: 生成最终综合报告")
    print("=" * 60)

    # 生成报告
    print("\n[1/2] 生成综合报告...")
    report = generate_full_report()

    # 保存
    print("\n[2/2] 保存报告...")
    output_dir = Path("knowledge/reports")
    output_file = output_dir / "final_report_mar_2026.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"    报告保存到: {output_file}")

    print("\n" + "=" * 60)
    print("Phase 6 完成!")
    print(f"  - 最终报告: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
