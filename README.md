# batch-file-validator-python
Automated batch file validator and audit logger in Python for transactional CSV processing.

# ⚙️ Batch File Validator & Audit Logger (Python)

A lightweight Python CLI utility designed to simulate pre-processing validation, data integrity checks, and structured audit logging for batch transactional files (such as payroll or mass payment CSVs).

## 🚀 Key Features
- **Schema & Header Validation:** Verifies required columns (`transaction_id`, `account_number`, `amount`, `currency`, `status`).
- **Business Rule Checks:** Detects duplicate transaction IDs, negative/zero amounts, invalid currency codes (`PYG`, `USD`), and malformed account numbers.
- **Audit Logging & Summary Report:** Generates an execution log (`audit.log`) and separates valid records from rejected ones for operational traceability.

## 🛠️ Tech Stack
- **Language:** Python 3.10+ (Standard Library: `csv`, `logging`, `datetime`, `pathlib`)
- **Use Case:** Batch Operations, Production Control, Data Quality Verification

## ▶️ How to Run
```bash
python validator.py
[2026-11-12 10:00:01] INFO - Starting batch validation for: sample_batch.csv
[2026-11-12 10:00:01] ERROR - Row 3 (TXN-1003): Invalid amount '-50000' (must be > 0)
[2026-11-12 10:00:01] ERROR - Row 5 (TXN-1002): Duplicate transaction_id detected
[2026-11-12 10:00:01] INFO - Validation completed. Total: 5 | Valid: 3 | Rejected: 2
