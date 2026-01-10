#!/bin/bash
# Bootstrap harness plugin into current project's .claude/ directory

set -e

# Determine source directory (where this script lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$PLUGIN_DIR/templates"

# Target is current working directory's .claude/
TARGET_DIR="${PWD}/.claude"

echo "Bootstrapping harness plugin..."
echo "  Source: $TEMPLATES_DIR"
echo "  Target: $TARGET_DIR"

# Create target directories
mkdir -p "$TARGET_DIR/agents"
mkdir -p "$TARGET_DIR/skills"

# Copy agents
if [ -d "$TEMPLATES_DIR/agents" ]; then
    cp -r "$TEMPLATES_DIR/agents/"* "$TARGET_DIR/agents/" 2>/dev/null || true
    echo "  Copied agents"
fi

# Copy skills
if [ -d "$TEMPLATES_DIR/skills" ]; then
    cp -r "$TEMPLATES_DIR/skills/"* "$TARGET_DIR/skills/" 2>/dev/null || true
    echo "  Copied skills"
fi

# Summary
echo ""
echo "Installed:"
[ -d "$TARGET_DIR/agents" ] && echo "  Agents: $(find "$TARGET_DIR/agents" -name "*.md" -type f 2>/dev/null | wc -l)"
[ -d "$TARGET_DIR/skills" ] && echo "  Skills: $(find "$TARGET_DIR/skills" -name "SKILL.md" -type f 2>/dev/null | wc -l)"
echo ""
echo "Done. Skills should now appear as slash commands."
