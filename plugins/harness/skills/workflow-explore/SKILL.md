---
name: harness:workflow-explore
description: This skill should be used when the user asks to "explore the codebase", "understand the architecture", "find patterns for a feature", or when the harness:feature orchestrator invokes the Explore phase.
context: fork
agent: Explore
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - mcp__plugin_engram-mcp_engram__*
hooks:
  Stop:
    - prompt: |
        Before this skill completes, validate that:
        1. progress.md exists and has "Phase: Explore"
        2. progress.md contains "## Codebase Exploration" section
        3. At least 3 relevant files were identified

        If validation fails, output what's missing. If validation passes, output "PHASE_COMPLETE".
---

# Explore Phase - Codebase Understanding

This phase explores the codebase to understand patterns, architecture, and integration points relevant to the feature being implemented.

## Context

**If invoked via orchestrator:** Receives context via `$ARGUMENTS`:
- `feature_slug`: The feature identifier (e.g., "dark-mode")
- `feature_description`: What the user wants to build
- `artifacts_path`: Path to `.artifacts/{feature-slug}/`

**If invoked directly by user:** Parse `$ARGUMENTS` for a feature description or exploration goal. If none provided, ask what aspect of the codebase to explore. For standalone exploration (not part of workflow), skip artifact creation and just present findings directly.

## Phase Execution

### Step 1: Search Engram for Prior Context

Before exploring the codebase, search engram for relevant past work:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} architecture patterns implementation"
  n_results: 5
```

Also search for insights (decisions/lessons) about similar features:

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "{feature_description}"
  insight_type: "all"
  n_results: 3
```

If relevant findings exist, incorporate them into exploration strategy.

### Step 2: Update Progress

Read current `{artifacts_path}/progress.md` and update:
- Set Phase to "Explore"
- Check off "Discovery" in checklist
- Add session log entry

### Step 3: Launch Explorer Agents

Launch 2-3 explorer agents in parallel using the Task tool:

**Agent 1: Pattern Discovery**
```
Task with subagent_type: "harness:code-explorer"
prompt: "Find features similar to '{feature_description}' in this codebase. Trace their implementation patterns, file organization, and coding conventions."
```

**Agent 2: Architecture Mapping**
```
Task with subagent_type: "harness:code-explorer"
prompt: "Map the architecture relevant to '{feature_description}'. Identify layers, abstractions, data flow patterns, and extension points."
```

**Agent 3: Integration Points**
```
Task with subagent_type: "harness:code-explorer"
prompt: "Identify where '{feature_description}' would integrate. Find entry points, hooks, configuration systems, and existing APIs that could be leveraged."
```

### Step 4: Synthesize Findings

After agents complete, synthesize their findings into structured documentation.

Read key files identified by agents to verify and deepen understanding.

### Step 5: Document in Progress

Add "## Codebase Exploration" section to `{artifacts_path}/progress.md`:

```markdown
## Codebase Exploration

### Key Patterns Discovered
- **{Pattern Name}**: {How it works and why it matters}

### Relevant Files
| File | Purpose | Relevance to Feature |
|------|---------|---------------------|
| `path/to/file.ts` | What it does | Why it matters |

### Architecture Notes
{High-level structure relevant to this feature}

### Integration Points
{Where the new feature will connect to existing code}

### Insights from Past Work
{Any relevant decisions/lessons from engram}
```

### Step 6: Persist to Engram

Record key architectural insights for future sessions:

**If significant patterns discovered:**
```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature_description}: Found {pattern} pattern in {location}. This approach {rationale}."
  category: "architecture"
  alternatives: ["other approaches considered"]
```

**If gotchas or important notes found:**
```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "When implementing features like {feature_description}: {lesson}"
  category: "pattern"
```

### Step 7: Commit Exploration

Commit the exploration findings:

```bash
git add .artifacts/{feature-slug}/
git commit -m "docs({feature-slug}): document codebase exploration"
```

### Step 8: Prepare Handoff

Summarize exploration for the next phase (Requirements):
- Top 3-5 most important findings
- Recommended approach based on patterns
- Questions that need user input

Output this summary - it will be passed to the Requirements phase.

## Completion Criteria

The Stop hook validates:
1. `progress.md` updated with Phase: Explore
2. "## Codebase Exploration" section exists
3. At least 3 relevant files documented

Phase is complete when hook outputs "PHASE_COMPLETE".

## Engram Integration Summary

| When | Tool | Purpose |
|------|------|---------|
| Start | `memory_search` | Find relevant past context |
| Start | `memory_insights` | Get related decisions/lessons |
| End | `memory_decision` | Record architectural choices |
| End | `memory_lesson` | Record patterns/gotchas |

The Stop hook will trigger `memory_sync` via the engram plugin's hooks.
