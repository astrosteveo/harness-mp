---
name: stats
description: Show memory statistics. Use when user asks "how much is indexed", "memory stats", "what's in memory", or wants to see the state of their Megatron memory index.
---

# Memory Statistics

Show statistics about the Megatron memory index for the current project.

## When to Use

- User wants to know what's indexed
- Checking if memory is working
- Debugging memory issues
- General curiosity about memory state

## What To Do

1. **Call `mcp__megatron__memory_stats`**
2. **Present the stats** in a readable format

## Example

**User:** `/megatron:stats`

**You:**
1. Call `mcp__megatron__memory_stats`
2. Respond with formatted stats:
   ```
   Megatron Memory Stats
   ─────────────────────
   Project: /home/user/my-project
   Indexed: 156 chunks
   Storage: .megatron/
   ```

## Stats Returned

- `project` - The project path
- `total_chunks` - Number of indexed conversation exchanges
- `memory_path` - Where the index is stored

## Notes

- Each chunk is roughly one user-assistant exchange
- Memory is project-local
- Use `/megatron:sync` to update the index
