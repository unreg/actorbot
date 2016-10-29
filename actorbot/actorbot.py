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
import aiohttp
import json

from actorbot.api import BaseMessage
from actorbot.utils import logger


class Bot(object):
    """
    Base bot object
    """
    def __init__(self, endpoint, token, name, conversation):
        super(Bot, self).__init__()
        self._endpoint = endpoint
        self._token = token
        self._name = name
        self._conversation = conversation

        self._session = aiohttp.ClientSession()
        self._socket = None

        self._queue = []
        self._conversations = {}

    @property
    def name(self):
        """
        Return defined bot name
        """
        return self._name

    async def _checkConnection(self):
        """
        Check websocket conenction and reconnect if error
        """
        if (self._socket is None) or (self._socket.closed):
            self._socket = await self._session.ws_connect(
                '%s/v1/bots/%s' % (self._endpoint, self._token))
            logger.debug('[%s] connect to %s', self._name,
                         '%s/v1/bots/%s' % (self._endpoint, self._token))

    async def _sendingQueue(self):
        """
        Return list of messages ready for sending 
        """
        return self._queue

    def toSend(self, message):
        """
        Append message in queue to sending
        """
        text = message.to_str().replace('"type"', '"$type"')
        logger.debug('[%s] send %s', self._name, text)
        self._queue.append(text)

    async def transport(self):
        """
        Checks task to send or receive. And executing what is there
        """
        await self._checkConnection()

        listener_task = asyncio.ensure_future(self._socket.receive())
        sender_task = asyncio.ensure_future(self._sendingQueue())

        done, pending = await asyncio.wait([listener_task, sender_task],
                                           return_when=asyncio.FIRST_COMPLETED)

        if listener_task in done:
            message = listener_task.result()
            await self._router(message)
        else:
            listener_task.cancel()

        if sender_task in done:
            queue = sender_task.result()
            while len(queue) > 0:
                message = queue.pop()
                self._socket.send_str(message)
        else:
            sender_task.cancel()

    async def _router(self, message):
        """
        Route incomming peer messages and server responses
        """
        if message.tp == aiohttp.MsgType.text:
            logger.debug('[%s] message: %r', self._name, message.data)
            incomming = BaseMessage(
                json.loads(message.data.replace('$type', 'type')))
            if incomming.type == 'Response':
                await self._conversations[int(incomming.id[:-5])].response_handler(incomming)
            if incomming.type == 'FatSeqUpdate':
                peer = incomming.body.peer
                if peer.id not in self._conversations:
                    self._conversations[peer.id] = self._conversation(self, peer)
                await self._conversations[peer.id].message_handler(incomming.body.message)

        elif message.tp == aiohttp.MsgType.error:
            logger.debug('[%s] error: %r', self._name, message.data)
        else:
            logger.debug('[%s] unknown message: %r', self._name, message)

    async def stop(self):
        """
        Close weboscket and session
        """
        await self._socket.close()
        self._session.close()
