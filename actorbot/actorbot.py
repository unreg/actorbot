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

import aiohttp
import asyncio
import json

from actorbot.api import BaseMessage
from actorbot.utils import logger, Event


class WsTransport(Event):
    """
        Actor bot Websocket transport
    """
    def __init__(self, endpoint, token, name, incomming, outgoing,
                 loop=None, sleep_time=0.1):
        """
        """
        super().__init__(interval=sleep_time)

        self._name = name

        self._incomming = incomming
        self._outgoing = outgoing

        self._url = self._bot_url(endpoint, token)

        if loop:
            self._loop = loop
        else:
            self._loop = asyncio.get_event_loop()

        self._ws = None

    @property
    def name(self):
        """
            Return bot name
        """
        return self._name

    def _bot_url(self, endpoint, token):
        """
        """
        return '%s/v1/bots/%s' % (endpoint, token)

    async def _connection(self):
        """
            Make wesocket connection
        """
        if self._ws is None:
            self._session = aiohttp.ClientSession(loop=self._loop)
            try:
                self._ws = await self._session.ws_connect(self._url)
                logger.debug('[%s] [transport] connect: %s', self.name, self._url)
            except Exception as e:
                logger.error('[%s] [transport] connect error: %s %s %s',
                             self.name, self._url, type(e), e)
        if self._ws.closed:
            try:
                self._ws = await self._session.ws_connect(self._url)
                logger.debug('[%s] [transport] reconnect: %s', self.name, self._url)
            except Exception as e:
                logger.error('[%s] [transport] reconnect error: %s %s',
                             self.name, self._url, type(e), e)

    async def process(self):
        """
            Processing websocket messages
        """
        logger.debug('[%s] [transport] wait', self.name)
        try:
            await self._connection()

            self.listener_task = asyncio.ensure_future(self._ws.receive())
            self.sender_task = asyncio.ensure_future(self._outgoing.get())

            done, pending = await asyncio.wait(
                [self.listener_task, self.sender_task],
                return_when=asyncio.FIRST_COMPLETED)

            if self.listener_task in done:
                logger.debug('[%s] [transport] receiving', self.name)
                await self._incomming.put(self.listener_task.result())
            else:
                self.listener_task.cancel()

            if self.sender_task in done:
                message = self.sender_task.result()
                if str(message) == 'close':
                    return
                self._ws.send_str(message)
                logger.debug('[%s] [transport] sending', self.name)
            else:
                self.sender_task.cancel()
        except Exception as e:
            logger.error('[%s] [transport] error: %s %s', self.name, type(e), e)

    async def run(self):
        """
            After run stopping coroutines and closed soclet and session
        """
        await super().run()

        self.listener_task.cancel()
        self.sender_task.cancel()

        if self._ws:
            await self._ws.close()
            logger.debug('[%s] [transport] websocket closed', self.name)
        if self._session:
            await self._session.close()
            logger.debug('[%s] [transport] aiohttp session closed', self.name)

    def stop(self):
        """
            Stop porcessing
        """
        super().stop()
        self._outgoing.put_nowait('close')


class Bot(Event):
    """
        Actor bot
    """
    def __init__(self, endpoint, token, name, conversation,
                 loop=None, sleep_time=0.1, params={}):
        """ """
        super().__init__(interval=sleep_time)

        self._name = name
        self._conversation = conversation

        if loop:
            self._loop = loop
        else:
            self._loop = asyncio.get_event_loop()

        self._incomming = asyncio.Queue(loop=loop)
        self._outgoing = asyncio.Queue(loop=loop)

        self._conversations = {}
        self._params = params

        self._transport = WsTransport(endpoint=endpoint, token=token,
                                      name=name,
                                      incomming=self._incomming,
                                      outgoing=self._outgoing,
                                      loop=self._loop)

    @property
    def name(self):
        """
            Retutn bot name
        """
        return self._name

    @property
    def transport(self):
        """
            Return websocket transport
        """
        return self._transport

    async def process(self):
        """
            Processing incomming messages
        """
        try:
            logger.debug('[%s] [processor] processor wait', self.name)
            message = await self._incomming.get()
            if str(message) == 'close':
                return
            if message.tp == aiohttp.MsgType.text:
                logger.debug('[%s] [processor] incomming message: %r',
                             self.name, message.data)
                incomming = BaseMessage(
                    json.loads(message.data.replace('$type', 'type')))
                if incomming.type == 'Response':
                    asyncio.ensure_future(
                        self._conversations[int(incomming.id[:-5])].response_handler(incomming))
                if incomming.type == 'FatSeqUpdate':
                    peer = incomming.body.peer
                    if peer.id not in self._conversations:
                        self._conversations[peer.id] = self._conversation(
                            self, peer, self._outgoing, **self._params)
                    asyncio.ensure_future(
                        self._conversations[peer.id].message_handler(
                            incomming.body.message))
            if message.tp in (aiohttp.MsgType.close, aiohttp.MsgType.error):
                logger.error('[%s] [processor] websocket error: data: %r, extra: %r',
                             self.name, message.data, message.extra)
        except Exception as e:
            logger.error('[%s] [processor] error: %s %s',
                         self.name, type(e), e)

    def stop(self):
        """
            Stop processing
        """
        super().stop()
        self._incomming.put_nowait('close')
