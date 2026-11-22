
from dataclasses import dataclass, field
from time import monotonic


class AgentBudgetExceeded(Exception):
    pass


@dataclass
class ExecutionBudget:
    max_tool_calls: int = 8
    max_seconds: float = 60.0
    tool_calls: int = 0
    deadline: float = field(init=False)

    def __post_init__(self):
        if self.max_tool_calls < 1 or self.max_seconds <= 0:
            raise ValueError("Invalid budget")
        self.deadline = monotonic() + self.max_seconds

    def check_time(self):
        if monotonic() >= self.deadline:
            raise AgentBudgetExceeded("Time budget exceeded")

    def reserve_tool_call(self):
        self.check_time()

        if self.tool_calls >= self.max_tool_calls:
            raise AgentBudgetExceeded("Tool budget exceeded")

        self.tool_calls += 1
