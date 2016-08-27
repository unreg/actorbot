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

- [x] send text
- [ ] find user
- [ ] get user
- [ ] get group
- [ ] create group


Requirements
============

* Python >= 3.5.1
* `aiohttp >= 0.22.0 <https://github.com/KeepSafe/aiohttp>`_
* jinja2


Getting started
===============

.. code-block:: python

    import asyncio

    from actorbot import ActorBot, BotFarm


    class EchoBot(ActorBot):

        # override base handler for your bot logic
        def handler(self, message):
            # set destination peer a sender
            dest = message.body.peer

            # create echo text message
            out_text = TextMessage(text=message.body.message.text)

            # make sendmessage object
            out_msg = SendMessage(self._get_id(), peer=dest, message=out_text)

            # send message
            self.send(out_msg)

    bot = EchoBot(endpoint='ENDPOINT',
                  token='TOKEN',
                  name='BOT_NAME')
    farm = BotFarm([echobot])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([farm.run()]))

