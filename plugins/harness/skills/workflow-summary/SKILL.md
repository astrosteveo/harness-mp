---
name: harness:workflow-summary
description: This skill should be used when the user asks to "summarize the feature", "complete the feature", "wrap up", or when the harness:feature orchestrator invokes the Summary phase.
context: fork
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-summary.sh"
          timeout: 10
---

# Summary Phase - Completion and Documentation

Document the completed feature and persist learnings. This phase has the MOST IMPORTANT engram integration.

## Context Parsing

Parse `$ARGUMENTS` for:
- `--slug <name>`: Feature slug
- `--description "<text>"`: Feature description
- `--artifacts <path>`: Artifacts directory path

## Phase Execution

Execute these steps IN ORDER. Do NOT skip steps.

### Step 1: Load All Artifacts

Read ALL phase artifacts:
- `{artifacts_path}/progress.md` - Full journey
- `{artifacts_path}/requirements.md` - Specifications
- `{artifacts_path}/design.md` - Architecture
- `{artifacts_path}/plan.md` - Implementation approach

Get git history:
```bash
git log --oneline -20
```

### Step 2: Update Progress to Final

Edit `progress.md`:
- Change "Phase:" to "Summary"
- Check off "Testing"
- Mark ALL checklist items [x]
- Add final session log entry

```markdown
## Checklist
- [x] Discovery
- [x] Codebase Exploration
- [x] Requirements
- [x] Architecture Design
- [x] Implementation
- [x] Code Review
- [x] Testing
- [x] Summary

## Session Log
### {YYYY-MM-DD}
- Feature completed
- All phases finished
- Summary documented
- Memory persisted
```

### Step 3: Create Summary Document

Write `.artifacts/{slug}/summary.md`:

```markdown
# {Feature Name} - Summary

## Completed
{YYYY-MM-DD}

## Overview
{2-3 sentence summary}

## Problem Solved
{what problem this addresses}

## Solution
{high-level approach}

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | {approach} | {why} |
| {Decision 2} | {choice} | {why} |

## Files

### Created
| File | Purpose |
|------|---------|
| `path` | {what} |

### Modified
| File | Changes |
|------|---------|
| `path` | {what} |

## Commits
| Hash | Message |
|------|---------|
| `abc` | feat: {msg} |
| `def` | fix: {msg} |

## Testing
- **Automated:** {N} tests passing
- **Manual:** {N} scenarios verified
- **User confirmed:** {date}

## Lessons Learned

### What Worked
- {positive}

### Challenges
- {challenge} → {resolution}

### Key Insights
- {insight for future}

## Known Limitations
- {limitation}

## Future Improvements
- {potential enhancement}
```

### Step 4: Persist to Engram (CRITICAL)

This is the MOST IMPORTANT engram integration. Persist EVERYTHING valuable.

**Feature completion (REQUIRED):**
```
mcp__plugin_engram-mcp_engram__memory_remember
  content: "COMPLETED: {feature_description}
  
  Approach: {architecture}
  Key files: {main files}
  Pattern: {main pattern used}
  
  Key decision: {most important decision}
  Key lesson: {most valuable insight}
  
  Phases: Discovery → Explore → Requirements → Design → Implement → Review → Testing → Summary"
  tags: ["feature-complete", "{slug}", "{pattern-type}"]
```

**Architecture decision (REQUIRED):**
```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature_type}: {approach} works because {reasons}. Integration: {how it connects}. Watch for: {gotcha}."
  category: "architecture"
  alternatives: ["{other approaches}"]
```

**Most valuable lesson (REQUIRED):**
```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "{key lesson}. Context: {when applies}. Remember: {actionable advice}."
  category: "pattern"
```

**Bug patterns (if any):**
```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Bug in {context}: {issue}. Cause: {cause}. Fix: {solution}. Prevention: {how to avoid}."
  category: "bug_fix"
  root_cause: "{cause}"
```

### Step 5: Sync Session (REQUIRED)

ALWAYS sync to ensure everything indexed:

```
mcp__plugin_engram-mcp_engram__memory_sync
```

### Step 6: Commit Summary

```bash
git add .artifacts/{slug}/
git commit -m "docs({slug}): complete feature summary"
```

### Step 7: Present Completion

Present to user:

```markdown
## Feature Complete!

### {Feature Name}

**Status:** All 8 phases completed

**Artifacts:**
- `progress.md` - Development journey
- `requirements.md` - Specifications
- `design.md` - Architecture
- `plan.md` - Implementation
- `summary.md` - Completion record

**Commits:** {N} total

**Persisted to Memory:**
- Feature summary
- Architecture decision
- Key lessons
```

### Step 8: Offer Push/PR (PAUSE)

Check for unpushed commits:
```bash
git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null || echo "none"
```

If unpushed commits exist, ask:

"Would you like to:
1. Push changes to remote
2. Create a pull request
3. Skip for now"

**Handle response:**

**Push:**
```bash
git push origin $(git branch --show-current)
```

**PR:**
```bash
gh pr create --title "{feature}" --body "## Summary
{description}

## Changes
{file list}

## Testing
- Manual testing completed
- User verified

---
Generated via /harness:feature"
```

**Skip:** Continue to completion

## Critical Rules

1. ALWAYS persist to engram (remember, decision, lesson, sync)
2. ALWAYS mark ALL checklist items complete
3. ALWAYS create summary.md
4. ALWAYS call memory_sync
5. Output "" (special signal for orchestrator)

## Why This Phase Matters

The Summary phase creates **compound learning**:
- Future `/harness:feature` searches find past completions
- Architecture decisions inform similar features
- Lessons prevent repeated mistakes
- Completion records track what was built
