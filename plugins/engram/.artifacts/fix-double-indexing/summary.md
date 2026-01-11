# Fix Double Indexing - Summary

## Overview

**Problem:** Content was being indexed twice in Engram - once by the live indexer (Stop hook) and once by batch sync (`engram sync`). This created duplicate chunks in ChromaDB with different IDs, causing noisy search results.

**Root Cause:** Different ID generation schemes:
- Live indexer: `{session_id}:exchange:{uuid}`
- Batch sync: `{session_id}:{uuid}`

**Solution:** Unified ID format + cleanup command for migration.

---

## What Was Built

### Code Changes

| File | Change | Lines |
|------|--------|-------|
| `engram/chunker.py` | Updated `_create_chunk()` ID format | +0 (modified) |
| `engram/project_memory.py` | Added `cleanup_duplicates()` method | +61 |
| `engram/cli.py` | Added `engram cleanup` command | +17 |
| **Total** | | **+78 lines** |

### New CLI Command

```bash
engram cleanup [-p PROJECT]
```

Removes duplicate chunks created by the old ID format mismatch.

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Canonical ID format | Live indexer format | More descriptive, primary indexing path |
| Approach | C (Pragmatic) | Right-sized for bug fix, ~80 lines |
| Migration | Explicit cleanup command | User-controlled, opt-in |
| Deferred | Debug logging, partial cleanup | Avoid over-engineering |

---

## Test Results

### Unit Tests
- New chunk ID format: `test-session:exchange:msg-001` ✅
- Cleanup removes old format duplicates ✅
- Upsert prevents new duplicates ✅

### Integration Tests (Live Project)
- `engram sync` after live indexing: 0 duplicates created ✅
- `engram search`: Relevant results, scores 0.59-0.73 ✅

---

## Usage

### For New Users
No action needed - the fix prevents duplicates automatically.

### For Existing Users with Duplicates
```bash
# Check current state
engram stats

# Remove duplicates from old ID format
engram cleanup

# Verify
engram stats
```

---

## Known Limitations

1. **Session IDs with colons**: If a session_id contains colons (unlikely), the cleanup ID parsing may not correctly identify duplicates. This is a theoretical edge case - Claude Code session IDs are typically UUIDs.

---

## Commits

```
b7711df feat(fix-double-indexing): unify ID format and add cleanup command
c2f3e1e docs(fix-double-indexing): update progress and add implementation plan
899b567 docs(fix-double-indexing): complete code review
a5869f9 docs(fix-double-indexing): complete manual testing verification
008cae8 docs(fix-double-indexing): add integration test results
```

---

## Lessons Learned

1. **Right-size the solution**: Started with 5 requirements, implemented 2 core ones. The others (debug logging, marker file sharing) weren't needed for the fix.

2. **Leverage existing behavior**: ChromaDB's `upsert()` handles deduplication when IDs match - no need for complex dedup logic.

3. **Automate what can be automated**: Manual testing checklist was converted to automated integration tests.

---

## Future Improvements (If Needed)

- Add debug logging for troubleshooting indexing issues
- Handle session IDs with colons in cleanup logic
- Add `--dry-run` flag to cleanup command
