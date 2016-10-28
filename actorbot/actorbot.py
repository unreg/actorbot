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


class ActorBot(object):

    """
    """

    def __init__(self, endpoint, token, name='', keep_alive=5):
        """
        """
        self._url = '%s/v1/bots/%s' % (endpoint, token)
        self._name = name
        self._session = aiohttp.ClientSession()
        self._keep_alive = keep_alive
        self._ws = None
        self._id = 0
        self._sent = {}
        self._queue = []

    async def _connection(self):
        """
        Connect and return aiohttp.ClientWebSocketResponse
        """
        if (self._ws is None) or (self._ws.closed):
            logger.debug('[%s] connect to %s', self._name, self._url)
            self._ws = await self._session.ws_connect(self._url)

    def _get_id(self):
        """
        Increment and return outgoing message ID
        """
        self._id += 1
        return self._id

    async def message_handler(self, message):
        """
        Handler for incomming messages
        """
        logger.debug('[%s] message receive: %r',
                     self._name, message.to_str())

    async def _response_handler(self, message):
        """
        Handler for incomming responses
        """
        logger.debug('[%s] response receive: %r',
                     self._name, message.to_str())
        handler = self._sent.pop(message.id, None)
        if handler is not None:
            await handler(message)
        logger.debug('%d non confirmed messages', len(self._sent))

    def _error_handler(self, message):
        """
        Handler for error
        """
        logger.debug('[%s] error: %r', self._name, message.data)

    def send(self, message, callback=None):
        """
        """
        text = message.to_str().replace('"type"', '"$type"')
        self._queue.append(text)
        self._sent[message.id] = callback
        logger.debug('send: %s', text)

    async def _route(self, message):
        """
        Route incomming message by type
        """
        if message.tp == aiohttp.MsgType.text:
            incomming = BaseMessage(
                json.loads(message.data.replace('$type', 'type')))
            if incomming.type == 'FatSeqUpdate':
                await self.message_handler(incomming)
            if incomming.type == 'Response':
                await self._response_handler(incomming)
        elif message.tp == aiohttp.MsgType.error:
            self._error_handler(message)
        else:
            logger.debug('[%s] unknown message type: %r', self._name, message)

    async def _sending_queue(self):
        """
        Return a queue text messages to sending
        """
        return self._queue

    async def receive(self):
        """
        Coroutine receive incoming messages and send outgoing
        """
        await self._connection()

        self._listener_task = asyncio.ensure_future(self._ws.receive())
        self._sender_task = asyncio.ensure_future(self._sending_queue())

        done, pending = await asyncio.wait(
            [self._listener_task, self._sender_task],
            return_when=asyncio.FIRST_COMPLETED)

        if self._listener_task in done:
            message = self._listener_task.result()
            await self._route(message)
        else:
            self._listener_task.cancel()

        if self._sender_task in done:
            messages = self._sender_task.result()
            while len(messages) > 0:
                message = messages.pop()
                self._ws.send_str(message)
        else:
            self._sender_task.cancel()

    async def stop(self):
        """
        Close websocket connection and session
        """
        self._listener_task.cancel()
        self._sender_task.cancel()
        await self._ws.close()
        self._session.close()
