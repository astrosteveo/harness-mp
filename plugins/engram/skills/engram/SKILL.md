---
name: engram:memory
description: Semantic memory for Claude Code - persistent context across sessions
---

# Engram - Semantic Memory

Persistent context across Claude Code sessions.

## MCP Tools

When this skill is active, you have access to the `engram` MCP server with these tools:

| Tool | Purpose |
|------|---------|
| `memory_search` | Semantic search across past sessions |
| `memory_resume` | Get context to continue previous work |
| `memory_remember` | Explicitly save important context |
| `memory_sync` | Index current session transcript |
| `memory_stats` | Check what's indexed |

## When to Use

- **Starting a session**: Use `memory_resume` to restore context from previous work
- **Mid-session**: Use `memory_search` to find relevant past discussions
- **Key decisions**: Use `memory_remember` to persist important context
- **Before ending**: Use `memory_sync` to ensure current session is indexed

## Commands

Slash commands are available at `/engram/*`:
- `/engram/resume` - Resume previous work
- `/engram/search <query>` - Search memory
- `/engram/remember <content>` - Save explicitly
- `/engram/sync` - Index current session
- `/engram/stats` - Show memory stats
