---
name: harness:workflow-review
description: This skill should be used when the user asks to "review the code", "check for issues", "code review", or when the harness:feature orchestrator invokes the Review phase.
context: fork
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-review.sh"
          timeout: 10
---

# Review Phase - Code Quality Verification

Review implemented code for quality, bugs, and consistency. Auto-proceed unless high-priority issues found.

## Context Parsing

Parse `$ARGUMENTS` for:
- `--slug <name>`: Feature slug
- `--description "<text>"`: Feature description
- `--artifacts <path>`: Artifacts directory path

## Phase Execution

Execute these steps IN ORDER. Do NOT skip steps.

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Implementation details
- `{artifacts_path}/design.md` - Expected architecture
- `{artifacts_path}/requirements.md` - Specifications

Get changed files:
```bash
git diff --name-only HEAD~{commits}
```

Search engram:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} review issues"
  n_results: 3
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "code review"
  insight_type: "lesson"
  n_results: 5
```

### Step 2: Update Progress

Edit `progress.md`:
- Change "Phase:" to "Review"
- Check off "Implementation"
- Add session log entry

### Step 3: Launch Reviewer Agents

Launch 3 parallel agents:

**Agent 1: Code Quality**
```
Task
  subagent_type: "harness:code-reviewer"
  prompt: "Review for CODE QUALITY:
           Files: {changed files}
           
           Check: Readability, DRY, naming, complexity.
           
           Report: Severity (High/Medium/Low), file:line, fix suggestion.
           Confidence threshold: 80+"
```

**Agent 2: Bugs and Logic**
```
Task
  subagent_type: "harness:code-reviewer"
  prompt: "Review for BUGS AND LOGIC:
           Files: {changed files}
           Requirements: {from requirements.md}
           
           Check: Logic errors, edge cases, null handling, security.
           
           Report: Severity, file:line, fix suggestion.
           Confidence threshold: 80+"
```

**Agent 3: Consistency**
```
Task
  subagent_type: "harness:code-reviewer"
  prompt: "Review for CONSISTENCY:
           Files: {changed files}
           Patterns: {from exploration}
           
           Check: Matches codebase patterns, conventions, integration.
           
           Report: Severity, file:line, fix suggestion.
           Confidence threshold: 80+"
```

### Step 4: Consolidate Findings

After agents complete, categorize all issues:

**High Priority** (must address):
- Security vulnerabilities
- Logic bugs causing incorrect behavior
- Breaking changes

**Medium Priority** (should address):
- Code quality issues
- Minor inconsistencies
- Missing edge case handling

**Low Priority** (nice to have):
- Style preferences
- Minor naming suggestions

De-duplicate overlapping findings.

### Step 5: Handle Issues (CONDITIONAL PAUSE)

**IF NO HIGH PRIORITY ISSUES:**
- Auto-fix medium priority issues that are straightforward
- Note: "Review complete. {N} minor issues addressed."
- Continue automatically

**IF HIGH PRIORITY ISSUES EXIST:**
- Present findings to user
- Ask: "Found {N} high priority issues. Fix now?"
- **PAUSE AND WAIT** for response
- Fix based on user decision

### Step 6: Apply Fixes

For each issue to fix:
1. Read the file
2. Apply the fix
3. Commit:
   ```bash
   git commit -m "fix({slug}): {description}"
   ```

For deferred issues:
- Document in progress.md as "Deferred: {reason}"

For accepted risks:
- Document in progress.md as "Accepted: {reason}"

### Step 7: Document Review

Add to `progress.md`:

```markdown
## Code Review

### Date
{YYYY-MM-DD}

### Issues
| Severity | Issue | File | Resolution |
|----------|-------|------|------------|
| High | {issue} | `file:line` | Fixed/Deferred/Accepted |
| Medium | {issue} | `file:line` | Fixed/Deferred |
| Low | {issue} | `file:line` | Fixed/Deferred |

### Summary
- Found: {N}
- Fixed: {N}
- Deferred: {N}
- Accepted: {N}

### Fix Commits
- `{hash}` - fix({slug}): {message}
```

### Step 8: Persist to Engram

```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Review of {feature}: Found {issue_type} in {context}. Fix: {solution}."
  category: "bug_fix"
  root_cause: "{cause}"
```

### Step 9: Commit Review Results

```bash
git add .artifacts/{slug}/
git commit -m "docs({slug}): complete code review"
```

## Critical Rules

1. ALWAYS launch all 3 reviewer agents
2. ALWAYS document all findings in progress.md
3. PAUSE only if high priority issues exist
4. Auto-proceed if no high priority issues
5. ALWAYS record lessons for significant bugs
