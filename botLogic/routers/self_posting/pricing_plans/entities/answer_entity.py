from dataclasses import dataclass
from aiogram.types import InlineKeyboardMarkup


@dataclass
class Answer:
    text: str
    buttons: InlineKeyboardMarkup
