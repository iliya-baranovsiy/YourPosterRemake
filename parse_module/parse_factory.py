from aiNewsParse import AiNewsParsing
from cryptoNewsParse import CryptoNewsParsing
from gamesNewsParse import GamesParsing
from itNewsParse import ItNewsParsing
from scienseNewsParse import ScienceParsing
from showBisNewsParse import ShowBisNewsParsing
from sportNewsParse import SportNewsParsing
from worldNewsPars import WorldNewsParsing


class ParseFactory:
    def create_parse_obb(self, news_type):
        match news_type:
            case "ai_news":
                return AiNewsParsing()
            case "crypto_news":
                return CryptoNewsParsing()
            case "games_news":
                return GamesParsing()
            case "it_news":
                return ItNewsParsing()
            case "science_news":
                return ScienceParsing()
            case "show_bis_news":
                return ShowBisNewsParsing()
            case "sports_news":
                return SportNewsParsing()
            case "world_news":
                return WorldNewsParsing()


parse_factory = ParseFactory()
