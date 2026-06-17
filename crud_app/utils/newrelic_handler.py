import logging
import requests
import json
import threading
import queue
import time
from crud_app.config.settings import NEW_RELIC_LICENSE_KEY

# New Relic Log API Endpoint
NEW_RELIC_LOG_URL = "https://log-api.newrelic.com/log/v1"

class NewRelicLogHandler(logging.Handler):
    def __init__(self, batch_size=10, flush_interval=5):
        super().__init__()
        self.queue = queue.Queue()
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.worker_thread = None
        self._lock = threading.Lock()
        
        # Use a Session to pool connections and reduce overhead
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Api-Key": NEW_RELIC_LICENSE_KEY
        })
        
    def _start_worker(self):
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.worker_thread = threading.Thread(target=self._process_logs, daemon=True)
            self.worker_thread.start()
        
    def emit(self, record):
        try:
            with self._lock:
                self._start_worker()

            # Format the log record into a string message
            log_message = self.format(record)
            
            # Base attributes
            attributes = {
                "service.name": "support-ticket-service",
                "file.name": record.filename,
                "line.number": record.lineno
            }
            
            # Parse custom key=value pairs from the message (e.g., ticketId=INC-4, event=ticket_creation)
            # The message looks like: ... | traceId=... | service=... | ticketId=...
            parts = log_message.split(" | ")
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    attributes[k.strip()] = v.strip()
            
            # We can also extract structured data from the record if needed
            log_data = {
                "message": log_message,
                "log.level": record.levelname,
                "logger.name": record.name,
                "attributes": attributes
            }
            
            self.queue.put(log_data)
        except Exception:
            self.handleError(record)

    def _process_logs(self):
        while True:
            logs = []
            try:
                # Try to get logs from the queue
                while len(logs) < self.batch_size:
                    log_entry = self.queue.get(timeout=self.flush_interval)
                    logs.append(log_entry)
            except queue.Empty:
                pass
            
            if logs:
                self._send_to_newrelic(logs)
                
    def _send_to_newrelic(self, logs):
        if not NEW_RELIC_LICENSE_KEY:
            # If no license key is configured, do not attempt to send
            return
        
        try:
            response = self.session.post(NEW_RELIC_LOG_URL, json=logs, timeout=5)
            if response.status_code >= 400:
                print(f"Failed to send logs to New Relic: {response.text}")
        except Exception as e:
            print(f"Exception sending logs to New Relic: {e}")
