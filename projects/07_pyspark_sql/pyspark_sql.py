from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("VoyageSQL") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("=" * 55)
print("Project 07 — PySpark SQL")
print("=" * 55)


# ── 1. LOAD CSV INTO DATAFRAME ───────────────────────────────
df = spark.read.csv("data/voyages.csv", header=True, inferSchema=True)


# ── 2. REGISTER AS TEMP VIEW ─────────────────────────────────
# SQL equivalent: CREATE OR REPLACE TEMP VIEW voyages AS SELECT * FROM ...
# This makes the DataFrame queryable with real SQL for the rest of this session.
df.createOrReplaceTempView("voyages")

print("\n[1] Temp view registered: 'voyages'")
print("    You can now run SQL against it just like a table.\n")


# ── 3. BASIC SELECT ──────────────────────────────────────────
# Exactly the SQL you already know — no translation needed.
print("[2] SELECT with WHERE clause")
spark.sql("""
    SELECT voyage_id, ship_name, destination, revenue_usd
    FROM voyages
    WHERE destination = 'Caribbean'
    ORDER BY revenue_usd DESC
""").show()


# ── 4. GROUP BY + aggregates ─────────────────────────────────
print("[3] GROUP BY destination — revenue summary")
spark.sql("""
    SELECT
        destination,
        COUNT(*)                            AS voyage_count,
        ROUND(AVG(passengers), 0)           AS avg_passengers,
        SUM(revenue_usd)                    AS total_revenue,
        ROUND(AVG(revenue_usd), 0)          AS avg_revenue
    FROM voyages
    GROUP BY destination
    ORDER BY total_revenue DESC
""").show()


# ── 5. CALCULATED COLUMN ─────────────────────────────────────
print("[4] Revenue per passenger by voyage")
spark.sql("""
    SELECT
        voyage_id,
        ship_name,
        destination,
        ROUND(revenue_usd / passengers, 2)  AS revenue_per_pax
    FROM voyages
    ORDER BY revenue_per_pax DESC
""").show()


# ── 6. SUBQUERY ──────────────────────────────────────────────
# SQL Server equivalent: SELECT ... FROM (SELECT ...) subq WHERE ...
# Find voyages where revenue is above the overall average
print("[5] Subquery — voyages above average revenue")
spark.sql("""
    SELECT voyage_id, ship_name, destination, revenue_usd
    FROM voyages
    WHERE revenue_usd > (SELECT AVG(revenue_usd) FROM voyages)
    ORDER BY revenue_usd DESC
""").show()


# ── 7. MIX SQL + DATAFRAME API ───────────────────────────────
# You can take a SQL result and keep working on it with the DataFrame API.
# This is common in real pipelines — SQL for the heavy lifting, then DF for final tweaks.
print("[6] SQL result handed off to DataFrame API for final output")
result_df = spark.sql("""
    SELECT
        ship_name,
        COUNT(*)            AS voyages,
        SUM(revenue_usd)    AS total_revenue
    FROM voyages
    GROUP BY ship_name
    ORDER BY total_revenue DESC
""")

result_df.show()


# ── 8. WRITE TO PARQUET ──────────────────────────────────────
print("[7] Writing ship revenue summary to Parquet...")
result_df.write.mode("overwrite").parquet("data/ship_revenue_output")
print("    Saved to data/ship_revenue_output/")


spark.stop()
print("\nDone.")
