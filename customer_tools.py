from fileinput import filename
import json
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "customers.json"

class CustomerLookupInput(BaseModel):
    customer_id: str = Field(pattern=r"^CUST\d{4}$")



class CustomerNotFoundError(Exception):
    """Raised when a customer is not found in the data."""
    pass

def load_records(filename:str) -> list[dict]:
    path = DATA_DIR / filename

    with path.open("r", encoding="utf-8") as f:
        records = json.load(f)
        return records




def get_customer(customer_id: str,
                      authorized_customer_id: str) -> dict:
    """
    Return an authorized customer's profile.

    Args:
        customer_id (str): The ID of the customer to retrieve.
        authorized_customer_id (str): The ID of the authorized customer making the request.

    Returns:
        dict: The data for the specified customer.

    Raises:
        CustomerNotFoundError: If the customer with the given ID is not found.
    """

    args = CustomerLookupInput(customer_id=customer_id)

    if args.customer_id != authorized_customer_id:
        raise PermissionError("Unauthorized access to customer data.")

    customers = load_records("customers.json")
    
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    raise CustomerNotFoundError(f"Customer with ID {args.customer_id} not found.")


def get_recent_transactions(
    customer_id: str,
    authorized_customer_id: str,
    limit: int = 5,
) -> list[dict]:
    """Return the customer's latest transactions."""

    get_customer(customer_id, authorized_customer_id)

    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValueError("Limit must be an integer")

    if not 1 <= limit <= 20:
        raise ValueError("Limit must be between 1 and 20")

    accounts = load_records("accounts.json")
    transactions = load_records("transactions.json")

    account_ids = {
        account["account_id"]
        for account in accounts
        if account["customer_id"] == customer_id
    }

    matching = [
        transaction
        for transaction in transactions
        if transaction["account_id"] in account_ids
    ]

    matching.sort(
        key=lambda item: item["date"],
        reverse=True,
    )

    return matching[:limit]

##if __name__ == "__main__":
##    result = get_customer("SSCUST0001", "SSCUST0001")
##    print(result)