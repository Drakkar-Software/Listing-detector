import dataclasses


class CoinsDB:
    def __init__(self):
        self.latest_tickers = []

        self._known_coins = {}

    def initialized(self):
        return bool(self._known_coins)

    def update_coins_from_tickers(self, tickers: list) -> list:
        updated_coins = _get_coins_from_tickers(tickers)
        added_coins = [
            coin
            for coin in updated_coins
            if coin not in self._known_coins
        ]
        self._known_coins = updated_coins
        self.latest_tickers = tickers
        return added_coins

    def get_price_pairs(self, coin: str):
        return self._known_coins[coin].trading_pairs

    def count(self):
        return len(self._known_coins)

    def coins(self):
        return list(self._known_coins)


def _get_coins_from_tickers(tickers: list):
    coins = {}
    for ticker in tickers:
        symbol = ticker["symbol"]
        if ":" in symbol:
            continue
        price = ticker["close"]
        base, quote = symbol.split("/") if "/" in symbol else (symbol, symbol)
        if base not in coins:
            coins[base] = Coin({symbol: price})
        else:
            coins[base].trading_pairs[symbol] = price
    return coins


@dataclasses.dataclass
class Coin:
    trading_pairs: dict[str, float]
