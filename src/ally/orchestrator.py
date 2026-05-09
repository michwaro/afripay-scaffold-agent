"""Deterministic five-agent accountability pipeline."""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

Emit = Callable[["Event"], None]

CATEGORY_KEYWORDS = {
    "rights violation": ("abuse", "arrest", "attack", "beaten", "evict", "harass", "threat", "violence"),
    "resource exploitation": ("forest", "gold", "land", "mine", "oil", "pollution", "resource", "water"),
    "broken commitment": ("budget", "clinic", "commitment", "promise", "road", "school", "service", "water"),
    "conflict trigger": ("clash", "conflict", "dispute", "militia", "protest", "tension", "violence", "weapon"),
}


@dataclass
class Event:
    agent: str
    status: str
    message: str
    evidence: list[str] | None = None
    ts: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        """Return a plain serializable event dictionary."""
        return {"agent": self.agent, "status": self.status, "message": self.message, "evidence": self.evidence, "ts": self.ts}


def _event(agent: str, status: str, message: str, evidence: list[str] | None = None) -> Event:
    return Event(agent=agent, status=status, message=message, evidence=evidence)


def _anonymous_id(report_text: str) -> str:
    return hashlib.sha256(report_text[:64].encode("utf-8")).hexdigest()[:16]


def _detect_script(report_text: str) -> str:
    for char in report_text:
        codepoint = ord(char)
        if 0x0600 <= codepoint <= 0x06FF:
            return "Arabic"
        if 0x0400 <= codepoint <= 0x04FF:
            return "Cyrillic"
    return "Latin"


def _classify_text(report_text: str) -> tuple[str, list[str]]:
    lowered = report_text.lower()
    scores = {
        category: [word for word in keywords if word in lowered]
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    category, matches = max(scores.items(), key=lambda item: len(item[1]))
    if not matches:
        return "rights violation", ["deterministic fallback: accountability concern"]
    return category, matches[:4]


def _load_udhr() -> dict[str, Any]:
    framework_path = ROOT / "frameworks" / "udhr.json"
    if not framework_path.exists():
        return {
            "display_name": "Universal Declaration of Human Rights",
            "articles": [
                {
                    "article": "Article 8",
                    "title": "Right to an effective remedy",
                    "keywords": ["accountability", "remedy", "rights", "violation"],
                }
            ],
        }
    return json.loads(framework_path.read_text())


def _match_rights(report_text: str, category: str) -> list[str]:
    framework = _load_udhr()
    lowered = f"{report_text} {category}".lower()
    matches = []
    for article in framework.get("articles", []):
        keywords = article.get("keywords", [])
        if any(str(keyword).lower() in lowered for keyword in keywords):
            matches.append(f"{article.get('article')}: {article.get('title')}")
    return matches[:3] or ["Article 8: Right to an effective remedy"]


def run_intake(report_text: str, emit: Emit) -> dict[str, Any]:
    emit(_event("Intake", "started", "Validating anonymous submission"))
    anonymous_id = _anonymous_id(report_text)
    word_count = len(report_text.split())
    emit(
        _event(
            "Intake",
            "evidence",
            "Submission anonymized",
            [f"anonymous_id={anonymous_id}", f"word_count={word_count}"],
        )
    )
    emit(_event("Intake", "completed", "Intake completed", [anonymous_id]))
    return {"report_text": report_text.strip(), "anonymous_id": anonymous_id, "word_count": word_count}


def run_translator(report_text: str, emit: Emit, prior: dict[str, Any]) -> dict[str, Any]:
    emit(_event("Translator", "started", "Detecting submission language"))
    script = _detect_script(report_text)
    emit(
        _event(
            "Translator",
            "evidence",
            "Deterministic script detection completed",
            [f"script={script}", "translated_text preserved from original report"],
        )
    )
    prior.update({"detected_script": script, "translated_text": report_text})
    emit(_event("Translator", "completed", "Translation step completed", [script]))
    return prior


def run_classifier(emit: Emit, prior: dict[str, Any]) -> dict[str, Any]:
    emit(_event("Classifier", "started", "Classifying accountability concern"))
    category, matches = _classify_text(str(prior.get("translated_text", "")))
    emit(_event("Classifier", "evidence", "Keyword category matches found", [category, *matches]))
    prior.update({"category": category, "category_evidence": matches})
    emit(_event("Classifier", "completed", "Classification completed", [category]))
    return prior


def run_rights_mapper(emit: Emit, prior: dict[str, Any]) -> dict[str, Any]:
    emit(_event("RightsMapper", "started", "Mapping concern to rights framework"))
    rights = _match_rights(str(prior.get("translated_text", "")), str(prior.get("category", "")))
    emit(_event("RightsMapper", "evidence", "UDHR article matches found", rights))
    prior["rights"] = rights
    emit(_event("RightsMapper", "completed", "Rights mapping completed", rights))
    return prior


def run_report_generator(emit: Emit, prior: dict[str, Any]) -> str:
    emit(_event("ReportGenerator", "started", "Assembling accountability brief"))
    evidence = [
        f"anonymous_id={prior.get('anonymous_id')}",
        f"category={prior.get('category')}",
        f"rights={', '.join(prior.get('rights', []))}",
    ]
    emit(_event("ReportGenerator", "evidence", "Brief inputs assembled", evidence))
    report = "\n".join(
        [
            "# Ally Accountability Brief",
            "",
            f"Anonymous ID: {prior.get('anonymous_id')}",
            f"Detected script: {prior.get('detected_script')}",
            f"Category: {prior.get('category')}",
            "",
            "## Rights Mapping",
            *[f"- {right}" for right in prior.get("rights", [])],
            "",
            "## Summary",
            str(prior.get("translated_text", "")).strip(),
        ]
    )
    emit(_event("ReportGenerator", "completed", "Report assembled", ["Markdown report generated"]))
    return report


def orchestrate(report_text: str) -> Iterator[Event]:
    events: list[Event] = []

    def emit(event: Event) -> None:
        events.append(event)

    prior = run_intake(report_text, emit)
    yield from events
    events.clear()

    prior = run_translator(report_text, emit, prior)
    yield from events
    events.clear()

    prior = run_classifier(emit, prior)
    yield from events
    events.clear()

    prior = run_rights_mapper(emit, prior)
    yield from events
    events.clear()

    report = run_report_generator(emit, prior)
    yield from events
    yield _event("Pipeline", "completed", "Report generated", [report])
