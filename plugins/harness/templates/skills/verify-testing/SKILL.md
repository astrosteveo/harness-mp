---
name: harness:verify-testing
description: Generates manual testing checklist based on requirements and guides user through verification. Tracks test results and handles issue fixes. Use after code review to verify the feature works correctly.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
context: fork
---

# Verify Testing

You are helping a developer verify a feature works correctly through manual testing.

**Progress is saved to `.artifacts/{feature-slug}/` for session continuity.**

---

## Goal

User verifies the feature works correctly through hands-on testing.

**DO NOT SKIP**: The feature cannot be closed out until the user has manually tested and confirmed it works.

---

## Instructions

Feature context: $ARGUMENTS

### Actions

1. Read the `requirements.md` to understand what needs to be tested
2. Present the user with a clear testing checklist based on the requirements
3. Explain how to test each aspect of the feature (what to do, what to expect)
4. **Ask the user to perform the tests and report back**
5. Wait for user confirmation that testing passed
6. If issues are found:
   - Document the issue
   - Fix it
   - Commit the fix
   - Ask user to re-test that specific scenario
7. Only proceed to Summary phase after user explicitly confirms: "Testing passed" or equivalent

### Testing Checklist Format

```markdown
## Manual Testing Checklist

Please test the following and confirm each works:

### Test 1: {Test Name}
**Steps**:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected Result**: {What should happen}

---

### Test 2: {Test Name}
**Steps**:
1. {Step 1}
2. {Step 2}

**Expected Result**: {What should happen}

---

Please reply with:
- PASS or FAIL for each test
- Any issues or unexpected behavior observed
```

### Artifact

Update `progress.md` with testing results:

```markdown
## Manual Testing
- Tested by: User
- Date: {date}
- Result: PASSED / FAILED

### Test Results
| Test | Result | Notes |
|------|--------|-------|
| {test name} | PASS/FAIL | {any notes} |

### Issues Found & Fixed
- {issue description} → Fixed in commit {hash}
```

### Git Commits

- After user reports issues: `fix({feature-slug}): {describe fix from testing}`
- After testing passes: `docs({feature-slug}): record successful manual testing`

---

## Next Steps

After testing passes, guide the user to use:
- `/harness:summarize-feature` to document what was accomplished
