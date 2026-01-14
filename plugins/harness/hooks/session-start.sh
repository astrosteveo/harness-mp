#!/usr/bin/env bash
# SessionStart hook for harness plugin

set -euo pipefail

# Determine plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Check if legacy skills directory exists and build warning
warning_message=""
legacy_skills_dir="${HOME}/.config/harness/skills"
if [ -d "$legacy_skills_dir" ]; then
    warning_message="\n\n<important-reminder>IN YOUR FIRST REPLY AFTER SEEING THIS MESSAGE YOU MUST TELL THE USER:⚠️ **WARNING:** Harness now uses Claude Code's skills system. Custom skills in ~/.config/harness/skills will not be read. Move custom skills to ~/.claude/skills instead. To make this message go away, remove ~/.config/harness/skills</important-reminder>"
fi

# Read using-harness content
using_harness_content=$(cat "${PLUGIN_ROOT}/skills/using-harness/SKILL.md" 2>&1 || echo "Error reading using-harness skill")

# Escape outputs for JSON using pure bash
escape_for_json() {
    local input="$1"
    local output=""
    local i char
    for (( i=0; i<${#input}; i++ )); do
        char="${input:$i:1}"
        case "$char" in
            $'\\') output+='\\' ;;
            '"') output+='\"' ;;
            $'\n') output+='\n' ;;
            $'\r') output+='\r' ;;
            $'\t') output+='\t' ;;
            *) output+="$char" ;;
        esac
    done
    printf '%s' "$output"
}

using_harness_escaped=$(escape_for_json "$using_harness_content")
warning_escaped=$(escape_for_json "$warning_message")

# Output context injection as JSON
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have harness.\n\n**Below is the full content of your 'harness:using-harness' skill - your introduction to using skills. For all other skills, use the 'Skill' tool:**\n\n${using_harness_escaped}\n\n${warning_escaped}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF

exit 0
