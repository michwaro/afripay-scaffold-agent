# Ally: Community Voice & Accountability Agent

Ally is a local-first, multi-agent accountability prototype that lets community members submit anonymous reports, streams five analysis agents in real time, and produces a Markdown brief for CSOs, human rights defenders, and community facilitators. It addresses OSF's Voice & Accountability track, with Peace & Community as a secondary track, by focusing on safe reporting, rights framing, and low-bandwidth access for marginalized or conflict-affected communities.

## Architecture

```text
ally-agent/
├── CAPSTONE_SPEC.md
├── README.md
├── AGENTS.md
├── pyproject.toml
├── frameworks/           # UDHR and framework JSON
├── analysis/             # analysis criteria/rules
├── src/ally/
│   ├── __init__.py
│   ├── cli.py            # submit command + serve command
│   ├── orchestrator.py   # five sub-agents + Event dataclass + orchestrate()
│   ├── server.py         # FastAPI + SSE streaming
│   └── analyzer.py       # OpenAI-backed analysis helper
├── web/
│   └── index.html        # single-file editorial UI
└── tests/
    ├── test_orchestrator.py
    └── test_server.py
```

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Run The Live Demo

```bash
ally serve
open http://localhost:8765
```

## CLI Usage

```bash
ally submit --report "describe what happened" --framework udhr
```

## Tests

```bash
pytest -q
```

## Built With Codex IDE

Codex generated `orchestrator.py`, `server.py`, `web/index.html`, and `CAPSTONE_SPEC.md` through iterative prompts, diffs, tests, and review. The human made the core product choices: the five sub-agent names, the fixed typed event shape, the rule that Intake anonymizes before any content analysis, and the OSF track alignment.

## Operating Constraints Addressed

- **Anonymity:** Intake creates a deterministic anonymous ID from the report prefix and avoids account requirements in the demo flow.
- **Low bandwidth:** The UI is a single HTML file and receives compact server-sent event lines.
- **Multilingual support:** Deterministic mode detects Arabic, Latin, and Cyrillic scripts; full translation is marked as future AI-backed behavior.
- **Displaced populations:** The demo runs locally without an API key and keeps submission friction low.
- **Adaptability:** Rights mapping is data-driven through framework JSON files, currently demonstrated with UDHR keywords.

## Next Steps

- SMS/USSD input for offline communities
- Pattern aggregation across anonymized reports
- Multi-country legal framework expansion
