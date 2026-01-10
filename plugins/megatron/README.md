# Megatron - Semantic Memory for Claude Code

Carry context across sessions with the **Vectorized Super Megatron Max 5000**.

## What It Does

When you're mid-task and context fills up, just `/new` or start a fresh session:

```
> resume
```

And everything is there - what you were working on, your todos, your progress.

## Skills

- `/recall <query>` - Search your semantic memory for past conversations
- `/resume` - Get context to continue where you left off

## Prerequisites

Install the `claude-memory` package:

```bash
pip install claude-memory
# or from source
pip install -e ~/workspace/claude-memory
```

This plugin auto-registers the MCP server when installed.

## How It Works

1. Every conversation exchange gets indexed to a project-local ChromaDB
2. When you start a new session, the memory is ready to query
3. Semantic search finds relevant context from your history
4. You pick up right where you left off

## The Flow

```
Working on feature...
├─ Every exchange → indexed to .claude-memory/
├─ Todos, plan files, decisions → all captured
│
├─ "oh shit context full"
├─ /new
│
└─ "resume"
    ↓
    Claude instantly sees:
    - Last session state
    - What was being worked on
    - Active todos
    - Recent exchanges
```

No more lost context. No more re-explaining. Just seamless continuation.
