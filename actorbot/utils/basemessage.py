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

import json

from actorbot.utils import logger


class BaseMessage(object):

    """
    """

    class SetNotExistAttr(Exception): pass


    def __init__(self, data):
        """
        """
        if isinstance(data, dict):
            self._data = data
        else:
            self._data = {}

    def __getattr__(self, attr):
        """
        """
        attr = self._data.get(attr, None)
        if isinstance(attr, dict):
            return BaseMessage(attr)
        else:
            return attr

    def __setattr__(self, attr, value):
        """
        """
        if attr == '_data':
            self.__dict__[attr] = value
        else:
            item = self.__dict__.get('_data').get(attr, None)
            if item is not None:
                if not isinstance(item, dict):
                    self.__dict__['_data'][attr] = value
            else:
                raise self.SetNotExistAttr(attr)

    def to_str(self):
        """
        """
        return json.dumps(self._data)
