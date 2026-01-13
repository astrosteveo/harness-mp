---
name: harness:workflow-requirements
description: This skill should be used when the user asks to "gather requirements", "define feature requirements", "clarify feature scope", or when the harness:feature orchestrator invokes the Requirements phase.
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - mcp__plugin_engram-mcp_engram__*
hooks:
  Stop:
    - prompt: |
        Before completing, validate:
        1. progress.md shows "Phase: Requirements"
        2. requirements.md exists with completed sections
        3. All identified questions were asked and answered
        4. Out of scope items are documented

        If validation fails, output what's missing. If passes, output "PHASE_COMPLETE".
---

# Requirements Phase - Specification Gathering

This phase resolves all ambiguities and documents complete requirements before design.

## Context

**If invoked via orchestrator:** Receives `$ARGUMENTS`:
- `feature_slug`: Feature identifier
- `feature_description`: What to build
- `artifacts_path`: Path to `.artifacts/{slug}/`

**If invoked directly:** Check for existing `.artifacts/*/progress.md` files. If found, ask which feature. If none, ask user to describe what needs requirements gathering.

## Phase Execution

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Current state, feature overview
- Any exploration findings if Explore phase completed

Search engram for similar requirements work:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} requirements edge cases"
  n_results: 5
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "requirements {feature_type}"
  insight_type: "decision"
  n_results: 3
```

### Step 2: Update Progress

Edit `progress.md`:
- Set Phase to "Requirements"
- Check off "Codebase Exploration" (if came from Explore)
- Add session log entry

### Step 3: Identify Ambiguities

Review the feature description and exploration findings. Identify underspecified aspects:

**Functional:**
- Core behavior details
- Edge cases
- Error handling
- Input validation

**Integration:**
- How it connects to existing features
- Data flow
- API contracts

**Non-functional:**
- Performance requirements
- Security considerations
- Accessibility needs
- Browser/platform support

**Scope:**
- What's explicitly included
- What's explicitly excluded
- Future considerations (not now)

### Step 4: Ask Questions Systematically

Present questions ONE AT A TIME using AskUserQuestion:

Format each question:
```
**Question {N}/{Total}**: {specific question}

**Context:** {why this matters}

**Recommendation:** {your suggested answer with rationale}
```

Wait for user answer before asking next question.

If user says "whatever you think is best" → apply the recommendation.

Track all Q&A for documentation.

### Step 5: Create Requirements Document

After all questions answered, write `.artifacts/{slug}/requirements.md`:

```markdown
# {Feature Name} - Requirements

## Overview
{Brief description of the feature}

## Problem Statement
{What problem this solves and why it matters}

## User Stories
- As a {user type}, I want to {action} so that {benefit}
- As a {user type}, I want to {action} so that {benefit}

## Functional Requirements

### Core Functionality
1. {Requirement with clear acceptance criteria}
2. {Requirement with clear acceptance criteria}

### Edge Cases
1. {Edge case}: {expected behavior}
2. {Edge case}: {expected behavior}

### Error Handling
1. {Error scenario}: {how to handle}
2. {Error scenario}: {how to handle}

## Non-Functional Requirements

### Performance
- {Constraint or target}

### Security
- {Security requirement}

### Accessibility
- {A11y requirement}

### Compatibility
- {Platform/browser requirements}

## Clarifications

### Q: {Question asked}
**A:** {User's answer}
**Rationale:** {Why this decision}

### Q: {Question asked}
**A:** {User's answer}
**Rationale:** {Why this decision}

## Out of Scope
- {Explicitly excluded item} - {why excluded}
- {Future consideration} - {when to revisit}

## Dependencies
- {External dependency}
- {Internal dependency}

## Success Criteria
- [ ] {Measurable criterion}
- [ ] {Measurable criterion}
```

### Step 6: Persist Decisions to Engram

Record key requirement decisions:

```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature}: Decided {decision}. Rationale: {why}. Alternatives considered: {alternatives}."
  category: "implementation"
  alternatives: ["{alt1}", "{alt2}"]
```

If important scope decisions made:

```
mcp__plugin_engram-mcp_engram__memory_remember
  content: "{feature} scope: Includes {in_scope}. Excludes {out_of_scope}. Key constraint: {constraint}."
  tags: ["requirements", "{slug}"]
```

### Step 7: Commit Requirements

Commit the requirements document:

```bash
git add .artifacts/{feature-slug}/
git commit -m "docs({feature-slug}): finalize requirements"
```

### Step 8: Prepare Handoff

Summarize for Design phase:
- Top 3-5 most critical requirements
- Key constraints that will influence design
- Any technical decisions already implied by requirements

## Completion Criteria

Stop hook validates:
1. `progress.md` updated with "Phase: Requirements"
2. `requirements.md` exists with all sections populated
3. All questions asked and answered
4. Out of scope documented

## Engram Integration

| When | Tool | Purpose |
|------|------|---------|
| Start | `memory_search` | Find similar requirements |
| Start | `memory_insights` | Get past requirement decisions |
| End | `memory_decision` | Record key decisions |
| End | `memory_remember` | Persist scope boundaries |
