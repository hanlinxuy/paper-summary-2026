---
name: kimi-summary-extractor
description: |
  Extract Kimi AI reading summaries from papers.cool/arxiv pages using curl.
  **Trigger**: "Kimi summary", "Kimi 阅读笔记", "papers.cool 摘要", "extract paper summary from papers.cool", "arxiv Kimi notes"
  **Use when**: 用户想要获取 arXiv 论文的 Kimi 阅读摘要，需要从 papers.cool 网站提取内容
  **API**: POST https://papers.cool/arxiv/kimi?paper={paper_id}
---

# Kimi Summary Extractor

从 papers.cool/arxiv 页面提取 Kimi AI 生成的阅读摘要。

## API 端点

```
POST https://papers.cool/arxiv/kimi?paper={paper_id}
```

**示例:**
```bash
curl -s -X POST "https://papers.cool/arxiv/kimi?paper=2602.21221"
```

## 返回格式

返回 HTML 格式的 Markdown 内容，包含 7 个 Q&A 部分：

| Q | 问题 |
|---|------|
| Q1 | 这篇论文试图解决什么问题？ |
| Q2 | 有哪些相关研究？ |
| Q3 | 论文如何解决这个问题？ |
| Q4 | 论文做了哪些实验？ |
| Q5 | 有什么可以进一步探索的点？ |
| Q6 | 总结一下论文的主要内容 |
| Q7 | 想要进一步了解论文 |

## 使用方法

### 1. 基本提取

```bash
# 获取原始 HTML
curl -s -X POST "https://papers.cool/arxiv/kimi?paper=2602.21221"
```

### 2. 转换为纯文本

```bash
# 使用 sed 去除 HTML 标签
curl -s -X POST "https://papers.cool/arxiv/kimi?paper=2602.21221" | sed 's/<[^>]*>//g' | sed '/^$/d'

# 或使用 lynx（如果安装了）
curl -s -X POST "https://papers.cool/arxiv/kimi?paper=2602.21221" | lynx -stdin -dump
```

### 3. 转换为 Markdown

```bash
# 使用 pandoc（如果安装了）
curl -s -X POST "https://papers.cool/arxiv/kimi?paper=2602.21221" | pandoc -f html -t markdown
```

### 4. 保存到文件

```bash
PAPER_ID="2602.21221"
curl -s -X POST "https://papers.cool/arxiv/kimi?paper=$PAPER_ID" > "kimi_summary_${PAPER_ID}.html"
```

### 5. 批量处理

```bash
for paper_id in 2602.21221 2310.06825 2401.15884; do
  echo "=== Paper: $paper_id ==="
  curl -s -X POST "https://papers.cool/arxiv/kimi?paper=$paper_id" > "kimi_${paper_id}.html"
  sleep 1  # 避免请求过快
done
```

## 注意事项

1. **请求频率**: 避免高频请求，批量处理时添加延迟
2. **网络依赖**: 需要能够访问 `papers.cool` 域名
3. **Paper ID 格式**: 支持标准 arXiv ID（如 `2602.21221`、`2310.06825`）
4. **编码**: 响应为 UTF-8 编码的中文内容

## 错误处理

- 如果论文不存在，返回错误页面
- 如果 Kimi 摘要未生成，可能需要等待一段时间后重试

## 触发场景

- 用户说 "获取论文 2602.21221 的 Kimi 摘要"
- 用户说 "这个论文的阅读笔记在哪里"
- 用户说 "papers.cool 上的 Kimi 总结"
- 用户提供 papers.cool/arxiv/ 链接并想要摘要
