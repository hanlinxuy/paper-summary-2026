#!/usr/bin/env python3
import json
import os
from pathlib import Path

# Configuration
KNOWLEDGE_DIR = Path("./knowledge")
PAPER_FILES = [
    "day_2026-02-20_papers.json",
    "day_2026-02-23_papers.json",
    "day_2026-02-24_papers.json",
    "day_2026-02-25_papers.json",
    "day_2026-02-26_papers.json",
    "day_2026-02-27_papers.json",
]
KIMI_SUMMARIES_DIR = KNOWLEDGE_DIR / "kimi_summaries"


def load_papers():
    """Load all papers from day_*_papers.json files"""
    all_papers = []
    for filename in PAPER_FILES:
        filepath = KNOWLEDGE_DIR / filename
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            date = data["date"]
            for paper in data["papers"]:
                paper["date"] = date
                all_papers.append(paper)
    return all_papers


def load_kimi_summary(arxiv_id):
    """Load Kimi summary for a given arxiv_id"""
    filepath = KIMI_SUMMARIES_DIR / f"{arxiv_id}.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def calculate_heat_score(index):
    """Calculate heat score based on index (1=highest)"""
    # heat_score = max(0, 100 - (index - 1) * 3)
    score = 100 - (index - 1) * 3
    return max(0, score)


def calculate_quality_score(summary):
    """Calculate quality score based on Kimi summary completeness"""
    if summary is None:
        return 0

    score = 0
    # q1-q6: non-empty and >30 chars → +15 each
    for i in range(1, 7):
        q_key = f"q{i}"
        if q_key in summary and summary[q_key] and len(str(summary[q_key])) > 30:
            score += 15

    # q7: non-empty → +5
    if "q7" in summary and summary["q7"]:
        score += 5

    return min(100, score)  # Cap at 100


def calculate_edge_score(title, abstract):
    """Calculate edge relevance score based on keywords"""
    if abstract is None:
        abstract = ""

    text = (title + " " + abstract).lower()

    edge_keywords = [
        "edge",
        "mobile",
        "on-device",
        "efficient",
        "tiny",
        "lightweight",
        "quantization",
        "pruning",
        "distillation",
        "compression",
        "inference",
        "latency",
        "real-time",
        "low-power",
    ]

    score = 0
    for keyword in edge_keywords:
        if keyword in text:
            score += 10

    return min(100, score)


def detect_architecture(title, abstract):
    """Detect model architecture from title and abstract"""
    if abstract is None:
        abstract = ""

    text = (title + " " + abstract).lower()

    architectures = []

    if "transformer" in text or "attention" in text:
        architectures.append("Transformer")
    if "moe" in text or "mixture of expert" in text:
        architectures.append("MoE")
    if "diffusion" in text:
        architectures.append("Diffusion")
    if "mamba" in text or "ssm" in text or "state space" in text:
        architectures.append("Mamba/SSM")
    if "rnn" in text or "lstm" in text or "gru" in text:
        architectures.append("RNN")
    if "cnn" in text or "convolution" in text:
        architectures.append("CNN")
    if "vit" in text or "vision transformer" in text:
        architectures.append("ViT")
    if "vla" in text or "vision-language-action" in text:
        architectures.append("VLA")

    return "+".join(architectures) if architectures else "Other"


def calculate_total_score(heat_score, edge_score):
    """Calculate total score: 70% heat + 30% edge"""
    return 0.7 * heat_score + 0.3 * edge_score


def main():
    # Load all papers
    papers = load_papers()
    print(f"Loaded {len(papers)} papers")

    # Check for duplicates
    seen_ids = set()
    unique_papers = []
    for paper in papers:
        if paper["arxiv_id"] not in seen_ids:
            seen_ids.add(paper["arxiv_id"])
            unique_papers.append(paper)
        else:
            print(f"Duplicate found: {paper['arxiv_id']}")

    print(f"Unique papers: {len(unique_papers)}")

    # Calculate scores for each paper
    scored_papers = []
    missing_summaries = []

    for paper in unique_papers:
        arxiv_id = paper["arxiv_id"]

        # Load Kimi summary
        summary = load_kimi_summary(arxiv_id)

        if summary is None:
            missing_summaries.append(arxiv_id)
            quality_score = 0
        else:
            quality_score = calculate_quality_score(summary)

        heat_score = calculate_heat_score(paper["index"])
        edge_score = calculate_edge_score(paper["title"], paper.get("abstract", ""))
        architecture = detect_architecture(paper["title"], paper.get("abstract", ""))
        total_score = calculate_total_score(heat_score, edge_score)

        scored_papers.append(
            {
                "arxiv_id": arxiv_id,
                "title": paper["title"],
                "authors": paper["authors"],
                "subjects": paper["subjects"],
                "date": paper["date"],
                "index": paper["index"],
                "url": paper["url"],
                "heat_score": heat_score,
                "quality_score": quality_score,
                "edge_score": edge_score,
                "architecture": architecture,
                "total_score": total_score,
                "kimi_summary": summary,
            }
        )

    print(f"\nMissing summaries for {len(missing_summaries)} papers:")
    for mid in missing_summaries:
        print(f"  - {mid}")

    # Sort by total score (descending)
    scored_papers.sort(key=lambda x: x["total_score"], reverse=True)

    # Select top 20
    top_20 = scored_papers[:20]

    # Add rank
    for i, paper in enumerate(top_20, 1):
        paper["rank"] = i

    # Print top 20 summary
    print("\n" + "=" * 100)
    print("TOP 20 PAPERS")
    print("=" * 100)
    for paper in top_20:
        print(
            f"{paper['rank']:2}. {paper['total_score']:5.1f} | H:{paper['heat_score']:5.1f} Q:{paper['quality_score']:5.1f} E:{paper['edge_score']:5.1f} | {paper['architecture']:15} | {paper['arxiv_id']} | {paper['title'][:40]}..."
        )

    # Save to JSON
    output = {
        "date_range": "2026-02-20 to 2026-02-27",
        "total_candidates": len(unique_papers),
        "selected_count": len(top_20),
        "selected_papers": top_20,
    }

    output_file = KNOWLEDGE_DIR / "selected_papers_2026-02.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nJSON saved to: {output_file}")

    # Generate markdown report
    markdown = generate_markdown(top_20)
    md_file = KNOWLEDGE_DIR / "papers_2026-02-20_to_2026-02-28_filtering.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Markdown saved to: {md_file}")

    return top_20


def generate_markdown(papers):
    """Generate markdown filtering report"""
    md = """# 论文筛选报告 - 2026年2月20日至27日

> 日期范围: 2026-02-20 至 2026-02-27 (6个工作日)
> 候选总数: 146篇
> 筛选方式: 热度排序(70%) + 端侧相关性(30%)
> 最终选出: 20篇

---

"""

    for paper in papers:
        md += f"## {paper['rank']}. {paper['title']}\n\n"
        md += f"**arXiv**: {paper['arxiv_id']}\n\n"
        md += f"**作者**: {', '.join(paper['authors'][:5])}"
        if len(paper["authors"]) > 5:
            md += f" 等{len(paper['authors'])}人"
        md += "\n\n"
        md += f"**分类**: {', '.join(paper['subjects'])}\n\n"
        md += f"**模型架构**: {paper['architecture']}\n\n"
        md += f"**热度排名**: #{paper['index']} ({paper['date']})\n\n"
        md += f"**综合得分**: {paper['total_score']:.1f}/100 (热度:{paper['heat_score']:.1f} + 端侧:{paper['edge_score']:.1f})\n\n"

        # Add Kimi summary if available
        if paper["kimi_summary"]:
            md += "### Kimi 7-Q&A 摘要\n\n"

            q1 = paper["kimi_summary"].get("q1", "")
            if q1:
                md += f"**Q1: 这篇论文试图解决什么问题？**\n{q1[:500]}"
                if len(q1) > 500:
                    md += "...(truncated)"
                md += "\n\n"

            q2 = paper["kimi_summary"].get("q2", "")
            if q2:
                md += f"**Q2: 相关研究有哪些？它们有什么不足？**\n{q2[:500]}"
                if len(q2) > 500:
                    md += "...(truncated)"
                md += "\n\n"

            q3 = paper["kimi_summary"].get("q3", "")
            if q3:
                md += f"**Q3: 本文的核心方法是什么？**\n{q3[:500]}"
                if len(q3) > 500:
                    md += "...(truncated)"
                md += "\n\n"

        md += "---\n\n"

    return md


if __name__ == "__main__":
    main()
