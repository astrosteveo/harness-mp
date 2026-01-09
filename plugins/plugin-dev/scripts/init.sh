#!/bin/bash
set -e

DEST="$CLAUDE_PROJECT_DIR/.claude"

mkdir -p "$DEST/skills" "$DEST/agents" "$DEST/commands"

cp -r "${CLAUDE_PLUGIN_ROOT}/templates/skills/"* "$DEST/skills/"
cp -r "${CLAUDE_PLUGIN_ROOT}/templates/agents/"* "$DEST/agents/"
cp -r "${CLAUDE_PLUGIN_ROOT}/templates/commands/"* "$DEST/commands/"

echo "=== Installed Skills ==="
ls -1 "$DEST/skills/"
echo ""
echo "=== Installed Agents ==="
ls -1 "$DEST/agents/"
echo ""
echo "=== Installed Commands ==="
ls -1 "$DEST/commands/"
echo ""
echo "plugin-dev installed to .claude/ - skills, agents, and commands are now available."
