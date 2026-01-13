# Fix Double Indexing - Implementation Plan

## Status: Complete

## Changes Made

### 1. chunker.py (Line 96)

**Before:**
```python
id=f"{first_msg.session_id}:{first_msg.uuid}"
```

**After:**
```python
id=f"{first_msg.session_id}:exchange:{first_msg.uuid}"
```

This makes batch sync generate the same ID format as the live indexer.

---

### 2. project_memory.py (New method: cleanup_duplicates)

Added `cleanup_duplicates()` method to `ProjectMemory` class:

```python
def cleanup_duplicates(self) -> dict:
    """Remove duplicate chunks from old ID format."""
```

**Logic:**
1. Get all document IDs from ChromaDB
2. Group IDs by base form (without `exchange:` or `partial:` prefix)
3. For groups with both old and new format, delete the old format ID
4. Return stats: {removed, kept, scanned}

---

### 3. cli.py (New command: cleanup)

Added `engram cleanup` command:

```
Usage: engram cleanup [OPTIONS]

  Remove duplicate chunks from old ID format.

Options:
  -p, --project PATH
  --help              Show this message and exit.
```

---

## Files Changed

| File | Lines Added | Lines Removed | Net |
|------|-------------|---------------|-----|
| `engram/chunker.py` | 1 | 1 | 0 |
| `engram/project_memory.py` | 61 | 0 | +61 |
| `engram/cli.py` | 17 | 0 | +17 |
| **Total** | **79** | **1** | **+78** |

---

## Test Results

### ID Format Test
```
$ uv run python -c "..."
Chunk ID: sess-1:exchange:test-123
```

### CLI Test
```
$ uv run engram --help
Commands:
  cleanup   Remove duplicate chunks from old ID format.
  ...
```

### Cleanup Logic Test
```
Before cleanup: 2 chunks
Cleanup stats: {'removed': 1, 'kept': 1, 'scanned': 2}
After cleanup: 1 chunks
Remaining IDs: ['sess-1:exchange:msg-001']
```

---

## Commit

```
b7711df feat(fix-double-indexing): unify ID format and add cleanup command
```
