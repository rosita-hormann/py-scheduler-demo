
import time

from scheduler import start_scheduler, timestamp


def task(trigger_name):
    print(f"[{timestamp()}] START: {trigger_name}", flush=True)

    time.sleep(12)

    print(f"[{timestamp()}] END: {trigger_name}", flush=True)


if __name__ == "__main__":
    start_scheduler(task)
