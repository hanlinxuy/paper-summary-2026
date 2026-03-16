#!/usr/bin/env python3
"""
爬取 papers.cool 3月1-16日的论文
由于date参数返回500，先获取当前页面再筛选
"""

import subprocess
import re
import json
from pathlib import Path
from datetime import datetime


def fetch_papers_page():
    """获取papers.cool页面HTML"""
    url = "https://papers.cool/arxiv/cs.CL,cs.LG,cs.AI,cs.CV?sort=1"
    result = subprocess.run(
        ["curl", "-s", "-L", url], capture_output=True, text=True, timeout=60
    )
    return result.stdout


def parse_papers(html):
    """解析HTML提取论文信息"""
    papers = []

    # 提取论文块 (每个paper在一个div.panel.paper中)
    paper_blocks = re.findall(
        r'<div id="(\d{4}\.\d+)" class="panel paper"[^>]*>(.*?)</div>\s*<hr[^>]*>',
        html,
        re.DOTALL,
    )

    for arxiv_id, block in paper_blocks:
        # 提取标题
        title_match = re.search(r'<a[^>]*class="title-link[^"]*"[^>]*>(.*?)</a>', block)
        title = re.sub(r"<[^>]+>", "", title_match.group(1)) if title_match else ""

        # 提取作者
        authors_match = re.search(
            r'<p[^>]*class="metainfo authors[^"]*"[^>]*>(.*?)</p>', block, re.DOTALL
        )
        if authors_match:
            authors_text = authors_match.group(1)
            # 提取所有作者名
            authors = re.findall(r'query=([^"]+)"[^>]*>([^<]+)</a>', authors_text)
            author_names = [a[1] for a in authors]
        else:
            author_names = []

        # 提取摘要
        summary_match = re.search(
            r'<p[^>]*class="summary[^"]*"[^>]*>(.*?)</p>', block, re.DOTALL
        )
        summary = (
            re.sub(r"<[^>]+>", "", summary_match.group(1)) if summary_match else ""
        )

        # 提取分类
        subjects_match = re.search(
            r'<p[^>]*class="metainfo subjects[^"]*"[^>]*>(.*?)</p>', block, re.DOTALL
        )
        if subjects_match:
            subjects_text = subjects_match.group(1)
            subjects = re.findall(r">([^<]+)</a>", subjects_text)
        else:
            subjects = []

        # 提取发布日期
        date_match = re.search(
            r'<p[^>]*class="metainfo date[^"]*"[^>]*>.*?<span[^>]*>(\d{4}-\d{2}-\d{2}[^<]*)</span>',
            block,
            re.DOTALL,
        )
        publish_date = date_match.group(1) if date_match else ""

        paper = {
            "arxiv_id": arxiv_id,
            "title": title.strip(),
            "authors": author_names,
            "abstract": summary.strip(),
            "subjects": subjects,
            "publish_date": publish_date.strip() if publish_date else "",
        }
        papers.append(paper)

    return papers


def filter_by_date(papers, start_date, end_date):
    """筛选指定日期范围的论文"""
    filtered = []
    for paper in papers:
        try:
            # 解析日期 (格式: 2026-03-13 17:58:14 UTC)
            date_str = paper["publish_date"].split()[0]
            paper_date = datetime.strptime(date_str, "%Y-%m-%d")

            if start_date <= paper_date <= end_date:
                filtered.append(paper)
        except:
            continue
    return filtered


def save_papers_by_date(papers, output_dir):
    """按日期保存论文到不同文件"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 按日期分组
    by_date = {}
    for paper in papers:
        try:
            date_str = paper["publish_date"].split()[0]
            date_key = date_str[5:].replace("-", "")  # 转换为 MMDD 格式
            if date_key not in by_date:
                by_date[date_key] = []
            by_date[date_key].append(paper)
        except:
            continue

    # 每天保存前15篇
    for date_key, papers_list in sorted(by_date.items()):
        date_dir = output_dir / f"{date_key}"
        date_dir.mkdir(exist_ok=True)

        # 取前15篇
        top_15 = papers_list[:15]

        output_file = date_dir / "papers.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(top_15, f, ensure_ascii=False, indent=2)

        print(f"✓ 日期 {date_key}: 保存 {len(top_15)} 篇论文到 {output_file}")


def main():
    print("=" * 60)
    print("爬取 papers.cool 论文")
    print("=" * 60)

    # 获取页面
    print("\n[1/3] 获取 papers.cool 页面...")
    html = fetch_papers_page()
    print(f"    获取到 {len(html)} 字符")

    # 解析论文
    print("\n[2/3] 解析论文列表...")
    all_papers = parse_papers(html)
    print(f"    解析到 {len(all_papers)} 篇论文")

    # 筛选3月1-16日
    print("\n[3/3] 筛选 2026-03-01 至 2026-03-16 的论文...")
    start_date = datetime(2026, 3, 1)
    end_date = datetime(2026, 3, 16)
    filtered_papers = filter_by_date(all_papers, start_date, end_date)
    print(f"    筛选出 {len(filtered_papers)} 篇论文")

    # 保存
    output_dir = "knowledge/papers/2026-03/candidates"
    save_papers_by_date(filtered_papers, output_dir)

    # 保存完整列表
    all_output = Path(output_dir) / "all_papers_mar1-16.json"
    with open(all_output, "w", encoding="utf-8") as f:
        json.dump(filtered_papers, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 完整列表保存到: {all_output}")

    print("\n" + "=" * 60)
    print("Phase 1 完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
