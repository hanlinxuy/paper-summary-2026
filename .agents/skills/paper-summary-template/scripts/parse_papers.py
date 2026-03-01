#!/usr/bin/env python3
import re
import json
import os
from html import unescape


def parse_papers_html(html_content, date_str):
    papers = []
    paper_blocks = re.findall(
        r'<div\s+id="(\d{4}\.\d+)"\s+class="panel\s+paper"[^>]*>(.*?)(?=<div\s+id="\d{4}\.\d+"\s+class="panel\s+paper"|\s*</body>)',
        html_content,
        re.DOTALL,
    )

    for i, (arxiv_id, block) in enumerate(paper_blocks):
        if i >= 30:
            break

        index_match = re.search(r'<span\s+class="index[^"]*">#(\d+)</span>', block)
        index = int(index_match.group(1)) if index_match else i + 1

        title_match = re.search(
            r'<a\s+id="title-' + arxiv_id + r'"[^>]*>([^<]+)</a>', block
        )
        title = title_match.group(1) if title_match else ""
        title = unescape(title.strip())

        authors = []
        author_pattern = re.compile(
            r'<a\s+class="author[^"]*"[^>]*>([^<]+)</a>', re.MULTILINE
        )
        for author_match in author_pattern.finditer(block):
            authors.append(unescape(author_match.group(1).strip()))

        subjects = []
        subject_pattern = re.compile(
            r'<a\s+class="subject-\d"[^>]*href="/arxiv/([^"]+)"', re.MULTILINE
        )
        for subj_match in subject_pattern.finditer(block):
            subjects.append(subj_match.group(1))

        url = f"https://arxiv.org/abs/{arxiv_id}"

        papers.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "subjects": subjects,
                "index": index,
                "url": url,
            }
        )

    return papers


def main():
    os.makedirs("./knowledge", exist_ok=True)

    files = [
        ("/tmp/papers_2026-02-20.html", "2026-02-20"),
        ("/tmp/papers_2026-02-23.html", "2026-02-23"),
        ("/tmp/papers_2026-02-24.html", "2026-02-24"),
        ("/tmp/papers_2026-02-25.html", "2026-02-25"),
        ("/tmp/papers_2026-02-26.html", "2026-02-26"),
        ("/tmp/papers_2026-02-27.html", "2026-02-27"),
    ]

    for filepath, date_str in files:
        print(f"Processing {filepath}...")

        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()

        papers = parse_papers_html(html_content, date_str)

        result = {"date": date_str, "total_extracted": len(papers), "papers": papers}

        output_path = f"./knowledge/day_{date_str}_papers.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"  Extracted {len(papers)} papers to {output_path}")


if __name__ == "__main__":
    main()
