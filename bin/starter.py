import asyncio

import functools
import os
import signal
import logging

from actorbot import BotFarm
from actorbot import Bot
from actorbot.bots import StickerConversation

from actorbot.utils import logger_init, logger


async def exit(signame):
    """
    """
    logger.info('waiting for shutdown asyncio tasks')
    await farm.stop()


if __name__ == '__main__':
    logger_init(stream_log_level=logging.DEBUG)

    nbot = Bot(endpoint='ENDPOINT',
               token='TOKEN',
               name='NAME',
               conversation=StickerConversation)
    farm = BotFarm([nbot])

    loop = asyncio.get_event_loop()

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda: asyncio.async(exit(signame)))
    logger.info('Bot farm running forever, press Ctrl+C to interrupt.')

    try:
        loop.run_until_complete(asyncio.wait([farm.run()]))
    finally:
        loop.close()
