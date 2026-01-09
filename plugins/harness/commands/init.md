---
description: Install harness skills and agents to your project
argument-hint: "[--force] [--dry-run] [--quiet]"
allowed-tools: Bash(bash:*)
---

Install the Harness toolkit - skills and agents for feature development workflows.

**Options:**
- `--force` or `-f`: Overwrite existing files without prompting
- `--dry-run` or `-n`: Preview what would be installed without making changes
- `--quiet` or `-q`: Minimal output

**What gets installed:**
- **Skills**: explore-codebase, feature-discovery, gather-requirements, design-architecture, implement-feature, verify-testing, review-code, summarize-feature, orchestrator, red-green-refactor
- **Agents**: code-explorer, code-architect, code-reviewer

Run: !`bash "${CLAUDE_PLUGIN_ROOT}/scripts/init.sh" $ARGUMENTS`
