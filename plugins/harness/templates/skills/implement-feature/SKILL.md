---
name: implement-feature
description: Builds a feature following the designed architecture. Creates implementation plan, writes code following codebase conventions, and commits frequently. Use after architecture design is approved.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Skill
context: fork
---

# Implement Feature

You are helping a developer build a feature following the designed architecture.

**Progress is saved to `.artifacts/{feature-slug}/` for session continuity.**

---

## Goal

Build the feature following the approved design.

**DO NOT START WITHOUT USER APPROVAL**

---

## Instructions

Feature context: $ARGUMENTS

### Actions

1. Wait for explicit user approval to proceed
2. Create `plan.md` with implementation steps
3. Read all relevant files identified in previous phases
4. Implement following chosen architecture
5. Follow codebase conventions strictly
6. Write clean, well-documented code
7. Update todos as you progress
8. Update `progress.md` after each significant milestone

### Artifact

Create `plan.md` before starting implementation:

```markdown
# {Feature Name} - Implementation Plan

## Pre-Implementation Checklist
- [ ] User approved design
- [ ] All key files read and understood
- [ ] Development environment ready

## Files to Modify
| File | Changes |
|------|---------|
| `{path}` | {what changes} |

## Files to Create
| File | Purpose |
|------|---------|
| `{path}` | {purpose} |

## Implementation Steps
1. [ ] {Step 1}
   - Details: {specifics}
   - Files: {files involved}

2. [ ] {Step 2}
   - Details: {specifics}
   - Files: {files involved}

## Testing Strategy
- {How to verify the implementation works}

## Rollback Plan
- {How to undo if something goes wrong}
```

### During Implementation

Update `progress.md` with:
- Completed steps
- Current blockers
- Next actions
- Any deviations from plan

### Git Commits

Frequent throughout implementation:
- After creating plan: `docs({feature-slug}): create implementation plan`
- After each file created: `feat({feature-slug}): add {ComponentName}`
- After each file modified: `feat({feature-slug}): {describe change}`
- After fixing issues: `fix({feature-slug}): {describe fix}`
- After refactoring: `refactor({feature-slug}): {describe refactor}`
- Periodically update progress: `docs({feature-slug}): update progress after {milestone}`

**Important**: Commit code changes and artifact updates separately when possible for cleaner history.

---

## Next Steps

After implementation is complete, guide the user to use:
- `/review-code` to review for quality and correctness
