
import random
import time

from google.genai import errors

RETRYABLE_CODES = {429, 500, 502, 503, 504}


def is_retryable(exc: Exception) -> bool:
    if isinstance(exc, (TimeoutError, ConnectionError)):
        return True

    if isinstance(exc, errors.APIError):
        return getattr(exc, "code", None) in RETRYABLE_CODES

    return False


def call_llm_with_retry(
    fn,
    max_attempts=3,
    base_delay=0.5,
    max_delay=5.0,
    sleep=time.sleep,
    random_fn=random.random,
):
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")

    if base_delay < 0 or max_delay < 0:
        raise ValueError("Delays cannot be negative")

    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as exc:
            final_attempt = attempt == max_attempts - 1

            if final_attempt or not is_retryable(exc):
                raise

            cap = min(
                base_delay * (2 ** attempt),
                max_delay,
            )
            sleep(cap * random_fn())
