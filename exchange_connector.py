import os

import ccxt.async_support
import logging


def get_exchange():
    exchange_name = os.getenv("EXCHANGE", "binance")
    exchange = getattr(ccxt.async_support, exchange_name)()
    exchange.logger.setLevel(logging.INFO)
    return exchange


async def get_tickers(exchange: ccxt.async_support.Exchange) -> list:
    if isinstance(exchange, ccxt.async_support.binance):
        response = await exchange.fapiPublicGetTickerPrice()
        if not exchange.markets_by_id or any(
            ticker["symbol"] not in exchange.markets_by_id
            for ticker in response
        ):
            await reload_markets(exchange)
        return [
            {
                "symbol": exchange.safe_symbol(ticker["symbol"], marketType="spot"),
                "close": ticker.get("price", 0),
                "timestamp": ticker.get("time", 0),
            }
            for ticker in response
        ]
    return [
        ticker
        for ticker in (await exchange.fetch_tickers()).values()
    ]


async def get_ohlcv(exchange: ccxt.async_support.Exchange, symbol: str, timeframe: str) -> list:
    return await exchange.fetch_ohlcv(symbol, timeframe=timeframe)


async def reload_markets(exchange: ccxt.async_support.Exchange):
    logging.getLogger(f"{exchange.id}").info("reloading market")
    return await exchange.load_markets(reload=True)
