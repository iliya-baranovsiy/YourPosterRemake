import asyncio

from .celery_app import app
from parse_module.aiNewsParse import AiNewsParsing
from parse_module.cryptoNewsParse import CryptoNewsParsing
from parse_module.gamesNewsParse import GamesParsing
from parse_module.itNewsParse import ItNewsParsing
from parse_module.scienseNewsParse import ScienceParsing
from parse_module.showBisNewsParse import ShowBisNewsParsing
from parse_module.sportNewsParse import SportNewsParsing
from parse_module.worldNewsPars import WorldNewsParsing
from database.parse_db.parse_orm import clean_old_data
from database.backgroundt_tasks_db.orm import BackGroundTasksORM


@app.task(name="tasks.parse_ai_news", queue="parsing")
def parse_ai_news():
    AiNewsParsing().parse()


@app.task(name="tasks.parse_crypto_news", queue="parsing")
def parse_crypto_news():
    CryptoNewsParsing().parse()


@app.task(name="tasks.parse_games_news", queue="parsing")
def parse_games_news():
    GamesParsing().parse()


@app.task(name="tasks.parse_it_news", queue="parsing")
def parse_it_news():
    ItNewsParsing().parse()


@app.task(name="tasks.parse_science_news", queue="parsing")
def parse_science_news():
    ScienceParsing().parse()


@app.task(name="tasks.parse_show_bis_news", queue="parsing")
def parse_show_bis_news():
    ShowBisNewsParsing().parse()


@app.task(name="tasks.parse_sports_news", queue="parsing")
def parse_sports_news():
    SportNewsParsing().parse()


@app.task(name="tasks.parse_world_news", queue="parsing")
def parse_world_news():
    WorldNewsParsing().parse()


@app.task(name="tasks.clean_old_parse_data", queue="parsing")
def clean_old_parse_data_task():
    clean_old_data()


@app.task(name="tasks.clean_old_posted_data", queue="parsing")
def clean_old_posts_data_task():
    asyncio.run(BackGroundTasksORM().clear_old_posts_data())
