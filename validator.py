import csv
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

REQUIRED_COLUMNS = {"transaction_id", "account_number", "amount", "currency", "reference"}
ALLOWED_CURRENCIES = {"PYG", "USD"}


def validate_batch_file(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        logging.error(f"Input file not found: {file_path}")
        return {"total": 0, "valid": 0, "rejected": 0}

    logging.info(f"Starting batch validation for: {path.name}")
    seen_ids = set()
    valid_rows = []
    rejected_rows = []

    with path.open(mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(set(reader.fieldnames)):
            logging.error(f"Invalid CSV header. Expected: {REQUIRED_COLUMNS}")
            return {"total": 0, "valid": 0, "rejected": 0}

        for row_num, row in enumerate(reader, start=2):
            txn_id = row["transaction_id"].strip()
            account = row["account_number"].strip()
            currency = row["currency"].strip().upper()
            errors = []

            if txn_id in seen_ids:
                errors.append(f"Duplicate transaction_id '{txn_id}'")
            else:
                seen_ids.add(txn_id)

            if not account.isdigit() or len(account) < 6:
                errors.append(f"Invalid account_number '{account}'")

            try:
                amount = float(row["amount"])
                if amount <= 0:
                    errors.append(f"Invalid amount '{row['amount']}' (must be > 0)")
            except ValueError:
                errors.append(f"Non-numeric amount '{row['amount']}'")

            if currency not in ALLOWED_CURRENCIES:
                errors.append(f"Unsupported currency '{currency}'")

            if errors:
                logging.error(f"Row {row_num} ({txn_id}): {', '.join(errors)}")
                rejected_rows.append(row)
            else:
                valid_rows.append(row)

    total = len(valid_rows) + len(rejected_rows)
    logging.info(
        f"Validation completed. Total: {total} | Valid: {len(valid_rows)} | Rejected: {len(rejected_rows)}"
    )
    return {"total": total, "valid": len(valid_rows), "rejected": len(rejected_rows)}


if __name__ == "__main__":
    validate_batch_file("sample_batch.csv")
