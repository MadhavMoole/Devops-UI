import logging
import sys
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# Custom formatter for structured-like logging
class StructuredFormatter(logging.Formatter):
    def format(self, record):
        # In a real production app, we would use json-logging or structlog
        # to output JSON for ELK/Loki.
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return f"[{log_record['timestamp']}] {log_record['level']} | {log_record['module']}.{log_record['funcName']} | {log_record['message']}"

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("devops_manager")
    logger.setLevel(logging.INFO)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(StructuredFormatter())
    logger.addHandler(console_handler)
    
    # File Handler (Rotating)
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(StructuredFormatter())
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()
