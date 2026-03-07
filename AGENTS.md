# Agent Guidance (Repository Playbook)

This repo is a tiny Python CLI chatbot that talks to an OpenAI-compatible server.
It is intentionally minimal: there is no package manager config (no `pyproject.toml`),
no test runner config, and no formal formatter/linter config.

If you add tooling (ruff/black/pytest/etc.), keep it lightweight and document any new
commands in this file.

## Repo Map

- `chatbot.py`: CLI entrypoint + request/response logic (stdlib-only)
- `README.md`: how to run + environment variables
- `opencode.json`: OpenCode config (model/provider + permissions)
- `CODE_REVIEW_AGENT.md`: reusable prompt for a code review agent

## Cursor / Copilot Rules

- Cursor rules: none found (no `.cursor/rules/` and no `.cursorrules`).
- Copilot rules: none found (no `.github/copilot-instructions.md`).

If those files are added later, treat them as higher-priority constraints.

## Setup

This project runs on the Python standard library.

- Recommended Python: `python3` (any reasonably recent 3.x)
- Optional virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -V
```

There is currently no `requirements.txt`.

## Run (Development)

```bash
python3 chatbot.py
```

Override connection settings:

```bash
OPENAI_BASE_URL="http://localhost:4141" \
OPENAI_API_KEY="dummy" \
OPENAI_MODEL="gpt-4" \
python3 chatbot.py
```

## Build / Lint / Test

There is no build step and no configured test suite.
Use the following smoke checks before/after changes.

### Build (Syntax/Import Smoke)

- Bytecode compile all Python (fast syntax check):

```bash
python3 -m compileall -q .
```

- Import the entrypoint (catches top-level import errors):

```bash
python3 -c "import chatbot; print('ok')"
```

### Lint (Current + Optional)

No linter is pinned in this repository.

- Optional (if you have ruff installed globally):

```bash
ruff check .
ruff format .
```

- Optional (if you have black installed globally):

```bash
black .
```

If you introduce lint/format tooling as a dependency, prefer adding a minimal
`pyproject.toml` so commands are reproducible.

### Test (Current + How To Add)

No tests exist yet.

- Baseline: run the module compile/import smoke checks (see above).

If you add tests, prefer stdlib `unittest` unless the repo adopts `pytest`.

Suggested layout:

- `tests/test_chatbot.py`
- keep tests hermetic; do not require a live server by default

#### Run All Tests (unittest)

```bash
python3 -m unittest -v
```

#### Run A Single Test File (unittest)

```bash
python3 -m unittest -v tests.test_chatbot
```

#### Run A Single Test Case Or Method (unittest)

```bash
python3 -m unittest -v tests.test_chatbot.TestNormalizeBaseUrl
python3 -m unittest -v tests.test_chatbot.TestNormalizeBaseUrl.test_adds_v1
```

If the repo later adopts `pytest`, document the equivalents:

- `pytest -q`
- `pytest -q tests/test_chatbot.py::TestX::test_y`

## Code Style (Python)

This codebase is small; optimize for clarity and correctness over abstraction.

### Imports

- Prefer standard library only unless there is a strong reason.
- Group imports in this order with a blank line between groups:
  1) stdlib, 2) third-party, 3) local
- Avoid wildcard imports.
- Keep imports at module top (no lazy imports) unless it materially reduces
  startup cost and is justified.

### Formatting

- Indentation: 4 spaces.
- Prefer PEP 8 style.
- Target line length: ~88 characters (black-friendly) unless readability suffers.
- Prefer double quotes for user-facing strings only when it improves escaping;
  otherwise be consistent within the file.

### Types

- Use `from __future__ import annotations` (already present in `chatbot.py`).
- Use precise types for public-ish helpers (even in a script).
- Prefer built-in generics (Py3.9+): `list[str]`, `dict[str, Any]`.
  Note: `chatbot.py` currently uses `typing.List/Dict`; keep consistent within
  a file unless you decide to migrate the whole file.
- Use `Any` only at boundaries (e.g., decoded JSON) and then validate/narrow.

### Naming Conventions

- Functions/variables: `snake_case`.
- Private helpers: prefix with `_` (e.g., `_normalize_base_url`).
- Constants: `UPPER_SNAKE_CASE`.
- Types/classes: `PascalCase`.
- Prefer descriptive names over abbreviations (`timeout_s`, `dt_ms` are OK).

### Error Handling

- Wrap external boundaries with explicit, actionable errors:
  network calls, JSON decoding, schema parsing.
- Re-raise with context using `raise ... from e` (already used).
- Do not swallow exceptions silently.
- Keep error messages stable and user-oriented for CLI output.

### I/O and CLI Behavior

- Keep the CLI responsive; avoid long blocking operations without feedback.
- Do not log secrets (API keys, auth headers).
- Keep output deterministic and easy to read in terminals.

### HTTP / API Contract

- The code targets an OpenAI-compatible endpoint:
  `POST {base_url}/chat/completions` with `Authorization: Bearer <key>`.
- When changing request payload/response parsing:
  validate compatibility (choices/message/content) and keep clear errors.
- Prefer timeouts on all network calls.

### Dependencies

- Default to stdlib. If adding deps, justify the tradeoff and keep the list small.
- If adding a dependency manager (`uv`, `pip-tools`, `poetry`, etc.), document:
  install, lock/update, and the canonical run/test commands.

## Safe Refactors

- Keep `chatbot.py` runnable as a script (`python3 chatbot.py`).
- Preserve the current CLI commands: `/help`, `/reset`, `/system`, `/exit`.
- Add small pure helpers for logic that can be unit-tested without network.
