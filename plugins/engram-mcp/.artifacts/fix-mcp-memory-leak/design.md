# Fix MCP Server Memory Leak - Design

## Selected Approach: Manual LRU with OrderedDict

Python's `functools.lru_cache` works with functions, not instance methods that need `self`. 
A simple `OrderedDict`-based LRU is clean and requires minimal code.

## Implementation

```python
from collections import OrderedDict

class EngramMCPServer:
    MAX_CACHED_PROJECTS = 5

    def __init__(self):
        self.memories: OrderedDict[str, ProjectMemory] = OrderedDict()

    def get_memory(self, project_path: str) -> ProjectMemory:
        """Get or create memory for a project (LRU cached)."""
        if project_path in self.memories:
            # Move to end (most recently used)
            self.memories.move_to_end(project_path)
            return self.memories[project_path]
        
        # Create new instance
        memory = ProjectMemory(Path(project_path))
        self.memories[project_path] = memory
        
        # Evict oldest if over limit
        while len(self.memories) > self.MAX_CACHED_PROJECTS:
            self.memories.popitem(last=False)  # Remove oldest (first)
        
        return memory
```

## Changes

| File | Change | Lines |
|------|--------|-------|
| `mcp_server.py` | Replace dict with OrderedDict + LRU logic | ~10 |

## Why This Approach

1. **Simple:** ~10 lines of code
2. **No dependencies:** Uses stdlib `OrderedDict`
3. **Predictable:** Exactly 5 projects max
4. **Efficient:** O(1) for access and eviction
5. **Transparent:** No change to tool behavior

## Alternative Considered: functools.lru_cache

Could use `@lru_cache` on a module-level function, but:
- Awkward to integrate with instance methods
- Less control over eviction timing
- Harder to test

## Testing Strategy

1. Unit test: Verify cache never exceeds 5 entries
2. Unit test: Verify LRU eviction order
3. Integration test: Verify MCP tools still work correctly
