---
name: harness:workflow-summary
description: This skill should be used when the user asks to "summarize the feature", "complete the feature", "wrap up", or when the harness:feature orchestrator invokes the Summary phase.
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(git:*)
  - mcp__plugin_engram-mcp_engram__*
hooks:
  Stop:
    - prompt: |
        Before completing, validate:
        1. progress.md shows "Phase: Summary" with all items checked
        2. summary.md exists with all sections completed
        3. Memory was persisted to engram (memory_remember called)
        4. Session was synced (memory_sync called)

        If validation fails, output what's missing. If passes, output "WORKFLOW_COMPLETE".
---

# Summary Phase - Completion and Documentation

This phase documents the completed feature and persists learnings for future sessions.

## Context

**If invoked via orchestrator:** Receives `$ARGUMENTS`:
- `feature_slug`: Feature identifier
- `feature_description`: What was built
- `artifacts_path`: Path to `.artifacts/{slug}/`

**If invoked directly:** Check for existing artifacts with completed testing. If found, proceed. If not, note that summary is typically done after testing.

## Phase Execution

### Step 1: Load All Artifacts

Read all phase artifacts:
- `{artifacts_path}/progress.md` - Full journey
- `{artifacts_path}/requirements.md` - What was specified
- `{artifacts_path}/design.md` - Architecture chosen
- `{artifacts_path}/plan.md` - Implementation approach

Also get git history for the feature:
```bash
git log --oneline --since="{start_date}" -- .
```

### Step 2: Update Progress to Final State

Edit `progress.md`:
- Set Phase to "Summary"
- Check off "Testing"
- Mark ALL checklist items as complete
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
```

### Step 3: Create Summary Document

Write `.artifacts/{slug}/summary.md`:

```markdown
# {Feature Name} - Summary

## Completed
{YYYY-MM-DD}

## Overview
{What was built in 2-3 sentences}

## Problem Solved
{What problem this feature addresses}

## Solution
{High-level description of the approach taken}

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | {approach} | {why} |
| {Decision 2} | {choice} | {why} |
| {Decision 3} | {choice} | {why} |

## Files Changed

### New Files
| File | Purpose |
|------|---------|
| `path/to/new.ts` | {what it does} |

### Modified Files
| File | Changes |
|------|---------|
| `path/to/existing.ts` | {what changed} |

## Commits
| Hash | Message |
|------|---------|
| `abc123` | feat({slug}): {message} |
| `def456` | fix({slug}): {message} |

## Testing
- **Automated:** {N} tests, all passing
- **Manual:** {N} scenarios verified
- **User confirmed:** {date}

## Lessons Learned

### What Went Well
- {Positive outcome}
- {Effective approach}

### What Could Improve
- {Challenge faced}
- {Suggestion for next time}

### Key Insights
- {Important learning for future features}

## Known Limitations
- {Any limitations of current implementation}
- {Edge cases not fully handled}

## Future Improvements
- {Potential enhancement}
- {Deferred feature}

## Related Work
- {Link to similar features}
- {Documentation references}
```

### Step 4: Update Roadmap (if exists)

Check for `.artifacts/roadmap.md`:

If exists:
1. Move this feature to "Completed" section
2. Add any deferred items to "Planned" section
3. Update any related items

### Step 5: Persist to Engram - Comprehensive

This is the most important engram integration point. Persist everything valuable.

**Feature completion summary:**
```
mcp__plugin_engram-mcp_engram__memory_remember
  content: "COMPLETED: {feature_description}

Approach: {architecture approach}
Key files: {main files created/modified}
Pattern used: {main pattern}

Key decision: {most important decision and why}
Lesson learned: {most valuable insight}

Duration: {phases completed over N sessions}"
  tags: ["feature-complete", "{slug}", "{pattern-type}", "{tech-stack}"]
```

**Key architectural decision:**
```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature_type} features: {approach} works well because {reasons}. Key integration: {how it connects}. Watch out for: {gotcha}."
  category: "architecture"
  alternatives: ["{other approaches considered}"]
```

**Most valuable lesson:**
```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "{Most important lesson from this feature}. Context: {when this applies}. Remember: {actionable advice}."
  category: "pattern"
```

**If notable bugs were fixed:**
```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Bug pattern in {context}: {issue}. Root cause: {cause}. Fix: {solution}. Prevention: {how to avoid}."
  category: "bug_fix"
  root_cause: "{cause}"
```

### Step 6: Sync Session

Ensure everything is indexed:

```
mcp__plugin_engram-mcp_engram__memory_sync
```

### Step 7: Commit Summary

Commit the summary document:

```bash
git add .artifacts/{feature-slug}/
git commit -m "docs({feature-slug}): complete feature summary"
```

### Step 8: Present Completion Summary

Present final summary to user:

```markdown
## Feature Complete!

### {Feature Name}

**Status:** All 8 phases completed

**Artifacts Created:**
- `progress.md` - Full development journey
- `requirements.md` - Feature specification
- `design.md` - Architecture decision
- `plan.md` - Implementation approach
- `summary.md` - Completion documentation

**Key Accomplishments:**
- {Main thing built}
- {Secondary accomplishment}
- {Third accomplishment}

**Commits:** {N} commits

**Persisted to Memory:**
- Feature summary with tags
- Architectural decision
- Key lessons learned

---

The feature has been fully documented and learnings persisted for future sessions.
```

### Step 9: Offer to Push Changes

Check if there are unpushed commits:

```bash
git log origin/{branch}..HEAD --oneline
```

If there are unpushed commits, ask the user:

"Would you like to push these changes to the remote repository?"

**If user says yes:**
```bash
git push origin {current-branch}
```

**If user wants a PR:**
```bash
gh pr create --title "{feature-name}" --body "## Summary
{Brief description of what was built}

## Changes
{List of main changes}

## Testing
- Manual testing completed
- User verified feature works

---
Generated via /harness:feature workflow"
```

Present the push result or PR URL to the user.

### Step 10: Output Completion Signal

Output "WORKFLOW_COMPLETE" for orchestrator.

## Completion Criteria

Stop hook validates:
1. `progress.md` shows "Phase: Summary" with all checked
2. `summary.md` exists and is complete
3. `memory_remember` was called (feature summary persisted)
4. `memory_sync` was called (session indexed)

Output: "WORKFLOW_COMPLETE" (special signal for orchestrator)

## Engram Integration - Summary Phase is Critical

This phase has the most important engram integration:

| Tool | Content | Purpose |
|------|---------|---------|
| `memory_remember` | Full feature summary | Searchable completion record |
| `memory_decision` | Architecture choice | Inform future similar features |
| `memory_lesson` | Key insights | Compound learning |
| `memory_sync` | Current session | Ensure everything indexed |

**Why this matters:**
- Future features can search "how did we implement X"
- Architecture decisions provide rationale for similar choices
- Lessons prevent repeating mistakes
- Completion records show what was built and when

## Standalone Usage

When invoked directly (not via workflow):
- Can summarize any recent work
- Will still persist to engram
- Useful for documenting ad-hoc implementations
