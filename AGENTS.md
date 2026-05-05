# AGENTS.md — AfriPay Security Scaffold Agent

## Setup
- Python 3.11+, install with: `pip install -e ".[dev]"`
- Copy `.env.example` to `.env` and fill in sandbox credentials
- Verify setup: `python -m afripay --help`

## Testing
- Run: `pytest -q`
- All tests must pass before any PR or commit
- Test files live in `tests/` and mirror the source structure
- Always add a test for new providers before considering a task done

## Style
- Type hints required on all functions
- No print() — use `rich.console.Console` for output
- Provider spec files are JSON, security rules are YAML — do not mix
- Generated output code must include a comment block explaining each 
  security decision made

## Review guidelines
- Always show a diff before applying multi-file changes
- Generated scaffolds must include webhook signature verification — 
  this is non-negotiable, flag it if a provider spec doesn't define one
- Keep the CLI surface minimal; resist adding flags until task 7