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

from actorbot import Bot
from actorbot.bots import EchoConversation
from actorbot.utils import logger_init, logger


def exit(signame):
    """
    """
    logger.info('waiting for shutdown asyncio tasks')
    loop.remove_signal_handler(signal.SIGTERM)
    loop.remove_signal_handler(signal.SIGINT)
    for bot in bots:
        bot.transport.stop()
        bot.stop()


if __name__ == '__main__':
    logger_init(stream_log_level=logging.DEBUG)

    loop = asyncio.get_event_loop()

    echobot = Bot(endpoint='wss://ws-api-actor.tmnhy.su',
                  token='5bf5860cd6b76749f508185f64369fabd02c647f',
                  name='apiai',
                  conversation=EchoConversation)

    bots = [echobot]
    transports = [asyncio.ensure_future(bot.transport.run()) for bot in bots]
    processors = [asyncio.ensure_future(bot.run()) for bot in bots]

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(
            getattr(signal, signame), functools.partial(exit, signame))
    logger.info('Bot farm running forever, press Ctrl+C to interrupt.')

    try:
        loop.run_until_complete(asyncio.wait(transports + processors))
    finally:
        loop.close()
