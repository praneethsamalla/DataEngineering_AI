import pandas as pd
import json
from datetime import datetime

# ── CONFIGURATION ────────────────────────────────────────────────────────────
# Define expectations for this dataset — like constraints you'd put on a SQL table
RULES = {
    "required_columns": ["order_id", "customer_name", "region", "product", "quantity", "unit_price", "order_date"],
    "not_null":         ["order_id", "customer_name", "region", "quantity", "unit_price"],
    "unique":           ["order_id"],
    "positive_values":  ["quantity", "unit_price"],  # no negative quantities or prices
    "value_ranges": {
        "quantity":   {"min": 1,  "max": 500},   # flag suspiciously large orders
        "unit_price": {"min": 1,  "max": 1000},
    },
}

# ── LOAD DATA ────────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv("data/orders.csv")
print(f"Rows loaded: {len(df)}\n")

# ── RUN CHECKS ───────────────────────────────────────────────────────────────
issues = []  # collect all problems found — SQL analogy: rows in an error log table

# CHECK 1: Required columns present
# SQL: verify all expected columns exist in the table schema
print("Running checks...")
missing_cols = [c for c in RULES["required_columns"] if c not in df.columns]
if missing_cols:
    issues.append({"check": "missing_columns", "detail": missing_cols, "rows": "N/A"})

# CHECK 2: Null values in required fields
# SQL: SELECT * FROM orders WHERE order_id IS NULL OR customer_name IS NULL ...
for col in RULES["not_null"]:
    null_rows = df[df[col].isnull()]
    if not null_rows.empty:
        issues.append({
            "check": "null_value",
            "detail": f"Column '{col}' has {len(null_rows)} null(s)",
            "rows": null_rows.index.tolist(),
        })

# CHECK 3: Duplicate unique keys
# SQL: SELECT order_id, COUNT(*) FROM orders GROUP BY order_id HAVING COUNT(*) > 1
for col in RULES["unique"]:
    dupes = df[df.duplicated(subset=[col], keep=False)]
    if not dupes.empty:
        issues.append({
            "check": "duplicate_key",
            "detail": f"Column '{col}' has {len(dupes)} duplicate rows",
            "rows": dupes.index.tolist(),
        })

# CHECK 4: Negative values
# SQL: SELECT * FROM orders WHERE quantity < 0 OR unit_price < 0
for col in RULES["positive_values"]:
    if col in df.columns:
        neg_rows = df[df[col] < 0]
        if not neg_rows.empty:
            issues.append({
                "check": "negative_value",
                "detail": f"Column '{col}' has {len(neg_rows)} negative value(s)",
                "rows": neg_rows.index.tolist(),
            })

# CHECK 5: Out of range values
# SQL: SELECT * FROM orders WHERE quantity > 500 OR quantity < 1
for col, bounds in RULES["value_ranges"].items():
    if col in df.columns:
        out_of_range = df[(df[col] < bounds["min"]) | (df[col] > bounds["max"])]
        if not out_of_range.empty:
            issues.append({
                "check": "out_of_range",
                "detail": f"Column '{col}' has {len(out_of_range)} value(s) outside [{bounds['min']}, {bounds['max']}]",
                "rows": out_of_range.index.tolist(),
            })

# ── REPORT ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("DATA QUALITY REPORT")
print("=" * 50)
print(f"File:        data/orders.csv")
print(f"Rows:        {len(df)}")
print(f"Checks run:  5")
print(f"Issues found:{len(issues)}")
print("=" * 50)

if not issues:
    print("ALL CHECKS PASSED")
else:
    for i, issue in enumerate(issues, 1):
        print(f"\n[Issue {i}] {issue['check'].upper()}")
        print(f"  Detail: {issue['detail']}")
        print(f"  Rows:   {issue['rows']}")

# ── SAVE REPORT ──────────────────────────────────────────────────────────────
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report = {
    "run_at":       timestamp,
    "file":         "data/orders.csv",
    "row_count":    len(df),
    "issues_found": len(issues),
    "issues":       issues,
}

report_file = f"data/quality_report_{timestamp}.json"
with open(report_file, "w") as f:
    json.dump(report, f, indent=2)

print(f"\nReport saved to: {report_file}")
print("PASS" if not issues else "FAIL — review issues above")
