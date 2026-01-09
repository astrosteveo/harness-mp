---
name: summarize-feature
description: Documents completed feature with summary of what was built, key decisions, files changed, and lessons learned. Updates roadmap. Use after manual testing verification passes.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
context: fork
---

# Summarize Feature

You are helping a developer document a completed feature and close out the development session.

**Progress is saved to `.artifacts/{feature-slug}/` for session continuity.**

---

## Goal

Document what was accomplished and update the roadmap.

---

## Instructions

Feature context: $ARGUMENTS

### Actions

1. Mark all todos complete
2. Update `progress.md` to mark all phases complete
3. Create `summary.md`
4. Update `.artifacts/roadmap.md`:
   - Mark the completed feature as done (move to "Completed Features" section)
   - Add any deferred items or future improvements identified during development to "Planned Features"

### Artifact

Create `summary.md`:

```markdown
# {Feature Name} - Summary

## Completed
{Date completed}

## What Was Built
{Description of the feature}

## Key Decisions
| Decision | Rationale |
|----------|-----------|
| {decision} | {why} |

## Files Modified
| File | Changes |
|------|---------|
| `{path}` | {summary of changes} |

## Files Created
| File | Purpose |
|------|---------|
| `{path}` | {purpose} |

## Manual Testing
- Tested by: {User}
- Date: {date}
- Result: PASSED
- {Summary of what was verified}

## Known Limitations
- {Any limitations or technical debt}

## Future Improvements
- {Potential enhancements}

## Lessons Learned
- {What went well}
- {What could be improved}
```

### Final Progress Update

Update `progress.md`:

```markdown
## Status
Phase: COMPLETE
Started: {date}
Completed: {date}

## Current State
- [x] Phase 1: Discovery
- [x] Phase 2: Codebase Exploration
- [x] Phase 3: Clarifying Questions
- [x] Phase 4: Architecture Design
- [x] Phase 5: Implementation
- [x] Phase 6: Quality Review
- [x] Phase 7: Manual Testing Verification
- [x] Phase 8: Summary
```

### Git Commits

- `docs({feature-slug}): complete feature summary`
- `docs(roadmap): mark {feature-slug} complete, add deferred items`

---

## Feature Development Complete

Congratulate the user on completing the feature. Provide a brief summary of the journey:
- How many sessions it took
- Key milestones achieved
- Any notable decisions or challenges overcome
