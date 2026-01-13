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
  - WebSearch
  - WebFetch
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

### Step 3: Research Current Best Practices

**IMPORTANT:** Before designing, research how others are solving similar problems today.

Perform 2-4 web searches based on the feature type:

```
WebSearch
  query: "{feature_description} best practices 2025"
```

```
WebSearch
  query: "{feature_type} modern architecture patterns"
```

```
WebSearch
  query: "{technology_stack} {feature_description} implementation guide"
```

If relevant frameworks or libraries might help:
```
WebSearch
  query: "{feature_type} libraries frameworks comparison 2025"
```

**What to look for:**
- Current best practices and patterns
- Modern frameworks/libraries that solve this problem
- Common pitfalls others have encountered
- Performance considerations
- Security best practices

**Summarize findings:**
- List 2-3 relevant approaches from research
- Note any libraries/frameworks worth considering
- Flag any outdated patterns to avoid
- Identify industry-standard solutions

If a specific article or documentation looks valuable, use WebFetch to get details:
```
WebFetch
  url: "{relevant_url}"
  prompt: "Extract the key architectural patterns and recommendations for {feature_type}"
```

**Add research findings to progress.md:**
```markdown
## Design Research

### Web Research ({date})
- **Best Practices:** {summary}
- **Recommended Approaches:** {list}
- **Libraries to Consider:** {list}
- **Patterns to Avoid:** {outdated approaches}
- **Key Sources:** {urls}
```

### Step 4: Launch Architect Agents

Launch 2-3 architect agents in parallel to explore different approaches.

**Include research context in all prompts:**
- Best practices discovered in Step 3
- Recommended libraries/frameworks
- Patterns to avoid

**Agent 1: Minimal Change Approach**
```
Task with subagent_type: "harness:code-architect"
prompt: "Design a MINIMAL CHANGE approach for '{feature_description}'.
Requirements: {key requirements}
Existing patterns: {from exploration}
Current best practices: {from web research}
Libraries to consider: {from research}

Focus on: Smallest possible change, maximum reuse of existing code, fastest to implement.
Document: Files to modify, components to reuse, trade-offs."
```

**Agent 2: Modern Best Practices Approach**
```
Task with subagent_type: "harness:code-architect"
prompt: "Design a MODERN BEST PRACTICES approach for '{feature_description}'.
Requirements: {key requirements}
Existing patterns: {from exploration}
Current best practices: {from web research}
Recommended libraries: {from research}
Patterns to avoid: {outdated approaches from research}

Focus on: Industry-standard solutions, modern patterns, leveraging well-maintained libraries.
Document: Recommended stack, why these choices align with current standards, trade-offs."
```

**Agent 3: Pragmatic Approach**
```
Task with subagent_type: "harness:code-architect"
prompt: "Design a PRAGMATIC approach for '{feature_description}'.
Requirements: {key requirements}
Existing patterns: {from exploration}
Current best practices: {from web research}
Libraries to consider: {from research}

Focus on: Balance of modern practices and codebase consistency, reasonable abstractions.
Document: Recommended structure, key decisions, trade-offs."
```

### Step 5: Synthesize Approaches

After agents complete, synthesize findings:

1. Read each agent's output
2. Identify common elements across approaches
3. Note key differentiators
4. Form YOUR recommendation based on:
   - Requirements fit
   - Codebase consistency
   - Implementation complexity
   - Future maintainability

### Step 6: Present Options to User

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

### Step 7: Create Design Document

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

### Step 8: Persist to Engram

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

### Step 9: Commit Design

Commit the design document:

```bash
git add .artifacts/{feature-slug}/
git commit -m "docs({feature-slug}): select {approach-name} architecture"
```

### Step 10: Prepare Handoff

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
