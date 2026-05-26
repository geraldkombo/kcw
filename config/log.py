import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

request_id_var: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    return request_id_var.get()


def set_request_id(rid: str | None = None) -> str:
    rid = rid or uuid.uuid4().hex[:12]
    request_id_var.set(rid)
    return rid


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "-"
        return True


def configure_logging(log_level: str = "INFO", log_json: bool = True) -> None:
    handlers: list[logging.Handler] = []
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RequestIDFilter())

    if log_json:
        import json

        class JSONFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                obj: dict[str, Any] = {
                    "timestamp": self.formatTime(record, self.datefmt),
                    "level": record.levelname,
                    "logger": record.name,
                    "request_id": getattr(record, "request_id", "-"),
                    "message": record.getMessage(),
                }
                if record.exc_info and record.exc_info[0]:
                    obj["exception"] = self.formatException(record.exc_info)
                return json.dumps(obj, default=str)

        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] [%(request_id)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )

    handlers.append(handler)

    logging.basicConfig(level=getattr(logging, log_level.upper(), logging.INFO), handlers=handlers, force=True)

    for lib in ("httpx", "neo4j", "urllib3"):
        logging.getLogger(lib).setLevel(logging.WARNING)
