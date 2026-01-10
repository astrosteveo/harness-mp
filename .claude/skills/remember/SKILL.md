---
name: remember
description: Explicitly save something important to memory. Use when user says "remember this", "save this", "note this for later", or wants to explicitly store a decision, preference, or important context for future sessions.
---

# Remember Something Important

Explicitly save something to the Megatron memory index with high priority.

## When to Use

- Important decisions or architecture choices
- User preferences or patterns
- Key insights or breakthroughs
- Anything the user wants to persist across sessions

## What To Do

1. **Parse what the user wants to remember** from their message
2. **Call `mcp__megatron__memory_remember`** with the content and optional tags
3. **Confirm** what was saved

## Example

**User:** `/megatron:remember we decided to use JWT tokens with 15 minute expiry and refresh token rotation`

**You:**
1. Call `mcp__megatron__memory_remember` with content and tags like `["auth", "decision"]`
2. Respond: "Got it! Saved to memory: JWT tokens with 15 min expiry + refresh rotation. Tagged: auth, decision"

**User:** `/megatron:remember` (no content)

**You:** Ask what they'd like to remember.

## Parameters

- `content` - What to remember (required)
- `tags` - Optional categories for organization (e.g., "decision", "preference", "architecture")

## Notes

- Remembered items get higher retrieval priority
- Great for decisions, preferences, and key context
- Memory is project-local - stored in `.megatron/`
