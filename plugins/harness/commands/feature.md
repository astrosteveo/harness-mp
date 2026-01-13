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

Coordinates feature development through 8 skill-based phases.

```
PHASES: Discovery → Explore → Requirements → Design → Implement → Review → Testing → Summary
                                   ⏸           ⏸         ⏸          ⏸        ⏸
```

Phases marked ⏸ have pause points requiring user confirmation.

## Phase Skills

| # | Phase | Skill | Purpose |
|---|-------|-------|---------|
| 1 | Discovery | `harness:workflow-discovery` | Understand request, create tracking |
| 2 | Explore | `harness:workflow-explore` | Map codebase patterns |
| 3 | Requirements | `harness:workflow-requirements` | Gather specifications |
| 4 | Design | `harness:workflow-design` | Select architecture |
| 5 | Implement | `harness:workflow-implement` | Build the feature |
| 6 | Review | `harness:workflow-review` | Code quality check |
| 7 | Testing | `harness:workflow-testing` | User verification |
| 8 | Summary | `harness:workflow-summary` | Document completion |

## Orchestration

### Step 1: Parse Arguments

From `$ARGUMENTS` extract:
- `feature_description` (required): What to build
- `--phase <name>`: Jump to specific phase (discovery|explore|requirements|design|implement|review|testing|summary)
- `--tdd`: Enable test-driven development mode
- `--skip <phase>`: Skip a phase (can repeat)

### Step 2: Search Engram for Context

```
mcp__plugin_engram-mcp_engram__memory_resume
```

Check for relevant prior work. If recent session had same feature, note context.

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} feature"
  n_results: 3
```

If similar features found, summarize briefly.

### Step 3: Check for Existing Artifacts

```bash
ls -la .artifacts/*/progress.md 2>/dev/null
```

**If matching artifacts found:**
1. Generate expected slug from `feature_description`
2. Check if `.artifacts/{slug}/progress.md` exists
3. If yes: Read it, extract current phase from "Phase:" line
4. Announce: "Resuming **{feature}** from **{phase}** phase"
5. Set `current_phase` to that phase

**If no matching artifacts AND no `--phase` flag:**
1. Set `current_phase` to "discovery"

**If `--phase` flag provided:**
1. Set `current_phase` to specified phase
2. If artifacts don't exist, warn user and start from discovery

### Step 4: Build Skill Arguments

Construct arguments for phase skill:

```
--slug {feature_slug}
--description "{feature_description}"
--artifacts .artifacts/{feature_slug}/
--tdd {true|false}
```

### Step 5: Invoke Current Phase Skill

Invoke the appropriate skill:

```
Skill
  skill: "harness:workflow-{current_phase}"
  args: "{constructed arguments}"
```

Each skill runs with `context: fork`:
- Isolated context (doesn't bloat main conversation)
- State passes through artifacts
- Engram provides cross-context memory

### Step 6: Handle Skill Output

When skill completes, examine its output:

**If output contains "PHASE_COMPLETE":**
1. Determine next phase in sequence
2. Check if next phase should be skipped (via `--skip`)
3. If next phase has pause point, present summary and ask to continue
4. Otherwise, invoke next phase skill

**If output contains "WORKFLOW_COMPLETE":**
1. Feature is done
2. Present final completion message
3. Stop orchestration

**If output contains "USER_INPUT_REQUIRED":**
1. The skill needs user input
2. Present the questions to user
3. Collect answers
4. Re-invoke skill with answers appended to args

**If output contains error or "BLOCKED":**
1. Present error to user
2. Ask how to proceed (retry / skip / abort)
3. Act on user choice

### Step 7: Phase Transitions

Transition logic:

| From | To | Pause? |
|------|-----|--------|
| Discovery | Explore | No |
| Explore | Requirements | No |
| Requirements | Design | Yes - "Ready to design?" |
| Design | Implement | Yes - "Ready to implement?" |
| Implement | Review | Yes - "Ready for review?" |
| Review | Testing | Yes - "Ready for testing?" |
| Testing | Summary | Yes - "Confirm feature complete?" |
| Summary | (end) | - |

At pause points:
1. Present phase completion summary
2. Ask: "Ready to proceed to {next_phase}?"
3. Wait for confirmation ("yes", "proceed", "continue")
4. If user wants changes, handle appropriately

### Step 8: Error Recovery

**Skill timeout or failure:**
1. Check artifacts for partial progress
2. Offer to retry from last good state
3. Search engram for similar errors

**Missing artifacts:**
1. Warn user
2. Offer to restart from discovery
3. Or jump to specified phase with --phase

**User abort:**
1. Save current state to progress.md
2. Sync to engram
3. Note how to resume later

## State Management

All state flows through artifacts in `.artifacts/{feature-slug}/`:

| Artifact | Created By | Contains |
|----------|------------|----------|
| `progress.md` | Discovery | Phase tracking, session log |
| `requirements.md` | Requirements | Feature specification |
| `design.md` | Design | Architecture decision |
| `plan.md` | Implement | Implementation steps |
| `summary.md` | Summary | Completion record |

Each skill:
1. Reads artifacts from previous phases
2. Updates `progress.md` with current phase
3. Creates its phase-specific artifact
4. Persists insights to engram

## Engram Integration

### Workflow Start
- `memory_resume`: Get session context
- `memory_search`: Find similar features

### Each Phase (via skills)
- `memory_search`: Phase-specific context
- `memory_insights`: Relevant decisions/lessons
- `memory_decision`: Record choices made
- `memory_lesson`: Record patterns/gotchas

### Workflow End (Summary phase)
- `memory_remember`: Comprehensive feature record
- `memory_sync`: Ensure everything indexed

### Cross-Session Continuity

User closes Claude → comes back later:
1. `/harness:feature "dark mode"`
2. Orchestrator finds `.artifacts/dark-mode/progress.md`
3. `memory_resume` provides session context
4. Workflow continues from last phase

## Quick Reference

| Command | Effect |
|---------|--------|
| `/harness:feature "add auth"` | Start new or resume |
| `/harness:feature --phase design` | Jump to design |
| `/harness:feature --tdd` | Enable TDD mode |
| `/harness:feature --skip explore` | Skip explore phase |

## Example Flow

```
User: /harness:feature "add dark mode toggle"

Orchestrator:
  → Searches engram: finds past "theming" work
  → No existing artifacts for "dark-mode-toggle"
  → Invokes harness:workflow-discovery

Discovery skill (forked):
  → Searches engram for similar features
  → Asks clarifying questions
  → Creates .artifacts/dark-mode-toggle/
  → Creates progress.md
  → Returns "PHASE_COMPLETE"

Orchestrator:
  → Invokes harness:workflow-explore

Explore skill (forked):
  → Searches engram for architecture patterns
  → Launches explorer agents
  → Documents findings
  → Returns "PHASE_COMPLETE"

Orchestrator:
  → Invokes harness:workflow-requirements

Requirements skill (forked):
  → Asks requirement questions (pause points)
  → Creates requirements.md
  → Returns "PHASE_COMPLETE"

Orchestrator:
  → PAUSE: "Ready to proceed to Design?"

User: "yes"

Orchestrator:
  → Invokes harness:workflow-design

... continues through all phases ...

Summary skill (forked):
  → Creates summary.md
  → Persists to engram
  → Returns "WORKFLOW_COMPLETE"

Orchestrator:
  → Presents completion message
  → Feature development complete!
```
