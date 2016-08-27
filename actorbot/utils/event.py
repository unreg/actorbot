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

from actorbot.utils import logger


class Event(object):

    """
    """

    def __init__(self, interval=1.0):
        """
        """
        try:
            self.interval = float(interval)
        except Exception as e:
            logging.exception('Error while setting interval: %s', e)
        self._running = True
        self._count = 0

    @property
    def count(self):
        """
        """
        return self._count

    async def process(self):
        """
        """
        pass

    async def run(self):
        """
        """
        while self._running:
            self._count += 1
            await self.process()
            await self._sleep()

    async def _sleep(self):
        """
        """
        await asyncio.sleep(self.interval)

    def stop(self):
        """
        """
        self._running = False
