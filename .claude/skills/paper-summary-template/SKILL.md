---
name: paper-summary-template
description: |
  论文摘要 Jinja2 模板使用指南。当用户需要了解模板格式、变量或自定义摘要输出时触发。
  **触发场景**:
  - "论文摘要模板怎么写"
  - "自定义摘要格式"
  - "jinja2 模板变量"
  - "模板有哪些"
---

# 论文摘要模板指南

## 可用模板

所有模板文件统一位于项目根目录 `templates/` 下：

| 模板文件 | 用途 |
|---------|------|
| `templates/academic_summary.md.j2` | 学术摘要（背景→方法→结果→结论） |
| `templates/structured_analysis.md.j2` | 结构化分析（含 Kimi 摘要、可信度/重要性评分） |

## 模板变量

```jinja2
{{ paper_id }}          # arXiv ID
{{ title }}             # 论文标题
{{ authors }}           # 作者
{{ original_abstract }} # 原文摘要
{{ kimi_summary }}      # Kimi 生成的摘要
{{ pdf_summary }}       # PDF 提取内容
{{ local_comment }}     # 本地评论
```

## 使用方式

1. 在项目根目录 `templates/` 创建或修改 `.j2` 文件
2. 调用 skill 时传入模板路径: `templates/structured_analysis.md.j2`

## 默认值处理

```jinja2
{{ variable | default("未提供", true) }}
```

## 条件渲染

```jinja2
{% if pdf_summary %}
## PDF 内容
{{ pdf_summary }}
{% endif %}
```
