# Manual Test Checklist Feature Design

**Goal:** Add manual test checklists to implementation plans, presented to users at appropriate checkpoints during execution.

**Problem:** Current workflow automates testing via TDD but doesn't give users a structured way to manually verify the full surface area of changes before completing work.

---

## Design

### 1. Plan Document Changes

The `writing-plans` skill adds a **Manual Test Checklist** section to every plan. Goes after all tasks, before closing notes.

**Template:**

```markdown
---

## Manual Test Checklist

> **For Claude:** Present this checklist to the user at the appropriate checkpoint.
> For subagent-driven: after all tasks complete, before finishing-a-development-branch.
> For batch execution: after each batch completes.

### [Component/Area Name]
<!-- Tasks N-M -->

- [ ] [Action to perform] → [Expected result]
- [ ] [Action to perform] → [Expected result]

### [Another Component]
<!-- Tasks X-Y -->

- [ ] [Action to perform] → [Expected result]
```

**Example:**

```markdown
## Manual Test Checklist

### Authentication
<!-- Tasks 1-3 -->

- [ ] Login with valid credentials → Redirects to /dashboard, shows username in header
- [ ] Login with wrong password → Shows "Invalid credentials", stays on login page
- [ ] Click "Logout" → Returns to /login, clears session cookie

### Dashboard
<!-- Tasks 4-5 -->

- [ ] Load dashboard with no data → Shows "No items yet" empty state
- [ ] Create new item → Item appears in list without page refresh
```

---

### 2. Execution Skill Changes

#### subagent-driven-development

After all tasks complete, before dispatching final code reviewer:

1. Present full Manual Test Checklist to user
2. Wait for user confirmation or issue reports
3. If issues: dispatch fix subagent
4. If confirmed: proceed to final code reviewer → finishing-a-development-branch

**Flow addition:**

```
[All tasks complete]
[Present Manual Test Checklist]

"All tasks implemented and reviewed. Before final review, please verify manually:

### Authentication
- [ ] Login with valid credentials → Redirects to /dashboard
...

Let me know when you've completed manual testing, or if you found issues."

[User confirms or reports issues]
[Handle accordingly]
[Proceed to final review]
```

#### executing-plans

After each batch completes, include relevant checklist items in report:

1. Identify which checklist groups map to completed tasks (via `<!-- Tasks N-M -->` comments)
2. Present those items in batch report
3. Wait for user feedback including manual test results

**Flow addition:**

```
Batch 1 complete (Tasks 1-3).

**What was implemented:**
- Task 1: Login endpoint
- Task 2: Session management
- Task 3: Logout endpoint

**Manual tests for this batch:**

### Authentication
- [ ] Login with valid credentials → Redirects to /dashboard
- [ ] Click "Logout" → Returns to /login

Ready for feedback. Please verify manual tests above.
```

---

### 3. Guidance for Plan Authors

Add to `writing-plans` SKILL.md:

**Format:**
- [ ] [Concrete action] → [Observable expected result]

**What to include:**
- User-facing behavior that automated tests don't fully cover
- Visual/UI verification (layout, styling, responsiveness)
- Integration points (API calls, database state, external services)
- Error states and edge cases worth human verification
- Anything the implementer can't verify themselves

**What NOT to include:**
- Things fully covered by automated tests (don't duplicate)
- Internal implementation details user can't observe
- Vague items ("make sure it works")

**Mapping to batches:**
Add `<!-- Tasks N-M -->` comment after each group heading so executing-plans can identify relevant items per batch.

---

## Files to Modify

| File | Change |
|------|--------|
| `skills/writing-plans/SKILL.md` | Add Manual Test Checklist section template and author guidance |
| `skills/subagent-driven-development/SKILL.md` | Add checkpoint after all tasks to present checklist, wait for confirmation |
| `skills/executing-plans/SKILL.md` | Add checklist presentation to batch report step |

---

## Notes

- Commits already happen per task (baked into writing-plans task structure) - no changes needed
- Checklist items grouped by component for easy navigation
- Task mapping comments enable batch-appropriate presentation in executing-plans
