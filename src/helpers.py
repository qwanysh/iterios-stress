from datetime import date, timedelta
import json
from random import choice
import sys

from loguru import logger

with open('assets/search_options.json', 'r') as file:
    search_options = json.load(file)


def get_random_country() -> dict:
    return choice(search_options['countries'])


def get_random_dep_city() -> dict:
    return choice(search_options['dep_cities'])


def get_date_range(middle_date: date) -> tuple[date, date]:
    return middle_date - timedelta(days=2), middle_date + timedelta(days=2)


def get_random_dates() -> tuple[date, date]:
    today = date.today()
    dates = [
        today + timedelta(days=7),
        today + timedelta(days=14),
        today + timedelta(days=21),
    ]
    random_date = choice(dates)
    return get_date_range(random_date)


def get_random_nights():
    return choice(search_options['nights'])


def get_currency() -> dict:
    return search_options['currency']


def get_adapter_ids(main_reference: dict) -> list[int]:
    return [adapter['id'] for adapter in main_reference['operators']]


def get_search_start_payload(country_id: int, dep_city_id: int, main_reference: dict) -> dict:
    date_from, date_till = get_random_dates()
    night_from, night_till = get_random_nights()
    adapter_ids = get_adapter_ids(main_reference)
    currency = get_currency()
    return {
        'country': country_id,
        'dep_city': dep_city_id,
        'date_from': date_from.isoformat(),
        'date_till': date_till.isoformat(),
        'night_from': night_from,
        'night_till': night_till,
        'adapter': adapter_ids,
        'currency': currency['id'],
    }


def setup_logger():
    logger.remove()
    logger.add(sys.stdout, format='{time:YYYY.MM.DD HH:mm:ss} {level:8} {message}')


def get_timing_results(timings: list) -> dict:
    clean_timings = list(filter(bool, timings))
    average_time = 0
    max_time = 0
    min_time = 0

    if clean_timings:
        average_time = sum(clean_timings) / len(clean_timings)
        max_time = max(clean_timings)
        min_time = min(clean_timings)

    return {
        'average': round(average_time, 2),
        'max': max_time,
        'min': min_time,
        'total': len(timings),
        'failed': len(timings) - len(clean_timings),
    }
