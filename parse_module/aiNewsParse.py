from database.parse_db.models import AiNewsTable
from .itNewsParse import ItNewsParsing


class AiNewsParsing(ItNewsParsing):
    def __init__(self):
        self.url = "https://habr.com/ru/flows/ai_and_ml/news/"
        super().__init__(AiNewsTable, self.url)
