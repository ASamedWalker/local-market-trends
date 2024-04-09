import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import subprocess

class ChangeHandler(LoggingEventHandler):
    """Logs all the events captured."""

    def on_modified(self, event):
        super().on_modified(event)
        if not event.is_directory:
            print(f"Detected change in {event.src_path}, running seed_data.py")
            subprocess.run(["python", "-m", "src.data.seed_data"])

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else './src'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()