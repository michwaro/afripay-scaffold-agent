# AGENTS.md — Ally: Community Voice & Accountability Agent

## Setup
- Python 3.11+: `pip install -e ".[dev]"`
- `OPENAI_API_KEY` is optional; deterministic mode works without it.
- Verify: `python -m ally --help`
- Serve: `ally serve` → open http://localhost:8765

## Sub-agents

### Intake
- **Role:** Validates the submission and creates an anonymous deterministic report ID before analysis.
- **Inputs:** Raw `report_text`.
- **Evidence emitted:** `anonymous_id=<hash>` and `word_count=<count>`.

### Translator
- **Role:** Detects the report script and preserves the original text in deterministic mode.
- **Inputs:** Raw `report_text` plus Intake output.
- **Evidence emitted:** `script=<Arabic|Latin|Cyrillic>` and a note that deterministic mode preserved the original text.

### Classifier
- **Role:** Maps the report to one accountability category using deterministic keyword matching.
- **Inputs:** Prior pipeline state, especially `translated_text`.
- **Evidence emitted:** Selected category plus matched keywords for rights violation, resource exploitation, broken commitment, or conflict trigger.

### RightsMapper
- **Role:** Links the classified concern to relevant UDHR article titles using framework keywords.
- **Inputs:** Prior pipeline state, especially `translated_text` and `category`.
- **Evidence emitted:** Matched UDHR article labels and titles, with Article 8 as the deterministic fallback.

### ReportGenerator
- **Role:** Assembles prior outputs into a Markdown accountability brief.
- **Inputs:** Prior pipeline state, including anonymous ID, detected script, category, and rights matches.
- **Evidence emitted:** Brief inputs such as anonymous ID, category, rights matches, and confirmation that Markdown was generated.

## Event Contract
- Event fields are fixed: `agent`, `status`, `message`, `evidence`, `ts`.
- Status values are fixed: `started`, `thinking`, `evidence`, `completed`, `failed`.
- Every sub-agent emits at least one `started`, one `evidence`, and one `completed` or `failed` event.
- Five agents always run in order: Intake, Translator, Classifier, RightsMapper, ReportGenerator.

## Testing
- Run: `pytest -q`
- Mock OpenAI and HTTP calls in tests.
- `orchestrate()` must work without `OPENAI_API_KEY`.

## Style
- Type hints on all functions.
- No `print()` — use `rich.console.Console` in CLI, SSE events in server.
- `web/index.html` must remain a single file.
- Anonymization happens in Intake before any content analysis; this ordering is a hard security requirement.
