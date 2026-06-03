import requests
import pandas as pd
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)  # inherits config set up in scheduler.py

# ── TASK 1: FETCH WEATHER DATA ───────────────────────────────────────────────
def fetch_weather():
    logger.info("[Task 1] Fetching weather data...")

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 34.05,
        "longitude": -118.24,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "windspeed_10m_max"],
        "timezone": "America/Los_Angeles",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"API call failed — status code: {response.status_code}")

    data = response.json()
    daily = data["daily"]

    df = pd.DataFrame({
        "date":         daily["time"],
        "temp_high_c":  daily["temperature_2m_max"],
        "temp_low_c":   daily["temperature_2m_min"],
        "rainfall_mm":  daily["precipitation_sum"],
        "max_wind_kmh": daily["windspeed_10m_max"],
    })

    df["temp_high_f"] = (df["temp_high_c"] * 9 / 5) + 32
    df["temp_low_f"]  = (df["temp_low_c"]  * 9 / 5) + 32

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"data/weather_{timestamp}.csv"
    df.to_csv(output_file, index=False)

    logger.info(f"[Task 1] Done — {len(df)} rows saved to {output_file}")
    return output_file


# ── TASK 2: QUALITY CHECK ────────────────────────────────────────────────────
def quality_check(file_path):
    logger.info(f"[Task 2] Running quality check on {file_path}...")

    df = pd.read_csv(file_path)
    issues = []

    for col in ["date", "temp_high_f", "temp_low_f"]:
        if df[col].isnull().any():
            issues.append(f"Null values found in column: {col}")

    if (df["temp_high_f"] < 32).any() or (df["temp_high_f"] > 130).any():
        issues.append("temp_high_f has values outside realistic range (32–130°F)")

    if len(df) != 7:
        issues.append(f"Expected 7 rows, got {len(df)}")

    if issues:
        raise Exception("Quality check failed:\n" + "\n".join(f"  - {i}" for i in issues))

    logger.info(f"[Task 2] All checks passed — {len(df)} rows, data looks good")
