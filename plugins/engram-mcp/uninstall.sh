#!/bin/bash
# Uninstall engram-mcp plugin from a target project
#
# Usage: ./uninstall.sh [target_directory]
#        ./uninstall.sh              # uninstalls from current directory
#        ./uninstall.sh /path/to/project

set -e

TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "Uninstalling engram-mcp from: $TARGET_DIR"

# Remove commands
CMD_DIR="$TARGET_DIR/.claude/commands/engram"
if [ -d "$CMD_DIR" ]; then
    rm -rf "$CMD_DIR"
    echo "  Removed: .claude/commands/engram/"
fi

# Remove skill
SKILL_DIR="$TARGET_DIR/.claude/skills/engram"
if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    echo "  Removed: .claude/skills/engram/"
fi

# Remove hooks
HOOKS_FILE="$TARGET_DIR/.claude/hooks/engram-hooks.json"
if [ -f "$HOOKS_FILE" ]; then
    rm -f "$HOOKS_FILE"
    echo "  Removed: .claude/hooks/engram-hooks.json"
fi

SCRIPT_FILE="$TARGET_DIR/.claude/scripts/live-index.sh"
if [ -f "$SCRIPT_FILE" ]; then
    rm -f "$SCRIPT_FILE"
    echo "  Removed: .claude/scripts/live-index.sh"
fi

# Remove from MCP config
MCP_FILE="$TARGET_DIR/.mcp.json"
if [ -f "$MCP_FILE" ] && grep -q '"engram"' "$MCP_FILE" 2>/dev/null; then
    echo "  Removing engram from .mcp.json"
    python3 -c "
import json
with open('$MCP_FILE') as f:
    config = json.load(f)
if 'mcpServers' in config and 'engram' in config['mcpServers']:
    del config['mcpServers']['engram']
with open('$MCP_FILE', 'w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')
"
fi

echo ""
echo "Note: .engram/ directory preserved (contains your memory data)"
echo "      Delete manually if no longer needed: rm -rf $TARGET_DIR/.engram"
echo ""
echo "Done!"
