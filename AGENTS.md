# AGENTS.md - Paper Summary Project

## Project Overview

This is a personal research project for tracking and summarizing arXiv papers. It fetches paper metadata and AI-generated summaries from papers.cool, then ranks papers by relevance.

**Project Type**: Python scripts for paper data processing (no web app, no tests)

---

## Commands

### Running Scripts

All scripts are in `.agents/skills/paper-summary-template/scripts/`:

```bash
# Activate virtual environment first
source .venv/bin/activate

# Parse papers from papers.cool HTML (requires HTML in /tmp/)
python .agents/skills/paper-summary-template/scripts/parse_papers.py

# Fetch Kimi summaries for all papers
python .agents/skills/paper-summary-template/scripts/fetch_kimi_summaries.py

# Score and select top N papers
python .agents/skills/paper-summary-template/scripts/select_papers.py

# Run with Python directly
python3 .agents/skills/paper-summary-template/scripts/select_papers.py
```

### Linting & Formatting

No formal linter/formatter configured. Run manually if needed:

```bash
# Format with black (if installed)
black .agents/skills/paper-summary-template/scripts/

# Lint with ruff (if installed)
ruff check .agents/skills/paper-summary-template/scripts/
```

### Virtual Environment

```bash
# Create (if needed)
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt
```

---

## Code Style

### Language & Tools

- **Language**: Python 3.14
- **Dependencies**: aiohttp (async HTTP), no other formal dependencies
- **No type checking** enforced (plain Python)

### Formatting

- **Indentation**: 4 spaces
- **Line length**: No strict limit, but prefer <120 chars
- **Strings**: Double quotes for strings, single quotes only when containing double quotes
- **Blank lines**: Two blank lines between top-level definitions

### Imports

```python
# Standard library first, then third-party
import json
import os
from pathlib import Path
from typing import Dict, Optional

import aiohttp
```

### Naming Conventions

- **Functions**: `snake_case` (e.g., `load_papers`, `calculate_heat_score`)
- **Variables**: `snake_case` (e.g., `all_papers`, `arxiv_id`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_CONCURRENT`, `REQUESTS_PER_SECOND`)
- **Classes**: PascalCase (not used much in this project)

### Error Handling

- Use bare `except Exception` only when specific exceptions are unknown
- Include error messages in return dicts: `{"success": False, "error": "reason"}`
- Log errors to console with `print(f"[FAIL] {arxiv_id}: {error}")`

### Type Hints

Encouraged but not strictly required:

```python
def load_papers() -> list[dict]:
    """Load all papers from day_*_papers.json files"""
    ...

def parse_html_qa(html_content: str) -> Optional[Dict[str, str]]:
    ...
```

---

## Project Structure

```
.
├── .agents/skills/          # Agent skills and templates
│   ├── paper-summary-template/
│   │   ├── scripts/         # Python scripts (main code)
│   │   │   ├── parse_papers.py
│   │   │   ├── fetch_kimi_summaries.py
│   │   │   └── select_papers.py
│   │   ├── templates/       # Jinja2 templates for output
│   │   └── SKILL.md
│   ├── kimi-summary-extractor/
│   ├── papers-cool-filter/
│   └── read-arxiv-paper/
├── knowledge/               # Paper data
│   ├── papers/             # 30篇论文TeX分析 (gitignored)
│   └── reports/            # 报告 (tracked in git)
│       ├── structured_analysis_30.md
│       └── final_report_feb-2026.md
├── .venv/                   # Virtual environment
└── AGENTS.md                # This file
```

**Git规则**:
- `knowledge/papers/` - 本地生成，不上传
- `knowledge/reports/` - 需上传到Git

---

## Data Formats

### Input: Papers JSON

```json
{
  "date": "2026-02-20",
  "total": 30,
  "papers": [
    {
      "arxiv_id": "2602.17270",
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "subjects": ["cs.CL", "cs.LG"],
      "index": 1,
      "url": "https://arxiv.org/abs/2602.17270"
    }
  ]
}
```

### Output: Kimi Summary

```json
{
  "arxiv_id": "2602.17270",
  "q1": "Problem being solved...",
  "q2": "Related work...",
  "q3": "Method...",
  "q4": "Experiments...",
  "q5": "Future work...",
  "q6": "Summary...",
  "q7": "Follow-up questions..."
}
```

---

## External APIs

| API | URL | Purpose |
|-----|-----|---------|
| papers.cool | `https://papers.cool/arxiv/kimi?paper={arxiv_id}` | Get Kimi AI summaries |
| arXiv | `https://arxiv.org/abs/{arxiv_id}` | Paper metadata |

---

## Notes for Agents

1. **No formal CI/CD** - This is a personal research project
2. **No tests** - Scripts are run manually in sequence
3. **Data is gitignored** - Only scripts and templates are versioned
4. **Output is ephemeral** - Generated summaries can be regenerated
5. **Chinese content** - Many paper titles/summaries are in Chinese
6. **Markdown格式** - 不要使用YAML frontmatter (---)，直接用 # 标题开头
