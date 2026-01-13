# Fix MCP Server Memory Leak - Summary

## Overview

**Problem:** The `self.memories` dict in `EngramMCPServer` grew unbounded, accumulating `ProjectMemory` instances (each holding a ChromaDB client) without any cleanup.

**Solution:** LRU cache with max 5 projects using Python's `OrderedDict`.

---

## What Was Built

### Code Changes

| File | Change | Lines |
|------|--------|-------|
| `engram/mcp_server.py` | LRU cache implementation | +14 |

### Implementation Details

```python
from collections import OrderedDict

class EngramMCPServer:
    MAX_CACHED_PROJECTS = 5

    def __init__(self):
        self.memories: OrderedDict[str, ProjectMemory] = OrderedDict()

    def get_memory(self, project_path: str) -> ProjectMemory:
        if project_path in self.memories:
            self.memories.move_to_end(project_path)  # LRU: move to end
            return self.memories[project_path]

        memory = ProjectMemory(Path(project_path))
        self.memories[project_path] = memory

        while len(self.memories) > self.MAX_CACHED_PROJECTS:
            self.memories.popitem(last=False)  # Evict oldest

        return memory
```

---

## Test Results

| Test | Result |
|------|--------|
| Cache never exceeds 5 entries | ✅ PASS |
| LRU eviction order correct | ✅ PASS |
| MCP server works normally | ✅ PASS |
| MCP tools work correctly | ✅ PASS |

---

## Commits

```
ca0086a feat(fix-mcp-memory-leak): implement LRU cache for ProjectMemory
```

---

## Benefits

1. **Bounded memory:** Max 5 ProjectMemory instances regardless of projects accessed
2. **Predictable:** No more unbounded growth
3. **Efficient:** O(1) access and eviction with OrderedDict
4. **Simple:** 14 lines of code, no external dependencies
5. **Transparent:** No change to MCP tool behavior
