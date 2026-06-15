# Project 06 — PySpark Basics

Learn the PySpark DataFrame API by mapping every operation to SQL equivalents.

## What this covers
- Creating a SparkSession (your "database connection")
- Reading CSV into a DataFrame
- SELECT, WHERE, GROUP BY, ORDER BY
- Adding calculated columns (withColumn)
- Writing output to Parquet format

## SQL ↔ PySpark cheat sheet

| SQL | PySpark |
|-----|---------|
| `SELECT *` | `df.show()` |
| `SELECT col1, col2` | `df.select("col1", "col2")` |
| `WHERE col = 'x'` | `df.filter(col("x") == "x")` |
| `GROUP BY` + `COUNT/SUM/AVG` | `df.groupBy().agg(count(), sum(), avg())` |
| `ORDER BY col DESC` | `.orderBy(col("x").desc())` |
| `SELECT *, a/b AS new_col` | `df.withColumn("new_col", col("a") / col("b"))` |
| `LIMIT 5` | `df.show(5)` |
| `DESCRIBE TABLE` | `df.printSchema()` |

## Setup

```bash
cd projects/06_pyspark_basics
source venv/bin/activate
python pyspark_basics.py
```

## Why Parquet?
Parquet is the standard output format in modern DE pipelines. Compared to CSV:
- Columnar storage — reads only the columns a query needs
- Built-in compression — typically 5–10x smaller than CSV
- Schema embedded — no guessing column types
- Native format for Snowflake external stages, Delta Lake, and Spark
