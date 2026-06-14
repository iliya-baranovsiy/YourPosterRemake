from enum import Enum
from dataclasses import dataclass


class Action(Enum):
    BUY = "buy"
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    RENEW = "renew"


@dataclass
class ActionData:
    text: str
    action: Action
