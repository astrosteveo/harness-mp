# Engram Roadmap

## Completed Features

### fix-double-indexing (2026-01-11)
Fixed double indexing bug where content was indexed twice by live indexer and batch sync with different ID formats. Unified ID generation and added `engram cleanup` migration command.

**Files changed**: `chunker.py`, `project_memory.py`, `cli.py`

---

## Planned Features

### debug-logging
Add optional verbose logging for troubleshooting indexing decisions.
- Show what's being indexed, skipped, and deduplicated
- Use Python logging with configurable level
- Output to stderr or `.engram/debug.log`

*Deferred from fix-double-indexing (R5)*

### marker-file-sharing
Share marker files between live and batch indexers for more efficient incremental syncing.
- Batch sync reads marker files and starts from last indexed line
- Avoid re-processing content already indexed by live indexer

*Deferred from fix-double-indexing (R2)*

### partial-chunk-cleanup
Explicitly delete partial chunks when exchange completes.
- Track pending partials in live indexer
- Clean up `{session}:partial:{uuid}` when `{session}:exchange:{uuid}` is created

*Deferred from fix-double-indexing (R3)*

### enhanced-stats
Improve `engram stats` command with more detailed information.
- Show duplicate detection results
- Display chunk counts by session
- Show index health metrics

---

## Future Ideas

- Cross-project memory querying
- Configurable embedding models
- Memory pruning/aging strategies
- Export/import memory between machines
