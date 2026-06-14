from enum import Enum


class Status(str, Enum):
    OK: str = "success"
    BAD: str = "error"
