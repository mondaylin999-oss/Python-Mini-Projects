import os
import asyncio
import sqlite3
import time
import psutil

# --- PATH LOCKING ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "metrics.db")


class MetricsDatabase:
    """Handles synchronous SQLite logging (typical in async wrappers)."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_usage REAL NOT NULL,
                ram_usage REAL NOT NULL,
                metric_type TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def log_metric(self, cpu, ram, metric_type):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO system_logs (timestamp, cpu_usage, ram_usage, metric_type) VALUES (?, ?, ?, ?)",
            (timestamp, cpu, ram, metric_type)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()


async def monitor_system_resources(db):
    """Task A: Async task running every 2 seconds to poll CPU and RAM."""
    print("🚀 Task 1: System Resource Monitor Started...")
    
    try:
        while True:
            # psutil fetches hardware status
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
            
            print(f"📊 [RESOURCE CHECK] CPU Usage: {cpu}% | RAM Usage: {ram}%")
            db.log_metric(cpu, ram, "Hardware_Check")

            # Non-blocking pause: allows the event loop to switch to other tasks!
            await asyncio.sleep(2)
            
    except asyncio.CancelledError:
        print("🛑 Task 1: Resource Monitor Stopped.")


async def simulate_background_health_check(db):
    """Task B: Async task running every 5 seconds simulating network/server pings."""
    print("🌐 Task 2: Background Health Checker Started...")
    
    try:
        while True:
            await asyncio.sleep(5)
            
            # Simulated non-blocking server check
            cpu_snapshot = psutil.cpu_percent(interval=None)
            ram_snapshot = psutil.virtual_memory().percent
            
            print("🟢 [HEALTH CHECK] Server Status: HEALTHY | System Logged.")
            db.log_metric(cpu_snapshot, ram_snapshot, "Health_Check")

    except asyncio.CancelledError:
        print("🛑 Task 2: Health Checker Stopped.")


async def main():
    db = MetricsDatabase()
    print("=== ⚡ ASYNC SYSTEM MONITORING ENGINE ===")
    print("Press Ctrl+C in terminal to stop monitoring gracefully.\n")

    # Schedule both asynchronous tasks concurrently on the Event Loop
    task1 = asyncio.create_task(monitor_system_resources(db))
    task2 = asyncio.create_task(simulate_background_health_check(db))

    try:
        # Run both tasks concurrently
        await asyncio.gather(task1, task2)
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user! Shutting down async event loop...")
        task1.cancel()
        task2.cancel()
        await asyncio.gather(task1, task2, return_exceptions=True)
    finally:
        db.close()
        print("📁 Database connection closed. Clean shutdown complete!")


if __name__ == "__main__":
    # Entry point for the asyncio Event Loop
    asyncio.run(main())