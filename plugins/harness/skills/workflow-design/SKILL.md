---
name: harness:workflow-design
description: This skill should be used when the user asks to "design architecture", "evaluate approaches", "plan feature implementation", or when the harness:feature orchestrator invokes the Design phase.
context: fork
agent: Plan
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__plugin_engram-mcp_engram__*
hooks:
  Stop:
    - prompt: |
        Before completing, validate:
        1. progress.md shows "Phase: Design"
        2. design.md exists with chosen approach documented
        3. User selected an approach (not just presented options)
        4. Rationale for selection is documented

        If validation fails, output what's missing. If passes, output "PHASE_COMPLETE".
---

# Design Phase - Architecture Selection

This phase evaluates multiple approaches and selects the best architecture for implementation.

## Context

**If invoked via orchestrator:** Receives `$ARGUMENTS`:
- `feature_slug`: Feature identifier
- `feature_description`: What to build
- `artifacts_path`: Path to `.artifacts/{slug}/`

**If invoked directly:** Check for existing artifacts. Read `requirements.md` if available. If starting fresh, ask for feature description and key constraints.

## Phase Execution

### Step 1: Load Context

Read existing artifacts:
- `{artifacts_path}/progress.md` - Current state
- `{artifacts_path}/requirements.md` - What must be built
- Any exploration findings (patterns, integration points)

Search engram for architectural patterns:

```
mcp__plugin_engram-mcp_engram__memory_search
  query: "{feature_description} architecture design approach"
  n_results: 5
```

```
mcp__plugin_engram-mcp_engram__memory_insights
  query: "architecture {feature_type}"
  insight_type: "decision"
  n_results: 5
```

Past architectural decisions are especially valuable here.

### Step 2: Update Progress

Edit `progress.md`:
- Set Phase to "Design"
- Check off "Requirements"
- Add session log entry

### Step 3: Launch Architect Agents

Launch 2-3 architect agents in parallel to explore different approaches:

**Agent 1: Minimal Change Approach**
```
Task with subagent_type: "harness:code-architect"
prompt: "Design a MINIMAL CHANGE approach for '{feature_description}'.
Requirements: {key requirements}
Existing patterns: {from exploration}

Focus on: Smallest possible change, maximum reuse of existing code, fastest to implement.
Document: Files to modify, components to reuse, trade-offs."
```

**Agent 2: Clean Architecture Approach**
```
Task with subagent_type: "harness:code-architect"
prompt: "Design a CLEAN ARCHITECTURE approach for '{feature_description}'.
Requirements: {key requirements}
Existing patterns: {from exploration}

Focus on: Maintainability, clear abstractions, future extensibility.
Document: New components, interfaces, data flow, trade-offs."
```

**Agent 3: Pragmatic Approach**
```
Task with subagent_type: "harness:code-architect"
prompt: "Design a PRAGMATIC approach for '{feature_description}'.
Requirements: {key requirements}
Existing patterns: {from exploration}

Focus on: Balance of speed and quality, reasonable abstractions, matches team patterns.
Document: Recommended structure, key decisions, trade-offs."
```

### Step 4: Synthesize Approaches

After agents complete, synthesize findings:

1. Read each agent's output
2. Identify common elements across approaches
3. Note key differentiators
4. Form YOUR recommendation based on:
   - Requirements fit
   - Codebase consistency
   - Implementation complexity
   - Future maintainability

### Step 5: Present Options to User

Present a clear comparison:

```markdown
## Approach Comparison

### Option A: Minimal Change
**Summary:** {1-2 sentences}
**Pros:** {bullet list}
**Cons:** {bullet list}
**Effort:** {relative estimate}

### Option B: Clean Architecture
**Summary:** {1-2 sentences}
**Pros:** {bullet list}
**Cons:** {bullet list}
**Effort:** {relative estimate}

### Option C: Pragmatic
**Summary:** {1-2 sentences}
**Pros:** {bullet list}
**Cons:** {bullet list}
**Effort:** {relative estimate}

---

**My Recommendation:** Option {X}

**Rationale:** {Why this is the best fit given requirements and codebase}
```

Ask: "Which approach would you like to use?"

**PAUSE POINT** - Wait for user selection.

### Step 6: Create Design Document

After user selects, write `.artifacts/{slug}/design.md`:

```markdown
# {Feature Name} - Design

## Chosen Approach
{Name of selected approach}

## Rationale
{Why this approach was selected}
{How it fits requirements}
{How it matches codebase patterns}

## Approaches Considered

### Approach A: {Name}
- **Summary**: {description}
- **Pros**: {list}
- **Cons**: {list}
- **Why not chosen**: {reason if not selected}

### Approach B: {Name}
...

## Architecture Overview

### High-Level Design
{Description of overall structure}

### Component Design

#### {Component 1}
- **Purpose:** {what it does}
- **Interface:** {public API/props}
- **Dependencies:** {what it uses}
- **Location:** {where it lives in codebase}

#### {Component 2}
...

### Data Flow
{How data moves through the system}

```
[User Action] → [Component A] → [Component B] → [Result]
```

### Integration Points
{Where new code connects to existing code}

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {decision} | {choice} | {why} |

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {risk} | Low/Med/High | Low/Med/High | {how to address} |

## Open Questions
- {Any remaining questions for implementation}
```

### Step 7: Persist to Engram

Record the architectural decision:

```
mcp__plugin_engram-mcp_engram__memory_decision
  content: "For {feature}: Selected {approach} approach. Key reasons: {rationale}. Components: {main components}. Trade-off accepted: {trade-off}."
  category: "architecture"
  alternatives: ["{other approaches considered}"]
```

If notable patterns chosen:

```
mcp__plugin_engram-mcp_engram__memory_remember
  content: "{feature} architecture: {approach}. Key pattern: {pattern}. Integration via {integration point}."
  tags: ["architecture", "{slug}", "{pattern-type}"]
```

### Step 8: Commit Design

Commit the design document:

```bash
git add .artifacts/{feature-slug}/
git commit -m "docs({feature-slug}): select {approach-name} architecture"
```

### Step 9: Prepare Handoff

Summarize for Implement phase:
- Chosen approach name
- Key components to build
- Recommended implementation order
- Critical integration points

## Completion Criteria

Stop hook validates:
1. `progress.md` updated with "Phase: Design"
2. `design.md` exists with chosen approach
3. User actively selected an approach
4. Rationale documented

## Engram Integration

| When | Tool | Purpose |
|------|------|---------|
| Start | `memory_search` | Find similar architectures |
| Start | `memory_insights` | Get past design decisions |
| End | `memory_decision` | Record approach selection |
| End | `memory_remember` | Persist key patterns |
