import aiohttp
import asyncio
import async_timeout
import json
import uuid

from actorbot.api import messaging
from actorbot.bots import Conversation
from actorbot.utils import logger


class ApiAi(object):
    """ """
    URL = 'https://api.api.ai/v1/query'

    def __init__(self, token):
        self._token = token
        self._sessionID = uuid.uuid4()

    async def _get_request(self, user_says):
        """
        """
        headers = {
            'Authorization': 'Bearer %s' % self._token,
            'Content-Type': 'application/json; charset=utf-8'
        }
        data = {
            'query': user_says,
            'sessionId': str(self._sessionID),
            'lang': 'en'
        }
        with async_timeout.timeout(15):
            async with aiohttp.ClientSession() as session:
                async with session.post(self.URL,
                    headers=headers, data=json.dumps(data)) as resp:
                    if resp.status == 200:
                        return await resp.json()

    async def answer(self, user_says):
        """
        """
        answer = await self._get_request(user_says)
        return answer['result']['speech']


class ApiAiConversation(Conversation):
    """
        Simple integration with api.ai
    """
    def _initialization(self, kwargs):
        """
        """
        self._apiai = ApiAi(token=kwargs.get('token', None))

    async def message_handler(self, message):
        """ """
        await self.sendText(await self._apiai.answer(message.text))

    async def response_handler(self, message):
        """ """
        await super().response_handler(message)
