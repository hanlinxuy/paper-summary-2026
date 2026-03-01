# AGENTS.md - Paper Summary Project

## 目录结构

```
.
├── .agents/skills/          # Agent技能
│   ├── paper-summary-template/
│   ├── kimi-summary-extractor/
│   ├── papers-cool-filter/
│   └── read-arxiv-paper/
├── knowledge/
│   ├── papers/             # 论文TeX分析 (gitignore)
│   └── reports/            # 报告 (上传Git)
└── AGENTS.md
```

## 工作流程

1. papers-cool-filter → 筛选论文
2. kimi-summary-extractor → 获取Kimi摘要
3. read-arxiv-paper → 生成TeX深度分析
4. paper-summary-template → 结构化输出

## 注意事项

- **Git**: papers/ 不上传，reports/ 上传
- **Markdown**: 不用 --- YAML，直接 # 标题
- **输出**: knowledge/reports/structured_analysis_30.md, final_report_feb-2026.md
