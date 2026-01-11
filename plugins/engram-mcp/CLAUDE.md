# Engram MCP Plugin

This is the Claude Code plugin configuration for [engram](https://github.com/astrosteveo/engram).

## What This Plugin Provides

- **MCP Server**: Semantic memory tools (search, resume, remember, sync, stats)
- **Commands**: `/engram/remember`, `/engram/resume`, `/engram/search`, `/engram/stats`, `/engram/sync`
- **Hooks**: Live indexing on conversation turns
- **Skill**: `using-engram` for guidance

## Installation

```bash
./install.sh /path/to/project
```

## The Actual Code

The engram library lives at: https://github.com/astrosteveo/engram

This plugin runs it via `uvx --from git+https://github.com/astrosteveo/engram`.

## Plugin Structure

```
engram-mcp/
├── .claude-plugin/plugin.json   # Plugin manifest
├── .mcp.json                    # MCP server config
├── commands/                    # Slash command documentation
├── skills/using-engram/         # Usage skill
├── hooks/hooks.json             # Live indexing hook
├── scripts/live-index.sh        # Hook script (uvx wrapper)
├── install.sh                   # Install to a project
└── uninstall.sh                 # Remove from a project
```
