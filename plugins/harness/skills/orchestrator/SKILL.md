---
name: orchestrator
description: Guided feature development with codebase understanding and architecture focus. Orchestrates the full feature development workflow from discovery through summary.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task, Skill
---

# Feature Development Workflow

You are helping a developer implement a new feature using a systematic approach. This skill orchestrates the full workflow.

---

## Workflow Overview

The feature development process consists of 8 phases, each with its own skill:

| Phase | Skill | Purpose |
|-------|-------|---------|
| 1 | `/feature-discovery` | Initialize feature, understand requirements |
| 2 | `/explore-codebase` | Deep dive into relevant existing code |
| 3 | `/gather-requirements` | Ask clarifying questions, document requirements |
| 4 | `/design-architecture` | Design and compare implementation approaches |
| 5 | `/implement-feature` | Build the feature |
| 6 | `/review-code` | Review for quality and correctness |
| 7 | `/verify-testing` | Manual testing verification |
| 8 | `/summarize-feature` | Document completion |

---

## Session Continuity

**All progress is saved to `.artifacts/{feature-slug}/` and committed to Git.**

### Starting a New Feature
When `$ARGUMENTS` contains a new feature request, invoke `/feature-discovery`.

### Resuming an Existing Feature
When `.artifacts/{feature-slug}/` exists:

1. Read `progress.md` to identify current phase
2. Present summary: "Resuming {feature-name} from Phase {N}"
3. Invoke the appropriate skill for the current phase

### Artifact Directory Structure
```
.artifacts/{feature-slug}/
├── requirements.md   # Phase 3: Feature requirements and Q&A
├── design.md         # Phase 4: Architecture decision and rationale
├── plan.md           # Phase 5: Implementation plan with file list
├── progress.md       # Ongoing: Current status and next steps
└── summary.md        # Phase 8: Final summary and lessons learned
```

---

## Core Principles

- **Ask clarifying questions**: Identify all ambiguities before designing
- **Understand before acting**: Read and comprehend existing code patterns first
- **Simple and elegant**: Prioritize readable, maintainable code
- **Use TodoWrite**: Track all progress throughout
- **Commit frequently**: Git log should read like a narrative

---

## Git Commit Strategy

```
{type}({feature-slug}): {concise description}
```

**Types:**
- `feat` - New functionality
- `docs` - Artifact or documentation updates
- `fix` - Bug fixes
- `refactor` - Code restructuring
- `chore` - Maintenance tasks

---

## Instructions

Feature request: $ARGUMENTS

### Actions

1. Check if `.artifacts/` contains a matching feature directory
   - If resuming: Read `progress.md`, determine current phase, invoke appropriate skill
   - If new: Invoke `/feature-discovery` with the feature request

2. After each phase completes, guide the user to the next skill in the workflow

3. Track overall progress and ensure no phases are skipped
