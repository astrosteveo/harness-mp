---
description: Install plugin-dev skills and agents to your project
argument-hint: "[--force] [--dry-run] [--quiet]"
allowed-tools: Bash(bash:*)
---

Install the Plugin-Dev toolkit - skills, agents, and commands for building Claude Code plugins.

**Options:**
- `--force` or `-f`: Overwrite existing files without prompting
- `--dry-run` or `-n`: Preview what would be installed without making changes
- `--quiet` or `-q`: Minimal output

**What gets installed:**
- **Skills**: plugin-structure, hook-development, mcp-integration, lsp-integration, plugin-settings, command-development, agent-development, skill-development
- **Agents**: agent-creator, plugin-validator, skill-reviewer
- **Commands**: create-plugin

Run: !`bash "${CLAUDE_PLUGIN_ROOT}/scripts/init.sh" $ARGUMENTS`
