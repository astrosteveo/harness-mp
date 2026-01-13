---
name: harness:workflow-requirements
description: This skill should be used when the user asks to "gather requirements", "define feature requirements", "clarify feature scope", or when the harness:feature orchestrator invokes the Requirements phase.
context: fork
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-requirements.sh"
          timeout: 10
---

# Requirements Phase - Specification Gathering

Resolve ambiguities and document complete requirements. This phase ensures clarity before design.

## Context Parsing

Parse `$ARGUMENTS` for:
- `--slug <name>`: Feature slug
- `--description "<text>"`: Feature description
- `--artifacts <path>`: Artifacts directory path

## Phase Execution

Execute these steps IN ORDER. Do NOT skip steps.

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Current state, exploration findings
- Check for any exploration notes

Search engram:

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
- Change "Phase:" to "Requirements"
- Check off "Codebase Exploration"
- Add session log entry

### Step 3: Identify Ambiguities

Review feature description and exploration. Categorize what needs clarification:

**Functional:** Core behavior, edge cases, error handling
**Integration:** How it connects, data flow, APIs
**Non-functional:** Performance, security, accessibility
**Scope:** What's in, what's out, future considerations

### Step 4: Ask Questions (If Needed)

ONLY ask questions if genuinely unclear. Maximum 3 questions total.

Present questions ONE AT A TIME using AskUserQuestion:

```
Question {N}/{Total}: {specific question}

Context: {why this matters for implementation}

Recommendation: {your suggested answer}
```

Accept "whatever you think is best" → apply recommendation.

Track all Q&A for documentation.

### Step 5: Create Requirements Document

Write `.artifacts/{slug}/requirements.md`:

```markdown
# {Feature Name} - Requirements

## Overview
{2-3 sentence description}

## Problem Statement
{What problem this solves}

## User Stories
- As a {user}, I want {action} so that {benefit}
- As a {user}, I want {action} so that {benefit}

## Functional Requirements

### Core Functionality
1. {Requirement} - {acceptance criteria}
2. {Requirement} - {acceptance criteria}

### Edge Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| {edge case} | {behavior} |

### Error Handling
| Error Condition | Response |
|-----------------|----------|
| {condition} | {handling} |

## Non-Functional Requirements

### Performance
- {constraint or target}

### Security
- {security consideration}

### Accessibility
- {a11y requirement}

## Clarifications
{If questions were asked}

### Q: {question}
**A:** {answer}
**Rationale:** {why this decision}

## Out of Scope
- {excluded item} - {why}
- {future consideration} - {when to revisit}

## Success Criteria
- [ ] {measurable criterion}
- [ ] {measurable criterion}
```

### Step 6: Persist to Engram

Record key decisions:

```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature}: {decision}. Rationale: {why}."
  category: "implementation"
  alternatives: ["{considered alternatives}"]
```

```
mcp__plugin_engram-mcp_engram__memory_remember
  content: "{feature} scope: In={in_scope}. Out={out_of_scope}. Key constraint: {constraint}."
  tags: ["requirements", "{slug}"]
```

### Step 7: Commit Requirements

```bash
git add .artifacts/{slug}/
git commit -m "docs({slug}): finalize requirements"
```

## Critical Rules

1. NEVER ask more than 3 questions total
2. ALWAYS create requirements.md before completing
3. ALWAYS document Out of Scope section
4. ALWAYS include success criteria
5. Accept defaults when user defers decisions
