# Marketplace

Curated Claude Code plugins for development workflows and memory.

## Plugins

| Plugin | Description | Repo |
|--------|-------------|------|
| **harness** | Agentic skills framework & development methodology | [astrosteveo/harness](https://github.com/astrosteveo/harness) |
| **engram** | Semantic memory - persistent context across sessions | [astrosteveo/engram](https://github.com/astrosteveo/engram) |
| **hookify** | Create custom hooks via markdown - no coding required | [astrosteveo/hookify](https://github.com/astrosteveo/hookify) |

## Installation

```bash
# Add marketplace
/plugin marketplace add astrosteveo/marketplace

# Install plugins
/plugin install harness@astrosteveo/marketplace
/plugin install engram@astrosteveo/marketplace
/plugin install hookify@astrosteveo/marketplace
```

## Plugin Details

### harness

Agentic skills framework with 15+ skills:
- Development workflow (brainstorming, planning, TDD, code review)
- Project tracking (GitHub issues → .artifacts/ → archive)
- Collaboration patterns (subagents, parallel agents)

### engram

MCP server for semantic memory:
- Indexes Claude Code conversation transcripts
- Hybrid search (semantic + BM25)
- `resume` to pick up where you left off

Requires: `uv tool install engram-mcp` + `engram init` in your project

### hookify

Create custom hooks without coding:
- Markdown configuration files with YAML frontmatter
- Regex pattern matching
- Analyze conversations to find unwanted behaviors
