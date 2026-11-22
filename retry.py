import time

def call_with_retry(
    fn,
    max_attempts=3,
    base_delay=0.5,
    sleep=time.sleep,
    retryable=(TimeoutError, ConnectionError),
):
    """Retry selected transient errors with backoff."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    for attempt in range(1, max_attempts + 1):
        try:
            return fn()

        except retryable:
            if attempt == max_attempts:
                raise

            delay = base_delay * (2 ** (attempt - 1))
            sleep(delay)