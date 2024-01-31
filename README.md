# Listing-detector

Used to notify new listings on an exchange. 

Notification example:
```
New binance listing
@here BTC is now trading live: {'BTC/USDT': '42458.60', 'BTC/USDC': '42426.1'}
```

## Configuration

Can be configured by env variables:
```
EXCHANGE=binance
SLEEP_TIME=30
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234232
```
Where:
- `EXCHANGE` is the ccxt id of your exchange
- `SLEEP_TIME` is the amount of seconds to sleep between each check
- `DISCORD_WEBHOOK_URL` is the url of the discord webhook to send notifications to
