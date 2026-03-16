#!/usr/bin/env python3
"""
使用 arXiv API 获取3月1-16日的论文
修复XML解析问题
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path
from datetime import datetime

ARXIV_API = "http://export.arxiv.org/api/query"


def fetch_arxiv_papers(start_date, end_date, categories, max_results=3000):
    """从arXiv API获取论文"""

    # 构建查询
    cat_query = " OR ".join([f"cat:{c}" for c in categories])
    date_query = f"submittedDate:[{start_date} TO {end_date}]"
    query = f"({cat_query}) AND {date_query}"

    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    print(f"请求URL: {url[:100]}...")

    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; PaperBot/1.0)"}
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        data = response.read()

    return data.decode("utf-8")


def parse_atom_feed(xml_text):
    """解析Atom格式的返回数据 - 使用正则表达式"""
    papers = []

    # 提取所有entry
    entries = re.findall(r"<entry>(.*?)</entry>", xml_text, re.DOTALL)
    print(f"找到 {len(entries)} 个entry")

    for entry in entries:
        # arXiv ID
        id_match = re.search(r"<id>([^/]+/([^\s<]+))</id>", entry)
        arxiv_id = id_match.group(2) if id_match else ""

        # 标题
        title_match = re.search(r"<title>([^*]*?)</title>", entry, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        title = re.sub(r"\s+", " ", title)

        # 作者
        authors = []
        for author_match in re.finditer(
            r"<author>.*?\s*<name>([^\s<][^<]*)</name>.*?</author>", entry, re.DOTALL
        ):
            authors.append(author_match.group(1).strip())

        # 摘要
        summary_match = re.search(r"<summary>(.*?)\s*</summary>", entry, re.DOTALL)
        abstract = summary_match.group(1).strip() if summary_match else ""

        # 分类
        categories = []
        for cat_match in re.finditer(r'category term="([^"]+)"', entry):
            cat = cat_match.group(1)
            if cat not in categories:
                categories.append(cat)

        # 发布日期
        published_match = re.search(r"<published>([^\s<]+)", entry)
        published = published_match.group(1) if published_match else ""

        # 更新日期
        updated_match = re.search(r"<updated>([^\s<]+)", entry)
        updated = updated_match.group(1) if updated_match else ""

        paper = {
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "categories": categories,
            "published": published,
            "updated": updated,
        }
        papers.append(paper)

    return papers


def save_by_date(papers, output_dir, daily_limit=15):
    """按日期保存论文"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 按日期分组
    by_date = {}
    for paper in papers:
        try:
            if not paper["published"]:
                continue
            date_str = paper["published"][:10]  # YYYY-MM-DD
            if date_str not in by_date:
                by_date[date_str] = []
            by_date[date_str].append(paper)
        except:
            continue

    # 每天保存前daily_limit篇
    total = 0
    for date_str in sorted(by_date.keys()):
        papers_list = by_date[date_str]
        date_key = date_str[5:].replace("-", "")  # MMDD
        date_dir = output_dir / date_key
        date_dir.mkdir(exist_ok=True)

        # 取前daily_limit篇
        top_papers = papers_list[:daily_limit]

        output_file = date_dir / "papers.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(top_papers, f, ensure_ascii=False, indent=2)

        total += len(top_papers)
        print(f"✓ 日期 {date_str} ({date_key}): 保存 {len(top_papers)} 篇论文")

    return total, len(by_date)


def main():
    print("=" * 60)
    print("使用 arXiv API 获取3月论文")
    print("=" * 60)

    # 配置
    categories = ["cs.CL", "cs.LG", "cs.AI", "cs.CV"]
    start_date = "202603010000"  # YYYYMMDDHHMM
    end_date = "202603162359"

    # 获取数据
    print(f"\n[1/3] 从 arXiv API 获取论文...")
    print(f"    分类: {', '.join(categories)}")
    print(f"    日期: 2026-03-01 至 2026-03-16")

    try:
        xml_text = fetch_arxiv_papers(
            start_date, end_date, categories, max_results=3000
        )
        print(f"    获取到 {len(xml_text)} 字符数据")
    except Exception as e:
        print(f"    错误: {e}")
        import traceback

        traceback.print_exc()
        return

    # 解析
    print(f"\n[2/3] 解析论文数据...")
    papers = parse_atom_feed(xml_text)
    print(f"    总计: {len(papers)} 篇论文")

    if papers:
        print(f"\n    样本: {papers[0]['title'][:60]}...")
        print(f"    日期: {papers[0]['published']}")

    # 按日期分组并保存
    print(f"\n[3/3] 按日期分组并保存...")
    output_dir = "knowledge/papers/2026-03/candidates"
    total, num_days = save_by_date(papers, output_dir, daily_limit=15)

    # 保存完整列表
    all_output = Path(output_dir) / "all_papers_arxiv_mar1-16.json"
    with open(all_output, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 完整列表 ({len(papers)} 篇) 保存到: {all_output}")

    print("\n" + "=" * 60)
    print(f"Phase 1 完成!")
    print(f"  - 总计: {len(papers)} 篇论文")
    print(f"  - 天数: {num_days} 天")
    print(f"  - 每天精选: 最多15篇")
    print(f"  - 实际保存: {total} 篇")
    print("=" * 60)


if __name__ == "__main__":
    main()
