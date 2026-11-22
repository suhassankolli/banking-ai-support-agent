
import pytest

from agent_limits import AgentBudgetExceeded, ExecutionBudget


def test_tool_limit():
    budget = ExecutionBudget(max_tool_calls=2)

    budget.reserve_tool_call()
    budget.reserve_tool_call()

    with pytest.raises(AgentBudgetExceeded):
        budget.reserve_tool_call()


def test_expired_deadline():
    budget = ExecutionBudget()
    budget.deadline = 0

    with pytest.raises(AgentBudgetExceeded):
        budget.check_time()


def test_invalid_budget():
    with pytest.raises(ValueError):
        ExecutionBudget(max_tool_calls=0)
