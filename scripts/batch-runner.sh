#!/bin/bash
#
# batch-runner.sh - Batch process paper IDs with concurrency control
#
# Usage:
#   ./scripts/batch-runner.sh "id1 id2 id3"
#   ./scripts/batch-runner.sh --max-concurrent 8 "id1 id2 id3"
#   ./scripts/batch-runner.sh --model gpt-4 "id1 id2 id3"
#   ./scripts/batch-runner.sh --dry-run "id1 id2 id3"
#

set -euo pipefail

MAX_CONCURRENT=4
MODEL=""
DRY_RUN=false
PAPER_IDS=""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] "paper_ids..."

Batch process paper IDs with concurrency control.

OPTIONS:
    --max-concurrent N    Maximum concurrent jobs (default: 4)
    --model MODEL         Override default model for opencode
    --dry-run             Print commands without executing
    -h, --help            Show this help message

ARGUMENTS:
    paper_ids             Space-separated list of paper IDs

EXAMPLES:
    $(basename "$0") "id1 id2 id3"
    $(basename "$0") --max-concurrent 8 "id1 id2 id3"
    $(basename "$0") --model gpt-4 "id1 id2 id3"
    $(basename "$0") --dry-run "id1 id2 id3"
EOF
    exit 0
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --max-concurrent)
                MAX_CONCURRENT="$2"
                shift 2
                ;;
            --model)
                MODEL="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            -h|--help)
                usage
                ;;
            *)
                if [[ -z "$PAPER_IDS" ]]; then
                    PAPER_IDS="$1"
                else
                    log_error "Unknown argument: $1"
                    usage
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$PAPER_IDS" ]]; then
        log_error "Paper IDs are required"
        usage
    fi
}

get_workdir() {
    local paper_id="$1"
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    echo "/tmp/paper-${paper_id}-${timestamp}"
}

main() {
    parse_args "$@"

    read -ra PAPER_ID_ARRAY <<< "$PAPER_IDS"
    local total=${#PAPER_ID_ARRAY[@]}

    log_info "Starting batch processing: $total papers"
    log_info "Max concurrent: $MAX_CONCURRENT"
    [[ -n "$MODEL" ]] && log_info "Model: $MODEL"
    [[ "$DRY_RUN" == "true" ]] && log_info "DRY RUN MODE"

    echo ""

    local success_count=0
    local failed_count=0
    local -a pids=()

    for i in "${!PAPER_ID_ARRAY[@]}"; do
        local paper_id="${PAPER_ID_ARRAY[$i]}"
        local current=$((i + 1))

        while [[ ${#pids[@]} -ge $MAX_CONCURRENT ]]; do
            for idx in "${!pids[@]}"; do
                if ! kill -0 "${pids[$idx]}" 2>/dev/null; then
                    wait "${pids[$idx]}" 2>/dev/null || true
                    local exit_code=$?

                    if [[ $exit_code -eq 0 ]]; then
                        ((success_count++))
                    else
                        ((failed_count++))
                    fi

                    unset 'pids[idx]'
                fi
            done
            if [[ ${#pids[@]} -ge $MAX_CONCURRENT ]]; then
                sleep 0.5
            fi
        done

        echo -ne "\rProcessing $current/$total..."

        local workdir
        workdir=$(get_workdir "$paper_id")
        mkdir -p "$workdir"

        (
            if [[ "$DRY_RUN" == "true" ]]; then
                echo "[DRY-RUN] Would execute: ./scripts/read-paper.sh ${paper_id} ${workdir}"
                [[ -n "$MODEL" ]] && echo "[DRY-RUN] Model: --model $MODEL"
            else
                log_info "Processing paper: $paper_id (workdir: $workdir)"
                local cmd="./scripts/read-paper.sh \"${paper_id}\" \"${workdir}\""
                [[ -n "$MODEL" ]] && cmd="$cmd --model $MODEL"
                if eval "$cmd"; then
                    log_info "Success: $paper_id"
                else
                    log_error "Failed: $paper_id"
                    exit 1
                fi
            fi
        ) &
        pids+=($!)
    done

    echo -ne "\rProcessing $total/$total..."
    for pid in "${pids[@]:-}"; do
        wait "$pid" 2>/dev/null || true
        local exit_code=$?
        if [[ $exit_code -eq 0 ]]; then
            ((success_count++))
        else
            ((failed_count++))
        fi
    done

    echo ""
    echo ""

    log_info "Batch processing complete"
    echo "==================================="
    echo -e "${GREEN}Success: $success_count${NC}"
    echo -e "${RED}Failed:  $failed_count${NC}"
    echo "==================================="

    if [[ $failed_count -gt 0 ]]; then
        exit 1
    fi
    exit 0
}

main "$@"
