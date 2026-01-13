---
name: harness:workflow-review
description: This skill should be used when the user asks to "review the code", "check for issues", "code review", or when the harness:feature orchestrator invokes the Review phase.
context: fork
agent: general-purpose
allowed-tools:
  - Task
  - Read
  - Edit
  - Glob
  - Grep
  - Bash(git:*)
  - AskUserQuestion
  - mcp__plugin_engram-mcp_engram__*
hooks:
  Stop:
    - prompt: |
        Before completing, validate:
        1. progress.md shows "Phase: Review"
        2. Review findings were documented in progress.md
        3. User decided on each high-priority issue (fix/defer/accept)
        4. Any fixes requested were applied

        If validation fails, output what's missing. If passes, output "PHASE_COMPLETE".
---

# Review Phase - Code Quality Verification

This phase reviews implemented code for quality, bugs, and consistency.

## Context

**If invoked via orchestrator:** Receives `$ARGUMENTS`:
- `feature_slug`: Feature identifier
- `feature_description`: What was built
- `artifacts_path`: Path to `.artifacts/{slug}/`

**If invoked directly:** Check for recent changes via `git diff`. If no changes, ask what code to review.

## Phase Execution

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Implementation summary
- `{artifacts_path}/design.md` - Expected architecture
- `{artifacts_path}/requirements.md` - What was supposed to be built

Get list of changed files:
```bash
git diff --name-only HEAD~{n}  # or appropriate range
```

Search engram for review context:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} code review issues"
  n_results: 3
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "code review {feature_type}"
  insight_type: "lesson"
  n_results: 5
```

Past review lessons help focus on common issues.

### Step 2: Update Progress

Edit `progress.md`:
- Set Phase to "Review"
- Check off "Implementation"
- Add session log entry

### Step 3: Launch Reviewer Agents

Launch 3 reviewer agents in parallel:

**Agent 1: Code Quality Review**
```
Task with subagent_type: "harness:code-reviewer"
prompt: "Review these files for CODE QUALITY:
{list of changed files}

Focus on:
- Simplicity and readability
- DRY violations
- Code elegance
- Naming clarity
- Comment quality (only where needed)

Requirements context: {key requirements}
Design context: {chosen approach}

Report issues with severity (High/Medium/Low) and specific line references."
```

**Agent 2: Bug and Logic Review**
```
Task with subagent_type: "harness:code-reviewer"
prompt: "Review these files for BUGS AND LOGIC ERRORS:
{list of changed files}

Focus on:
- Logic errors
- Edge cases not handled
- Null/undefined issues
- Race conditions
- Error handling gaps
- Security vulnerabilities

Requirements context: {key requirements}

Report issues with severity and specific line references."
```

**Agent 3: Consistency Review**
```
Task with subagent_type: "harness:code-reviewer"
prompt: "Review these files for CODEBASE CONSISTENCY:
{list of changed files}

Focus on:
- Matches existing patterns
- Follows project conventions
- Consistent with similar features
- Proper use of existing utilities
- Integration correctness

Codebase patterns: {from exploration phase}

Report issues with severity and specific line references."
```

### Step 4: Consolidate Findings

After agents complete, consolidate all findings:

**High Priority** - Should fix before proceeding
- Security vulnerabilities
- Logic bugs
- Breaking changes

**Medium Priority** - Consider fixing
- Code quality issues
- Minor inconsistencies
- Missed edge cases

**Low Priority** - Nice to have
- Style preferences
- Minor naming suggestions
- Optional improvements

De-duplicate overlapping findings across reviewers.

### Step 5: Present Findings

Present consolidated findings to user:

```markdown
## Code Review Results

### High Priority Issues ({N})

#### Issue 1: {Title}
- **File:** `path/to/file.ts:{line}`
- **Severity:** High
- **Category:** {Bug/Security/Breaking}
- **Description:** {what's wrong}
- **Recommendation:** {how to fix}

...

### Medium Priority Issues ({N})
...

### Low Priority Issues ({N})
...

### Summary
- Total issues: {N}
- High: {N} | Medium: {N} | Low: {N}
```

**PAUSE POINT**

Ask: "How would you like to proceed?"
- Fix all high priority now
- Fix high + medium now
- Review each and decide
- Proceed as-is (accept risks)

### Step 6: Apply Fixes

Based on user decision:

**If fixing issues:**
1. Address each issue in priority order
2. Commit fixes:
   ```
   fix({slug}): {description of fix}
   ```
3. Mark issue as resolved

**If deferring issues:**
1. Document in progress.md as "Deferred"
2. Note reason for deferral

**If accepting risks:**
1. Document in progress.md as "Accepted"
2. Note user accepted the risk

### Step 7: Document Review Results

Add to `progress.md`:

```markdown
## Code Review

### Review Date
{YYYY-MM-DD}

### Issues Found

| Severity | Issue | File | Resolution |
|----------|-------|------|------------|
| High | {issue} | `file:line` | Fixed/Deferred/Accepted |
| Medium | {issue} | `file:line` | Fixed/Deferred/Accepted |
| Low | {issue} | `file:line` | Fixed/Deferred/Accepted |

### Summary
- Total found: {N}
- Fixed: {N}
- Deferred: {N}
- Accepted: {N}

### Commits
- `{hash}` - fix({slug}): {message}
```

### Step 8: Persist Lessons to Engram

If notable issues found:

```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Review of {feature_type}: Found {issue_type} in {context}. Fix: {solution}."
  category: "bug_fix"
  root_cause: "{cause}"
```

If review revealed pattern issues:

```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "When implementing {pattern}: Watch for {issue}. Better approach: {recommendation}."
  category: "anti_pattern"
```

### Step 9: Commit Review Results

Commit the review documentation (and any remaining fixes):

```bash
git add .artifacts/{feature-slug}/
git add -u  # stage any modified files from fixes
git commit -m "docs({feature-slug}): complete code review"
```

### Step 10: Prepare Handoff

Summarize for Testing phase:
- Review status (all clear / issues remaining)
- Key areas that need testing attention
- Any deferred issues to be aware of

## Completion Criteria

Stop hook validates:
1. `progress.md` updated with "Phase: Review"
2. Review findings documented
3. User decided on high-priority issues
4. Fixes applied if requested

## Engram Integration

| When | Tool | Purpose |
|------|------|---------|
| Start | `memory_search` | Find similar review issues |
| Start | `memory_insights` | Get past review lessons |
| End | `memory_lesson` | Record bugs found |
| End | `memory_lesson` | Record anti-patterns |
