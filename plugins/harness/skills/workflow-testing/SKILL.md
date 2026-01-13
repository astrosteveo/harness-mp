---
name: harness:workflow-testing
description: This skill should be used when the user asks to "test the feature", "verify it works", "run manual testing", or when the harness:feature orchestrator invokes the Testing phase.
context: fork
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-testing.sh"
          timeout: 10
---

# Testing Phase - User Verification

Guide user through testing and verify the feature works. User confirmation REQUIRED - cannot be skipped.

## Context Parsing

Parse `$ARGUMENTS` for:
- `--slug <name>`: Feature slug
- `--description "<text>"`: Feature description
- `--artifacts <path>`: Artifacts directory path

## Phase Execution

Execute these steps IN ORDER. This phase CANNOT be skipped or auto-passed.

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Implementation and review status
- `{artifacts_path}/requirements.md` - What to verify
- `{artifacts_path}/design.md` - Expected behavior

Search engram:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} testing"
  n_results: 3
```

### Step 2: Update Progress

Edit `progress.md`:
- Change "Phase:" to "Testing"
- Check off "Code Review"
- Add session log entry

### Step 3: Run Automated Tests

Detect and run test suite:

```bash
# Detect framework and run
npm test 2>&1 || yarn test 2>&1 || pytest 2>&1 || cargo test 2>&1 || go test ./... 2>&1
```

Report results:
- **Passing**: "All {N} automated tests pass"
- **Failing**: List failures, investigate
- **None**: "No automated tests found"

If tests fail from new code:
1. Diagnose issue
2. Fix
3. Commit: `fix({slug}): fix failing test`
4. Re-run tests

### Step 4: Generate Manual Test Checklist

Based on requirements.md, create checklist:

```markdown
## Manual Testing Checklist

Test each scenario and report results.

---

### Test 1: {Core Functionality}
**Steps:**
1. {action}
2. {action}
3. {action}

**Expected:** {outcome}

---

### Test 2: {Secondary Feature}
**Steps:**
1. {action}
2. {action}

**Expected:** {outcome}

---

### Test 3: {Edge Case}
**Steps:**
1. {trigger condition}

**Expected:** {graceful handling}

---

### Test 4: {Error Scenario}
**Steps:**
1. {cause error}

**Expected:** {error message/recovery}
```

### Step 5: Present to User (REQUIRED PAUSE)

Present checklist using AskUserQuestion:

"Please test each scenario:

{checklist}

Report: All passed? Or which failed?"

**STOP AND WAIT** for user response.

DO NOT proceed until user explicitly confirms testing.

### Step 6: Handle Failures

If user reports any failure:

1. **Understand**
   - Ask: "What happened vs expected?"
   - Get error messages if any

2. **Diagnose**
   - Read relevant code
   - Identify root cause

3. **Fix**
   - Apply minimal fix
   - Commit: `fix({slug}): {description}`

4. **Re-test**
   - Ask user to re-test that specific scenario
   - Wait for confirmation

5. **Repeat** until all tests pass

Record each fix:
```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Testing {feature}: Found {issue} in {scenario}. Fix: {solution}."
  category: "bug_fix"
  root_cause: "{cause}"
```

### Step 7: Get Final Confirmation (REQUIRED)

After all scenarios tested:

"All test scenarios completed. Do you confirm the feature works correctly?"

**STOP AND WAIT** for explicit "yes" / "confirmed" / "works".

### Step 8: Document Results

Add to `progress.md`:

```markdown
## Testing

### Date
{YYYY-MM-DD}

### Automated Tests
- Status: {PASS/FAIL/N/A}
- Total: {N}
- Passed: {N}

### Manual Testing
| Test | Description | Result |
|------|-------------|--------|
| 1 | {core} | PASS |
| 2 | {secondary} | PASS |
| 3 | {edge case} | PASS |
| 4 | {error} | PASS |

### Issues Fixed During Testing
| Issue | Fix | Commit |
|-------|-----|--------|
| {issue} | {solution} | {hash} |

### User Confirmation
- Date: {date}
- Status: CONFIRMED
```

### Step 9: Commit Testing Results

```bash
git add .artifacts/{slug}/
git commit -m "docs({slug}): record successful testing"
```

## Critical Rules

1. NEVER auto-pass testing - user MUST confirm
2. ALWAYS present manual test checklist
3. ALWAYS wait for explicit user confirmation
4. ALWAYS fix and re-test failures before proceeding
5. ALWAYS document all test results
