---
name: harness:workflow-discovery
description: This skill should be used when the user asks to "start a new feature", "initialize feature tracking", "begin feature development", or when the harness:feature orchestrator invokes the Discovery phase.
context: fork
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-discovery.sh"
          timeout: 10
---

# Discovery Phase - Feature Initialization

Initialize feature tracking and understand the request. This phase creates the foundation for all subsequent phases.

## Context Parsing

Parse `$ARGUMENTS` for:
- `feature_description` (required): What to build
- `--slug <name>`: Optional explicit slug override

If no description provided and invoked directly, ask: "What feature would you like to build?"

## Phase Execution

Execute these steps IN ORDER. Do NOT skip steps.

### Step 1: Search Engram for Context

IMMEDIATELY search for relevant prior work:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} implementation"
  n_results: 5
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "{feature_description}"
  insight_type: "all"
  n_results: 3
```

If relevant context found, note it briefly: "Found prior work on {topic}."

### Step 2: Generate Feature Slug

Create a slug from the description:
- Lowercase only
- Hyphens instead of spaces
- No special characters
- Short but descriptive (3-5 words max)

**Examples:**
| Description | Slug |
|-------------|------|
| "Add dark mode toggle" | `dark-mode-toggle` |
| "User authentication with OAuth" | `oauth-authentication` |
| "Fix memory leak in parser" | `parser-memory-leak-fix` |

### Step 3: Create Artifacts Directory

Execute this command:

```bash
mkdir -p .artifacts/{slug}
```

Verify the directory exists before proceeding.

### Step 4: Assess Clarity

Evaluate if the request is clear enough to proceed:

**CLEAR (proceed without questions):**
- Specific functionality described
- Clear scope boundaries
- Technical approach implied

**UNCLEAR (ask 1-2 questions max):**
- Ambiguous scope
- Multiple interpretations possible
- Missing critical constraints

If unclear, use AskUserQuestion with maximum 2 questions. Accept reasonable defaults for anything not specified.

### Step 5: Create Progress Artifact

Write `.artifacts/{slug}/progress.md`:

```markdown
# {Feature Name} - Progress

## Status
Phase: Discovery
Started: {YYYY-MM-DD}
Updated: {YYYY-MM-DD}

## Checklist
- [x] Discovery
- [ ] Codebase Exploration
- [ ] Requirements
- [ ] Architecture Design
- [ ] Implementation
- [ ] Code Review
- [ ] Testing
- [ ] Summary

## Feature
**Description:** {description}
**Problem:** {what it solves}
**Scope:** {boundaries}

## Session Log
### {YYYY-MM-DD}
- Initialized tracking
- Request: {user's original request}
```

### Step 6: Persist to Engram

Record feature start:

```
mcp__plugin_engram-mcp_engram__memory_remember
  content: "Started feature: {description}. Slug: {slug}. Purpose: {purpose}."
  tags: ["feature-start", "{slug}"]
```

### Step 7: Commit Artifacts

```bash
git add .artifacts/{slug}/
git commit -m "docs({slug}): initialize feature tracking"
```

## Critical Rules

1. ALWAYS create the artifacts directory
2. ALWAYS create progress.md before completing
3. NEVER ask more than 2 clarifying questions
4. NEVER complete without a valid slug
5. Proceed automatically unless genuinely blocked
