# Papers.cool 爬虫辅助脚本

## 文件列表

### 1. parse_papers.py
解析 papers.cool HTML 页面，提取论文信息

**功能**:
- 解析 papers.cool 页面HTML
- 提取 arxiv_id, title, authors, subjects, index
- 输出 JSON 格式

**用法**:
```bash
python parse_papers.py 2026-02-20
```

**输出**:
```json
{
  "date": "2026-02-20",
  "total": 30,
  "papers": [...]
}
```

---

### 2. fetch_kimi_summaries.py
批量获取 Kimi 7-Q&A 摘要

**功能**:
- 读取论文列表 JSON
- 并发调用 Kimi API
- 解析 HTML 提取 Q1-Q7
- 保存为独立 JSON 文件

**用法**:
```bash
python fetch_kimi_summaries.py
```

**API**:
```
POST https://papers.cool/arxiv/kimi?paper={arxiv_id}
```

---

### 3. select_papers.py
综合评分选出 Top N 论文

**功能**:
- 读取论文元数据和 Kimi 摘要
- 综合评分算法
- 输出选中论文列表

**评分算法**:
```
综合分 = 0.6 × 热度分 + 0.4 × 质量分
```

---

## 使用流程

```bash
# 1. 下载 HTML
curl -s "https://papers.cool/arxiv/cs.CL,cs.LG,cs.AI,cs.CV?date=2026-02-20&sort=1" > /tmp/papers_2026-02-20.html

# 2. 解析论文列表
python parse_papers.py 2026-02-20

# 3. 获取 Kimi 摘要
python fetch_kimi_summaries.py

# 4. 评分选论文
python select_papers.py
```
