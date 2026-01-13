---
name: harness:workflow-explore
description: This skill should be used when the user asks to "explore the codebase", "understand the architecture", "find patterns for a feature", or when the harness:feature orchestrator invokes the Explore phase.
context: fork
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-explore.sh"
          timeout: 10
---

# Explore Phase - Codebase Understanding

Map the codebase to understand patterns, architecture, and integration points relevant to the feature.

## Context Parsing

Parse `$ARGUMENTS` for:
- `--slug <name>`: Feature slug
- `--description "<text>"`: Feature description
- `--artifacts <path>`: Artifacts directory path

If not provided, check for existing `.artifacts/*/progress.md` and ask which feature to explore.

## Phase Execution

Execute these steps IN ORDER. Do NOT skip steps.

### Step 1: Search Engram for Prior Context

IMMEDIATELY search engram:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} architecture patterns"
  n_results: 5
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "{feature_description}"
  insight_type: "decision"
  n_results: 3
```

Incorporate findings into exploration strategy.

### Step 2: Update Progress

Read `{artifacts_path}/progress.md` and update:
- Change "Phase:" to "Explore"
- Check off "Discovery" in checklist
- Add session log entry

### Step 3: Launch Explorer Agents

Launch 3 parallel agents using Task tool. ALL THREE must be launched in a SINGLE message:

**Agent 1: Pattern Discovery**
```
Task
  subagent_type: "harness:code-explorer"
  prompt: "Find features similar to '{feature_description}' in this codebase.
           Identify: implementation patterns, file organization, coding conventions.
           Return: File paths with relevance notes, pattern descriptions."
```

**Agent 2: Architecture Mapping**
```
Task
  subagent_type: "harness:code-explorer"
  prompt: "Map architecture relevant to '{feature_description}'.
           Identify: layers, abstractions, data flow, extension points.
           Return: Architecture diagram (text), key interfaces, boundaries."
```

**Agent 3: Integration Points**
```
Task
  subagent_type: "harness:code-explorer"
  prompt: "Find where '{feature_description}' integrates with existing code.
           Identify: entry points, hooks, config systems, APIs to leverage.
           Return: Integration map with file:line references."
```

Wait for ALL agents to complete before proceeding.

### Step 4: Synthesize Findings

After agents complete:
1. Read key files identified by agents
2. Verify and deepen understanding
3. Identify the most important patterns

### Step 5: Document in Progress

Add to `{artifacts_path}/progress.md`:

```markdown
## Codebase Exploration

### Key Patterns
| Pattern | Location | Relevance |
|---------|----------|-----------|
| {name} | {path} | {why it matters} |

### Relevant Files
| File | Purpose | Feature Relevance |
|------|---------|-------------------|
| `path/file.ts` | {what it does} | {why it matters} |

### Architecture Notes
{High-level structure description}

### Integration Points
{Where new code connects to existing code}

### Prior Context (Engram)
{Any relevant decisions/lessons from memory}
```

### Step 6: Persist to Engram

Record significant findings:

```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature_description}: Found {pattern} pattern at {location}. Approach: {rationale}."
  category: "architecture"
```

```
mcp__plugin_engram-mcp_engram__memory_lesson
  content: "Codebase uses {pattern} for {purpose}. Integration point: {location}."
  category: "pattern"
```

### Step 7: Commit Exploration

```bash
git add .artifacts/{slug}/
git commit -m "docs({slug}): document codebase exploration"
```

## Critical Rules

1. ALWAYS launch all 3 explorer agents in parallel
2. ALWAYS document at least 3 relevant files
3. ALWAYS update progress.md with exploration section
4. NEVER complete without synthesizing agent findings
5. Proceed automatically to Requirements phase
