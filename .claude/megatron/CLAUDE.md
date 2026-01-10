# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Megatron is a semantic memory system for Claude Code. It indexes conversation transcripts from `~/.claude/projects/` into project-local vector databases, enabling context persistence across sessions.

## Commands

```bash
# Setup (in project root)
uv sync

# Run MCP server (for Claude Code integration)
uv run megatron-mcp

# CLI commands (for manual use)
uv run megatron init                    # Initialize project memory
uv run megatron sync                    # Sync from latest transcript
uv run megatron project-search "query"  # Search project memory
uv run megatron resume                  # Get resume context
uv run megatron project-stats           # Show memory stats
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

## Docker

Build and run:

```bash
docker build -t megatron .
docker run -i --rm -v $(pwd):/workspace -v ~/.claude:/root/.claude megatron
```

The MCP server uses stdio JSON-RPC protocol (MCP 2024-11-05).
