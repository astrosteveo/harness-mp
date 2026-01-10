---
name: resume
description: Resume work from where you left off. Use when user says "resume", "continue where we left off", "pick up where we left off", "what were we working on", or starts a new session and wants to continue previous work.
---

# Resume Previous Work

You are helping the user seamlessly continue their work from a previous session. The Megatron memory system has captured context from past sessions in this project.

## When This Skill Activates

- User says "resume" or "continue"
- User starts a new session and asks "where were we"
- User wants to pick up previous work

## What To Do

1. **Use the `mcp__megatron__memory_resume` tool** to get the resume context
2. **Analyze the context** which includes:
   - Last session timestamp
   - What was being worked on (in-progress tasks)
   - Active todos and their states
   - Recent plan files
   - Last few conversation exchanges
3. **Summarize for the user:**
   - "Last session you were working on X"
   - "You had these todos in progress: ..."
   - "The plan was to: ..."
   - "Want me to continue from there?"
4. **If there's a specific in-progress task**, offer to pick it up immediately.

## Available MCP Tools

- `mcp__megatron__memory_resume` - Get full resume context
- `mcp__megatron__memory_search` - Search for specific topics
- `mcp__megatron__memory_sync` - Manually sync from latest transcript
- `mcp__megatron__memory_stats` - Check memory stats

## Example Flow

**User:** resume

**You:**
1. Call `mcp__megatron__memory_resume`
2. Parse the output
3. Respond: "Welcome back! Last session (2 hours ago) you were implementing the user authentication system. You had 3/5 todos completed, with 'Add JWT refresh tokens' in progress. Want me to continue with that?"

## Notes

- Project memory is stored in `.megatron/` in the project root
- Each project has its own isolated memory
- The resume context is automatically available if the megatron-mcp plugin is installed
