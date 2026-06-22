from enum import Enum


class PostTheme(str, Enum):
    AI_NEWS = "Новости ИИ"
    CRYPTO_NEWS = "Новости криптовалюты"
    GAMES_NEWS = "Новости игр"
    IT_NEWS = "Новости IT"
    SCIENCE_NEWS = "Новости науки"
    SHOW_BIS_NEWS = "Новости шоу бизнеса"
    SPORT_NEWS = "Новости спорта"
    WORLD_NEWS = "Новости мира"
    OWN_FILE = "Свой файл"
    AI_POSTS = "ИИ посты"
    UNDEFINED = "Не определена"

    @property
    def kb_value(self):
        mapping = {
            PostTheme.AI_POSTS: "ainews",
            PostTheme.CRYPTO_NEWS: "cryptonews",
            PostTheme.GAMES_NEWS: "gamesnews",
            PostTheme.IT_NEWS: "itnews",
            PostTheme.SCIENCE_NEWS: "sciencenews",
            PostTheme.SHOW_BIS_NEWS: "showbiznews",
            PostTheme.SPORT_NEWS: "sportsnews",
            PostTheme.WORLD_NEWS: "worldnews"
        }
        return mapping[self]

    @classmethod
    def enum_value(cls, kb_value: str):
        mapping = {
            "ainews": cls.AI_NEWS,
            "cryptonews": cls.CRYPTO_NEWS,
            "gamesnews": cls.GAMES_NEWS,
            "itnews": cls.IT_NEWS,
            "sciencenews": cls.SCIENCE_NEWS,
            "showbiznews": cls.SHOW_BIS_NEWS,
            "sportsnews": cls.SPORT_NEWS,
            "worldnews": cls.WORLD_NEWS,
        }
        return mapping[kb_value]


class Resource(str, Enum):
    DATABASE = "Данные сервиса"
    FILE = "Данные с файла"
    AI_POSTS = "Данные с ИИ"
