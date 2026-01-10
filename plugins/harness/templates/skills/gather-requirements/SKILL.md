---
name: harness:gather-requirements
description: Systematically identifies and resolves ambiguities by asking clarifying questions one at a time. Creates comprehensive requirements document. Use after codebase exploration to fill in gaps before designing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
context: fork
---

# Gather Requirements

You are helping a developer fill in gaps and resolve all ambiguities before designing the feature.

**Progress is saved to `.artifacts/{feature-slug}/` for session continuity.**

---

## Goal

Fill in gaps and resolve all ambiguities before designing.

**CRITICAL**: This is one of the most important phases. DO NOT SKIP.

---

## Instructions

Feature context: $ARGUMENTS

### Actions

1. Review the codebase findings and original feature request
2. Identify underspecified aspects:
   - Edge cases
   - Error handling
   - Integration points
   - Scope boundaries
   - Design preferences
   - Backward compatibility
   - Performance needs
3. **Ask questions ONE AT A TIME** — do not overwhelm the user with a list
4. **For each question, provide a clear recommendation** labeled as "**Recommendation:**"
5. **Wait for the user's answer before asking the next question**
6. Continue until all ambiguities are resolved

### Question Format

```
**Question {N}/{Total}**: {The specific question}

**Recommendation:** {Your suggested answer with brief rationale}
```

If the user says "whatever you think is best", apply your recommendation and confirm what you decided.

### Artifact

After questions are answered, create `requirements.md`:

```markdown
# {Feature Name} - Requirements

## Overview
{Brief description of what the feature does}

## Problem Statement
{What problem this solves}

## User Stories
- As a {user}, I want to {action} so that {benefit}

## Functional Requirements
1. {Requirement 1}
2. {Requirement 2}

## Non-Functional Requirements
- Performance: {constraints}
- Compatibility: {constraints}

## Clarifications
### Q: {Question 1}
A: {User's answer}

### Q: {Question 2}
A: {User's answer}

## Out of Scope
- {Explicitly excluded items}

## Key Files Identified
- `{path}` - {why relevant}
```

### Git Commits

Multiple as phase progresses:
- After presenting questions: `docs({feature-slug}): identify clarifying questions`
- After each significant user answer: `docs({feature-slug}): record user clarification on {topic}`
- After finalizing requirements: `docs({feature-slug}): finalize requirements`

---

## Next Steps

After requirements are gathered, guide the user to use:
- `/harness:design-architecture` to design implementation approaches
