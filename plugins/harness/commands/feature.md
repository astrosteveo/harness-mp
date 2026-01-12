---
description: Start or resume feature development workflow
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite, mcp__plugin_engram-mcp_engram__memory_search, mcp__plugin_engram-mcp_engram__memory_remember, mcp__plugin_engram-mcp_engram__memory_sync
argument-hint: <feature-description> [--phase <name>] [--tdd] [--skip <phase>]
---

# Feature Development Workflow

You are orchestrating a structured feature development workflow. Drive the process autonomously, pausing only at decision points where user input is required.

## Arguments

- `$ARGUMENTS` - Feature description and optional flags
- `--phase <name>` - Jump to specific phase (discovery, explore, requirements, design, implement, review, testing, summary)
- `--tdd` - Use test-driven development for implementation
- `--skip <phase>` - Skip a phase (can be repeated)

---

# Initialization

## Step 1: Search Project Memory

Use `mcp__plugin_engram-mcp_engram__memory_search` to find relevant past context:
- Previous work on similar features
- Past architectural decisions that might apply
- Lessons learned from related implementations

If relevant findings exist, present them: "I found previous context that may be relevant: [summary]"

## Step 2: Check for Existing Artifacts

Check if resuming an existing feature:
```bash
ls -la .artifacts/*/progress.md 2>/dev/null
```

**If artifacts exist:**
1. Read `progress.md` to determine current phase
2. Present: "Resuming **{feature-name}** from **{phase}**"
3. Jump to that phase

**If no artifacts:** Proceed to Phase 1: Discovery

## Step 3: Load Configuration

Read configuration (in priority order, merge settings):
1. `.claude/harness.yaml` (project overrides)
2. `~/.claude/harness.yaml` (user defaults)
3. `${CLAUDE_PLUGIN_ROOT}/config/workflow.yaml` (plugin defaults)

Note: skipped phases, TDD mode, agent count, model preferences.

---

# Phase 1: Discovery

**Goal:** Understand what needs to be built and set up tracking.

## Actions

1. Generate `feature-slug` from the feature name (lowercase, hyphenated)
2. Create `.artifacts/{feature-slug}/` directory
3. If the feature request is unclear, ask:
   - What problem are you solving?
   - What should the feature do?
   - Any constraints or requirements?
4. Summarize understanding and confirm with user

## Artifact: progress.md

Create `.artifacts/{feature-slug}/progress.md`:

```markdown
# {Feature Name} - Progress

## Status
Phase: Discovery
Started: {date}
Last Updated: {date}

## Checklist
- [x] Discovery
- [ ] Codebase Exploration
- [ ] Requirements
- [ ] Architecture Design
- [ ] Implementation
- [ ] Code Review
- [ ] Testing
- [ ] Summary

## Session Log
### {date}
- Started feature development
- Initial request: {summary}
```

## Git Commit

```
docs({feature-slug}): initialize feature tracking
```

**Automatic transition** to Phase 2.

---

# Phase 2: Explore Codebase

**Goal:** Deep understanding of existing patterns and architecture.

## Actions

1. Launch 2-3 `code-explorer` agents in parallel using Task tool with `subagent_type: "harness:code-explorer"`. Each agent should focus on a different aspect:
   - "Find similar features and trace their implementation"
   - "Map the architecture and abstractions for this area"
   - "Identify integration points and extension patterns"

2. Wait for agents to complete

3. Read all key files identified by the agents

4. Present comprehensive summary of findings

## Artifact Update

Add to `progress.md`:

```markdown
## Codebase Exploration

### Key Patterns
- {Pattern 1}: {description}
- {Pattern 2}: {description}

### Relevant Files
| File | Purpose | Relevance |
|------|---------|-----------|
| `{path}` | {what it does} | {why it matters} |

### Architecture Notes
{High-level structure understanding}

### Integration Points
{Where the new feature connects to existing code}
```

## Git Commit

```
docs({feature-slug}): document codebase exploration
```

**Automatic transition** to Phase 3.

---

# Phase 3: Gather Requirements

**Goal:** Resolve all ambiguities before designing.

**CRITICAL:** This phase is essential. Do not skip.

## Actions

1. Review exploration findings and original request
2. Identify underspecified aspects:
   - Edge cases
   - Error handling
   - Integration points
   - Scope boundaries
   - Performance needs
3. **Ask questions ONE AT A TIME**
4. **For each question, provide a recommendation**
5. Wait for user answer before asking the next question
6. Continue until all ambiguities resolved

## Question Format

```
**Question {N}/{Total}**: {The specific question}

**Recommendation:** {Your suggested answer with rationale}
```

If user says "whatever you think is best", apply your recommendation and confirm.

## PAUSE POINT

Wait for user answers to each question.

## Artifact: requirements.md

After all questions answered, create `.artifacts/{feature-slug}/requirements.md`:

```markdown
# {Feature Name} - Requirements

## Overview
{Brief description}

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
A: {Answer}

## Out of Scope
- {Excluded items}
```

## Git Commit

```
docs({feature-slug}): finalize requirements
```

**Automatic transition** to Phase 4.

---

# Phase 4: Design Architecture

**Goal:** Evaluate multiple approaches and select the best one.

## Actions

1. Search engram for past architectural patterns relevant to this feature type

2. Launch 2-3 `code-architect` agents in parallel using Task tool with `subagent_type: "harness:code-architect"`. Each with a different focus:
   - **Minimal changes**: Smallest change, maximum reuse
   - **Clean architecture**: Maintainability, elegant abstractions
   - **Pragmatic balance**: Speed + quality trade-off

3. Review all approaches and form your recommendation

4. Present to user:
   - Brief summary of each approach
   - Trade-offs comparison
   - **Your recommendation with reasoning**

## PAUSE POINT

Ask user: "Which approach would you like to use?"

## Artifact: design.md

After user selects, create `.artifacts/{feature-slug}/design.md`:

```markdown
# {Feature Name} - Design

## Chosen Approach
{Name}

## Rationale
{Why selected}

## Approaches Considered

### Approach A: {Name}
- **Summary**: {description}
- **Pros**: {list}
- **Cons**: {list}

### Approach B: {Name}
...

## Architecture Overview
{High-level description}

## Component Design
### {Component 1}
- Purpose: {what it does}
- Interface: {public API}
- Dependencies: {what it uses}

## Data Flow
{How data moves through the system}

## Risks and Mitigations
| Risk | Mitigation |
|------|------------|
| {risk} | {mitigation} |
```

## Git Commit

```
docs({feature-slug}): select {approach-name} architecture
```

**Automatic transition** to Phase 5.

---

# Phase 5: Implement Feature

**Goal:** Build the feature following the approved design.

Check if TDD mode is enabled (via `--tdd` flag or config `tdd.mode: always`).

## If TDD Mode

Follow the red-green-refactor cycle:

### TDD Setup
1. Verify test framework is configured
2. Create `test-plan.md` with ordered test cases (simplest to complex)

### For Each Test Case
1. **RED**: Write failing test, verify it fails, commit: `test({feature-slug}): add failing test for {behavior}`
2. **GREEN**: Write minimum code to pass, commit: `feat({feature-slug}): implement {behavior}`
3. **REFACTOR**: Clean up if needed, commit: `refactor({feature-slug}): {description}`

### TDD Artifacts
- `.artifacts/{feature-slug}/test-plan.md` - Ordered test cases
- `.artifacts/{feature-slug}/tdd-progress.md` - Cycle tracking

## If Standard Mode

### PAUSE POINT

Present implementation plan and wait for approval before coding.

## Artifact: plan.md

Create `.artifacts/{feature-slug}/plan.md`:

```markdown
# {Feature Name} - Implementation Plan

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
2. [ ] {Step 2}

## Testing Strategy
{How to verify it works}
```

## Implementation

After approval:
1. Implement following the plan
2. Follow codebase conventions strictly
3. Update todos as you progress
4. Commit frequently:
   - `feat({feature-slug}): {description}`
   - `fix({feature-slug}): {description}`

## Git Commits

Frequent throughout:
```
feat({feature-slug}): add {component}
feat({feature-slug}): implement {behavior}
fix({feature-slug}): {fix description}
```

**Automatic transition** to Phase 6.

---

# Phase 6: Code Review

**Goal:** Ensure quality and correctness.

## Actions

1. Launch 3 `code-reviewer` agents in parallel using Task tool with `subagent_type: "harness:code-reviewer"`. Each with different focus:
   - **Simplicity/DRY/Elegance**: Duplication, complexity, clarity
   - **Bugs/Correctness**: Logic errors, edge cases, runtime issues
   - **Conventions/Patterns**: Consistency with codebase

2. Consolidate findings by severity

3. Present findings organized as:
   - High Priority (recommend fixing now)
   - Medium Priority (consider fixing)
   - Low Priority (nice to have)

4. Ask user: "What would you like to do?"
   - Fix now
   - Fix later
   - Proceed as-is

5. Address issues based on user decision

## Artifact Update

Add to `progress.md`:

```markdown
## Code Review

### Issues Found
| Severity | Issue | Resolution |
|----------|-------|------------|
| High | {issue} | Fixed / Deferred / Accepted |

### Summary
- Total: {N}, Fixed: {N}, Deferred: {N}
```

## Git Commits

```
fix({feature-slug}): {fix from review}
```

**Automatic transition** to Phase 7.

---

# Phase 7: Testing Verification

**Goal:** User verifies the feature works correctly.

**CRITICAL:** Do not skip. Feature cannot be closed until user confirms.

## Actions

1. Read `requirements.md` to understand what needs testing
2. Present testing checklist with clear steps and expected results
3. Ask user to perform tests and report back

## Testing Checklist Format

```markdown
## Manual Testing

Please test and confirm each works:

### Test 1: {Name}
**Steps:**
1. {Step 1}
2. {Step 2}

**Expected:** {What should happen}

---

Reply with PASS or FAIL for each test.
```

## PAUSE POINT

Wait for user confirmation: "Testing passed" or issue reports.

## If Issues Found

1. Document the issue
2. Fix it
3. Commit: `fix({feature-slug}): {description}`
4. Ask user to re-test

## Artifact Update

Add to `progress.md`:

```markdown
## Testing
- Date: {date}
- Result: PASSED

| Test | Result |
|------|--------|
| {name} | PASS |
```

## Git Commit

```
docs({feature-slug}): record successful testing
```

**Automatic transition** to Phase 8.

---

# Phase 8: Summary

**Goal:** Document completion and persist learnings.

## Actions

1. Mark all checklist items complete in `progress.md`
2. Create `summary.md`
3. Update `.artifacts/roadmap.md` if it exists:
   - Move feature to "Completed" section
   - Add deferred items to "Planned" section

## Artifact: summary.md

Create `.artifacts/{feature-slug}/summary.md`:

```markdown
# {Feature Name} - Summary

## Completed
{Date}

## What Was Built
{Description}

## Key Decisions
| Decision | Rationale |
|----------|-----------|
| {decision} | {why} |

## Files Changed
| File | Changes |
|------|---------|
| `{path}` | {summary} |

## Testing
- Result: PASSED
- {What was verified}

## Known Limitations
- {Any limitations}

## Future Improvements
- {Potential enhancements}

## Lessons Learned
- {What went well}
- {What could improve}
```

## Persist to Memory

Use `mcp__plugin_engram-mcp_engram__memory_remember` to save key learnings:

```
For {feature-name}: Implemented using {pattern}. Key decision: {decision}. Lesson: {lesson}.
```

## Sync Session

Use `mcp__plugin_engram-mcp_engram__memory_sync` to index this session.

## Git Commit

```
docs({feature-slug}): complete feature summary
```

## Complete

Congratulate the user:
- Phases completed
- Artifacts created
- Key accomplishments

---

# Phase Navigation

Jump to any phase with `--phase`:

| Phase | Name |
|-------|------|
| 1 | `discovery` |
| 2 | `explore` |
| 3 | `requirements` |
| 4 | `design` |
| 5 | `implement` |
| 6 | `review` |
| 7 | `testing` |
| 8 | `summary` |

Example: `/harness:feature --phase design`

---

# Error Recovery

If something goes wrong:
1. Check `progress.md` for last known state
2. Restart phase: `/harness:feature --phase {name}`
3. Search engram for similar past issues
