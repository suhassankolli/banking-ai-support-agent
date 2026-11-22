
import sys
from pathlib import Path

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from retry import call_with_retry


def test_retry_succeeds_after_transient_failure():
    attempts = []
    delays = []

    def unstable():
        attempts.append(1)

        if len(attempts) < 3:
            raise TimeoutError("Temporary failure")

        return "success"

    result = call_with_retry(
        unstable,
        sleep=delays.append,
    )

    assert result == "success"
    assert len(attempts) == 3
    assert delays == [0.5, 1.0]


def test_non_transient_error_not_retried():
    attempts = []

    def unauthorized():
        attempts.append(1)
        raise PermissionError("Access denied")

    with pytest.raises(PermissionError):
        call_with_retry(
            unauthorized,
            sleep=lambda _: None,
        )

    assert len(attempts) == 1
