---
name: design-architecture
description: Designs multiple implementation approaches with different trade-offs using parallel architect agents. Presents options and helps user select the best approach. Use after requirements are gathered.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task
context: fork
---

# Design Architecture

You are helping a developer design the architecture for a feature by exploring multiple approaches.

**Progress is saved to `.artifacts/{feature-slug}/` for session continuity.**

---

## Goal

Design multiple implementation approaches with different trade-offs and help user select the best one.

---

## Instructions

Feature context: $ARGUMENTS

### Actions

1. Launch 2-3 code-architect agents in parallel with different focuses:
   - **Minimal changes**: Smallest change, maximum reuse of existing code
   - **Clean architecture**: Maintainability, elegant abstractions
   - **Pragmatic balance**: Speed + quality trade-off

2. Review all approaches and form your opinion on which fits best for this specific task
   - Consider: small fix vs large feature, urgency, complexity, team context

3. Present to user:
   - Brief summary of each approach
   - Trade-offs comparison
   - **Your recommendation with reasoning**
   - Concrete implementation differences

4. **Ask user which approach they prefer**

### Artifact

After user selects approach, create `design.md`:

```markdown
# {Feature Name} - Design

## Chosen Approach
{Name of chosen approach}

## Rationale
{Why this approach was selected}

## Approaches Considered

### Approach A: {Name}
- **Summary**: {brief description}
- **Pros**: {list}
- **Cons**: {list}
- **Effort**: {estimate}

### Approach B: {Name}
- **Summary**: {brief description}
- **Pros**: {list}
- **Cons**: {list}
- **Effort**: {estimate}

## Architecture Overview
{High-level description of the solution}

## Component Design
### {Component 1}
- Purpose: {what it does}
- Interface: {public API}
- Dependencies: {what it uses}

## Data Flow
{How data moves through the system}

## Integration Points
- {Where this connects to existing code}

## Risks and Mitigations
| Risk | Mitigation |
|------|------------|
| {risk} | {mitigation} |
```

### Git Commits

Multiple as phase progresses:
- After presenting options: `docs({feature-slug}): document architecture options`
- After user selects approach: `docs({feature-slug}): select {approach-name} approach`

---

## Next Steps

After architecture is designed, guide the user to use:
- `/implement-feature` to build the feature
