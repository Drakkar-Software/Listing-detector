import aiohttp
import os
import logging


def get_discord_url():
    return os.getenv("DISCORD_WEBHOOK_URL", "")


async def send_discord_notification(subject, title, content):
    if url := get_discord_url():
        logger = logging.getLogger("notifications")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json={
                        "content": subject,
                        "username": "New listings detector",
                        "embeds": [
                            {
                                "description": content,
                                "title": title
                            }
                        ]
                    }
                ) as resp:
                    resp.raise_for_status()
                    logger.debug(f"Notification successfully sent: {content}")
        except aiohttp.ClientError as err:
            logger.error(f"Failed to send discord notification: {err}")
            logger.exception(err)

