---
name: recall
description: Search semantic memory from past Claude Code sessions. Use when user asks "what do I remember about X", "recall conversations about Y", "search my memory for Z", or wants to find past context about a topic.
---

# Semantic Memory Recall

You are helping the user search and explore their semantic memory - a database of all their past Claude Code conversations, indexed for semantic retrieval.

## How to Use This Skill

When the user invokes `/megatron:recall` with a query (or asks you to remember/megatron:recall something):

1. **Use the `mcp__megatron__memory_search` tool** with the user's query
2. **Analyze and summarize** the results:
   - What topics/projects were discussed
   - Key decisions or solutions found
   - Relevant code patterns or architectures
3. **Offer to dig deeper** if needed - search with different queries or look at related context

## Example Interactions

**User:** `/megatron:recall authentication system`

**You:** Search for authentication-related conversations using `mcp__megatron__memory_search`, then summarize what was discussed, decisions made, and any code patterns used.

**User:** `/megatron:recall` (no query)

**You:** Ask what they'd like to remember, or use `mcp__megatron__memory_stats` to show what's indexed.

**User:** "What do we remember about the API refactor?"

**You:** Search for API refactor context and provide a synthesized summary.

## Available MCP Tools

- `mcp__megatron__memory_search` - Search with a semantic query
- `mcp__megatron__memory_stats` - Show index statistics
- `mcp__megatron__memory_remember` - Explicitly save something important

## Notes

- Results include relevance scores (higher is more relevant)
- Memory is project-local - stored in `.megatron/` in each project
- The search is semantic, not keyword-exact
