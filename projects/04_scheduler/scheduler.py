import schedule
import time
import json
from datetime import datetime
from pipeline_tasks import fetch_weather, quality_check  # import our two tasks

# ── RUN LOG ──────────────────────────────────────────────────────────────────
# Every run gets logged — success or failure, with timestamps
# SQL analogy: an audit/reconciliation log table

LOG_FILE = "data/logs/run_log.json"

def write_log(status, message, duration_seconds):
    """Appends a run record to the log file."""
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []  # start fresh if file doesn't exist yet

    logs.append({
        "run_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status":   status,
        "message":  message,
        "duration": f"{duration_seconds:.1f}s",
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


# ── PIPELINE RUNNER ──────────────────────────────────────────────────────────
# This is the function the scheduler calls — runs Task 1 then Task 2 in sequence
# SQL analogy: the Agent Job step that chains stored procedure calls

def run_pipeline():
    print(f"\n{'='*50}")
    print(f"Pipeline started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    start = time.time()

    try:
        # Step 1 — fetch data, get back the output file path
        weather_file = fetch_weather()

        # Step 2 — validate the file Task 1 produced
        quality_check(weather_file)

        duration = time.time() - start
        write_log("SUCCESS", "All tasks completed", duration)
        print(f"\nPipeline PASSED in {duration:.1f}s")

    except Exception as e:
        # If any task fails, log it and move on — don't crash the scheduler
        duration = time.time() - start
        write_log("FAILED", str(e), duration)
        print(f"\nPipeline FAILED after {duration:.1f}s")
        print(f"Error: {e}")


# ── SCHEDULER ────────────────────────────────────────────────────────────────
# This is what Airflow replaces — scheduling, retries, monitoring, alerting
# Right now we're doing it manually so you can see exactly what the pain is

if __name__ == "__main__":
    print("Scheduler starting...")
    print("Pipeline will run every 1 minute (Ctrl+C to stop)\n")

    # Run once immediately so you don't wait for the first interval
    run_pipeline()

    # Then schedule it to repeat every 1 minute
    # In production this would be "every day at 6am" or similar
    schedule.every(1).minutes.do(run_pipeline)

    # Keep the scheduler alive — checks every 10 seconds if a job is due
    while True:
        schedule.run_pending()
        time.sleep(10)
