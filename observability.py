
import json
import logging
import time
import uuid


logger = logging.getLogger("banking_agent")


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )


def new_request_id() -> str:
    return str(uuid.uuid4())


def build_event(event: str, request_id: str, **fields):
    return {
        "timestamp": time.time(),
        "event": event,
        "request_id": request_id,
        **fields,
    }


def log_event(event: str, request_id: str, **fields):
    record = build_event(event, request_id, **fields)
    logger.info(json.dumps(record))
