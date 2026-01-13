#!/usr/bin/env bash
# Session start hook for harness plugin - verifies plugin is loaded

LOG="/tmp/harness-hook-debug.log"
echo "[$(date)] Hook: harness SessionStart" >> "$LOG"

INPUT=$(cat)
echo "  Input (truncated): ${INPUT:0:200}..." >> "$LOG"
echo "[$(date)] harness plugin loaded successfully" >> "$LOG"
echo "---" >> "$LOG"

exit 0
