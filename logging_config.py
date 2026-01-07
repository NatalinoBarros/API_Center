import logging
import os
from logging.handlers import RotatingFileHandler
from flask import has_request_context, request
from datetime import datetime  

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.method = request.method
            record.path = request.path
            record.remote_addr = request.remote_addr
        else:
            record.method = None
            record.path = None
            record.remote_addr = None
        return super().format(record)

def setup_logging(app=None, log_dir="logs", level=logging.INFO):
    os.makedirs(log_dir, exist_ok=True)

    fmt = RequestFormatter(
        "[%(asctime)s] %(levelname)s %(name)s "
        "remote=%(remote_addr)s %(method)s %(path)s - %(message)s"
    )
    date_str = datetime.now().strftime("%Y-%m-%d")  # ex: 2026-01-07 [web:68][web:81]
    log_filename = os.path.join(log_dir, f"app-{date_str}.log")  # [web:75][web:68]

    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=5_000_000,
        backupCount=5
    )
    
    file_handler.setLevel(level)
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(file_handler)
    root.addHandler(console_handler)

    if app is not None:
        app.logger.handlers = root.handlers
        app.logger.setLevel(level)
