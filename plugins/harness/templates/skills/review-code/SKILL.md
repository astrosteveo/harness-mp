---
name: harness:review-code
description: Reviews implemented code for simplicity, DRY, elegance, bugs, and project conventions using parallel reviewer agents. Presents findings and helps prioritize fixes. Use after implementation is complete.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task
context: fork
---

# Review Code

You are helping a developer review implemented code for quality and correctness.

**Progress is saved to `.artifacts/{feature-slug}/` for session continuity.**

---

## Goal

Ensure code is simple, DRY, elegant, easy to read, and functionally correct.

---

## Instructions

Feature context: $ARGUMENTS

### Actions

1. Launch 3 code-reviewer agents in parallel with different focuses:
   - **Simplicity/DRY/Elegance**: Look for duplication, unnecessary complexity, unclear code
   - **Bugs/Functional Correctness**: Logic errors, edge cases, potential runtime issues
   - **Project Conventions/Abstractions**: Consistency with codebase patterns, proper use of existing abstractions

2. Consolidate findings and identify highest severity issues that you recommend fixing

3. **Present findings to user and ask what they want to do**:
   - Fix now
   - Fix later
   - Proceed as-is

4. Address issues based on user decision

### Findings Format

```markdown
## Code Review Findings

### High Priority (Recommend Fixing Now)
1. **{Issue}** in `{file}:{line}`
   - Problem: {description}
   - Suggestion: {how to fix}

### Medium Priority (Consider Fixing)
1. **{Issue}** in `{file}:{line}`
   - Problem: {description}
   - Suggestion: {how to fix}

### Low Priority (Nice to Have)
1. **{Issue}** in `{file}:{line}`
   - Problem: {description}
   - Suggestion: {how to fix}

### Positive Observations
- {What was done well}
```

### Artifact

Update `progress.md` with review findings and resolutions.

Add a section:

```markdown
## Code Review Results

### Issues Found
| Severity | Issue | Resolution |
|----------|-------|------------|
| High | {issue} | Fixed / Deferred / Accepted |

### Review Summary
- Total issues: {N}
- Fixed: {N}
- Deferred: {N}
- Accepted as-is: {N}
```

### Git Commits

- After documenting findings: `docs({feature-slug}): record review findings`
- After each fix applied: `fix({feature-slug}): {describe fix from review}`

---

## Next Steps

After review is complete, guide the user to use:
- `/harness:verify-testing` to perform manual testing verification
