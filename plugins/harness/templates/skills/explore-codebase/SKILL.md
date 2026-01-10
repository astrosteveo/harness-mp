---
name: harness:explore-codebase
description: Deep exploration of codebase to understand patterns, architecture, and relevant code for a feature. Launches parallel exploration agents and synthesizes findings. Use after feature discovery or when you need to understand how existing code works.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task
context: fork
---

# Explore Codebase

You are helping a developer understand the codebase in depth before implementing a feature.

**Progress is saved to `.artifacts/{feature-slug}/` for session continuity.**

---

## Goal

Understand relevant existing code and patterns at both high and low levels.

---

## Instructions

Feature context: $ARGUMENTS

### Actions

1. Launch 2-3 code-explorer agents in parallel. Each agent should:
   - Trace through the code comprehensively
   - Focus on getting a comprehensive understanding of abstractions, architecture, and flow of control
   - Target a different aspect of the codebase
   - Include a list of 5-10 key files to read

   **Example agent prompts**:
   - "Find features similar to [feature] and trace through their implementation comprehensively"
   - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively"
   - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively"
   - "Identify UI patterns, testing approaches, or extension points relevant to [feature]"

2. Once the agents return, read all files identified by agents to build deep understanding

3. Present comprehensive summary of findings and patterns discovered

### Artifact

Update `progress.md` with exploration findings summary and key files list.

Add a section:

```markdown
## Codebase Exploration Findings

### Key Patterns Discovered
- {Pattern 1}: {description}
- {Pattern 2}: {description}

### Relevant Files
| File | Purpose | Relevance |
|------|---------|-----------|
| `{path}` | {what it does} | {why it matters for this feature} |

### Architecture Notes
{High-level understanding of how the codebase is structured}

### Integration Points
- {Where the new feature will connect to existing code}
```

### Git Commit

`docs({feature-slug}): document codebase exploration findings`

---

## Next Steps

After exploration is complete, guide the user to use:
- `/harness:gather-requirements` to clarify requirements and resolve ambiguities
