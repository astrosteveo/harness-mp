# Fix Double Indexing - Architecture Design

## Selected Approach: C (Pragmatic Balance)

**Rationale**: Right-sized solution for a bug fix. Provides migration path for existing duplicates without over-engineering.

---

## Changes Overview

| File | Lines | Change |
|------|-------|--------|
| `chunker.py` | ~1 | Update ID format to match live indexer |
| `project_memory.py` | ~25 | Add `cleanup_duplicates()` method |
| `cli.py` | ~20 | Add `engram cleanup` command |
| **Total** | **~46** | |

---

## Detailed Design

### 1. ID Format Fix (chunker.py)

**Current** (`chunker.py:96`):
```python
chunk_id = f"{first_msg.session_id}:{first_msg.uuid}"
```

**New**:
```python
chunk_id = f"{first_msg.session_id}:exchange:{first_msg.uuid}"
```

This matches the live indexer's format in `live_indexer.py:153`.

---

### 2. Cleanup Method (project_memory.py)

Add `cleanup_duplicates()` method to `ProjectMemory` class:

```python
def cleanup_duplicates(self) -> dict:
    """Remove duplicate chunks from old ID format.

    Returns dict with counts: {removed: int, kept: int}
    """
    # 1. Get all document IDs from collection
    # 2. Group by base ID (session:uuid suffix)
    # 3. For each group with multiple IDs:
    #    - Keep the one with 'exchange:' or 'partial:' prefix
    #    - Delete the one without prefix (old format)
    # 4. Return stats
```

**Logic**:
```
Old format: abc123:msg-001
New format: abc123:exchange:msg-001

Group by suffix after removing 'exchange:' or 'partial:':
  abc123:msg-001 -> base = "abc123:msg-001"
  abc123:exchange:msg-001 -> base = "abc123:msg-001"

If group has both old and new format, delete old.
```

---

### 3. CLI Command (cli.py)

Add `cleanup` command:

```python
@cli.command()
def cleanup():
    """Remove duplicate chunks from old ID format."""
    memory = ProjectMemory(Path.cwd())
    stats = memory.cleanup_duplicates()
    click.echo(f"Cleanup complete:")
    click.echo(f"  Removed: {stats['removed']} duplicate chunks")
    click.echo(f"  Kept: {stats['kept']} chunks")
```

---

## Implementation Order

1. **chunker.py** - ID format fix (prevents new duplicates)
2. **project_memory.py** - cleanup_duplicates() method
3. **cli.py** - engram cleanup command
4. **Test** - Verify fix works end-to-end

---

## Testing Strategy

### Unit Tests
- `test_chunk_id_format()` - Verify new ID format matches live indexer
- `test_cleanup_duplicates()` - Verify old format IDs are removed

### Integration Tests
- Index content via batch sync, verify ID format
- Create mock duplicates, run cleanup, verify removal
- Verify search results don't contain duplicates after cleanup

### Manual Testing
1. Run `engram sync` on a project with existing data
2. Run `engram cleanup`
3. Verify `engram stats` shows reduced chunk count
4. Verify `engram search` returns no duplicates

---

## Rollback Plan

If issues arise:
1. Revert chunker.py change (1 line)
2. Cleanup command is additive, no rollback needed
3. Existing data is preserved (cleanup only removes duplicates)

---

## Not Implementing (Deferred)

| Feature | Reason |
|---------|--------|
| Debug logging (R5) | Can add later if troubleshooting needed |
| Partial cleanup (R3) | Low impact - partials get overwritten by exchanges |
| Marker file sharing (R2) | Adds complexity, upsert handles most cases |
| id_generator.py module | Over-engineering for 1-line ID format |
