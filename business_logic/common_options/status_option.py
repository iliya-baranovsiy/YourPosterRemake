from enum import Enum
from dataclasses import dataclass
from business_logic.services.subscribe_service.options import Action


class Status(str, Enum):
    OK: str = "success"
    BAD: str = "error"


@dataclass
class DescriptionStatus:
    status: Status
    action: Action
