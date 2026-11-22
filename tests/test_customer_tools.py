import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from customer_tools import (
    get_customer,
    get_recent_transactions,
)

def test_valid_customer():
    result = get_customer("CUST0001", "CUST0001")
    assert result["customer_id"] == "CUST0001"

def test_invalid_customer_id():
    with pytest.raises(ValidationError):
        get_customer("INVALID", "INVALID")

def test_recent_transactions():
    result = get_recent_transactions(
        "CUST0001",
        "CUST0001",
        limit=5,
    )
    assert len(result) == 5
    assert all(
        txn["account_id"] == "ACC0001"
        for txn in result
    )
    
def test_invalid_transaction_limit():
    with pytest.raises(ValueError):
        get_recent_transactions(
            "CUST0001",
            "CUST0001",
            limit=100,
        )


def test_cross_customer_transaction_access():
    with pytest.raises(PermissionError):
        get_recent_transactions(
            "CUST0002",
            "CUST0001",
        )