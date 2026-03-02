#!/usr/bin/env python3
import json
from pathlib import Path
import re

KNOWLEDGE_DIR = Path("./knowledge")
STRUCTURED_PAPERS_DIR = KNOWLEDGE_DIR / "reports" / "structured_papers"
OUTPUT_FILE = KNOWLEDGE_DIR / "selected_papers_feb_2026_v2.json"

EDGE_KEYWORDS = [
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
    "acceleration",
    "optimization",
    "compact",
    "sparse",
    "hardware",
    "deploy",
    "attention",
    "flash",
    "memory",
    "cache",
    "kv",
    "fast",
    "speed",
]


def extract_paper_info(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    arxiv_id = filepath.stem

    title_match = re.search(r"^## (.+)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Unknown"

    method_match = re.search(
        r"\*\*核心方法\*\*: (.+?)(?=\n\n|\n-|\Z)", content, re.DOTALL
    )
    method = method_match.group(1) if method_match else ""

    problem_match = re.search(
        r"\*\*解决的问题\*\*: (.+?)(?=\n\n|\n-|\Z)", content, re.DOTALL
    )
    problem = problem_match.group(1) if problem_match else ""

    results_match = re.search(
        r"### 效果评估.*?\n\n(.+?)(?=\n###|\Z)", content, re.DOTALL
    )
    results = results_match.group(1) if results_match else ""

    credibility_match = re.search(r"\*\*文章可信度\*\*: (\d+)/10", content)
    credibility = int(credibility_match.group(1)) if credibility_match else 5

    importance_match = re.search(r"\*\*文章重要性\*\*: (\d+)/10", content)
    importance = int(importance_match.group(1)) if importance_match else 5

    edge_value_match = re.search(r"\*\*端侧设备实用价值\*\*: (\d+)/10", content)
    edge_value = int(edge_value_match.group(1)) if edge_value_match else 5

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "method": method,
        "problem": problem,
        "results": results,
        "credibility": credibility,
        "importance": importance,
        "edge_value": edge_value,
        "content": content,
    }


def calculate_edge_score(title, method, problem):
    text = (title + " " + method + " " + problem).lower()
    score = 0
    matched = []
    for keyword in EDGE_KEYWORDS:
        if keyword in text:
            score += 8
            matched.append(keyword)
    return min(100, score), matched


def detect_architecture(title, method, problem):
    text = (title + " " + method + " " + problem).lower()
    architectures = []

    if "transformer" in text or "attention" in text:
        architectures.append("Transformer")
    if "moe" in text or "mixture of expert" in text or "expert" in text:
        architectures.append("MoE")
    if "diffusion" in text:
        architectures.append("Diffusion")
    if "mamba" in text or "ssm" in text or "state space" in text:
        architectures.append("Mamba")
    if "rnn" in text or "lstm" in text:
        architectures.append("RNN")
    if "cnn" in text or "convolution" in text:
        architectures.append("CNN")
    if "vit" in text or "vision transformer" in text:
        architectures.append("ViT")
    if "vla" in text or "vision-language-action" in text or "robot" in text:
        architectures.append("VLA/Robot")
    if "agent" in text or "agentic" in text:
        architectures.append("Agent")
    if "reasoning" in text:
        architectures.append("Reasoning")
    if "memory" in text or "cache" in text or "kv" in text:
        architectures.append("Memory")
    if "video" in text:
        architectures.append("Video")
    if "3d" in text or "three" in text:
        architectures.append("3D")

    return "+".join(architectures) if architectures else "Other"


def main():
    papers = []

    for filepath in sorted(STRUCTURED_PAPERS_DIR.glob("*.md")):
        info = extract_paper_info(filepath)
        papers.append(info)

    print(f"Loaded {len(papers)} papers")

    scored_papers = []
    for i, paper in enumerate(papers):
        heat_score = 100 - i * 3
        heat_score = max(0, heat_score)

        edge_score, matched_keywords = calculate_edge_score(
            paper["title"], paper["method"], paper["problem"]
        )
        architecture = detect_architecture(
            paper["title"], paper["method"], paper["problem"]
        )

        total_score = 0.7 * heat_score + 0.3 * edge_score

        scored_papers.append(
            {
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "architecture": architecture,
                "heat_score": round(heat_score, 1),
                "edge_score": edge_score,
                "matched_keywords": matched_keywords,
                "total_score": round(total_score, 1),
                "credibility": paper["credibility"],
                "importance": paper["importance"],
                "edge_value": paper["edge_value"],
            }
        )

    scored_papers.sort(key=lambda x: x["total_score"], reverse=True)

    for i, paper in enumerate(scored_papers, 1):
        paper["rank"] = i

    print("\n" + "=" * 130)
    print("TOP 30 PAPERS (热度70% + 端侧30%)")
    print("=" * 130)
    for paper in scored_papers:
        print(
            f"{paper['rank']:2}. {paper['total_score']:5.1f} | H:{paper['heat_score']:5.1f} E:{paper['edge_score']:3} | {paper['architecture']:25} | {paper['arxiv_id']} | {paper['title'][:35]}..."
        )

    output = {
        "date_range": "2026-02-01 to 2026-02-28",
        "total_candidates": len(papers),
        "selected_count": len(scored_papers),
        "scoring": "热度70% + 端侧相关性30%",
        "selected_papers": scored_papers,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to: {OUTPUT_FILE}")

    ranked_ids = [p["arxiv_id"] for p in scored_papers]
    id_file = KNOWLEDGE_DIR / "selected_30_ids_v2.txt"
    with open(id_file, "w") as f:
        f.write("\n".join(ranked_ids))
    print(f"Ranked IDs saved to: {id_file}")

    return scored_papers


if __name__ == "__main__":
    main()
