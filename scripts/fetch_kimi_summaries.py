#!/usr/bin/env python3
"""
Phase 4: 批量获取Kimi摘要
使用 papers.cool API 获取每篇论文的Kimi 7-Q&A摘要
"""

import subprocess
import json
import time
from pathlib import Path
import re


def fetch_kimi_summary(paper_id):
    """获取单篇论文的Kimi摘要"""
    url = f"https://papers.cool/arxiv/kimi?paper={paper_id}"

    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", url],
            capture_output=True,
            text=True,
            timeout=30,
        )

        html = result.stdout

        # 如果返回的是HTML，需要解析
        if "<html" in html.lower():
            # 提取Q&A内容
            qa_pairs = parse_kimi_html(html)
            return qa_pairs
        else:
            return {"raw": html}

    except Exception as e:
        return {"error": str(e)}


def parse_kimi_html(html):
    """解析Kimi返回的HTML，提取7个Q&A"""
    qa_pairs = {}

    # 尝试提取Q1-Q7
    for i in range(1, 8):
        # 查找问题
        q_pattern = (
            rf"Q{i}[:：](.*?)(?=Q{i + 1}[:：]|$)" if i < 7 else rf"Q{i}[:：](.*?)$"
        )
        q_match = re.search(q_pattern, html, re.DOTALL | re.IGNORECASE)

        if q_match:
            content = q_match.group(1).strip()
            # 清理HTML标签
            content = re.sub(r"<[^\u003e]+>", "", content)
            content = re.sub(r"\s+", " ", content)
            qa_pairs[f"Q{i}"] = content

    return qa_pairs


def main():
    print("=" * 60)
    print("Phase 4: 批量获取Kimi摘要")
    print("=" * 60)

    # 读取Top 30论文
    print("\n[1/3] 读取Top 30论文列表...")
    with open("knowledge/selected_30_ids_mar_2026.txt", "r") as f:
        paper_ids = [line.strip() for line in f if line.strip()]
    print(f"    读取到 {len(paper_ids)} 篇论文ID")

    # 创建输出目录
    output_dir = Path("knowledge/reports/mar2026_kimi")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 批量获取Kimi摘要
    print(f"\n[2/3] 批量获取Kimi摘要...")
    summaries = {}

    for i, paper_id in enumerate(paper_ids, 1):
        print(f"    [{i:2}/30] 获取 {paper_id}...", end=" ")

        summary = fetch_kimi_summary(paper_id)
        summaries[paper_id] = summary

        # 保存单个文件
        output_file = output_dir / f"{paper_id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print("✓")

        # 短暂延迟，避免请求过快
        if i < len(paper_ids):
            time.sleep(0.5)

    # 保存汇总
    print(f"\n[3/3] 保存汇总...")
    all_summary_file = Path("knowledge/reports/kimisummary_mar_2026.json")
    with open(all_summary_file, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    print(f"    汇总保存到: {all_summary_file}")

    print("\n" + "=" * 60)
    print("Phase 4 完成!")
    print(f"  - 获取Kimi摘要: {len(summaries)} 篇")
    print(f"  - 单篇文件目录: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
