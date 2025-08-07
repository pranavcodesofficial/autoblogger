# scheduler.py
import schedule
import time
import subprocess
from datetime import datetime

def run_generator():
    print(f"[{datetime.now()}] 🚀 Running autoblog generator...")
    subprocess.run(["python", "autoblogger/generator.py"])

# Schedule daily at 9 AM
schedule.every().day.at("09:00").do(run_generator)

print("🕒 Scheduler is running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)