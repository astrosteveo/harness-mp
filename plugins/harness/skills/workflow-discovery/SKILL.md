---
name: harness:workflow-discovery
description: This skill should be used when the user asks to "start a new feature", "initialize feature tracking", "begin feature development", or when the harness:feature orchestrator invokes the Discovery phase.
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Bash(mkdir:*)
  - Bash(ls:*)
  - AskUserQuestion
  - mcp__plugin_engram-mcp_engram__*
hooks:
  Stop:
    - prompt: |
        Before completing, validate:
        1. Feature slug was generated (lowercase, hyphenated)
        2. .artifacts/{slug}/ directory exists
        3. progress.md was created with Phase: Discovery
        4. User confirmed understanding of the feature

        If validation fails, output what's missing. If passes, output "PHASE_COMPLETE".
---

# Discovery Phase - Feature Initialization

This phase understands the feature request and creates tracking infrastructure.

## Context

**If invoked via orchestrator:** Receives `$ARGUMENTS`:
- `feature_description`: What the user wants to build

**If invoked directly:** Parse `$ARGUMENTS` for feature description. If none provided, ask what feature the user wants to build.

## Phase Execution

### Step 1: Search Engram for Similar Features

Before starting, check if similar features were built before:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} feature implementation"
  n_results: 5
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "{feature_description}"
  insight_type: "all"
  n_results: 3
```

If relevant findings exist, mention: "Found relevant context from past work: {brief summary}"

### Step 2: Generate Feature Slug

Create a slug from the feature description:
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Keep it short but descriptive

Examples:
- "Add dark mode toggle" → `dark-mode-toggle`
- "User authentication with OAuth" → `oauth-authentication`
- "Fix memory leak in parser" → `fix-parser-memory-leak`

### Step 3: Create Artifacts Directory

```bash
mkdir -p .artifacts/{feature-slug}
```

### Step 4: Clarify Feature Understanding (if needed)

**Only ask questions if genuinely unclear.** If the request is specific enough to proceed, skip to Step 5.

If clarification needed, ask using AskUserQuestion:
- What problem does this feature solve?
- What should the feature do (high-level)?
- Are there any constraints or requirements?

**Keep questions minimal.** Better to make reasonable assumptions and validate in Requirements phase.

If user says "whatever you think is best" → apply reasonable defaults.

### Step 5: Quick Confirmation

Present a brief summary:

```
**Feature:** {name}
**Purpose:** {what it does}
**Scope:** {high-level scope}

Proceeding with Discovery → Explore → Requirements...
```

**Only pause if:**
- Feature scope is ambiguous
- Multiple interpretations possible
- User explicitly requested confirmation

**Otherwise:** State understanding and continue automatically. Requirements phase will validate details.

### Step 6: Create Progress Artifact

Write `.artifacts/{feature-slug}/progress.md`:

```markdown
# {Feature Name} - Progress

## Status
Phase: Discovery
Started: {YYYY-MM-DD}
Last Updated: {YYYY-MM-DD}

## Checklist
- [x] Discovery
- [ ] Codebase Exploration
- [ ] Requirements
- [ ] Architecture Design
- [ ] Implementation
- [ ] Code Review
- [ ] Testing
- [ ] Summary

## Feature Overview
**Description:** {description}
**Problem:** {what problem it solves}
**Scope:** {boundaries}

## Session Log
### {YYYY-MM-DD}
- Initialized feature tracking
- Request: {summary of user's request}
- Understanding confirmed
```

### Step 7: Persist to Engram

Record the feature initiation:

```
mcp__plugin_engram-mcp_engram__memory_remember
  content: "Started feature: {feature_description}. Slug: {slug}. Purpose: {purpose}."
  tags: ["feature-start", "{slug}"]
```

### Step 8: Commit Artifacts

Commit the discovery artifacts:

```bash
git add .artifacts/{feature-slug}/
git commit -m "docs({feature-slug}): initialize feature tracking"
```

### Step 9: Prepare Handoff

Output summary for orchestrator/next phase:
- Feature slug
- Feature description
- Artifacts path
- Any important context from engram search

## Completion Criteria

Stop hook validates:
1. Feature slug generated
2. `.artifacts/{slug}/` directory exists
3. `progress.md` created with "Phase: Discovery"
4. User confirmed understanding

## Standalone Usage

When invoked directly (not via workflow):
- Still create artifacts directory and progress.md
- User can continue with `/harness:feature {slug}` later
- Or just use this as a planning/clarification tool
