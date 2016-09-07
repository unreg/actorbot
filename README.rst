========
ActorBot
========

A simple python implementation `Actor Messaging <https://github.com/actorapp>`_ bot API
======================================================

Features
========

* simple, small and extensible. It's easy to write own `Actor Messaging <https://github.com/actorapp>`_ bots.
* pure Python with asyncio and aiohttp
* websocket connection to Actor ws|wss API-endpoint
* sending and receiving text messages
* API module
* `LICENSE <https://github.com/unreg/actorbot/blob/master/LICENSE.txt>`_

API module
==========

- Messaging: SendMessage, UpdateMessageContent

- Groups: CreateGroup, InviteUser

- KeyValue: SetVAlue, GetValue, DeleteValue, GetKeys

- Files: UploadFile, DownloadFile

- Stickers: CreateStickerPack, AddSticker, ShowStickers, DeleteSticker, MakeStickerPackDefault

- Bots: CreateBot

- Users: FindUser, ChangeUserName, ChangeUserNickname, ChangeUserAbout, ChangeUserAvatar, IsAdmin, AddSlashCommand, RemoveSlashCommand, AddUserExtString, AddUserExtBool, RemoveUserExt


  more in `Wiki <https://github.com/unreg/actorbot/wiki>`_


Requirements
============

* Python >= 3.5.1
* `aiohttp >= 0.22.0 <https://github.com/KeepSafe/aiohttp>`_


Getting started
===============


Simple echo bot example:

.. code-block:: python

    from actorbot import ActorBot
    from actorbot.api import messaging

    from actorbot.utils import logger


    class EchoBot(ActorBot):

        async def _delivered(self, response):
            logger.debug('[%s] message id=%s delivered: %s',
                         self._name, response.id, response.body.date)

        async def message_handler(self, message):
            await super().message_handler(message)
            out_msg = messaging.SendMessage(self._get_id(),
                                            peer=message.body.peer,
                                            message=message.body.message)
            self.send(out_msg, callback=self._delivered)


run EchoBot in farm:

.. code-block:: python

    import asyncio

    from actorbot import BotFarm
    from actorbot.bots import EchoBot


    echobot = EchoBot(endpoint='ENDPOINT',
                      token='TOKEN',
                      name='BOT_NAME')
    farm = BotFarm([echobot])

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait([farm.run()]))
    finally:
        loop.close()
