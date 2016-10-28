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
* sending and receiving messages
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


Requirements
============

* Python >= 3.5.1
* `aiohttp >= 0.22.0 <https://github.com/KeepSafe/aiohttp>`_
* async_timeout >= 1.1.0 (optional)


Getting started
===============


Make your own conversation inherited from base class *Conversation*. For example simple echo bot:

.. code-block:: python

    from actorbot.bots import Conversation
    from actorbot.api import messaging


    class EchoConversation(Conversation):
        """
        Simple echo bot
        """
        async def message_handler(self, message):
            """ """
            out_msg = messaging.SendMessage(self._get_id(),
                                            peer=self._peer,
                                            message=message)
            self.send(out_msg)

        async def response_handler(self, message):
            """ """
            await super().response_handler(message)


run new bot in farm with own conversation:

.. code-block:: python

    from actorbot import BotFarm
    from actorbot import Bot
    from actorbot.bots import EchoConversation

    ...

    newbot = Bot(endpoint='YOUR_ACTOR_SERVER_ENDPOINT',
                 token='YOUR_BOT_TOKEN',
                 name='SOME_BOT_NAME',
                 conversation=EchoConversation)
    farm = BotFarm([newbot])
    loop.run_until_complete(asyncio.wait([farm.run()]))

    ...
    