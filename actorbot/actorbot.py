import asyncio
import aiohttp
import json

from actorbot.api import BaseMessage
from actorbot.utils import logger


class Bot(object):
    """docstring for ClassName"""
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
        """
        return self._name

    async def _checkConnection(self):
        """
        """
        if (self._socket is None) or (self._socket.closed):
            self._socket = await self._session.ws_connect(
                '%s/v1/bots/%s' % (self._endpoint, self._token))
            logger.debug('[%s] connect to %s', self._name,
                         '%s/v1/bots/%s' % (self._endpoint, self._token))

    async def _sendingQueue(self):
        """
        """
        return self._queue

    def toSend(self, message):
        """
        """
        text = message.to_str().replace('"type"', '"$type"')
        logger.debug('[%s] send %s', self._name, text)
        self._queue.append(text)

    async def transport(self):
        """
        """
        await self._checkConnection()

        listener_task = asyncio.ensure_future(self._socket.receive())
        sender_task = asyncio.ensure_future(self._sendingQueue())

        done, pending = await asyncio.wait([listener_task, sender_task],
                                           return_when=asyncio.FIRST_COMPLETED)

        if listener_task in done:
            message = listener_task.result()
            self._router(message)
        else:
            listener_task.cancel()

        if sender_task in done:
            queue = sender_task.result()
            while len(queue) > 0:
                message = queue.pop()
                self._socket.send_str(message)
        else:
            sender_task.cancel()

    def _router(self, message):
        """
        """
        if message.tp == aiohttp.MsgType.text:
            logger.debug('[%s] message: %r', self._name, message.data)
            incomming = BaseMessage(
                json.loads(message.data.replace('$type', 'type')))
            if incomming.type == 'Response':
                self._conversations[int(incomming.id[:-5])].response_handler(incomming)
            if incomming.type == 'FatSeqUpdate':
                peer = incomming.body.peer
                if peer.id not in self._conversations:
                    self._conversations[peer.id] = self._conversation(self, peer)
                self._conversations[peer.id].message_handler(incomming.body.message)

        elif message.tp == aiohttp.MsgType.error:
            logger.debug('[%s] error: %r', self._name, message.data)
        else:
            logger.debug('[%s] unknown message: %r', self._name, message)

    async def stop(self):
        """
        """
        await self._socket.close()
        self._session.close()
