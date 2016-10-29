#Copyright (c) 2016 Vladimir Vorobev.
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import asyncio

import functools
import os
import signal
import logging

from actorbot import BotFarm
from actorbot import Bot
from actorbot.bots import EchoConversation

from actorbot.utils import logger_init, logger


async def exit(signame):
    """
    """
    logger.info('waiting for shutdown asyncio tasks')
    await farm.stop()


if __name__ == '__main__':
    logger_init(stream_log_level=logging.DEBUG)

    newbot = Bot(endpoint='',
                 token='',
                 name='',
                 conversation=EchoConversation)
    farm = BotFarm([newbot])

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
