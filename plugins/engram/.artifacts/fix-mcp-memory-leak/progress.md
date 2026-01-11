# Fix MCP Server Memory Leak - Progress

## Status
Phase: 1 - Discovery
Started: 2026-01-11
Last Updated: 2026-01-11

## Current State
- [x] Phase 1: Discovery
- [ ] Phase 2: Codebase Exploration
- [ ] Phase 3: Clarifying Questions
- [ ] Phase 4: Architecture Design
- [ ] Phase 5: Implementation
- [ ] Phase 6: Quality Review
- [ ] Phase 7: Manual Testing Verification
- [ ] Phase 8: Summary

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
