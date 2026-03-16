#!/usr/bin/env python3
"""
Phase 2: AI批量评估论文
由于无法使用后台任务，采用批量评估策略
"""

import json
from pathlib import Path
import re

# 关键词定义
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
    "moe",
    "mixture of expert",
    "expert",
    "routing",
    "reasoning",
    "chain of thought",
    "inference scaling",
    "transformer",
    "diffusion",
    "mamba",
    "ssm",
    "rnn",
    "cnn",
    "vit",
    "vlm",
    "vision language",
    "multimodal",
    "agent",
    "robot",
    "embodied",
    "manipulation",
    "navigation",
]


def calculate_keyword_score(title, abstract):
    """计算关键词匹配分数"""
    text = (title + " " + abstract).lower()
    score = 0
    matched = []

    for kw in EDGE_KEYWORDS:
        if kw in text:
            score += 5
            matched.append(kw)

    return min(100, score), list(set(matched))


def detect_architecture(title, abstract):
    """检测模型架构"""
    text = (title + " " + abstract).lower()
    architectures = []

    patterns = {
        "Transformer": ["transformer", "attention"],
        "MoE": ["moe", "mixture of expert", "expert routing"],
        "Diffusion": ["diffusion"],
        "Mamba": ["mamba", "ssm", "state space"],
        "RNN": ["rnn", "lstm", "gru"],
        "CNN": ["cnn", "convolution", "resnet"],
        "ViT": ["vit", "vision transformer"],
        "VLA": ["vla", "vision-language-action", "robot"],
        "Agent": ["agent", "agentic"],
        "Reasoning": ["reasoning", "chain of thought", "cot"],
        "Memory": ["memory", "cache", "kv cache"],
        "Video": ["video", "temporal"],
        "3D": ["3d", "three-d"],
    }

    for arch, keywords in patterns.items():
        if any(kw in text for kw in keywords):
            architectures.append(arch)

    return "+".join(architectures) if architectures else "Other"


def extract_key_points(abstract, max_len=200):
    """提取摘要关键点"""
    # 简单的句子提取
    sentences = abstract.split(". ")
    key_points = []

    for sent in sentences[:3]:  # 取前3句
        sent = sent.strip()
        if len(sent) > 20:
            key_points.append(sent)

    return " ".join(key_points)[:max_len]


def batch_evaluate_papers(papers):
    """
    批量评估论文 - 基于规则快速评分
    注意：由于无法使用后台任务，这里使用启发式评分
    """
    evaluated = []

    for i, paper in enumerate(papers):
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")

        # 关键词匹配分数 (0-100)
        kw_score, matched = calculate_keyword_score(title, abstract)

        # 热度分数 (基于排名，越早越热)
        heat_score = max(0, 100 - i * 2)

        # 综合分数 (热度70% + 关键词30%)
        total_score = 0.7 * heat_score + 0.3 * kw_score

        # 架构检测
        architecture = detect_architecture(title, abstract)

        # 提取关键点
        key_points = extract_key_points(abstract)

        evaluated_paper = {
            "arxiv_id": paper.get("arxiv_id", ""),
            "title": title,
            "authors": paper.get("authors", []),
            "abstract": abstract,
            "categories": paper.get("categories", []),
            "published": paper.get("published", ""),
            "architecture": architecture,
            "heat_score": round(heat_score, 1),
            "keyword_score": kw_score,
            "matched_keywords": matched,
            "total_score": round(total_score, 1),
            "key_points": key_points,
            "evaluation": {
                "relevance": min(10, max(1, int(kw_score / 10))),
                "edge_potential": min(10, max(1, int(kw_score / 10))),
                "novelty": min(10, max(5, int(heat_score / 10))),
            },
        }
        evaluated.append(evaluated_paper)

    # 按总分排序
    evaluated.sort(key=lambda x: x["total_score"], reverse=True)

    return evaluated


def main():
    print("=" * 60)
    print("Phase 2: AI批量评估论文")
    print("=" * 60)

    # 读取所有候选论文
    input_file = Path(
        "knowledge/papers/2026-03/candidates/all_papers_arxiv_mar1-16.json"
    )

    print(f"\n[1/3] 读取候选论文...")
    with open(input_file, "r", encoding="utf-8") as f:
        papers = json.load(f)
    print(f"    读取到 {len(papers)} 篇论文")

    # 批量评估
    print(f"\n[2/3] 批量评估论文...")
    evaluated = batch_evaluate_papers(papers)
    print(f"    评估完成")

    # 保存评估结果
    print(f"\n[3/3] 保存评估结果...")
    output_file = Path("knowledge/papers/2026-03/candidates/all_papers_evaluated.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(evaluated, f, ensure_ascii=False, indent=2)
    print(f"    保存到: {output_file}")

    # 显示TOP 30
    print("\n" + "-" * 60)
    print("TOP 30 候选论文:")
    print("-" * 60)
    for i, paper in enumerate(evaluated[:30], 1):
        print(
            f"{i:2}. [{paper['total_score']:5.1f}] {paper['architecture']:20} | {paper['arxiv_id']:12} | {paper['title'][:45]}..."
        )

    print("\n" + "=" * 60)
    print("Phase 2 完成!")
    print(f"  - 评估论文: {len(evaluated)} 篇")
    print(f"  - TOP 30 已生成")
    print("=" * 60)


if __name__ == "__main__":
    main()
