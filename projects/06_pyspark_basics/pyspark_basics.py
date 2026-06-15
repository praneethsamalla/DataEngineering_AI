from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, round

# SparkSession is the entry point to PySpark — like opening a database connection.
# "local[*]" means run on your laptop using all available CPU cores (no cluster needed).
spark = SparkSession.builder \
    .appName("VoyageAnalysis") \
    .master("local[*]") \
    .getOrCreate()

# Suppress noisy INFO logs so output is readable
spark.sparkContext.setLogLevel("WARN")

print("=" * 55)
print("Project 06 — PySpark Basics")
print("=" * 55)


# ── 1. READ CSV ──────────────────────────────────────────────
# SQL equivalent: CREATE TABLE voyages AS SELECT * FROM 'voyages.csv'
# inferSchema=True tells Spark to detect column types automatically
df = spark.read.csv("data/voyages.csv", header=True, inferSchema=True)

print("\n[1] Schema (column names + detected types)")
print("    SQL equivalent: DESCRIBE TABLE voyages")
df.printSchema()


# ── 2. SELECT * LIMIT 5 ──────────────────────────────────────
# SQL equivalent: SELECT * FROM voyages LIMIT 5
print("[2] First 5 rows (SELECT * FROM voyages LIMIT 5)")
df.show(5)


# ── 3. SELECT specific columns ───────────────────────────────
# SQL equivalent: SELECT voyage_id, ship_name, destination, revenue_usd FROM voyages
print("[3] Select specific columns")
df.select("voyage_id", "ship_name", "destination", "revenue_usd").show()


# ── 4. WHERE filter ──────────────────────────────────────────
# SQL equivalent: SELECT * FROM voyages WHERE destination = 'Caribbean'
print("[4] Filter: Caribbean voyages only")
df.filter(col("destination") == "Caribbean").show()


# ── 5. GROUP BY + aggregates ─────────────────────────────────
# SQL equivalent:
#   SELECT destination,
#          COUNT(*) AS voyage_count,
#          ROUND(AVG(passengers), 0) AS avg_passengers,
#          SUM(revenue_usd) AS total_revenue
#   FROM voyages
#   GROUP BY destination
#   ORDER BY total_revenue DESC
print("[5] GROUP BY destination — voyage count, avg passengers, total revenue")
df.groupBy("destination") \
    .agg(
        count("*").alias("voyage_count"),
        round(avg("passengers"), 0).alias("avg_passengers"),
        sum("revenue_usd").alias("total_revenue")
    ) \
    .orderBy(col("total_revenue").desc()) \
    .show()


# ── 6. Add a calculated column ───────────────────────────────
# SQL equivalent: SELECT *, ROUND(revenue_usd / passengers, 2) AS revenue_per_pax FROM voyages
print("[6] Add calculated column: revenue per passenger")
df.withColumn("revenue_per_pax", round(col("revenue_usd") / col("passengers"), 2)) \
    .select("voyage_id", "ship_name", "destination", "revenue_per_pax") \
    .orderBy(col("revenue_per_pax").desc()) \
    .show()


# ── 7. Write output to Parquet ───────────────────────────────
# SQL equivalent: CREATE TABLE voyage_output AS SELECT ...
# Parquet is the standard columnar format in DE — like a compressed, indexed CSV
# that query engines (Spark, Snowflake, dbt) read 10x faster than CSV
print("[7] Writing output to Parquet format...")
df.write.mode("overwrite").parquet("data/voyages_output")
print("    Saved to data/voyages_output/")


spark.stop()
print("\nDone.")
