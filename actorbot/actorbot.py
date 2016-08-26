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
import datetime
import random
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from actorbot.utils import logger, BaseMessage


def random_id(id):
    """
    """
    return ''.join([
        datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        '%03d' % int(id),
        '%02d' % random.randint(0, 100)])


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
        self._env = Environment()
        self._env.loader = FileSystemLoader('./actorbot/templates')

    def handler(self, message):
        """
        """
        pass

    def _get_id(self):
        """
        """
        self._id += 1
        return self._id

    async def _connect(self):
        """
        """
        logger.debug('[%s] connect to %s', self._name, self._url)
        return await self._session.ws_connect(self._url)

    def sendMessage(self, id, peer_type, peer_id, accessHash, text):
        """
        """
        data = {
            'type': 'Request',
            'id': id,
            'service': 'messaging',
            'body_type': 'SendMessage',
            'peer_type': peer_type,
            'peer_id': peer_id,
            'accessHash': accessHash,
            'randomId': random_id(id),
            'message_type': 'Text',
            'message_text': text
        }
        template = self._env.get_template('sendmessage')
        text = template.render(data)
        res = ''.join([s.strip() for s in text.split()])
        self._ws.send_str(res)

    async def receive(self):
        """
        """
        if (self._ws is None) or (self._ws.closed):
            self._ws = await self._connect()

        try:
            res = await asyncio.wait_for(self._ws.receive(),
                                            timeout=self._keep_alive)
            if res.tp == aiohttp.MsgType.error:
                logger.error('[%s] receive: %s', self._name, res.tp.data)
            elif res.tp == aiohttp.MsgType.closed:
                logger.debug('[%s] websocket connection closed', self._name)
            else:
                logger.debug('[%s] receive: %s', self._name, res.data)
                message = BaseMessage(
                    json.loads(res.data.replace('$type', 'type')))
                if message.type == 'FatSeqUpdate':
                    self.handler(message)
        except Exception as e:
            logger.debug('[%s] idle', self._name)

    async def stop(self):
        """
        """
        await self._ws.close()
        self._session.close()
