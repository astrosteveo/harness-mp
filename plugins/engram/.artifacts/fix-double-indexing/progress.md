# Fix Double Indexing - Progress

## Status
Phase: 4 - Architecture Design (Complete)
Started: 2026-01-11
Last Updated: 2026-01-11

## Current State
- [x] Phase 1: Discovery
- [x] Phase 2: Codebase Exploration
- [x] Phase 3: Clarifying Questions
- [x] Phase 4: Architecture Design
- [ ] Phase 5: Implementation
- [ ] Phase 6: Quality Review
- [ ] Phase 7: Manual Testing Verification
- [ ] Phase 8: Summary

## Problem Statement
Content is being indexed twice in engram:
1. **Live indexing** via `live_indexer.py` on Stop hook events
2. **Batch sync** via CLI `engram sync` or during `engram init`

This causes:
- Duplicate chunks in ChromaDB with different IDs
- Noisy search results (same content appears multiple times)
- Wasted storage and embedding compute

## Root Causes Identified
1. Live indexer and batch sync use different ID generation schemes
2. No deduplication check before indexing
3. Marker files track line numbers, not message UUIDs
4. ChromaDB upserts only help if IDs match exactly

## Codebase Exploration Findings

### Key Patterns Discovered

- **Exchange-based chunking**: Both indexers group messages into user+assistant exchange pairs for semantic coherence
- **Upsert-based storage**: ChromaDB's `upsert()` is used which should deduplicate identical IDs, but ID schemes differ
- **Line-based progress tracking**: Live indexer uses marker files (`.indexed_{session_id}`) tracking line numbers
- **No progress tracking for batch sync**: Batch sync re-processes the entire transcript every time
- **Content prefixing**: All indexed content uses `User:` and `Assistant:` prefixes for role identification

### Relevant Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `/home/astrosteveo/workspace/marketplace/plugins/engram/engram/live_indexer.py` | Real-time indexing via Stop hook | Primary source of one ID scheme (`{session}:exchange:{uuid}`) |
| `/home/astrosteveo/workspace/marketplace/plugins/engram/engram/chunker.py` | Batch chunking logic | Primary source of other ID scheme (`{session}:{uuid}`) |
| `/home/astrosteveo/workspace/marketplace/plugins/engram/engram/project_memory.py` | ChromaDB storage layer | Where upsert happens, could add dedup logic |
| `/home/astrosteveo/workspace/marketplace/plugins/engram/engram/parser.py` | JSONL transcript parsing | Extracts Message objects with UUIDs |
| `/home/astrosteveo/workspace/marketplace/plugins/engram/engram/cli.py` | CLI commands (sync, init) | Entry points for batch indexing |
| `/home/astrosteveo/workspace/marketplace/plugins/engram/engram/mcp_server.py` | MCP tools (memory_sync) | Another batch sync entry point |
| `/home/astrosteveo/workspace/marketplace/plugins/engram/hooks/hooks.json` | Hook configuration | Triggers live indexing on Stop event |

### Architecture Notes

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          INDEXING ENTRY POINTS                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   LIVE INDEXING (Stop Hook)              BATCH INDEXING                 │
│   ┌──────────────────────┐               ┌──────────────────────┐       │
│   │ hooks.json           │               │ CLI: engram sync     │       │
│   │   ↓                  │               │ CLI: engram init     │       │
│   │ live-index.sh        │               │ MCP: memory_sync     │       │
│   │   ↓                  │               │   ↓                  │       │
│   │ live_indexer.py      │               │ project_memory.py    │       │
│   │   run_live_indexer() │               │   index_transcript() │       │
│   └──────────────────────┘               └──────────────────────┘       │
│             │                                      │                    │
│             ▼                                      ▼                    │
│   ┌──────────────────────┐               ┌──────────────────────┐       │
│   │ INLINE CHUNKING      │               │ parser.py            │       │
│   │ - Reads transcript   │               │   parse_transcript() │       │
│   │ - Skips indexed      │               │        ↓             │       │
│   │   lines (marker)     │               │ chunker.py           │       │
│   │ - Creates exchanges  │               │   chunk_by_exchange()│       │
│   └──────────────────────┘               └──────────────────────┘       │
│             │                                      │                    │
│             ▼                                      ▼                    │
│   ┌──────────────────────┐               ┌──────────────────────┐       │
│   │ ID FORMAT:           │               │ ID FORMAT:           │       │
│   │ {session}:exchange:  │               │ {session}:{uuid}     │       │
│   │   {first_uuid}       │               │                      │       │
│   │         OR           │               │                      │       │
│   │ {session}:partial:   │               │                      │       │
│   │   {first_uuid}       │               │                      │       │
│   └──────────────────────┘               └──────────────────────┘       │
│             │                                      │                    │
│             └──────────────┬───────────────────────┘                    │
│                            ▼                                            │
│                  ┌──────────────────────┐                               │
│                  │ project_memory.py    │                               │
│                  │   index_chunk()      │                               │
│                  │   collection.upsert()│                               │
│                  └──────────────────────┘                               │
│                            │                                            │
│                            ▼                                            │
│                  ┌──────────────────────┐                               │
│                  │ ChromaDB             │                               │
│                  │ .engram/index/       │                               │
│                  │                      │                               │
│                  │ PROBLEM: Different   │                               │
│                  │ IDs = Duplicate      │                               │
│                  │ documents for same   │                               │
│                  │ content!             │                               │
│                  └──────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### Integration Points

1. **ID Generation Unification**: The fix must happen in either:
   - `chunker.py:_create_chunk()` (line 96) - change to match live indexer format
   - `live_indexer.py` (lines 153, 175) - change to match batch format
   - Both should use the same deterministic ID scheme

2. **Deduplication Check**: Could be added in `project_memory.py:index_chunk()` before upsert

3. **Progress Tracking**: Batch sync could adopt live indexer's marker file approach

### Detailed ID Format Analysis

| Indexer | ID Pattern | Example | Location |
|---------|------------|---------|----------|
| Live (complete exchange) | `{session_id}:exchange:{first_uuid}` | `abc123:exchange:msg-001` | `live_indexer.py:153` |
| Live (partial exchange) | `{session_id}:partial:{first_uuid}` | `abc123:partial:msg-005` | `live_indexer.py:175` |
| Batch (chunker) | `{session_id}:{first_uuid}` | `abc123:msg-001` | `chunker.py:96` |

**Critical Issue**: Same content indexed via live and batch will have different IDs:
- Live: `abc123:exchange:msg-001`
- Batch: `abc123:msg-001`

### State Management Comparison

| Aspect | Live Indexer | Batch Sync |
|--------|--------------|------------|
| Progress tracking | `.indexed_{session_id}` marker files | None |
| What's tracked | Last line number indexed | N/A (re-indexes all) |
| Incremental | Yes (skips processed lines) | No (processes entire transcript) |
| Idempotency | Via line tracking + upsert | Via upsert only |

## Session Log
### Session 1 - 2026-01-11
- Started feature development
- Deep exploration of engram codebase completed
- Identified double indexing as highest priority issue
- Root causes: Different ID generation, no dedup, marker files track lines not UUIDs

### Session 2 - 2026-01-11
- Completed comprehensive codebase exploration with parallel agents
- Traced through both live indexing and batch sync flows completely
- Documented ID format mismatch as primary cause of double indexing
- Mapped all relevant files and integration points
- Created architecture diagram showing the dual indexing paths

### Session 3 - 2026-01-11
- Gathered requirements through clarifying questions
- Decisions made:
  - R1: Use live indexer ID format as canonical (`{session}:exchange:{uuid}`)
  - R2: Skip already-indexed content using shared marker files
  - R3: Delete partial chunks when exchange completes
  - R4: Provide `engram cleanup` command for migration
  - R5: Add optional debug logging for troubleshooting
- Documented requirements in requirements.md

### Session 4 - 2026-01-11
- Designed three architecture approaches:
  - A: Minimal (1 line change, no cleanup)
  - B: Full (all requirements, new module, logging)
  - C: Pragmatic (ID fix + cleanup command, ~45 lines)
- Selected Approach C as right-sized solution for bug fix
- Documented design in design.md
- Deferred: debug logging, partial cleanup, marker file sharing
