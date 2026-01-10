# Megatron MCP Server

MCP server plugin for Megatron semantic memory.

## Prerequisites

Install the `claude-memory` package:

```bash
pip install claude-memory
# or from source
pip install -e ~/workspace/claude-memory
```

## What This Does

Registers the Megatron MCP server which provides these tools to Claude:

- `memory_search` - Search semantic memory for past conversations
- `memory_resume` - Get context to continue where you left off
- `memory_remember` - Explicitly save something to memory
- `memory_sync` - Sync from latest transcript
- `memory_stats` - Get memory statistics

## Usage

Once installed, Claude will automatically have access to the memory tools.

For skills like `/recall` and `/resume`, also install the `megatron` plugin.
