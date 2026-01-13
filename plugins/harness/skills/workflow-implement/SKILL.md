---
name: harness:workflow-implement
description: This skill should be used when the user asks to "implement the feature", "write the code", "build it", or when the harness:feature orchestrator invokes the Implement phase.
context: fork
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-implement-pretool.sh"
          timeout: 5
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-implement.sh"
          timeout: 10
---

# Implement Phase - Building the Feature

Implement the feature according to the approved design. User approval of plan required before coding.

## Context Parsing

Parse `$ARGUMENTS` for:
- `--slug <name>`: Feature slug
- `--description "<text>"`: Feature description
- `--artifacts <path>`: Artifacts directory path
- `--tdd`: Enable test-driven development mode

## Phase Execution

Execute these steps IN ORDER. The PreToolUse hook logs all Write/Edit operations.

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Current state
- `{artifacts_path}/requirements.md` - What to build
- `{artifacts_path}/design.md` - How to build

Search engram:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} implementation"
  n_results: 5
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "implementation {feature_type}"
  insight_type: "lesson"
  n_results: 5
```

Past lessons (bugs, gotchas) are critical here.

### Step 2: Update Progress

Edit `progress.md`:
- Change "Phase:" to "Implement"
- Check off "Architecture Design"
- Add session log entry

### Step 3: Create Implementation Plan (REQUIRED FIRST)

BEFORE writing any source code, create `.artifacts/{slug}/plan.md`:

```markdown
# {Feature Name} - Implementation Plan

## Approach
{from design.md}

## Files to Modify
| File | Changes | Order |
|------|---------|-------|
| `path/file` | {changes} | 1 |

## Files to Create
| File | Purpose | Order |
|------|---------|-------|
| `path/file` | {purpose} | 2 |

## Implementation Steps

### Step 1: {Component}
- [ ] {task}
- [ ] {task}

### Step 2: {Component}
- [ ] {task}
- [ ] {task}

## Testing Strategy
{how to verify}

## Commit Strategy
{logical commit points}
```

### Step 4: Get Plan Approval (REQUIRED PAUSE)

Present plan to user using AskUserQuestion:

"Here is the implementation plan:

{plan summary}

Ready to proceed with implementation?"

**STOP AND WAIT** for explicit approval.

Acceptable responses: "yes", "proceed", "go ahead", "approved", "looks good"

### Step 5A: Implement (Standard Mode)

If NOT in TDD mode:

1. **Work through steps in order**
   - Read files before modifying
   - Make focused, minimal changes
   - Follow codebase conventions

2. **Commit frequently**
   ```bash
   git add -A
   git commit -m "feat({slug}): {description}"
   ```

3. **Update plan.md progress**
   - Check off completed steps
   - Note deviations

### Step 5B: Implement (TDD Mode)

If `--tdd` flag set:

For each feature requirement:

1. **RED** - Write failing test
   ```bash
   # Run test, confirm failure
   ```
   ```bash
   git commit -m "test({slug}): add failing test for {behavior}"
   ```

2. **GREEN** - Minimum code to pass
   ```bash
   # Run test, confirm pass
   ```
   ```bash
   git commit -m "feat({slug}): implement {behavior}"
   ```

3. **REFACTOR** - Clean up
   ```bash
   git commit -m "refactor({slug}): {description}"
   ```

### Step 6: Record Lessons

If bugs or gotchas discovered:

```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "When implementing {type}: {lesson}. Cause: {cause}."
  category: "bug_fix"
  root_cause: "{cause}"
```

If useful patterns emerged:

```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Pattern for {type}: {pattern}. Works because {reason}."
  category: "pattern"
```

### Step 7: Update Progress

Add to `progress.md`:

```markdown
## Implementation

### Files Changed
| File | Changes |
|------|---------|
| `path` | {summary} |

### Files Created
| File | Purpose |
|------|---------|
| `path` | {purpose} |

### Commits
- `{hash}` - {message}

### Deviations
{any changes from plan}

### Issues Encountered
| Issue | Resolution |
|-------|------------|
| {issue} | {how fixed} |
```

## Critical Rules

1. ALWAYS create plan.md BEFORE any source code
2. ALWAYS get user approval of plan
3. ALWAYS commit frequently with conventional messages
4. ALWAYS record lessons for bugs/gotchas discovered
