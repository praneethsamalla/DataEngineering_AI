import requests
import pandas as pd
import logging
from datetime import datetime

# ── LOGGING SETUP ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("data/pipeline.log"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


# ── SOURCE 1: CITY REFERENCE DATA (CSV) ──────────────────────────────────────
# SQL analogy: SELECT * FROM city_reference_table
# This is your "dimension table" — static reference data about each city

def load_city_data():
    logger.info("Loading city reference data from CSV...")
    df = pd.read_csv("data/cities.csv")
    logger.info(f"Loaded {len(df)} cities")
    return df


# ── SOURCE 2: LIVE WEATHER DATA (API) ────────────────────────────────────────
# SQL analogy: SELECT * FROM external_weather_source
# This is your "fact data" — live metrics for each city

def fetch_weather_for_city(city, latitude, longitude):
    """Calls Open-Meteo API for a single city. Returns today's forecast as a dict."""
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":  latitude,
        "longitude": longitude,
        "daily":     ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone":  "auto",  # auto-detect timezone from coordinates
        "forecast_days": 1,   # just today
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"API failed for {city} — status: {response.status_code}")

    data = response.json()["daily"]

    return {
        "city":         city,
        "temp_high_f":  round((data["temperature_2m_max"][0] * 9 / 5) + 32, 1),
        "temp_low_f":   round((data["temperature_2m_min"][0] * 9 / 5) + 32, 1),
        "rainfall_mm":  data["precipitation_sum"][0],
    }


def load_weather_data(cities_df):
    """Loops through each city and fetches weather. Returns a DataFrame."""
    logger.info("Fetching live weather for all cities...")
    records = []

    for _, row in cities_df.iterrows():  # iterrows() = looping through rows like a cursor
        try:
            record = fetch_weather_for_city(row["city"], row["latitude"], row["longitude"])
            records.append(record)
            logger.info(f"  {row['city']}: {record['temp_high_f']}°F high")
        except Exception as e:
            logger.error(f"  {row['city']}: FAILED — {e}")

    df = pd.DataFrame(records)
    logger.info(f"Weather fetched for {len(df)} cities")
    return df


# ── STEP 3: MERGE ─────────────────────────────────────────────────────────────
# SQL analogy: SELECT * FROM city_reference r JOIN weather w ON r.city = w.city
# This is the core of this project — combining two sources into one dataset

def merge_sources(cities_df, weather_df):
    logger.info("Merging city reference data with weather data...")

    merged = cities_df.merge(
        weather_df,
        on="city",        # JOIN ON city name — like ON r.city = w.city
        how="inner",      # INNER JOIN — only cities that appear in both sources
    )

    # Drop coordinate columns — not needed in the output
    merged = merged.drop(columns=["latitude", "longitude"])

    logger.info(f"Merged dataset: {len(merged)} rows, {len(merged.columns)} columns")
    return merged


# ── STEP 4: ANALYZE ───────────────────────────────────────────────────────────
# SQL analogy: GROUP BY region with aggregates

def summarize(merged_df):
    logger.info("Summarizing by region...")

    summary = (
        merged_df.groupby("region")
        .agg(
            cities=("city", "count"),                    # COUNT(city)
            avg_high_f=("temp_high_f", "mean"),          # AVG(temp_high_f)
            total_population=("population_millions", "sum"),  # SUM(population)
        )
        .round(1)
        .reset_index()
        .sort_values("avg_high_f", ascending=False)
    )

    return summary


# ── STEP 5: OUTPUT ────────────────────────────────────────────────────────────
def save_output(merged_df, summary_df):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    merged_file  = f"data/merged_{timestamp}.csv"
    summary_file = f"data/summary_{timestamp}.csv"

    merged_df.to_csv(merged_file, index=False)
    summary_df.to_csv(summary_file, index=False)

    logger.info(f"Merged data saved to:  {merged_file}")
    logger.info(f"Summary saved to:      {summary_file}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Pipeline starting...")

    cities_df  = load_city_data()
    weather_df = load_weather_data(cities_df)
    merged_df  = merge_sources(cities_df, weather_df)
    summary_df = summarize(merged_df)

    print("\n=== MERGED DATASET ===")
    print(merged_df[["city", "region", "population_millions", "temp_high_f", "temp_low_f", "rainfall_mm"]].to_string(index=False))

    print("\n=== SUMMARY BY REGION ===")
    print(summary_df.to_string(index=False))

    save_output(merged_df, summary_df)
    logger.info("Pipeline complete.")
