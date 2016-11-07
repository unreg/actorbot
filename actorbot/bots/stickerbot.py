import aiohttp
import asyncio
import async_timeout
import io
from zipfile import ZipFile

from actorbot.api import stickers
from actorbot.api import users
from actorbot.bots import Conversation
from actorbot.utils import logger


CHUNK_SIZE = 4096 * 16


async def download(url):
    """  Download file in memory end return bytes object """
    res = None
    with async_timeout.timeout(30):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                while True:
                    chunk = await resp.content.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    if res is None:
                        res = chunk
                    else:
                        res += chunk
    return res


class StickerConversation(Conversation):
    """
        Simple sticker loader
    """

    stage = ('idle', 0)
    packdata = None
    names = []
    packId = None
    error = False

    async def message_handler(self, message):
        """ """

        if message.type != 'Text':
            return

        stage, substage = self.stage

        if stage == 'idle':
            command = message.text.split(' ')
            if (command[0] != '/load') or (len(command) != 2):
                text = '\n'.join([
                    ('Send me "/load" command'
                    ' and link on your own stickerpack zip-file.'),
                    'For example: /load http://domain.tld/pack.zip',
                    '',
                    ('*N.B.* For make sticker pack as default'
                    'you must have administrator permission.')])
                await self.sendText(text)
                self.error = True
            else:
                stage = 'run'
                await self.loadStickerPack(url=command[1])

    async def response_handler(self, message):
        """ """

        await super().response_handler(message)

        stage, substage = self.stage

        if self.error:
            self.cancel()
            return

        if substage in [0, 1, 3]:
            self.stage = (stage, substage + 1)
            await self.loadStickerPack()

        if substage == 2:
            if message.body.value:
                self.stage = (stage, substage + 1)
                await self.loadStickerPack(packId=message.body.value)
            else:
                self.error = True
                await self.sendText('Internal error: error create pack.')

        if substage == 4:
            if message.body.date:
                self.stage = (stage, substage + 1)
            await self.loadStickerPack()

        if substage == 4:
            if message.body.date:
                self.stage = (stage, substage + 1)
                await self.loadStickerPack()

        if substage == 5:
            self.stage = (stage, substage + 1)
            await self.loadStickerPack(code=message.body.code)

        if substage == 6:
            self.error = True

    def cancel(self):
        """ Clear  """
        self.stage = ('idle', 0)
        self.names = []
        self.packdata = None
        self.packId = None

    async def loadStickerPack(self, **kwargs):
        """
        """
        stage, substage = self.stage
        self.error = False

        # Download zip-file with stickers
        if substage == 0:
            url = kwargs.get('url')
            try:
                self.packdata = await download(url)
                text = 'Download: %d bytes' % (
                    len(self.packdata))
            except Exception as e:
                logger.error('Error download: %s %s', type(e), e)
                text = 'Failed download %s' % url
                self.error = True
            await self.sendText(text)

        # unpack stickers
        elif substage == 1:
            try:
                with ZipFile(io.BytesIO(self.packdata), 'r') as zf:
                    self.names = []
                    for name in zf.namelist():
                        name = name.split('_')[0]
                        if name not in self.names:
                            self.names.append(name)
                    if len(self.names) > 0:
                        text = 'Found %d names in zip-file.' % (
                            len(self.names))
                    else:
                        text = 'Stickers not found.' % (len(self.names))
                        self.error = True
                    await self.sendText(text)
            except Exception as e:
                logger.error('Error unzip pack: %s %s', type(e), e)
                text = 'Unpack error. Try once more.'
                self.error = True
                await self.sendText(text)

        # create pack
        elif substage == 2:
            out_msg =  stickers.CreateStickerPack(self._get_id(),
                                                  creatorUserId=self._peer.id)
            await self.send(out_msg)

        # set packId
        elif substage == 3:
            self.packId = kwargs.get('packId')
            text = ' '.join([
                'Create pack: %s.' % self.packId,
                ' Uploading stickers on server. Please wait...'
            ])
            await self.sendText(text)

        # upload stickers to server
        elif substage == 4:
            try:
                with ZipFile(io.BytesIO(self.packdata), 'r') as zf:
                    if len(self.names) > 0:
                        name = self.names.pop(0)
                        image128 = zf.read(name + '_128.webp')
                        image256 = zf.read(name + '_256.webp')
                        image512 = zf.read(name + '_512.webp')

                        out_msg = stickers.AddSticker(
                            self._get_id(),
                            ownerUserId=self._peer.id,
                            packId=self.packId,
                            emoji=[''],
                            small=list(image128), smallW=128, smallH=128,
                            medium=list(image256), mediumW=256, mediumH=256,
                            large=list(image512), largeW=512, largeH=512)
                        await self.send(out_msg)
                    else:
                        await self.sendText('All stickers uploaded.')
            except Exception as e:
                logger.error('Error unzip sticker: %s %s', type(e), e)
                text = 'Upload sticker error. Try once more.'
                self.error = True
                await self.sendText(text)

        # set pack as default
        elif substage == 5:
            out_msg = stickers.MakeStickerPackDefault(self._get_id(),
                                                      userId=self._peer.id,
                                                      packId=self.packId)
            await self.send(out_msg)

        # end of operation
        elif substage == 6:
            code = kwargs.get('code')
            if code:
                text = 'Error make pack as defaut: %s. Operation end.' % code
            else:
                text = 'Pack %s made default. Operation end.' % self.packId
            await self.sendText(text)
