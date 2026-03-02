#!/bin/bash
#
# read-paper.sh - 单论文分析 CLI 工具（完全本地方案）
#
# 使用方法:
#   ./scripts/read-paper.sh 2602.21221 /tmp/paper-workdir
#   ./scripts/read-paper.sh 2602.21221 /tmp/paper-workdir --model anthropic/claude-3-5-sonnet
#
# 参数:
#   paper_id    - arXiv 论文 ID (如 2602.21221)
#   workdir     - 工作目录路径 (用于临时缓存)
#   --model     - 可选，覆盖默认模型
#

set -euo pipefail

# 默认模型
DEFAULT_MODEL="minimax-cn-coding-plan/MiniMax-M2.5-highspeed"
MODEL="$DEFAULT_MODEL"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

usage() {
    cat << EOF
Usage: $(basename "$0") <paper_id> <workdir> [OPTIONS]

单论文分析 CLI 工具 - 完全本地方案，零全局配置

参数:
    paper_id            arXiv 论文 ID (如 2602.21221)
    workdir             工作目录路径 (用于临时缓存)

选项:
    --model MODEL       覆盖默认模型 (默认: $DEFAULT_MODEL)
    -h, --help          显示帮助信息

示例:
    $(basename "$0") 2602.21221 /tmp/paper-2602.21221
    $(basename "$0") 2602.21221 /tmp/paper-2602.21221 --model anthropic/claude-3-5-sonnet

输出:
    knowledge/papers/{paper_id}.md

EOF
}

# 解析参数
if [[ $# -lt 2 ]]; then
    usage
    exit 1
fi

PAPER_ID="$1"
WORKDIR="$2"
shift 2

# 解析可选参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            log_error "未知选项: $1"
            usage
            exit 1
            ;;
    esac
done

# 验证参数
if [[ ! "$PAPER_ID" =~ ^[0-9]+\.[0-9]+$ ]]; then
    log_error "无效的 paper_id 格式: $PAPER_ID"
    log_info "正确格式: 数字.数字 (如 2602.21221)"
    exit 1
fi

# 获取脚本所在目录的绝对路径（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PROMPT_FILE="$SCRIPT_DIR/paper-reader-prompt.md"

# 检查 prompt 文件是否存在
if [[ ! -f "$PROMPT_FILE" ]]; then
    log_error "Prompt 文件不存在: $PROMPT_FILE"
    exit 1
fi

log_info "开始分析论文: $PAPER_ID"
log_info "工作目录: $WORKDIR"
log_info "使用模型: $MODEL"
echo ""

# 创建工作目录
mkdir -p "$WORKDIR"

# 构建 opencode 命令
log_step "启动 opencode 进行分析..."

# 构建完整执行 prompt
FULL_PROMPT="你收到论文分析任务: paper_id=$PAPER_ID, workdir=$WORKDIR

你的任务是依次完成以下6个步骤，生成符合 templates/structured_analysis.md.j2 格式的结构化输出，完成后立即退出。

**模板结构要求**（已简化）:
- ### 基本信息: 作者、机构(affiliation)、arXiv ID
- ### 论文内容分析: 核心方法、解决的问题、1-2段话的内容概述
- ### 效果评估: 1-2段话的关键实验数据
- ### 价值评估: 三个评分维度

步骤1: 获取Kimi摘要（参考用，不直接输出）
curl -s -X POST \"https://papers.cool/arxiv/kimi?paper=$PAPER_ID\" > $WORKDIR/kimi.html
解析HTML提取Q1-Q7纯文本作为参考。

步骤2: 下载论文
curl -s -L \"https://arxiv.org/e-print/$PAPER_ID\" -o $WORKDIR/paper.tar.gz
mkdir -p $WORKDIR/source && cd $WORKDIR/source && tar -xzf ../paper.tar.gz
找到主tex文件。

步骤3: 提取元数据
从tex提取: title, authors, affiliation(从\\icmlaffiliation或作者单位), paper_id

步骤4: 深度分析（简洁）
读取tex正文，提取:
- method: 核心方法（1-2段话概括）
- problem: 解决的问题（1-2段话概括）
- results: 效果评估（1-2段话，包含关键数据、性能指标）

步骤5: 使用paper-summary-template skill
调用skill填充 templates/structured_analysis.md.j2，传入变量:
paper_id, title, authors, affiliation, method, problem, results
credibility_score, credibility_comment, importance_score, importance_comment, edge_value_score, edge_value_comment

步骤6: 写入输出
生成 knowledge/papers/$PAPER_ID.md 后退出。

重要: results控制在1-2段话内。'"

# 执行 opencode - 通过 stdin 传递完整任务
cd "$PROJECT_ROOT"
echo "$FULL_PROMPT" | opencode run \
    --model "$MODEL" \
    --title "paper-analysis-$PAPER_ID" \
    --format default

if [[ $? -ne 0 ]]; then
    log_error "opencode 执行失败"
    exit 1
fi

# 检查输出文件
OUTPUT_FILE="$PROJECT_ROOT/knowledge/papers/$PAPER_ID.md"

if [[ -f "$OUTPUT_FILE" ]]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    log_info "✅ 分析完成!"
    log_info "输出文件: $OUTPUT_FILE"
    log_info "文件大小: $FILE_SIZE"
    echo ""
    log_info "文件预览 (前20行):"
    head -20 "$OUTPUT_FILE"
    echo ""
    log_info "完整内容请查看: $OUTPUT_FILE"
else
    log_error "❌ 输出文件未生成: $OUTPUT_FILE"
    exit 1
fi
