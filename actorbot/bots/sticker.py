from actorbot.api import stickers
from actorbot.api import keyvalue
from actorbot.bots import Conversation
from actorbot.utils import logger


class StickerConv(Conversation):
    """
    """

    slashCommands = (
        ('createpack', 'create sticker pack'),
        ('selectpack', 'select sticker pack as current'),
        ('addsticker', 'create sticker in current pack'),
        ('delsticker', 'delete sticker from current pack'),
        ('showstickers', 'show stickers from current pack'),
        ('help', 'list commands'))
    admins = []
    command = ''
    stage = 0

    def message_handler(self, message):
        """
        """
        if message.type != 'Text':
            return
        if message.text == '/help':
            self.help()
        elif message.text == '/start':
            self.start()
        elif self.admins and (self._peer.id not in self.admins):
            self.sendText(
                text='Access denied. Administrator rights are required.')
            return
        elif message.text == '/createpack':
            self.createpack(message)
        else:
            if self.command == 'createpack':
                self.createpack(message)

    def response_handler(self, message):
        """
        """
        super().response_handler(message)
        if message.body is None:
            return
        if self.command == 'createpack':
            self.createpack(message)

    def createpack(self, message):
        """
        """
        if self.command and (self.command != 'createpack'):
            self.sendText('Wrong command')
            return

        if self.stage == 0:
            logger.debug(self.stage)
            self.stage = 1
            self.command = 'createpack'
            self.sendText(text='Enter name for you new stickerpack')
            return

        if self.stage == 1:
            logger.debug(self.stage)
            if message.type == 'Response':
                return
            self.stage = 2
            #self.stickerpackname = message.text
            #out_msg = stickers.CreateStickerPack(self._get_id(),
            #                                     creatorUserId=self._peer.id)
            #self.send(out_msg)
            return

        '''
        if self.stage == 2:
            self.stage = 3
            #logger.debug(message.body.)
            self.stickerpackid = message.body.value
            logger.debug('[%s] new command: %s:%d',
                         self._owner.name, self.command, self.stage)
            out_msg = keyvalue.GetValue(self._get_id(),
                keyspace='stickerbot', key='packs')
            self.send(out_msg)
            return

        if self.stage == 3:
            self.stage = 4
            logger.debug('[%s] new command: %s:%d',
                         self._owner.name, self.command, self.stage)
            return

        if self.stage == 4:
            self.stage = 5
            return
            #logger.debug('[%s] new command: %s:%d',
            #             self._owner.name, self.command, self.stage)
            #out_msg = keyvalue.GetValue(self._get_id(),
            #    keyspace='stickerbot', key='packs')
            #self.send(out_msg)
        '''