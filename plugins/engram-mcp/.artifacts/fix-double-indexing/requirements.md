# Fix Double Indexing - Requirements

## Problem Statement

Content is being indexed twice in engram:
1. **Live indexing** via `live_indexer.py` on Stop hook events
2. **Batch sync** via CLI `engram sync` or during `engram init`

This causes duplicate chunks in ChromaDB with different IDs, resulting in noisy search results and wasted storage.

## Root Cause

The two indexing paths use different ID generation schemes:
- Live indexer: `{session_id}:exchange:{first_uuid}` or `{session_id}:partial:{first_uuid}`
- Batch sync (chunker.py): `{session_id}:{first_uuid}`

ChromaDB's `upsert()` cannot deduplicate because the IDs differ.

---

## Requirements

### R1: Unified ID Format
- **Decision:** Use live indexer format as canonical
- **Format:** `{session_id}:exchange:{first_uuid}` for complete exchanges, `{session_id}:partial:{first_uuid}` for incomplete
- **Change:** Update `chunker.py` to generate IDs matching live indexer format

### R2: Skip Already-Indexed Content
- **Decision:** Batch sync should skip content already indexed by live indexer
- **Mechanism:** Share marker files between live and batch indexers
- **Files:** `.engram/.indexed_{session_id}` marker files track last indexed line number
- **Behavior:** Batch sync reads marker files and starts from last indexed line

### R3: Partial Exchange Cleanup
- **Decision:** Delete partial chunks when exchange completes
- **Behavior:** When assistant response arrives, delete `{session}:partial:{uuid}` and create `{session}:exchange:{uuid}`
- **Implementation:** Live indexer tracks pending partials and cleans up on completion

### R4: Migration/Cleanup Tool
- **Decision:** Provide explicit cleanup command
- **Command:** `engram cleanup` or `engram dedupe`
- **Function:** Detect and remove duplicate chunks from existing indexes
- **Scope:** Handle both old ID format duplicates and any partial/exchange overlaps

### R5: Debug Logging
- **Decision:** Add optional verbose logging
- **Purpose:** Track what's being indexed, skipped, and deduplicated
- **Implementation:** Use Python logging with configurable level
- **Output:** Log to stderr or `.engram/debug.log`

---

## Non-Requirements (Out of Scope)

- Cross-project memory querying
- Configurable embedding models
- Auto-cleanup on every sync (too slow)
- Enhanced stats command (nice-to-have, not this iteration)

---

## Success Criteria

1. Same content indexed via live and batch produces identical ChromaDB document IDs
2. Running `engram sync` after live indexing does not create duplicates
3. `engram cleanup` removes existing duplicates from indexes
4. Debug logging shows indexing decisions when enabled
5. No regression in search quality or performance

---

## Files to Modify

| File | Changes |
|------|---------|
| `chunker.py` | Update `_create_chunk()` ID format to match live indexer |
| `live_indexer.py` | Add partial cleanup logic, integrate marker file sharing |
| `project_memory.py` | Add `cleanup_duplicates()` method |
| `cli.py` | Add `engram cleanup` command, add debug logging setup |

## New Files

| File | Purpose |
|------|---------|
| (none expected) | All changes fit in existing modules |
