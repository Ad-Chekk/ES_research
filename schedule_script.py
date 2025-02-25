import schedule
import time
import subprocess

def run_script():
    subprocess.run(["python", "requests_metadata.py"])  # Replace 'script.py' with your actual script name

# Schedule the script to run every 15 minutes
schedule.every(15).minutes.do(run_script)

print("Scheduled to run script.py every 15 minutes...")

while True:
    schedule.run_pending()
    time.sleep(30)  # Check the schedule every 30 seconds
