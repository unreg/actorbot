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

from actorbot.utils import logger, Event


class BotFarm(Event):

    """
    """

    def __init__(self, bots=[], sleep_time=0.1):
        """
        """
        super().__init__(interval=sleep_time)
        self.bots = bots
        logger.info('add %d bot(s) to farm', len(bots))

    async def process(self):
        """
        """
        tasks = []
        for bot in self.bots:
            tasks.append(asyncio.ensure_future(bot.transport()))
        done, pending = await asyncio.wait(tasks)

    async def stop(self):
        """
        """
        super().stop()
        tasks = []
        for bot in self.bots:
            tasks.append(asyncio.ensure_future(bot.stop()))
        done, pending = await asyncio.wait(tasks)
