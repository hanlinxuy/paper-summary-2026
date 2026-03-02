#!/bin/bash

OUTPUT="knowledge/reports/final_report_feb-2026.md"

cat > "$OUTPUT" << 'EOF'
# 2026年2月AI/ML论文深度分析报告

> **报告生成时间**: 2026-03-02
> **数据来源**: papers.cool (cs.CL, cs.LG, cs.AI, cs.CV)
> **筛选范围**: 2026-02-01 至 2026-02-28 (19天有数据)
> **候选论文**: 566篇
> **核心论文**: 30篇

---

## 目录

EOF

extract_title() {
    local file="$1"
    local title=""
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^##[[:space:]]+(.+)$ ]]; then
            title="${BASH_REMATCH[1]}"
            break
        elif [[ "$line" =~ ^#[[:space:]]+(.+)$ ]]; then
            title="${BASH_REMATCH[1]}"
            break
        fi
    done < "$file"
    
    echo "$title"
}

counter=1
for file in knowledge/reports/structured_papers/*.md; do
    title=$(extract_title "$file")
    paper_id=$(basename "$file" .md)
    
    if [ -z "$title" ]; then
        title="论文 $paper_id"
    fi
    
    echo "$counter. [$title](#paper-$paper_id) - [$paper_id](https://arxiv.org/abs/$paper_id)" >> "$OUTPUT"
    counter=$((counter + 1))
done

echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"
echo "" >> "$OUTPUT"

for file in knowledge/reports/structured_papers/*.md; do
    paper_id=$(basename "$file" .md)
    
    echo "" >> "$OUTPUT"
    echo "<a id=\"paper-$paper_id\"></a>" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    
    cat "$file" >> "$OUTPUT"
    
    echo "" >> "$OUTPUT"
    echo "---" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    echo "[↑ 返回目录](#目录)" >> "$OUTPUT"
done

echo "报告已生成: $OUTPUT"
