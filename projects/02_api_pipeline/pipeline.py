import requests   # makes HTTP calls — like a browser fetching a webpage, but in code
import json        # handles JSON data — the API's response format
import pandas as pd
from datetime import datetime

# ── STEP 1: DEFINE THE REQUEST ───────────────────────────────────────────────
# SQL analogy: writing your SELECT query before running it

# Open-Meteo is a free weather API — no API key needed
# We're asking for 7 days of daily weather for Los Angeles
BASE_URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 34.05,          # Los Angeles
    "longitude": -118.24,
    "daily": [
        "temperature_2m_max",   # daily high temp (°C)
        "temperature_2m_min",   # daily low temp (°C)
        "precipitation_sum",    # total rain (mm)
        "windspeed_10m_max",    # max wind speed (km/h)
    ],
    "timezone": "America/Los_Angeles",
}

# ── STEP 2: CALL THE API ─────────────────────────────────────────────────────
# SQL analogy: executing the query against the external source
print("Calling weather API...")
response = requests.get(BASE_URL, params=params)

# Check the response — 200 means success, like a query returning rows
if response.status_code != 200:
    print(f"API call failed with status: {response.status_code}")
    exit()

print(f"Success! Status code: {response.status_code}")

# ── STEP 3: PARSE AND SAVE RAW JSON ─────────────────────────────────────────
# SQL analogy: landing raw data into a staging table before transforming
data = response.json()  # converts the API response text into a Python dictionary

# Save raw JSON to file — good habit, keeps a copy of the source data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
raw_file = f"data/raw_weather_{timestamp}.json"

with open(raw_file, "w") as f:
    json.dump(data, f, indent=2)  # indent=2 makes it readable when you open the file

print(f"Raw data saved to: {raw_file}")

# ── STEP 4: LOAD INTO PANDAS ─────────────────────────────────────────────────
# SQL analogy: SELECT from staging table into a clean working table
# The API returns daily data nested under a "daily" key
daily = data["daily"]

df = pd.DataFrame({
    "date":        daily["time"],
    "temp_high_c": daily["temperature_2m_max"],
    "temp_low_c":  daily["temperature_2m_min"],
    "rainfall_mm": daily["precipitation_sum"],
    "max_wind_kmh":daily["windspeed_10m_max"],
})

# Convert Celsius to Fahrenheit — adding a calculated column
# SQL: SELECT *, (temp_high_c * 9/5) + 32 AS temp_high_f
df["temp_high_f"] = (df["temp_high_c"] * 9 / 5) + 32
df["temp_low_f"]  = (df["temp_low_c"]  * 9 / 5) + 32

print("\n=== 7-DAY FORECAST (Los Angeles) ===")
print(df[["date", "temp_high_f", "temp_low_f", "rainfall_mm", "max_wind_kmh"]].to_string(index=False))

# ── STEP 5: SUMMARIZE ────────────────────────────────────────────────────────
# SQL: SELECT AVG(temp_high_f), MAX(rainfall_mm) FROM forecast
print("\n=== WEEK SUMMARY ===")
print(f"Average high:   {df['temp_high_f'].mean():.1f}°F")
print(f"Average low:    {df['temp_low_f'].mean():.1f}°F")
print(f"Total rainfall: {df['rainfall_mm'].sum():.1f}mm")
print(f"Max wind speed: {df['max_wind_kmh'].max():.1f} km/h")

# ── STEP 6: OUTPUT ───────────────────────────────────────────────────────────
# SQL: INSERT INTO output_table or write to external stage
output_file = f"data/forecast_{timestamp}.csv"
df.to_csv(output_file, index=False)
print(f"\nForecast saved to: {output_file}")
