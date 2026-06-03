import schedule
import time
import json
import logging
from datetime import datetime
from pipeline_tasks import fetch_weather, quality_check

# ── LOGGING SETUP ─────────────────────────────────────────────────────────────
# logging = Python's built-in way to record events — replaces print()
# SQL analogy: writing to an audit log table instead of just SELECT-ing results
#
# Two handlers = two destinations for every log message:
#   1. Console  — you see it in the terminal while it runs
#   2. Log file — persisted to disk so you can review runs later

LOG_FILE     = "data/logs/run_log.json"
LOG_FILE_TXT = "data/logs/pipeline.log"

logging.basicConfig(
    level=logging.INFO,                          # INFO and above get recorded (INFO, WARNING, ERROR)
    format="%(asctime)s | %(levelname)-8s | %(message)s",   # timestamp | level | message
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE_TXT),       # write to file
        logging.StreamHandler(),                 # also print to terminal
    ]
)

logger = logging.getLogger(__name__)  # one logger per module — standard Python pattern


# ── RUN LOG ──────────────────────────────────────────────────────────────────
# Structured JSON log — one record per pipeline run (success or failure)
# SQL analogy: an audit table you can query to see run history

def write_log(status, message, duration_seconds):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append({
        "run_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status":   status,
        "message":  message,
        "duration": f"{duration_seconds:.1f}s",
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


# ── PIPELINE RUNNER ──────────────────────────────────────────────────────────
def run_pipeline():
    logger.info("=" * 50)
    logger.info("Pipeline started")
    logger.info("=" * 50)

    start = time.time()

    try:
        weather_file = fetch_weather()
        quality_check(weather_file)

        duration = time.time() - start
        write_log("SUCCESS", "All tasks completed", duration)
        logger.info(f"Pipeline PASSED in {duration:.1f}s")

    except Exception as e:
        duration = time.time() - start
        write_log("FAILED", str(e), duration)
        logger.error(f"Pipeline FAILED after {duration:.1f}s")
        logger.error(f"Error: {e}")


# ── SCHEDULER ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Scheduler starting — pipeline runs every 1 minute (Ctrl+C to stop)")

    run_pipeline()

    schedule.every(1).minutes.do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(10)
