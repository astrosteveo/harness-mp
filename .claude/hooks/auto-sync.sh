#!/bin/bash
# Auto-sync memory on Stop event

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

input=$(cat)
cwd=$(echo "$input" | jq -r '.cwd // empty')
[[ -z "$cwd" ]] && cwd="$PROJECT_DIR"

cd "$PROJECT_DIR/.claude/megatron"
uv run megatron sync --project "$cwd" >/dev/null 2>&1 || true

exit 0
