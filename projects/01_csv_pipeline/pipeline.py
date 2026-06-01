import pandas as pd  # pandas = Python's data table library, like a SQL result set you can manipulate

# ── STEP 1: LOAD ────────────────────────────────────────────────────────────
# SQL equivalent: COPY INTO staging_table FROM 'sales.csv'
df = pd.read_csv("data/sales.csv")

print("=== RAW DATA (first 5 rows) ===")
print(df.head())          # SQL: SELECT * FROM sales LIMIT 5
print()

print("=== COLUMN TYPES ===")
print(df.dtypes)          # SQL: sp_help / DESCRIBE TABLE
print()

# ── STEP 2: TRANSFORM ───────────────────────────────────────────────────────
# Add a calculated column: total_sales = quantity * unit_price
# SQL equivalent: SELECT *, quantity * unit_price AS total_sales FROM sales
df["total_sales"] = df["quantity"] * df["unit_price"]

# Filter: only rows where total_sales > 200
# SQL equivalent: WHERE quantity * unit_price > 200
df_filtered = df[df["total_sales"] > 200]

print("=== FILTERED: orders where total_sales > 200 ===")
print(df_filtered[["order_id", "region", "product", "total_sales"]])
print()

# ── STEP 3: AGGREGATE ───────────────────────────────────────────────────────
# Group by region and sum total_sales
# SQL equivalent: SELECT region, SUM(total_sales) AS revenue FROM sales GROUP BY region ORDER BY revenue DESC
summary = (
    df.groupby("region")["total_sales"]
    .sum()
    .reset_index()                        # keeps region as a column (not just an index)
    .rename(columns={"total_sales": "revenue"})
    .sort_values("revenue", ascending=False)
)

print("=== REVENUE BY REGION ===")
print(summary)
print()

# ── STEP 4: OUTPUT ──────────────────────────────────────────────────────────
# Write results to a new CSV
# SQL equivalent: INSERT INTO output_table or COPY INTO external stage
summary.to_csv("data/output_summary.csv", index=False)  # index=False = don't write row numbers
df_filtered.to_csv("data/output_filtered.csv", index=False)

print("=== DONE ===")
print("Files written to data/output_summary.csv and data/output_filtered.csv")
