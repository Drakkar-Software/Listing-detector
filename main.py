import asyncio
import logging
import os

import ccxt.async_support

import exchange_connector
import coins_db
import notifications


async def find_new_coins(db: coins_db.CoinsDB, exchange) -> list:
    initialized = db.initialized()
    added_coins = db.update_coins_from_tickers(await exchange_connector.get_tickers(exchange))
    if initialized:
        return added_coins
    return []


async def coins_finder_loop(exchange: ccxt.async_support.Exchange):
    logger = logging.getLogger(f"{exchange.id}-loop")
    logger.debug("Starting")
    db = coins_db.CoinsDB()
    while True:
        try:
            logger.debug("New iteration")
            if new_coins := await find_new_coins(db, exchange):
                logger.info(f"New coins: {new_coins}")
                await asyncio.gather(*[
                    notifications.send_discord_notification(
                        "Listing detector",
                        f"New {exchange.id} listing",
                        f"@here {coin} is now trading live: {db.get_price_pairs(coin)}"
                    )
                    for coin in new_coins
                ])
            await asyncio.sleep(float(os.getenv("SLEEP_TIME")))
        except BaseException as err:
            logger.exception(err)


async def run_finder():
    exchange = exchange_connector.get_exchange()
    await coins_finder_loop(exchange)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s')
    asyncio.run(run_finder())
