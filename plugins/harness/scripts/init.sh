#!/bin/bash
set -e

DEST="$CLAUDE_PROJECT_DIR/.claude"

mkdir -p "$DEST/skills" "$DEST/agents"

cp -r "${CLAUDE_PLUGIN_ROOT}/templates/skills/"* "$DEST/skills/"
cp -r "${CLAUDE_PLUGIN_ROOT}/templates/agents/"* "$DEST/agents/"

echo "=== Installed Skills ==="
ls -1 "$DEST/skills/"
echo ""
echo "=== Installed Agents ==="
ls -1 "$DEST/agents/"
echo ""
echo "Harness installed to .claude/ - skills and agents are now available."
