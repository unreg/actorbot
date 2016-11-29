from actorbot.bots import Conversation
from actorbot.api import stickers


class StickerExtConversation(Conversation):
    startText = '''
        Hi! I'm a extended sticker-bot!
        Type me /help for see available commands.
        '''

    slashCommands = (
        ('showstickerpacks', 'show all sticker packs'),
        ('showstickers', 'show all stickers from sticker pack'),
        ('deletesticker', 'delete sticker by id'),
        ('cancel', 'cancel current command'),
        ('help', 'show this message'))

    stage = ('idle', 0)


    async def message_handler(self, message):
        """ Processing incomming messages and commands """

        # Only text message processing
        if message.type != 'Text':
            return

        stage, substage = self.stage

        command = message.text
        if command == '/cancel':
            self.stage = ('cancel', 0)

        if stage == 'idle':
            if command == '/start':
                await super().start()
            elif command == '/help':
                await super().help()
            elif command == '/showstickerpacks':
                self.stage = ('showpacks', 0)
            elif command == '/showstickers':
                self.stage = ('showstickers', 0)
            elif command == '/deletesticker':
                self.stage = ('deletesticker', 0)
            await self.process_command()
        else:
            await self.process_command(params=message.text)


    async def response_handler(self, message):
        """ Processing server responses """

        await super().response_handler(message)

        stage, substage = self.stage
        if stage == 'showpacks':
            if substage == 0:
                if message.body.ids:
                    self.stage = ('idle', 0)
                    await self.sendText(str(message.body.ids))

        if stage == 'showstickers':
            if substage == 0:
                self.stage = (stage, substage + 1)
            if substage == 1:
                if message.body.ids:
                    self.stage = ('idle', 0)
                    await self.sendText(str(message.body.ids))

        if stage == 'deletesticker':
            if substage == 0:
                self.stage = (stage, substage + 1)
            if substage == 1:
                self.stage = ('idle', 0)
                await self.sendText('Sticker deleted')

        if stage == 'cancel':
            if substage == 0:
                self.stage = ('idle', 0)


    async def process_command(self, **kwargs):
        """ Postprocessing commands """
        stage, substage = self.stage

        if stage == 'showpacks':
            # receive /showstickerpacks
            if substage == 0:
                out_msg = stickers.ShowStickerPacks(self._get_id(),
                    ownerUserId=self._peer.id)
                await self.send(out_msg)

        if stage == 'showstickers':
            # receive /showstickers
            if substage == 0:
                await self.sendText('give me stickerpack ID')

            # receive stickerpack ID
            if substage == 1:
                params = kwargs.get('params')
                out_msg = stickers.ShowStickers(self._get_id(),
                    ownerUserId=self._peer.id, packId=params)
                await self.send(out_msg)

        if stage == 'deletesticker':
            # receive /deleteticker
            if substage == 0:
                await self.sendText('give me packID:stickerID')

            # receive packId:stickerID
            if substage == 1:
                packId, stickerId = kwargs.get('params').split(':')
                out_msg = stickers.DeleteSticker(self._get_id(),
                    ownerUserId=self._peer.id,
                    packId=packId, stickerId=stickerId)
                await self.send(out_msg)

        if stage == 'cancel':
            # receive /cancel
            if substage == 0:
                await self.sendText('current command aborted')
