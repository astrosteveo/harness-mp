#!/usr/bin/env bash
# Live indexer - runs engram-live-index from GitHub via uvx

# Debug logging
LOG="/tmp/engram-hook-debug.log"
echo "[$(date)] Stop hook triggered" >> "$LOG"
echo "  CLAUDE_PLUGIN_ROOT=${CLAUDE_PLUGIN_ROOT:-unset}" >> "$LOG"
echo "  PWD=$PWD" >> "$LOG"

# Capture stdin for debugging
INPUT=$(cat)
echo "  Input: $INPUT" >> "$LOG"

# Run the indexer
echo "$INPUT" | uvx --from git+https://github.com/astrosteveo/engram engram-live-index 2>> "$LOG"
EXIT_CODE=$?

echo "[$(date)] Hook completed with exit code $EXIT_CODE" >> "$LOG"
echo "---" >> "$LOG"

# Output continue response
echo '{"continue": true}'
