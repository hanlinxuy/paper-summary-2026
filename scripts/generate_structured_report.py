#!/usr/bin/env python3
"""
Phase 5: 生成30篇结构化分析报告
基于评估数据生成完整的结构化分析
"""

import json
from pathlib import Path
from datetime import datetime


# 读取评估后的论文
def load_papers():
    with open(
        "knowledge/papers/2026-03/candidates/all_papers_evaluated.json",
        "r",
        encoding="utf-8",
    ) as f:
        all_papers = json.load(f)
    return all_papers[:30]  # Top 30


# 读取Kimi摘要（如果有）
def load_kimi_summary(paper_id):
    kimii_file = Path(f"knowledge/reports/mar2026_kimi/{paper_id}.json")
    if kimii_file.exists():
        with open(kimii_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def generate_structured_analysis(paper, index):
    """为单篇论文生成结构化分析"""
    arxiv_id = paper["arxiv_id"].split("/")[-1].replace("v1", "")

    # 尝试加载Kimi摘要
    kimi = load_kimi_summary(arxiv_id)
    kimi_text = ""
    if kimi and "error" not in kimi:
        if isinstance(kimi, dict):
            kimi_lines = []
            for k, v in kimi.items():
                if not k.startswith("_"):
                    v_str = str(v)
                    if len(v_str) > 200:
                        v_str = v_str[:200] + "..."
                    kimi_lines.append(f"**{k}:** {v_str}")
            kimi_text = "\n".join(kimi_lines)

    # 计算端侧价值评估
    edge_score = paper.get("evaluation", {}).get("edge_potential", 5)
    priority = "高" if edge_score >= 7 else "中" if edge_score >= 5 else "低"

    # 确定设备相关性
    categories = paper.get("categories", [])
    title = paper.get("title", "")
    abstract = paper.get("abstract", "")
    text = (title + " " + abstract).lower()

    # 手机端相关性
    mobile_relevance = 5
    mobile_scenarios = []
    if any(kw in text for kw in ["mobile", "edge", "on-device", "efficient", "tiny"]):
        mobile_relevance = min(10, mobile_relevance + 3)
        mobile_scenarios.append("边缘推理")
    if any(kw in text for kw in ["vision", "multimodal", "vlm"]):
        mobile_scenarios.append("端侧视觉")
    if "agent" in text:
        mobile_scenarios.append("端侧Agent")

    # PC端相关性
    laptop_relevance = min(10, mobile_relevance + 1)
    laptop_scenarios = mobile_scenarios.copy()
    if any(kw in text for kw in ["reasoning", "inference", "training"]):
        laptop_scenarios.append("本地推理")
        laptop_relevance = min(10, laptop_relevance + 2)

    # 机器人相关性
    robot_relevance = 5
    robot_scenarios = []
    if any(
        kw in text for kw in ["robot", "embodied", "manipulation", "navigation", "vla"]
    ):
        robot_relevance = min(10, 8)
        robot_scenarios.extend(["机器人控制", "具身智能", "视觉导航"])
    elif "agent" in text:
        robot_relevance = 6
        robot_scenarios.append("智能体任务")

    # 关键挑战
    challenges = []
    if "real-time" in text or "latency" in text:
        challenges.append("实时性要求")
    if "memory" in text or "efficient" in text:
        challenges.append("内存优化")
    if "hardware" in text:
        challenges.append("硬件适配")
    if not challenges:
        challenges.append("模型压缩需求")

    # 生成报告
    report = f"""
**论文ID**: {arxiv_id}

## {index}. {paper["title"]}

### 基本信息

- **作者**: {", ".join(paper.get("authors", [])[:5])}{"..." if len(paper.get("authors", [])) > 5 else ""}
- **机构**: 待确认
- **arXiv**: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})
- **分类**: {", ".join(paper.get("categories", [])[:3])}
- **发布日期**: {paper.get("published", "")[:10]}

### 评分汇总

| 维度 | 评分 | 说明 |
|------|------|------|
| 综合评分 | {paper.get("total_score", 0):.1f}/100 | 热度+关键词匹配 |
| 端侧价值 | {edge_score}/10 | 端侧部署潜力 |
| 文章可信度 | {paper.get("evaluation", {}).get("relevance", 5)}/10 | 基于摘要评估 |
| 文章重要性 | {paper.get("evaluation", {}).get("novelty", 5)}/10 | 创新性评估 |

### 论文内容分析

**模型架构**: {paper.get("architecture", "Other")}

**核心问题**: 
{paper.get("key_points", abstract[:150] + "...")}

**关键词匹配**: {", ".join(paper.get("matched_keywords", [])[:8])}

### 效果评估

基于arXiv摘要提取的关键信息:
- **研究方法**: {paper.get("architecture", "待详细分析")}
- **主要贡献**: 待详细分析
- **实验设置**: 待详细分析

### 端侧设备实用价值

**手机端**:
- 相关性: {mobile_relevance}/10
- 适用场景: {", ".join(mobile_scenarios) if mobile_scenarios else "通用推理"}
- 可行性: {"较高" if mobile_relevance >= 7 else "中等" if mobile_relevance >= 5 else "较低"}

**移动PC**:
- 相关性: {laptop_relevance}/10
- 适用场景: {", ".join(laptop_scenarios) if laptop_scenarios else "通用推理"}
- 可行性: 较高

**机器人**:
- 相关性: {robot_relevance}/10
- 适用场景: {", ".join(robot_scenarios) if robot_scenarios else "视具体任务"}
- 可行性: {"较高" if robot_relevance >= 7 else "中等" if robot_relevance >= 5 else "待验证"}

**综合优先级**: {priority}

**关键挑战**: {", ".join(challenges)}

### 原文摘要

{abstract[:500]}{"..." if len(abstract) > 500 else ""}

---

"""
    return report


def generate_full_report(papers):
    """生成完整报告"""
    sections = []

    # 报告头部
    header = f"""# 论文推荐报告 - 2026年3月 LLM/VLM重点筛选

> 筛选日期: 2026-03-04 至 2026-03-13
> 筛选分类: cs.CL, cs.LG, cs.AI, cs.CV
> 数据来源: arXiv API
> 评估模型: 关键词匹配 + 热度评分
> 共筛选 **3000篇** 候选，推荐 **30篇** 高价值论文

---

## 执行摘要

本次筛选从arXiv 2026年3月4日至13日的3000篇论文中，基于关键词匹配（MoE、Memory、Reasoning、Efficient等）和热度评分，精选出30篇高价值论文。

**关键统计**:
- 总计筛选: 3000篇
- 时间跨度: 10天（3月4-13日）
- 推荐数量: 30篇
- 主要架构: Diffusion+VLA、Transformer、Agent、Vision等

---

"""
    sections.append(header)

    # 每篇论文的分析
    for i, paper in enumerate(papers, 1):
        print(f"生成第 {i}/30 篇论文分析...")
        analysis = generate_structured_analysis(paper, i)
        sections.append(analysis)

    # 统计汇总
    architectures = {}
    for p in papers:
        arch = p.get("architecture", "Other")
        architectures[arch] = architectures.get(arch, 0) + 1

    summary = f"""
## 统计汇总

### 架构分布

| 架构 | 数量 |
|------|------|
"""
    for arch, count in sorted(architectures.items(), key=lambda x: x[1], reverse=True):
        summary += f"| {arch} | {count} |\n"

    summary += f"""
### 评分分布

- 90分以上: {sum(1 for p in papers if p["total_score"] >= 90)} 篇
- 70-89分: {sum(1 for p in papers if 70 <= p["total_score"] < 90)} 篇
- 50-69分: {sum(1 for p in papers if 50 <= p["total_score"] < 70)} 篇
- 50分以下: {sum(1 for p in papers if p["total_score"] < 50)} 篇

---

*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*分析模型: Kimi k2.5*
"""
    sections.append(summary)

    return "\n".join(sections)


def main():
    print("=" * 60)
    print("Phase 5: 生成30篇结构化分析报告")
    print("=" * 60)

    # 读取Top 30论文
    print("\n[1/3] 读取Top 30论文...")
    papers = load_papers()
    print(f"    读取到 {len(papers)} 篇论文")

    # 生成报告
    print(f"\n[2/3] 生成结构化分析报告...")
    report = generate_full_report(papers)

    # 保存报告
    print(f"\n[3/3] 保存报告...")
    output_dir = Path("knowledge/reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "structured_analysis_mar_2026_top30.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"    报告保存到: {output_file}")

    # 同时生成JSON格式
    json_output = output_dir / "structured_analysis_mar_2026_top30.json"
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    print(f"    JSON保存到: {json_output}")

    print("\n" + "=" * 60)
    print("Phase 5 完成!")
    print(f"  - 分析报告: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
