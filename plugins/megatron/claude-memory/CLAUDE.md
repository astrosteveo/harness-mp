# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Megatron is a semantic memory system for Claude Code. It indexes conversation transcripts from `~/.claude/projects/` into project-local vector databases, enabling context persistence across sessions.

## Commands

```bash
# Setup (in project root)
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run MCP server (for Claude Code integration)
python -m claude_memory.mcp_server

# CLI commands (for manual use)
claude-memory init                    # Initialize project memory
claude-memory sync                    # Sync from latest transcript
claude-memory project-search "query"  # Search project memory
claude-memory resume                  # Get resume context
claude-memory project-stats           # Show memory stats
```

## Architecture

```
MCP Server (mcp_server.py)
    │
    ├── memory_search    ─┐
    ├── memory_resume     │
    ├── memory_remember   ├── Tools exposed to Claude
    ├── memory_sync       │
    └── memory_stats     ─┘
            │
            ▼
ProjectMemory (project_memory.py)
    │
    ├── ChromaDB (per-project in .megatron/)
    ├── SessionState snapshots (state.json)
    └── Transcript parsing
            │
            ▼
Parser (parser.py) ──► Chunker (chunker.py)
    │                       │
    │ Reads JSONL           │ Groups into
    │ transcripts           │ user-assistant
    │ from ~/.claude/       │ exchanges
    └───────────────────────┘
```

**Data Flow:**
1. Parser reads Claude Code JSONL transcripts from `~/.claude/projects/`
2. Chunker groups messages into user-assistant exchanges (max 2000 chars)
3. ProjectMemory indexes chunks into ChromaDB with cosine similarity
4. MCP Server exposes query/remember/sync tools to Claude

**Storage:**
- Project memory: `<project>/.megatron/index/` (ChromaDB)
- Session state: `<project>/.megatron/state.json`
- Transcripts found by encoding project path (e.g., `/home/user/project` → `-home-user-project`)

## Installation

```bash
# Clone the repo
git clone <repo-url> ~/workspace/claude-memory
cd ~/workspace/claude-memory

# Set up venv and install
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

This installs:
- `claude-memory` - CLI tool
- `megatron-mcp` - MCP server entry point

## Claude Code Integration

Install the plugins from harness-mp:

1. **`megatron-mcp`** - Registers the MCP server (provides tools to Claude)
2. **`megatron`** - Adds `/recall` and `/resume` skills

The MCP server uses stdio JSON-RPC protocol (MCP 2024-11-05).
