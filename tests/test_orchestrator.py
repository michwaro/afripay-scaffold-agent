from ally.orchestrator import orchestrate


def test_orchestrate_runs_deterministic_pipeline_without_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    events = list(orchestrate("The community reports threats, violence, and a broken water promise."))
    agent_names = {event.agent for event in events}
    required_agents = {"Intake", "Translator", "Classifier", "RightsMapper", "ReportGenerator"}

    assert required_agents <= agent_names
    for agent in required_agents:
        statuses = {event.status for event in events if event.agent == agent}
        assert {"started", "completed"} <= statuses


def test_orchestrate_yields_final_pipeline_report(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    final_event = list(orchestrate("A school project was promised but never delivered."))[-1]

    assert final_event.agent == "Pipeline"
    assert final_event.status == "completed"
    assert final_event.evidence
    assert isinstance(final_event.evidence[0], str)
    assert final_event.evidence[0].strip()
