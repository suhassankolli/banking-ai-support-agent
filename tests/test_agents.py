
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from google.genai import types

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from agent import (
    AgentContext,
    BankingAgent,
    execute_tool,
)


def fake_response(parts, text=None):
    content = types.Content(
        role="model",
        parts=parts,
    )
    return SimpleNamespace(
        candidates=[SimpleNamespace(content=content)],
        text=text,
    )


class FakeModels:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    def generate_content(self, **kwargs):
        self.requests.append({
            **kwargs,
            "contents": list(kwargs["contents"]),
        })
        return next(self.responses)


class FakeClient:
    def __init__(self, responses):
        self.models = FakeModels(responses)


def test_agent_calls_customer_tool():
    first = fake_response([
        types.Part.from_function_call(
            name="get_customer",
            args={"customer_id": "CUST0001"},
        )
    ])

    second = fake_response(
        [types.Part.from_text(text="Customer found.")],
        text="Customer found.",
    )

    client = FakeClient([first, second])
    agent = BankingAgent(client=client)

    answer = agent.run(
        "Find CUST0001",
        AgentContext("CUST0001"),
    )

    assert answer == "Customer found."
    assert len(client.models.requests) == 2

    history = client.models.requests[1]["contents"]
    tool_part = history[-1].parts[0]

    assert tool_part.function_response.name == "get_customer"
    assert tool_part.function_response.response["status"] == "success"


def test_cross_customer_access_is_denied():
    result = execute_tool(
        "get_customer",
        {"customer_id": "CUST0002"},
        AgentContext("CUST0001"),
    )

    assert result["status"] == "error"
    assert result["error_type"] == "PermissionError"


def test_unknown_tool_is_rejected():
    result = execute_tool(
        "delete_account",
        {"customer_id": "CUST0001"},
        AgentContext("CUST0001"),
    )

    assert result["status"] == "error"


def test_empty_question_is_rejected():
    agent = BankingAgent(
        client=FakeClient([])
    )

    with pytest.raises(ValueError):
        agent.run(
            "   ",
            AgentContext("CUST0001"),
        )


def test_agent_step_limit():
    repeated = [
        fake_response([
            types.Part.from_function_call(
                name="get_customer",
                args={"customer_id": "CUST0001"},
            )
        ])
        for _ in range(2)
    ]

    agent = BankingAgent(
        client=FakeClient(repeated)
    )

    answer = agent.run(
        "Find customer",
        AgentContext("CUST0001"),
        max_steps=2,
    )

    assert "execution limit" in answer
