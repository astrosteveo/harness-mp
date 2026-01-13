---
name: harness:workflow-testing
description: This skill should be used when the user asks to "test the feature", "verify it works", "run manual testing", or when the harness:feature orchestrator invokes the Testing phase.
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(npm:*)
  - Bash(yarn:*)
  - Bash(pnpm:*)
  - Bash(pytest:*)
  - Bash(cargo:*)
  - Bash(go:*)
  - Bash(make:*)
  - AskUserQuestion
  - mcp__plugin_engram-mcp_engram__*
hooks:
  Stop:
    - prompt: |
        Before completing, validate:
        1. progress.md shows "Phase: Testing"
        2. Test checklist was presented to user
        3. User confirmed testing passed OR issues were fixed and re-tested
        4. Testing results documented in progress.md

        If validation fails, output what's missing. If passes, output "PHASE_COMPLETE".
---

# Testing Phase - User Verification

This phase guides user through testing and verifies the feature works correctly.

**CRITICAL:** This phase cannot be skipped. Features require user verification before completion.

## Context

**If invoked via orchestrator:** Receives `$ARGUMENTS`:
- `feature_slug`: Feature identifier
- `feature_description`: What was built
- `artifacts_path`: Path to `.artifacts/{slug}/`

**If invoked directly:** Check for recent implementation. If testing standalone, ask what feature to test.

## Phase Execution

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Implementation and review status
- `{artifacts_path}/requirements.md` - What needs to be verified
- `{artifacts_path}/design.md` - Expected behavior

Search engram for testing patterns:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} testing verification"
  n_results: 3
```

### Step 2: Update Progress

Edit `progress.md`:
- Set Phase to "Testing"
- Check off "Code Review"
- Add session log entry

### Step 3: Run Automated Tests (if applicable)

Check for and run existing test suites:

```bash
# Detect test runner and run
npm test  # or yarn test, pytest, cargo test, go test, etc.
```

Report results:
- Tests passing: ✓
- Tests failing: List failures
- No tests: Note this

If tests fail:
1. Identify failing tests
2. Determine if failure is from new code or existing issue
3. Fix if from new code, commit: `fix({slug}): fix failing test`

### Step 4: Generate Manual Test Checklist

Based on requirements.md, create a testing checklist:

```markdown
## Manual Testing Checklist

Please test each scenario and report PASS or FAIL.

---

### Test 1: {Core Functionality}
**What to test:** {description}
**Steps:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected result:** {what should happen}

**Your result:** PASS / FAIL

---

### Test 2: {Secondary Functionality}
**What to test:** {description}
**Steps:**
1. {Step 1}
2. {Step 2}

**Expected result:** {what should happen}

**Your result:** PASS / FAIL

---

### Test 3: {Edge Case}
**What to test:** {description}
**Steps:**
1. {Step 1}

**Expected result:** {what should happen}

**Your result:** PASS / FAIL

---

### Test 4: {Error Handling}
**What to test:** {description}
**Steps:**
1. {Trigger error condition}

**Expected result:** {graceful error handling}

**Your result:** PASS / FAIL

---

Please complete testing and report results.
```

### Step 5: Present Checklist and Wait

**PAUSE POINT - CRITICAL**

Present the testing checklist to user.

Ask: "Please test each scenario and let me know the results."

**DO NOT PROCEED** until user reports testing results.

Acceptable responses:
- "All passed" / "Testing passed" → Proceed to documentation
- "Test N failed: {description}" → Handle failure
- Individual PASS/FAIL for each test → Process results

### Step 6: Handle Test Failures

If any tests reported as FAIL:

1. **Understand the failure**
   - Ask for details: What happened vs. expected?
   - Ask for error messages if any

2. **Diagnose the issue**
   - Read relevant code
   - Identify root cause

3. **Fix the issue**
   - Make minimal fix
   - Commit: `fix({slug}): {description of fix}`

4. **Request re-test**
   - Ask user to re-test the specific scenario
   - Wait for confirmation

5. **Repeat until passing**

Record fix in engram:
```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Testing {feature}: Found {issue} when {scenario}. Fix: {solution}."
  category: "bug_fix"
  root_cause: "{cause}"
```

### Step 7: Document Testing Results

Add to `progress.md`:

```markdown
## Testing

### Date
{YYYY-MM-DD}

### Automated Tests
- Status: {PASSED / FAILED / N/A}
- Tests run: {N}
- Passed: {N}
- Failed: {N}

### Manual Testing

| Test | Description | Result | Notes |
|------|-------------|--------|-------|
| 1 | {Core functionality} | PASS | - |
| 2 | {Secondary functionality} | PASS | - |
| 3 | {Edge case} | PASS | - |
| 4 | {Error handling} | PASS | - |

### Issues Found During Testing
| Issue | Resolution |
|-------|------------|
| {issue} | Fixed in commit {hash} |

### Verification
- [ ] All automated tests passing
- [x] Manual testing completed
- [x] User confirmed feature works as expected
```

### Step 8: Get Final Confirmation

Ask user for explicit confirmation:

"Testing complete. All scenarios passed. Do you confirm the feature is working correctly?"

Wait for explicit "yes" / "confirmed" / "looks good" before proceeding.

### Step 9: Commit Testing Results

Commit testing documentation and any fixes:

```bash
git add .artifacts/{feature-slug}/
git add -u  # stage any files modified during bug fixes
git commit -m "docs({feature-slug}): record successful testing"
```

### Step 10: Prepare Handoff

Summarize for Summary phase:
- Testing status: PASSED
- Any issues found and fixed during testing
- User confirmation received

## Completion Criteria

Stop hook validates:
1. `progress.md` updated with "Phase: Testing"
2. Test checklist was presented
3. User confirmed testing passed (or issues fixed and re-tested)
4. Testing results documented

## Important Notes

- **Never auto-pass testing** - Always require user verification
- **Never skip re-testing** - If something was fixed, it must be re-tested
- **Document everything** - Testing results are important artifacts

## Engram Integration

| When | Tool | Purpose |
|------|------|---------|
| Start | `memory_search` | Find testing patterns |
| During | `memory_lesson` | Record bugs found |
| End | (auto via hooks) | Session indexed |
