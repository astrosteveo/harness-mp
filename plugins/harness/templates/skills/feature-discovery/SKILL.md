---
name: harness:feature-discovery
description: Initializes a new feature development session. Creates artifact directory, documents initial understanding, and sets up progress tracking. Use when starting work on a new feature or capability.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

# Feature Discovery

You are helping a developer initialize a new feature. This phase establishes the foundation for systematic feature development.

**All progress is saved to `.artifacts/{feature-slug}/` and committed to Git for session continuity.**

---

## Goal

Understand what needs to be built and set up tracking infrastructure.

---

## Instructions

Initial request: $ARGUMENTS

### Actions

1. Create todo list with discovery tasks
2. Generate `feature-slug` from the feature name (lowercase, hyphenated)
3. Create `.artifacts/{feature-slug}/` directory
4. If feature unclear, ask user for:
   - What problem are they solving?
   - What should the feature do?
   - Any constraints or requirements?
5. Summarize understanding and confirm with user

### Artifact

Initialize `progress.md` with:

```markdown
# {Feature Name} - Progress

## Status
Phase: 1 - Discovery
Started: {date}
Last Updated: {date}

## Current State
- [x] Phase 1: Discovery
- [ ] Phase 2: Codebase Exploration
- [ ] Phase 3: Clarifying Questions
- [ ] Phase 4: Architecture Design
- [ ] Phase 5: Implementation
- [ ] Phase 6: Quality Review
- [ ] Phase 7: Manual Testing Verification
- [ ] Phase 8: Summary

## Session Log
### Session 1 - {date}
- Started feature development
- Initial request: {summary}
```

### Git Commit

`docs({feature-slug}): initialize feature tracking`

---

## Next Steps

After discovery is complete, guide the user to use:
- `/harness:explore-codebase` to understand relevant existing code
- Or continue to clarifying questions if codebase is already understood
