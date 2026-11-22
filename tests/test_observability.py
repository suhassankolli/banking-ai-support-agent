
import json
import logging

from observability import build_event, log_event


def test_event_contains_required_fields():
    event = build_event(
        "agent_started",
        "request-123",
        model="test-model",
    )

    assert event["event"] == "agent_started"
    assert event["request_id"] == "request-123"
    assert event["model"] == "test-model"
    assert "timestamp" in event


def test_log_event_emits_json(caplog):
    with caplog.at_level(
        logging.INFO,
        logger="banking_agent",
    ):
        log_event(
            "tool_completed",
            "request-456",
            status="success",
        )

    record = json.loads(caplog.records[-1].message)

    assert record["event"] == "tool_completed"
    assert record["status"] == "success"
