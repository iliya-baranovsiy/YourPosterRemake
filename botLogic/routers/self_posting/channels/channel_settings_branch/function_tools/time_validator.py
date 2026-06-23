from datetime import datetime


def time_validator(text_time: str):
    try:
        datetime.strptime(text_time, '%H:%M')
        return True
    except:
        return False
