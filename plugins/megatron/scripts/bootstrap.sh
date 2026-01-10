#!/bin/bash
# Bootstrap megatron into current project's .claude/ directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$PLUGIN_DIR/templates"
TARGET_DIR="${PWD}/.claude"

echo "Bootstrapping megatron..."

# Create directories
mkdir -p "$TARGET_DIR/skills"
mkdir -p "$TARGET_DIR/hooks"

# Copy skills
cp -r "$TEMPLATES_DIR/skills/"* "$TARGET_DIR/skills/" 2>/dev/null || true
echo "  Copied skills"

# Copy hooks
cp -r "$TEMPLATES_DIR/hooks/"* "$TARGET_DIR/hooks/" 2>/dev/null || true
chmod +x "$TARGET_DIR/hooks/"*.sh 2>/dev/null || true
echo "  Copied hooks"

# MCP config
if [ -f "${PWD}/.mcp.json" ]; then
    echo "  .mcp.json exists - add megatron config manually if needed"
else
    cat > "${PWD}/.mcp.json" << 'EOF'
{
  "mcpServers": {
    "megatron-mcp": {
      "command": "uvx",
      "args": ["megatron-mcp"]
    }
  }
}
EOF
    echo "  Created .mcp.json"
fi

echo ""
echo "Done. Restart Claude Code."
