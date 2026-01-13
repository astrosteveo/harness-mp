---
description: Skill-based feature development workflow
argument-hint: <feature-description> [--phase <name>] [--tdd] [--skip <phase>]
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash(git:*)
  - Bash(ls:*)
  - Skill
  - mcp__plugin_engram-mcp_engram__*
---

# Feature Development Orchestrator

Coordinates feature development through 8 skill-based phases using the `Skill` tool.

## Phase Sequence

```
Discovery → Explore → Requirements → Design → Implement → Review → Testing → Summary
```

Each phase is a skill invoked via `Skill` tool:

| Phase | Skill Name | Purpose |
|-------|------------|---------|
| 1 | `harness:workflow-discovery` | Understand request, create tracking |
| 2 | `harness:workflow-explore` | Map codebase patterns |
| 3 | `harness:workflow-requirements` | Gather specifications |
| 4 | `harness:workflow-design` | Select architecture |
| 5 | `harness:workflow-implement` | Build the feature |
| 6 | `harness:workflow-review` | Code quality check |
| 7 | `harness:workflow-testing` | User verification |
| 8 | `harness:workflow-summary` | Document completion |

## Execution Instructions

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:
- `feature_description`: Everything that is not a flag
- `--phase <name>`: Jump to specific phase
- `--tdd`: Enable test-driven development
- `--skip <phase>`: Skip a phase (can repeat)

If no feature_description provided, ask: "What feature would you like to build?"

### Step 2: Check for Existing Work

Search for prior context:

```
Use: mcp__plugin_engram-mcp_engram__memory_resume
```

Then check artifacts:

```bash
ls -la .artifacts/*/progress.md 2>/dev/null
```

If matching artifacts exist:
1. Read `.artifacts/{slug}/progress.md`
2. Extract current phase from "Phase:" line
3. Resume from that phase

### Step 3: Determine Starting Phase

**Starting phase logic:**
- If `--phase` flag: Start from specified phase
- If matching artifacts found: Resume from saved phase
- Otherwise: Start from `discovery`

### Step 4: Invoke Phase Skill

**To invoke a phase skill, use the Skill tool:**

```
Skill
  skill: "harness:workflow-{phase}"
  args: "--description \"{feature_description}\" --slug {slug}"
```

**Example for discovery phase:**
```
Skill
  skill: "harness:workflow-discovery"
  args: "--description \"add dark mode toggle\""
```

**Example for design phase with existing artifacts:**
```
Skill
  skill: "harness:workflow-design"
  args: "--slug dark-mode-toggle --description \"add dark mode toggle\""
```

### Step 5: Handle Skill Output

After each skill completes, examine its output.

**Skill outputs follow this pattern:**
```
{PHASE} COMPLETE
Slug: {slug}
...
```

When you see `{PHASE} COMPLETE`:
1. Note the slug from output
2. Determine next phase in sequence
3. Check if next phase should be skipped (`--skip`)
4. Invoke next phase skill with the slug

### Step 6: Continue Through Phases

Automatically invoke the next skill after each completion:

| After | Invoke Next |
|-------|-------------|
| `DISCOVERY COMPLETE` | `harness:workflow-explore` |
| `EXPLORE COMPLETE` | `harness:workflow-requirements` |
| `REQUIREMENTS COMPLETE` | `harness:workflow-design` |
| `DESIGN COMPLETE` | `harness:workflow-implement` |
| `IMPLEMENT COMPLETE` | `harness:workflow-review` |
| `REVIEW COMPLETE` | `harness:workflow-testing` |
| `TESTING COMPLETE` | `harness:workflow-summary` |
| `SUMMARY COMPLETE` | Workflow finished |

### Step 7: Handle Blocked States

If a skill outputs `BLOCKED` or an error:
1. Present the issue to user
2. Ask how to proceed: retry, skip, or abort
3. Act accordingly

## Skill Arguments Reference

All skills accept these arguments:

| Argument | Required | Description |
|----------|----------|-------------|
| `--description` | Yes (first phase) | Feature description |
| `--slug` | No | Explicit slug (generated in discovery if not provided) |
| `--tdd` | No | Enable TDD mode |

Pass `--slug` to subsequent phases after discovery creates it.

## Error Recovery

**Skill failure:**
1. Check `.artifacts/{slug}/progress.md` for state
2. Offer to retry from current phase
3. Search engram for similar errors

**Missing artifacts:**
1. Warn user
2. Restart from discovery or specified `--phase`

**User abort:**
1. State saved in `progress.md`
2. Can resume later with `/harness:feature "{description}"`

## Quick Reference

| Command | Result |
|---------|--------|
| `/harness:feature "add auth"` | Start or resume feature |
| `/harness:feature --phase design` | Jump to design phase |
| `/harness:feature --tdd` | Enable TDD mode |
| `/harness:feature --skip explore` | Skip explore phase |

## Example Execution

```
User: /harness:feature "add dark mode toggle"

Orchestrator: Parse arguments → feature_description = "add dark mode toggle"
Orchestrator: Check engram → No prior work found
Orchestrator: Check artifacts → No existing artifacts
Orchestrator: Starting from discovery phase

Orchestrator: Invoking skill...
  Skill(skill: "harness:workflow-discovery", args: "--description \"add dark mode toggle\"")

[Discovery skill runs, creates artifacts]

Skill output:
  DISCOVERY COMPLETE
  Slug: dark-mode-toggle
  Path: .artifacts/dark-mode-toggle/

Orchestrator: Discovery complete. Invoking explore phase...
  Skill(skill: "harness:workflow-explore", args: "--slug dark-mode-toggle --description \"add dark mode toggle\"")

[Explore skill runs]

Skill output:
  EXPLORE COMPLETE
  Slug: dark-mode-toggle

Orchestrator: Explore complete. Invoking requirements phase...
  Skill(skill: "harness:workflow-requirements", args: "--slug dark-mode-toggle --description \"add dark mode toggle\"")

[... continues through all phases ...]

Skill output:
  SUMMARY COMPLETE
  Slug: dark-mode-toggle

Orchestrator: Feature development complete!
```
