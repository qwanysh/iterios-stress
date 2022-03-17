import asyncio
from time import time

from httpx import RequestError
from loguru import logger

from src.client import IteriosApiClient
from src.exceptions import FailedResponseError
from src.helpers import (
    get_random_country, get_random_dep_city, get_search_start_payload, get_timing_results,
    setup_logger,
)
from src.settings import settings


async def start_search(index: int):
    logger.info(f'Start search #{index}')
    start_time = time()

    try:
        async with IteriosApiClient() as client:
            country = get_random_country()
            dep_city = get_random_dep_city()
            main_reference = await client.get_main_reference(
                country_iso=country['iso_code'], dep_city_id=dep_city['id'],
            )
            payload = get_search_start_payload(
                country_id=country['id'], dep_city_id=dep_city['id'], main_reference=main_reference,
            )
            await client.start_search(payload)
    except (FailedResponseError, RequestError) as error:
        logger.error(f'Fail search #{index} ({repr(error)})')
        return index, None

    elapsed_time = round(time() - start_time, 2)
    logger.info(f'Finish search #{index} in {elapsed_time}s')
    return index, elapsed_time


async def main():
    logger.info(f'Test with {settings.request_count} requests')
    requests = [
        start_search(index)
        for index in range(1, settings.request_count + 1)
    ]
    timings = await asyncio.gather(*requests)

    last_time = None

    for timing in timings:
        index, elapsed_time = timing

        if not elapsed_time:
            logger.info(f'#{index} - fail')
            continue

        if last_time:
            difference = round(elapsed_time - last_time, 2)
            logger.info(f'#{index} - {elapsed_time}s ({difference:+}s)')
        else:
            logger.info(f'#{index} - {elapsed_time}s')

        last_time = elapsed_time

    elapsed_times = [timing[1] for timing in timings]
    results = get_timing_results(elapsed_times)
    logger.info(f"Results: min({results['min']}s), max({results['max']}s), average({results['average']}s), fails({results['failed']}/{results['total']})")  # noqa: E501


if __name__ == '__main__':
    setup_logger()
    asyncio.run(main())
