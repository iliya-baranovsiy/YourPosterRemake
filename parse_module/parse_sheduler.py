from datetime import datetime
import time
from parse_factory import parse_factory
from database.parse_db.parse_orm import clean_old_data

schedule_dict_map = [
    {'time': '8', 'task': ("world_news",), 'role': 'parse'},
    {'time': '10', 'task': ("sports_news",), 'role': 'parse'},
    {'time': '12', 'task': ("show_bis_news",), 'role': 'parse'},
    {'time': '14', 'task': ("it_news",), 'role': 'parse'},
    {'time': '16', 'task': ("world_news",), 'role': 'parse'},
    {'time': '18', 'task': ("sports_news",), 'role': 'parse'},
    {'time': '20', 'task': ("ai_news",), 'role': 'parse'},
    {'time': '22', 'task': ("games_news",), 'role': 'parse'},
    {'time': '0', 'task': ("science_news",), 'role': 'parse'},
    {'time': '2', 'task': ("crypto_news",), 'role': 'parse'},
    {'time': '3', 'task': (clean_old_data,), 'role': 'clear'},
    {'time': '4', 'task': ("it_news",), 'role': 'parse'},
]


def run_parse_scheduler():
    while True:
        current_hour = str(datetime.now().hour)
        for row in schedule_dict_map:
            if row['time'] == current_hour and row['role'] == "parse":
                for task in row['task']:
                    target_parse = parse_factory.create_parse_obb(task)
                    target_parse.parse()
            elif row['time'] == current_hour and row['role'] == "clear":
                for task in row['task']:
                    task()
        time.sleep(3600)


run_parse_scheduler()
