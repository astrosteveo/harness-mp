# Manual Test Checklist Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use harness:executing-plans to implement this plan task-by-task.

**Goal:** Add manual test checklist sections to plans, presented at appropriate checkpoints during execution.

**Architecture:** Modify three skill files: writing-plans gets checklist template + author guidance, executing-plans gets batch-level checklist presentation, subagent-driven-development gets end-of-work checklist checkpoint.

**Tech Stack:** Markdown skill files only - no code changes.

---

### Task 1: Add Manual Test Checklist Section to writing-plans

**Files:**
- Modify: `plugins/harness/skills/writing-plans/SKILL.md:89-96`

**Step 1: Add new section after "Remember" section**

Insert the following after line 95 (after the "Remember" bullet list, before "## Execution Handoff"):

```markdown

## Manual Test Checklist Section

Every plan ends with a Manual Test Checklist. This goes after all tasks, before any closing notes.

**Template:**

```markdown
---

## Manual Test Checklist

> **For Claude:** Present this checklist at appropriate checkpoints.
> - subagent-driven-development: after all tasks, before finishing-a-development-branch
> - executing-plans: relevant items after each batch

### [Component/Area Name]
<!-- Tasks N-M -->

- [ ] [Concrete action] → [Expected result]
```

**Format:** `- [ ] [Action] → [Expected result]`

**What to include:**
- User-facing behavior automated tests don't fully cover
- Visual/UI verification (layout, styling, responsiveness)
- Integration points (API calls, database state, external services)
- Error states and edge cases worth human verification

**What NOT to include:**
- Things fully covered by automated tests
- Internal implementation details user can't observe
- Vague items ("make sure it works")

**Task mapping:** Add `<!-- Tasks N-M -->` comment after each group heading so executing-plans can identify relevant items per batch.

**Example:**

```markdown
## Manual Test Checklist

### Authentication
<!-- Tasks 1-3 -->

- [ ] Login with valid credentials → Redirects to /dashboard, shows username
- [ ] Login with wrong password → Shows "Invalid credentials" error
- [ ] Click "Logout" → Returns to /login, clears session

### Dashboard
<!-- Tasks 4-5 -->

- [ ] Load with no data → Shows empty state message
- [ ] Create item → Appears in list without refresh
```
```

**Step 2: Verify the edit**

Open the file and confirm:
- New section appears between "## Remember" and "## Execution Handoff"
- Markdown formatting is correct (no syntax errors)
- Template shows task mapping comments

**Step 3: Commit**

```bash
git add plugins/harness/skills/writing-plans/SKILL.md
git commit -m "feat(writing-plans): add manual test checklist section template"
```

---

### Task 2: Add Manual Test Checkpoint to subagent-driven-development

**Files:**
- Modify: `plugins/harness/skills/subagent-driven-development/SKILL.md:79-82`

**Step 1: Update the process flowchart**

Find this section (around line 59-82):
```
    "More tasks remain?" -> "Dispatch final code reviewer subagent for entire implementation" [label="no"];
    "Dispatch final code reviewer subagent for entire implementation" -> "Use harness:finishing-a-development-branch";
```

Replace with:
```
    "More tasks remain?" -> "Present Manual Test Checklist to user" [label="no"];
    "Present Manual Test Checklist to user" [shape=box];
    "User confirms manual tests pass?" [shape=diamond];
    "User reports issues" [shape=box];
    "Dispatch fix subagent" [shape=box];
    "Present Manual Test Checklist to user" -> "User confirms manual tests pass?";
    "User confirms manual tests pass?" -> "Dispatch final code reviewer subagent for entire implementation" [label="yes"];
    "User confirms manual tests pass?" -> "User reports issues" [label="no"];
    "User reports issues" -> "Dispatch fix subagent";
    "Dispatch fix subagent" -> "Present Manual Test Checklist to user";
    "Dispatch final code reviewer subagent for entire implementation" -> "Use harness:finishing-a-development-branch";
```

**Step 2: Add Manual Test Checkpoint section**

Insert after "## Prompt Templates" section (after line 89), before "## Example Workflow":

```markdown

## Manual Test Checkpoint

After all tasks complete, before final code review:

1. **Extract checklist from plan** - Find the "## Manual Test Checklist" section
2. **Present to user:**

```
All tasks implemented and reviewed. Before final review, please verify manually:

### [Component]
- [ ] [Action] → [Expected result]
...

Let me know when complete, or report any issues found.
```

3. **Wait for user response**
4. **If issues reported:** Dispatch fix subagent with specific instructions
5. **If confirmed:** Proceed to final code reviewer

**Never skip this checkpoint** - user verification catches issues automated tests miss.
```

**Step 3: Update Example Workflow**

Find line 158-164:
```
...

[After all tasks]
[Dispatch final code-reviewer]
Final reviewer: All requirements met, ready to merge

Done!
```

Replace with:
```
...

[After all tasks]
[Present Manual Test Checklist from plan]

"All tasks implemented. Please verify manually:

### Authentication
- [ ] Login with valid credentials → Redirects to /dashboard
- [ ] Click Logout → Returns to /login

Let me know when complete, or report issues."

User: "All good, verified both items."

[Dispatch final code-reviewer]
Final reviewer: All requirements met, ready to merge

Done!
```

**Step 4: Verify the edit**

Open the file and confirm:
- Flowchart includes new checkpoint node
- New section explains the checkpoint process
- Example workflow shows the checkpoint in action

**Step 5: Commit**

```bash
git add plugins/harness/skills/subagent-driven-development/SKILL.md
git commit -m "feat(subagent-driven-dev): add manual test checkpoint after all tasks"
```

---

### Task 3: Add Batch-Level Manual Tests to executing-plans

**Files:**
- Modify: `plugins/harness/skills/executing-plans/SKILL.md:33-38`

**Step 1: Update Step 3 (Report)**

Find lines 33-38:
```markdown
### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."
```

Replace with:
```markdown
### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- **Show relevant manual test items** (from plan's Manual Test Checklist, filtered by task numbers in `<!-- Tasks N-M -->` comments)
- Say: "Ready for feedback. Please verify manual tests above."

**Manual test presentation:**
```
**Manual tests for this batch:**

### [Component]
- [ ] [Action] → [Expected result]
```

If plan has no Manual Test Checklist section, skip this part.
```

**Step 2: Add guidance for final batch**

Find lines 45-50 (Step 5):
```markdown
### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use harness:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice
```

Replace with:
```markdown
### Step 5: Complete Development

After all tasks complete and verified:
- Present any remaining manual test items not yet shown
- Wait for user confirmation that all manual tests pass
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use harness:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice
```

**Step 3: Verify the edit**

Open the file and confirm:
- Step 3 includes manual test presentation
- Step 5 includes final manual test confirmation
- Instructions are clear about filtering by task comments

**Step 4: Commit**

```bash
git add plugins/harness/skills/executing-plans/SKILL.md
git commit -m "feat(executing-plans): add batch-level manual test presentation"
```

---

## Manual Test Checklist

### writing-plans skill
<!-- Task 1 -->

- [ ] Open writing-plans/SKILL.md → New "Manual Test Checklist Section" appears between "Remember" and "Execution Handoff"
- [ ] Template shows correct format with task mapping comments
- [ ] Example shows grouped checklist items with component headers

### subagent-driven-development skill
<!-- Task 2 -->

- [ ] Open subagent-driven-development/SKILL.md → Flowchart includes "Present Manual Test Checklist" node after "More tasks remain? no"
- [ ] New "Manual Test Checkpoint" section explains the process
- [ ] Example workflow shows checkpoint interaction with user

### executing-plans skill
<!-- Task 3 -->

- [ ] Open executing-plans/SKILL.md → Step 3 mentions manual test presentation
- [ ] Step 5 includes final manual test confirmation before finishing
- [ ] Instructions explain task filtering via comments
