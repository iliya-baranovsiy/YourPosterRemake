from parse_module.itNewsParse import ItNewsParsing
from database.parse_db.models import AiNewsTable


class AiNewsParsing(ItNewsParsing):
    def __init__(self):
        self.url = "https://habr.com/ru/flows/ai_and_ml/news/"
        super().__init__(AiNewsTable, self.url)
