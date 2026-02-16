# Claude Context Reference

This document contains detailed, task-specific context that should not be loaded
into every session by default. Root `CLAUDE.md` links here for progressive disclosure.

## When To Use This Reference

Read this file when work involves one or more of:

- MCP server behavior and tool-selection heuristics
- memory workflows for longer-horizon work
- specialist subagent routing decisions
- deeper command examples for common engineering tasks

## Specialized Subagents (Project)

Project subagents are defined in `.claude/agents/`.

Recommended routing:

- `project-manager`: planning, prioritization, scope decomposition
- `computer-vision-engineer`: MediaPipe, pose tracking, video IO, overlays
- `biomechanics-specialist`: jump metrics validity and interpretation
- `python-backend-developer`: algorithm quality and API concerns
- `ml-data-scientist`: parameter tuning and validation design
- `devops-cicd-engineer`: CI workflows, SonarQube, deployment setup
- `technical-writer`: docs structure and clarity
- `qa-test-engineer`: coverage, edge cases, regression protection
- `frontend-developer`: React/TypeScript UI implementation

## MCP Servers and Recommended Usage

All project MCP configuration is in `.mcp.json`.

### `serena`

- Primary tool for semantic code exploration and symbol-aware edits.
- Prefer targeted symbol/pattern operations over reading large files.
- Best for architecture discovery, references, and precise refactors.

### `basic-memory`

- Project memory store for reusable context.
- Use to save findings and load relevant prior notes before complex tasks.
- Typical operations:
  - save: write a concise note in a scoped directory
  - retrieve: search by concept or build context from `memory://...` paths

### `exa` and `ref`

- `exa`: broad, fresh web/code context.
- `ref`: targeted documentation search and page retrieval.
- Use both when current best practices or APIs may have changed.

### `sequential-thinking`

- Use for multi-step or ambiguous reasoning where explicit decomposition helps.
- Good for architecture choices, tricky debugging, and trade-off analysis.

### `sonarqube`

- Use for quality gate checks, maintainability trends, and issue triage.

## Practical Memory Patterns

Examples:

- Before CMJ algorithm work: load biomechanics notes first.
- Before release-hardening: load development and testing standards notes.
- After discovering a reusable rule: write a short note immediately.

## Extended Workflow Examples

### Feature Work

1. Explore current behavior and constraints.
2. Draft an implementation and test plan.
3. Implement incrementally.
4. Run quality gates (`ruff`, `pyright`, targeted/full `pytest`).
5. Document rationale when behavior changes materially.

### Debugging Work

1. Reproduce and isolate.
2. Gather evidence from tests/logs/metrics.
3. Fix smallest root cause first.
4. Add regression test.
5. Re-run impacted quality gates.

### Documentation Work

1. Prefer concise docs with links to deeper references.
2. Keep root guidance stable and evergreen.
3. Avoid embedding volatile operational metrics in always-on context.

## Notes on Keeping Context Lean

- Favor "where to find details" over embedding all details.
- Prefer stable constraints over frequently changing numbers.
- Keep root `CLAUDE.md` small enough to stay relevant across tasks.
