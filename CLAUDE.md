# CLAUDE.md

This file is the always-on context for agents working in this repository.
Keep it high-signal and evergreen.

## Repository Purpose

Kinemotion provides video-based kinematic analysis for athletic performance.

Supported jump analyses:

- Drop Jump (ground contact time, flight time, RSI)
- Counter Movement Jump (jump height, flight time, countermovement depth)
- Squat Jump (concentric power profile; athlete mass required for power/force)

Current pose estimator:

- MediaPipe for production jump workflows
- RTMLib/RTMPose research and multi-sport expansion context in docs

## Architecture Snapshot

```text
src/kinemotion/
  cli.py
  api.py
  core/
  drop_jump/
  countermovement_jump/
  squat_jump/
tests/
frontend/
backend/
```

High-level flow:
`frontend` -> `backend` -> `src/kinemotion` analysis engine -> Supabase -> frontend

## Canonical Commands

Setup:

```bash
asdf install
uv sync
```

Development checks:

```bash
uv run ruff check --fix
uv run ruff format
uv run pyright
uv run pytest
```

Useful test commands:

```bash
uv run pytest tests/core/
uv run pytest tests/countermovement_jump/
uv run pytest tests/drop_jump/
uv run pytest tests/squat_jump/
```

CLI examples:

```bash
uv run kinemotion dropjump-analyze video.mp4
uv run kinemotion cmj-analyze video.mp4
uv run kinemotion sj-analyze video.mp4 --mass 75.0
```

## Code Quality Constraints

- Python type checking is strict (`pyright`).
- Ruff is the formatter/linter with line length `99` (source of truth: `pyproject.toml`).
- Keep cognitive complexity low (prefer helper extraction and early returns).
- Avoid duplication; prefer shared utilities and reusable helpers.
- Use Conventional Commits: `<type>(<scope>): <description>`.

## Critical Domain Gotchas

Video processing:

- Read first frame for dimensions instead of trusting OpenCV metadata fields.
- Handle rotation metadata from mobile recordings.
- Convert NumPy scalars to Python primitives before JSON serialization.

Counter Movement Jump:

- Use signed velocity, not absolute velocity.
- Use backward search from peak to detect phases robustly.
- Prefer 45-degree oblique camera view for better landmark separation.

Squat Jump:

- Mass is required for power and force metrics (`--mass` or `mass_kg`).
- No countermovement assumption; require static squat hold before takeoff.

## Task Routing and Specialists

Project subagents live in `.claude/agents/`.
Use them for domain-heavy tasks (biomechanics, CV, backend, QA, docs, DevOps).

Reference:

- `docs/development/agents-guide.md`

## Read X When Y

Read these only when task-relevant (progressive disclosure):

- Implementation internals:
  - `docs/technical/implementation-details.md`
- Testing strategy and standards:
  - `docs/development/testing.md`
  - `docs/development/testing-standards.md`
- Jump-specific behavior:
  - `docs/guides/cmj-guide.md`
  - `docs/guides/drop-jump-guide.md`
  - `docs/guides/sj-guide.md`
- Roadmap and product priorities:
  - `docs/strategy/1-STRATEGIC_SUMMARY.md`
  - `docs/strategy/MVP_VALIDATION_CHECKPOINTS.md`
- MCP usage patterns and deeper agent context:
  - `docs/development/claude-context-reference.md`

## Source-of-Truth Policy

When instructions in this file conflict with executable config or scripts:

- Prefer repository config files (`pyproject.toml`, workflow files, tool configs).
- Update this file in the same change set that updates those configs.

Avoid hard-coding volatile values (test counts, temporary percentages, release-only numbers).

## Maintenance Cadence

Refresh this file:

- monthly, and
- after major release/process/tooling changes.

Checklist for refresh:

- command validity
- style/type/test rules
- architecture summary correctness
- critical gotchas still current
