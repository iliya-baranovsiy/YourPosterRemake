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


class Resource(str, Enum):
    DATABASE = "Данные сервиса"
    FILE = "Данные с файла"
    AI_POSTS = "Данные с ИИ"
