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
    sleep_time = float(os.getenv("SLEEP_TIME", 30))
    start_message = f"Starting, sleep_time={sleep_time}s, discord url={notifications.get_discord_url()[:40]}..."
    logger.debug(start_message)
    await notifications.send_discord_notification(
        "Listing detector",
        f"Starting on {exchange.id}",
        start_message
    )
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
        except BaseException as err:
            await notifications.send_discord_notification(
                "Listing detector",
                f"ERROR on {exchange.id}",
                f"{err} ({err.__class__.__name__}), check logs"
            )
            logger.exception(err)
            await asyncio.sleep(sleep_time * 10)
        finally:
            await asyncio.sleep(sleep_time)


async def run_finder():
    exchange = exchange_connector.get_exchange()
    await coins_finder_loop(exchange)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s')
    asyncio.run(run_finder())
