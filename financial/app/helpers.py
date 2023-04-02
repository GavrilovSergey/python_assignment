from datetime import datetime, timedelta
from functools import lru_cache
from dateutil.parser import parse
from . import config, schemas

# Cache
@lru_cache()
def get_settings():
    return config.Settings()

tomorrow = datetime.utcnow() + timedelta(days=1)
distant_past = datetime(1900, 1, 1)

def validateDates(start_date: str, end_date: str):
    '''checks start_date and end_date, returns processed dates and error message'''
    if start_date:
        try:
            start_date = parse(start_date)
        except ValueError:
            return None, None, {"error": "Invalid start date parameter."}
    else:
        start_date = distant_past

    if end_date:
        try:
            end_date = parse(end_date)
        except ValueError:
            return None, None, {"error": "Invalid end date parameter."}
    else:
        end_date = tomorrow

    if start_date > tomorrow:
        return None, None, {"error": "Invalid start date parameter."}
    if start_date > end_date:
        return None, None, {"error": "Invalid start date or end date parameter."}

    return start_date, end_date, {"error": ""}