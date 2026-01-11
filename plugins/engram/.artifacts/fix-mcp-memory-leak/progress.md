# Fix MCP Server Memory Leak - Progress

## Status
Phase: COMPLETE
Started: 2026-01-11
Completed: 2026-01-11

## Current State
- [x] Phase 1: Discovery
- [x] Phase 2: Codebase Exploration (skipped - already explored)
- [x] Phase 3: Clarifying Questions
- [x] Phase 4: Architecture Design
- [x] Phase 5: Implementation
- [x] Phase 6: Quality Review
- [x] Phase 7: Testing Verification
- [x] Phase 8: Summary

## Problem Statement

The `EngramMCPServer` class in `mcp_server.py` has a memory leak:

```python
class EngramMCPServer:
    def __init__(self):
        self.memories: dict[str, ProjectMemory] = {}  # Grows unbounded!

    def get_memory(self, project_path: str) -> ProjectMemory:
        if project_path not in self.memories:
            self.memories[project_path] = ProjectMemory(Path(project_path))
        return self.memories[project_path]
```

**Issues:**
1. `self.memories` dict accumulates ProjectMemory instances forever
2. Each ProjectMemory holds a ChromaDB client (file handles, connections)
3. No cleanup mechanism - nothing ever removes entries
4. Long-running servers could exhaust file descriptors

## Session Log
### Session 1 - 2026-01-11
- Started feature development
- Initial request: Fix MCP server memory leak - self.memories dict grows unbounded
- Identified root cause in mcp_server.py lines 19-26
- Skipped codebase exploration (already done during fix-double-indexing)
- Requirements gathered:
  - R1: LRU cache for ProjectMemory instances
  - R2: Max 5 projects cached
- Design selected: Manual LRU with OrderedDict (~10 lines)
- Implemented LRU cache in mcp_server.py:
  - Added OrderedDict import
  - Added MAX_CACHED_PROJECTS = 5 constant
  - Updated get_memory() with LRU logic
- All tests PASSED:
  - Test 1: Cache size limit (never exceeds 5) ✓
  - Test 2: LRU eviction order (recently used kept) ✓
  - Test 3: MCP server still works ✓
  - Integration: MCP tools work correctly ✓
- Committed: feat(fix-mcp-memory-leak): implement LRU cache for ProjectMemory
