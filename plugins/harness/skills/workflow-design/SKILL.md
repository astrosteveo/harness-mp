---
name: harness:workflow-design
description: This skill should be used when the user asks to "design architecture", "evaluate approaches", "plan feature implementation", or when the harness:feature orchestrator invokes the Design phase.
context: fork
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/validate-design.sh"
          timeout: 10
---

# Design Phase - Architecture Selection

Evaluate approaches, research best practices, and select architecture. User approval required.

## Context Parsing

Parse `$ARGUMENTS` for:
- `--slug <name>`: Feature slug
- `--description "<text>"`: Feature description
- `--artifacts <path>`: Artifacts directory path

## Phase Execution

Execute these steps IN ORDER. Do NOT skip steps.

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Exploration findings
- `{artifacts_path}/requirements.md` - What must be built

Search engram:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} architecture design"
  n_results: 5
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "architecture {feature_type}"
  insight_type: "decision"
  n_results: 5
```

### Step 2: Update Progress

Edit `progress.md`:
- Change "Phase:" to "Design"
- Check off "Requirements"
- Add session log entry

### Step 3: Research Best Practices

REQUIRED: Research current best practices before designing.

Execute 2-4 web searches:

```
WebSearch
  query: "{feature_description} best practices 2026"
```

```
WebSearch
  query: "{feature_type} architecture patterns modern"
```

```
WebSearch
  query: "{technology_stack} {feature_description} implementation"
```

**Summarize findings:**
- Current best practices
- Recommended libraries/frameworks
- Patterns to avoid
- Industry-standard approaches

Add to progress.md:

```markdown
## Design Research

### Web Research ({date})
- **Best Practices:** {summary}
- **Libraries to Consider:** {list}
- **Patterns to Avoid:** {list}
- **Sources:** {urls}
```

### Step 4: Launch Architect Agents

Launch 3 parallel agents. Include research context in ALL prompts:

**Agent 1: Minimal Change**
```
Task
  subagent_type: "harness:code-architect"
  prompt: "Design MINIMAL CHANGE approach for '{feature_description}'.
           Requirements: {from requirements.md}
           Patterns: {from exploration}
           Best practices: {from web research}
           
           Focus: Smallest change, maximum reuse.
           Return: Files to modify, components, trade-offs."
```

**Agent 2: Modern Best Practices**
```
Task
  subagent_type: "harness:code-architect"
  prompt: "Design MODERN approach for '{feature_description}'.
           Requirements: {from requirements.md}
           Best practices: {from web research}
           Libraries: {recommended from research}
           
           Focus: Industry-standard, modern patterns.
           Return: Recommended stack, why it's current, trade-offs."
```

**Agent 3: Pragmatic Balance**
```
Task
  subagent_type: "harness:code-architect"
  prompt: "Design PRAGMATIC approach for '{feature_description}'.
           Requirements: {from requirements.md}
           Patterns: {from exploration}
           Best practices: {from web research}
           
           Focus: Balance modern + codebase consistency.
           Return: Structure, key decisions, trade-offs."
```

### Step 5: Synthesize Approaches

After agents complete:
1. Read each agent's output
2. Identify common elements
3. Note key differentiators
4. Form YOUR recommendation

### Step 6: Present to User (REQUIRED PAUSE)

Present comparison using AskUserQuestion:

```markdown
## Architecture Options

### Option A: Minimal Change
{summary}
- Pros: {list}
- Cons: {list}
- Effort: {relative}

### Option B: Modern Best Practices  
{summary}
- Pros: {list}
- Cons: {list}
- Effort: {relative}

### Option C: Pragmatic Balance
{summary}
- Pros: {list}
- Cons: {list}
- Effort: {relative}

**Recommendation:** Option {X} because {rationale}
```

Ask: "Which approach would you like to use?"

**STOP AND WAIT** for user selection.

### Step 7: Create Design Document

After user selects, write `.artifacts/{slug}/design.md`:

```markdown
# {Feature Name} - Design

## Chosen Approach
{selected approach name}

## Rationale
{why selected}
{how it fits requirements}
{how it matches codebase}

## Approaches Considered
| Approach | Summary | Why/Why Not |
|----------|---------|-------------|
| Minimal | {desc} | {reason} |
| Modern | {desc} | {reason} |
| Pragmatic | {desc} | {reason} |

## Architecture Overview

### High-Level Design
{structure description}

### Components

#### {Component 1}
- **Purpose:** {what}
- **Interface:** {API/props}
- **Location:** {path}

### Data Flow
```
[Input] → [Process] → [Output]
```

### Integration Points
{where new connects to existing}

## Technical Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| {item} | {choice} | {why} |

## Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk} | {level} | {plan} |
```

### Step 8: Persist to Engram

```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature}: Selected {approach}. Reasons: {rationale}. Trade-off: {accepted trade-off}."
  category: "architecture"
  alternatives: ["{other approaches}"]
```

### Step 9: Commit Design

```bash
git add .artifacts/{slug}/
git commit -m "docs({slug}): select {approach} architecture"
```

## Critical Rules

1. ALWAYS research web before designing
2. ALWAYS launch 3 architect agents
3. ALWAYS present options to user and wait for selection
4. NEVER create design.md without user approval
5. ALWAYS document rationale for selection
