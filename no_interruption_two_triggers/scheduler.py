
from datetime import datetime, timedelta, timezone
from queue import Queue
from threading import Event, Thread, Lock

from apscheduler.schedulers.blocking import BlockingScheduler


def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def start_scheduler(task):
    queue = Queue()
    worker_busy = Event()

    pending_triggers = set()
    pending_lock = Lock()

    # Add a task to the FIFO queue.
    def enqueue(trigger_name):
        with pending_lock:
            if trigger_name in pending_triggers:
                print(
                    f"[{timestamp()}] {trigger_name} activated (already queued, skipped)",
                    flush=True,
                )
                return

            waiting = worker_busy.is_set() or not queue.empty()
            status = " (queued)" if waiting else ""

            pending_triggers.add(trigger_name)
            queue.put(trigger_name)

        print(
            f"[{timestamp()}] {trigger_name} activated{status}",
            flush=True,
        )

    # Execute queued tasks one at a time.
    def worker():
        while True:
            trigger_name = queue.get()

            with pending_lock:
                worker_busy.set()

            try:
                task(trigger_name)
            except Exception as error:
                print(f"[{timestamp()}] ERROR: {error}", flush=True)
            finally:
                with pending_lock:
                    pending_triggers.remove(trigger_name)
                    worker_busy.clear()
                queue.task_done()

    Thread(target=worker, daemon=True).start()

    # Configure the scheduler.
    scheduler = BlockingScheduler(timezone="UTC")

    reference_time = datetime.now(timezone.utc)

    scheduler.add_job(
        enqueue,
        trigger="interval",
        seconds=5,
        start_date=reference_time + timedelta(seconds=5),
        args=["trigger_5_seconds"],
        id="trigger_5_seconds",
    )

    scheduler.add_job(
        enqueue,
        trigger="interval",
        seconds=9.99,
        start_date=reference_time + timedelta(seconds=9.99),
        args=["trigger_almost_10_seconds"],
        id="trigger_almost_10_seconds",
    )

    print("Scheduler started. Press Ctrl+C to stop.")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped.")
