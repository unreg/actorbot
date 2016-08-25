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

from actorbot.utils import logger_init, logger
from actorbot.utils import OutgoingMessage

from actorbot import ActorBot, BotFarm


class EchoBot(ActorBot):

    """
    """

    def handler(self, msg):
        """
        """
        logger.info('[%s] receive message from ID=%s',
                    self._name, msg.body.sender.id)

        out = OutgoingMessage(mid=self._id,
                              peer_type=msg.body.peer.type,
                              peer_accessHash=msg.body.peer.accessHash,
                              peer_id = msg.body.peer.id,
                              message_text = msg.body.message.text)
        self.send(out)
        logger.info('[%s] send message to ID=%s',
                    self._name, msg.body.sender.id)


async def exit(signame):
    """
    """
    logger.info('waiting for shutdown asyncio tasks')
    await farm.stop()


if __name__ == '__main__':
    logger_init(stream_log_level=logging.INFO)

    echobot = EchoBot(endpoint='ENDPOINT_HERE',
                      token='BOT_TOKEN_HERE',
                      name='BOT_NAME_HERE')
    farm = BotFarm([echobot])

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
