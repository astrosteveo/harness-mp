---
name: harness:red-green-refactor
description: Implements features using test-driven development (red-green-refactor cycle). Use when the user wants to add testable functionality, mentions TDD, or asks to write tests first before implementation.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Skill
context: fork
---

# Test-Driven Development

You are helping a developer implement functionality using strict TDD methodology. Follow the red-green-refactor cycle: write a failing test first, write minimal code to pass, then refactor.

**All progress is saved to `.artifacts/{feature-slug}/` alongside other feature artifacts.**

---

## Session Continuity

### Starting a New TDD Session
When `$ARGUMENTS` contains a new feature/function to implement, start from Phase 1.

### Resuming an Existing Session
When `$ARGUMENTS` references an existing feature or `.artifacts/{feature-slug}/` exists:

1. Read all artifact files in `.artifacts/{feature-slug}/`
2. Identify the last completed cycle from `tdd-progress.md`
3. Present a summary: "Resuming TDD for {feature}. Last cycle: {summary}"
4. Continue from the next incomplete cycle

### TDD Artifacts
These files are added to the existing `.artifacts/{feature-slug}/` directory:
```
.artifacts/{feature-slug}/
├── requirements.md      # (existing) Feature requirements
├── design.md            # (existing) Architecture design
├── plan.md              # (existing) Implementation plan
├── progress.md          # (existing) Overall feature progress
├── test-plan.md         # TDD: Ordered list of test cases
├── tdd-progress.md      # TDD: Current cycle status
└── tdd-summary.md       # TDD: Final testing summary
```

---

## Core Principles

- **Red first**: Never write production code without a failing test
- **Minimal green**: Write only enough code to make the test pass
- **Refactor with confidence**: Tests are your safety net
- **Small cycles**: Each test should take 1-5 minutes to implement
- **One behavior per test**: Tests should verify one specific thing
- **Commit frequently**: Commit after each green and each refactor

---

## Test Framework Setup

Before starting TDD, verify the test framework is configured:

1. Check for existing test setup (`vitest.config.ts`, `jest.config.js`, etc.)
2. If no test framework exists, recommend Vitest for this project (Vite-native)
3. Set up with: `npm install -D vitest`
4. Add test script to `package.json`: `"test": "vitest", "test:run": "vitest run"`
5. Create `vitest.config.ts` if needed

---

## Git Commit Strategy

Commits follow the TDD rhythm:

```
test({feature-slug}): add failing test for {behavior}     # RED
feat({feature-slug}): implement {behavior}                 # GREEN
refactor({feature-slug}): {description}                    # REFACTOR
```

---

## Phase 1: Requirements Analysis

**Goal**: Break the feature into testable behaviors

**Actions**:
1. Create todo list tracking all phases
2. Generate `feature-slug` from the feature name
3. Create `.artifacts/{feature-slug}/` directory (or use existing)
4. Analyze the feature and identify discrete, testable behaviors
5. Present the breakdown to user for confirmation

**Artifact**: Create `requirements.md`:
```markdown
# {Feature Name} - TDD Requirements

## Overview
{What we're building}

## Testable Behaviors
1. {Behavior 1} - {description}
2. {Behavior 2} - {description}
3. {Behavior 3} - {description}

## Dependencies
- {Any mocks or fixtures needed}

## Out of Scope
- {What we're NOT testing - UI rendering, etc.}
```

**Git Commit**: `docs({feature-slug}): define testable requirements for TDD`

---

## Phase 2: Test Plan

**Goal**: Order tests from simplest to most complex

**Actions**:
1. Review requirements and identify the simplest starting point
2. Order tests to build complexity incrementally
3. Identify any shared fixtures or test utilities needed
4. Present test plan to user

**Artifact**: Create `test-plan.md`:
```markdown
# {Feature Name} - Test Plan

## Test Order
Tests are ordered from simplest to most complex, each building on the last.

### Cycle 1: {Test Name}
- **Behavior**: {What we're testing}
- **Input**: {Test input}
- **Expected**: {Expected output}
- **Why first**: {Why this is the simplest starting point}

### Cycle 2: {Test Name}
- **Behavior**: {What we're testing}
- **Input**: {Test input}
- **Expected**: {Expected output}
- **Builds on**: {Previous test}

### Cycle 3: {Test Name}
...

## Shared Setup
- {Any beforeEach, fixtures, mocks}

## File Structure
- Test file: `src/{path}/__tests__/{name}.test.ts`
- Implementation: `src/{path}/{name}.ts`
```

**Git Commit**: `docs({feature-slug}): create TDD test plan with {N} cycles`

---

## Phase 3: TDD Cycles

**Goal**: Implement each test case using red-green-refactor

For each cycle in the test plan:

### RED: Write Failing Test
1. Write the test based on the test plan
2. Run the test - **verify it fails**
3. If test passes unexpectedly, the behavior already exists or test is wrong
4. Commit: `test({feature-slug}): add failing test for {behavior}`

### GREEN: Make It Pass
1. Write the **minimum** code to make the test pass
2. Do NOT add extra functionality
3. Do NOT handle edge cases not covered by tests yet
4. Run test - **verify it passes**
5. Commit: `feat({feature-slug}): implement {behavior}`

### REFACTOR: Clean Up
1. Look for duplication, unclear names, complex logic
2. Refactor production code while keeping tests green
3. Refactor test code if needed (but keep tests readable)
4. Run tests after each change
5. If refactored, commit: `refactor({feature-slug}): {description}`

### Cycle Complete
1. Update `tdd-progress.md` with cycle completion
2. Move to next cycle in test plan

**Progress Update Format** (in `tdd-progress.md`):
```markdown
## Cycle {N}: {Test Name}
- Status: COMPLETE
- RED: Test written, verified failing
- GREEN: Implementation complete, test passing
- REFACTOR: {What was refactored, or "No refactoring needed"}
- Commit(s): {list commit hashes}
```

---

## Phase 4: Integration Verification

**Goal**: Ensure the TDD'd code integrates correctly

**Actions**:
1. Run full test suite to check for regressions
2. If integrating with existing code, verify integration points
3. Check type safety (`npx tsc --noEmit`)
4. Run any existing build/lint commands

**Git Commit**: `test({feature-slug}): verify full test suite passes`

---

## Phase 5: Summary

**Goal**: Document what was accomplished

**Artifact**: Create `tdd-summary.md`:
```markdown
# {Feature Name} - TDD Summary

## Completed
{Date}

## Test Coverage
- {N} test cases implemented
- All tests passing

## Implementation
- Files created: {list}
- Files modified: {list}

## Key Design Decisions
- {Decision 1}: {rationale}
- {Decision 2}: {rationale}

## Cycles Summary
| Cycle | Behavior | Test | Status |
|-------|----------|------|--------|
| 1 | {behavior} | {test name} | PASS |
| 2 | {behavior} | {test name} | PASS |

## Lessons Learned
- {What went well}
- {What was challenging}
```

**Git Commit**: `docs({feature-slug}): complete TDD summary`

---

## Guidelines for This Project

### What to Test (Void Sector)
- Game logic: collision detection, inventory management, targeting calculations
- System behaviors: `MiningLaser` hit detection, `TargetingSystem` lock mechanics
- Data transformations: `MiningResult` processing, resource calculations
- State management: inventory capacity, lock states

### What NOT to Test
- Canvas rendering (visual output)
- Input handling (browser events)
- Animation/timing (requestAnimationFrame)

### Test File Location
Place tests adjacent to source:
```
src/game/systems/
├── MiningLaser.ts
├── __tests__/
│   └── MiningLaser.test.ts
```

### Mocking Game Objects
For systems that depend on entities:
```typescript
// Create minimal mock objects for testing
const mockShip = { position: { x: 0, y: 0 }, rotation: 0 };
const mockAsteroid = { position: { x: 100, y: 0 }, radius: 20 };
```
