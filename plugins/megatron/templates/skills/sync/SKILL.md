---
name: sync
description: Sync the current session to memory. Use when user says "save to memory", "sync memory", "index this session", or wants to ensure the current conversation is saved to the Megatron index.
---

# Sync Session to Memory

Manually trigger indexing of the current transcript into the Megatron memory index.

## When to Use

- Before starting a new session (to ensure current work is saved)
- After important decisions or breakthroughs
- When user explicitly wants to checkpoint their progress
- Before `/new` or closing the session

## What To Do

1. **Call `mcp__megatron__memory_sync`** to sync the current transcript
2. **Report the result** - how many chunks were indexed
3. **Optionally show stats** with `mcp__megatron__memory_stats`

## Example

**User:** `/megatron:sync`

**You:**
1. Call `mcp__megatron__memory_sync`
2. Respond: "Synced! Indexed 12 new exchanges to `.megatron/`. Your memory now has 156 total chunks."

## Notes

- Sync reads from the Claude transcript in `~/.claude/projects/`
- Only new/updated exchanges are indexed (upsert)
- Memory is project-local - stored in `.megatron/`
