
import pytest
from google.genai import errors

from llm_retry import call_llm_with_retry, is_retryable


def test_timeout_retries_then_succeeds():
    attempts = []
    delays = []

    def unstable():
        attempts.append(1)
        if len(attempts) < 3:
            raise TimeoutError("Temporary timeout")
        return "success"

    result = call_llm_with_retry(
        unstable,
        sleep=delays.append,
        random_fn=lambda: 1.0,
    )

    assert result == "success"
    assert len(attempts) == 3
    assert delays == [0.5, 1.0]


def test_permission_error_not_retried():
    attempts = []

    def forbidden():
        attempts.append(1)
        raise PermissionError("Denied")

    with pytest.raises(PermissionError):
        call_llm_with_retry(
            forbidden,
            sleep=lambda _: None,
        )

    assert len(attempts) == 1


def test_server_error_retryable():
    assert is_retryable(
        errors.ServerError(
            503, {"message": "Unavailable"}
        )
    )


def test_bad_request_not_retryable():
    assert not is_retryable(
        errors.ClientError(
            400, {"message": "Invalid request"}
        )
    )


def test_invalid_attempt_count():
    with pytest.raises(ValueError):
        call_llm_with_retry(
            lambda: "ok",
            max_attempts=0,
        )
