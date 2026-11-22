import csv
import json
import random
from pathlib import Path
from datetime import date, timedelta


DATA_DIR = Path(__file__).parent/ "data"
DATA_DIR.mkdir(exist_ok=True)

rng = random.Random(42)  # Seed for reproducibility

customers = []
accounts = []
transactions = []

for i in range(1, 101):
    cusomer_id = f"CUST{i:04d}"
    account_id = f"ACC{i:04d}"


    customers.append({
        "customer_id": cusomer_id,
        "name": f"Demo Customer {i}",
        "status": "ACTIVE" 
    })

    accounts.append({
        "account_id": account_id,
        "customer_id": cusomer_id,
        "balance": round(rng.uniform(1000, 25000), 2)
    })

    for j in range(1, 11):
        transactions.append({
            "transaction_id": f"TXN{i:04d}{j:02d}",
            "account_id": account_id,
            "date": (
                date(2026, 10, 31)
                - timedelta(days=j)
            ).isoformat(),
            "amount": round(rng.uniform(-500, 1000), 2),
            "description": f"Demo transaction {j}",
        })


def save_json(filename, records):
    path = DATA_DIR / filename
    path.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )


save_json("customers.json", customers)
save_json("accounts.json", accounts)
save_json("transactions.json", transactions)

print(f"Generated {len(customers)} customers")
print(f"Generated {len(accounts)} accounts")
print(f"Generated {len(transactions)} transactions")
