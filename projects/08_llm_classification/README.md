# Project 08 — LLM API Classification

Call the Gemini API (free tier, no card required) to classify each city's
climate type from structured weather data (temp highs/lows, rainfall) —
first project that uses an LLM as part of the pipeline instead of
hand-written transform logic.

## What this covers
- Calling an LLM API over plain REST (`requests` — same library as Project 02)
- Reading a secret (API key) from an environment variable, never hardcoded
- Looping over rows, building a prompt per row, parsing the response
- Writing enriched output back to CSV

## SQL analogy
This is like a scalar UDF you can't express in plain SQL —
`dbo.ClassifyClimate(@temp_high, @temp_low, @rainfall)` — except the
"function body" is an LLM reasoning over the inputs instead of code you wrote.

## Getting a free API key
1. Go to https://aistudio.google.com/apikey
2. Sign in with a Google account, click "Create API key"
3. No credit card required — free tier with rate limits is enough for this project

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="your-key-here"
```

## Run
```bash
python classify_climate.py
```

## Output
`data/cities_classified.csv` — original columns plus a `climate_type` column.
