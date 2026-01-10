---
description: Bootstrap megatron skills into the project's .claude directory
argument-hint: <none>
allowed-tools: ["Bash"]
---

# Bootstrap Megatron Plugin

Run the bootstrap script to copy megatron templates into this project's `.claude/` directory.

```bash
!bash "${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap.sh"
```

Report the output to the user.

Note: The MCP server and hooks remain loaded from the plugin. This only copies skills so they appear as slash commands.
