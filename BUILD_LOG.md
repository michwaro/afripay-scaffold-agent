# Build Log — Ally: Community Voice & Accountability Agent
## What I decided vs what Codex generated

This document records what I decided as the engineer and what
OpenAI Codex generated, as required by the Andela × OpenAI Codex
Accelerator submission guidelines.

---

## What I decided

### Product & domain
- **Problem selection:** I chose the PeaceTech domain and OSF impact
  partner alignment — anonymous community reporting for conflict-
  affected and marginalized communities
- **Project name:** I named the project Ally to convey a helpful,
  trusted friend accessible to anyone, in any language
- **OSF track alignment:** I aligned the project to Voice &
  Accountability (primary) + Peace & Community (secondary)
- **Operating constraints:** I defined the five field conditions the
  system must respect — anonymity, low bandwidth, multilingual
  support, displaced populations, and geographic adaptability

### Architecture
- **Five sub-agent names:** I named the agents Intake, Translator,
  Classifier, RightsMapper, and ReportGenerator to match the real
  analytical steps a human rights defender would follow
- **Agent ordering:** I made the rule that Intake must anonymize the
  submission before any content analysis begins a hard security
  requirement. Codex did not infer this — I specified it explicitly
  in every relevant prompt
- **Typed event shape:** I designed the fixed JSON contract
  `{agent, status, message, evidence, ts}` to ensure the browser
  UI and server stay decoupled and the event stream is predictable
- **Four classification categories:** I chose rights violation,
  resource exploitation, broken commitment, and conflict trigger
  to reflect OSF's real accountability taxonomy
- **Rights frameworks:** I selected UDHR and the African Charter on
  Human and Peoples' Rights as the two MVP frameworks based on
  OSF's geographic focus
- **Deterministic mode requirement:** I decided the demo must run
  without an OPENAI_API_KEY so facilitators in low-resource
  settings can use Ally without API access or billing
- **Single-file web UI:** I decided web/index.html must be one file
  with no build step to minimise deployment friction in
  low-bandwidth environments

### Design
- **Editorial visual direction:** I chose the design language —
  oversized serif headlines, color-blocked sections, stat callouts,
  and the paper/ink/accent color system
- **Hero headline:** I wrote "Give communities a voice. Keep them
  safe."
- **Problem stats:** I chose the three field-relevant numbers (72%,
  43, 0) and their captions based on OSF's operating context
- **Console UX:** I decided the submission form must require no
  account, no name, and no identity field of any kind

### Pivots and direction changes
- **Capstone pivot (AfriPay → Civic Policy Analyst → Ally):**
  The project changed direction twice as OSF's impact partner
  brief was clarified. Each pivot was my decision based on reading
  the brief and assessing alignment with the PeaceTech theme
- **Architecture upgrade:** I decided to adopt the Workshop 4
  multi-agent + FastAPI SSE + web UI shape rather than ship a
  CLI-only tool after reading the submission requirements carefully

---

## What Codex generated

### Code files
- **src/ally/orchestrator.py** — the Event dataclass, all five
  sub-agent functions, the orchestrate() generator, and the
  deterministic heuristics (script detection via Unicode ranges,
  keyword matching for classification, UDHR article matching,
  anonymous ID via hashing)
- **src/ally/server.py** — the FastAPI app, SSE StreamingResponse,
  PDF/text upload endpoint, CORS configuration, and static file
  serving
- **src/ally/cli.py** — Typer CLI with submit and serve commands,
  Rich console output
- **src/ally/analyzer.py** — OpenAI-backed analysis helper
- **web/index.html** — the entire single-file web app: all HTML,
  CSS (including animations and responsive layout), and JavaScript
  (SSE via fetch + ReadableStream, agent graph state machine,
  markdown renderer, OS tab switcher, smooth scroll)

### Data files
- **frameworks/udhr.json** — UDHR article encoding
- **frameworks/african_charter.json** — African Charter encoding
- **analysis/criteria.yaml** — analysis criteria per framework

### Test files
- **tests/test_orchestrator.py** — orchestrator unit tests
- **tests/test_server.py** — FastAPI endpoint tests
- **tests/test_cli.py** — CLI smoke tests
- **tests/test_cli_integration.py** — integration tests

### Configuration
- **pyproject.toml** — package setup, dependencies, entry points
- **.gitignore** — standard Python ignores

### Documentation (first drafts)
- **CAPSTONE_SPEC.md** — Codex generated the structured spec from
  my requirements; I reviewed and approved each section
- **README.md** — Codex generated from my specified outline;
  I reviewed for accuracy before committing
- **AGENTS.md** — Codex generated sub-agent descriptions from the
  orchestrator code; I verified the contracts were correct

---

## How I worked with Codex

Every Codex output went through this loop:

1. I wrote a structured prompt using the four-element format:
   Goal, Context, Constraints, Done when
2. Codex drafted a plan (I used Plan mode ON for complex tasks)
3. I reviewed and approved the plan before any file changed
4. Codex executed step by step, pausing for my review of each
   diff before proceeding
5. I ran pytest after every task and reviewed output in the
   browser before committing
6. I committed only after manual verification passed

I did not commit any code without reviewing the diff.
I did not mark any task done without pytest passing.

---

## Commits

| Commit | Task | Notes |
|--------|------|-------|
| Initial commit | Spec + AGENTS.md | I authored both files |
| Task 1 | Repo refactor → Ally | Codex executed, I reviewed diff |
| Task 2 | Orchestrator + typed events | Codex executed, I reviewed diff |
| Task 3 | FastAPI server + SSE | Codex executed, I reviewed diff |
| Task 4 | Editorial web UI | Codex executed, I reviewed in browser |
| Task 5 | #built section | Codex executed, I verified content |
| Task 6 | README + AGENTS.md | Codex drafted, I verified accuracy |
| Task 7 | BUILD_LOG.md | I authored, Codex assisted with structure |

---

## What this project would need to become production-ready

The following were deliberately out of scope for this proof of
concept. Each would require my engineering decisions before Codex
could implement them:

- Persistent anonymized report storage with threat modelling
- SMS/USSD input layer for communities without web access
- Live OpenAI API integration (currently deterministic mode only)
- End-to-end encryption of submitted reports
- Multi-country legal framework expansion
- CSO dashboard with pattern aggregation across reports
- Security audit of the anonymization implementation