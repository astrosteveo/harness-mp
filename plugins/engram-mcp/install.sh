#!/bin/bash
# Install engram-mcp plugin to a target project
#
# Usage: ./install.sh [target_directory]
#        ./install.sh              # installs to current directory
#        ./install.sh /path/to/project

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "Installing engram-mcp to: $TARGET_DIR"

# Create directories
mkdir -p "$TARGET_DIR/.claude/commands/engram"
mkdir -p "$TARGET_DIR/.claude/skills/engram"
mkdir -p "$TARGET_DIR/.claude/hooks"

# Copy commands
echo "  Copying commands..."
cp "$SCRIPT_DIR/commands/"*.md "$TARGET_DIR/.claude/commands/engram/"

# Copy skill
echo "  Copying skill..."
cp "$SCRIPT_DIR/skills/using-engram/SKILL.md" "$TARGET_DIR/.claude/skills/engram/"

# Copy hooks
echo "  Copying hooks..."
cp "$SCRIPT_DIR/hooks/hooks.json" "$TARGET_DIR/.claude/hooks/engram-hooks.json"
mkdir -p "$TARGET_DIR/.claude/scripts"
cp "$SCRIPT_DIR/scripts/live-index.sh" "$TARGET_DIR/.claude/scripts/"

# Set up MCP config
MCP_FILE="$TARGET_DIR/.mcp.json"
if [ -f "$MCP_FILE" ]; then
    if grep -q '"engram"' "$MCP_FILE" 2>/dev/null; then
        echo "  MCP: engram already configured"
    else
        echo "  MCP: Adding engram to .mcp.json"
        python3 -c "
import json
with open('$MCP_FILE') as f:
    config = json.load(f)
config.setdefault('mcpServers', {})['engram'] = {
    'command': 'uvx',
    'args': ['--from', 'git+https://github.com/astrosteveo/engram', 'engram-mcp']
}
with open('$MCP_FILE', 'w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')
"
    fi
else
    echo "  MCP: Creating .mcp.json"
    cat > "$MCP_FILE" << 'EOF'
{
  "mcpServers": {
    "engram": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/astrosteveo/engram", "engram-mcp"]
    }
  }
}
EOF
fi

# Add .engram/ to .gitignore
GITIGNORE="$TARGET_DIR/.gitignore"
if [ -f "$GITIGNORE" ]; then
    if ! grep -q "^\.engram/" "$GITIGNORE" 2>/dev/null; then
        echo -e "\n# Engram memory\n.engram/" >> "$GITIGNORE"
        echo "  Added .engram/ to .gitignore"
    fi
fi

echo ""
echo "Done! Restart Claude Code to enable engram."
