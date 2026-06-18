# Project 07 — PySpark SQL

Run real SQL queries against a Spark DataFrame using temp views.

## What this covers
- Registering a DataFrame as a SQL temp view (`createOrReplaceTempView`)
- Running `spark.sql()` with SELECT, WHERE, GROUP BY, subqueries
- Mixing the SQL API and DataFrame API in the same pipeline
- Writing results to Parquet

## SQL analogy
`createOrReplaceTempView("voyages")` is equivalent to:
```sql
CREATE OR REPLACE TEMP VIEW voyages AS SELECT * FROM ...;
```
After that, `spark.sql("SELECT ...")` is identical to running SQL in SQL Server or Snowflake.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python pyspark_sql.py
```

## Output
- Console: query results for each step
- `data/ship_revenue_output/` — Parquet files with ship revenue summary
