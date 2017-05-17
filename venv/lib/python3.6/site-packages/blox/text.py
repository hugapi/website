'''blox/text.py

Defines the basic Text rendering blox

Copyright (C) 2015  Timothy Edmund Crosley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

'''
import cgi

from blox.base import Blok
from blox.builder import Factory

factory = Factory('text')


class Text(Blok):
    '''Defines the most basic text block'''
    __slots__ = ('_value', )
    signals = ('value_changed', )

    def __init__(self, value=''):
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self.emit('value_changed', value)
            self._value = value

    def output(self, to=None, *args, **kwargs):
        '''Outputs the set text'''
        to.write(str(self._value))

    def __call__(self, text):
        '''Updates the text value'''
        self.value = text
        return self


class UnsafeText(Text):
    '''Defines text that comes from an untrusted source, and should therefore be escaped'''

    def output(self, to=None, *args, **kwargs):
        '''Outputs the set text'''
        to.write(cgi.escape(str(self._value)))


class unsafe(object):
    '''Wrap any str-able object in this to explicity mark it's output as unsafe'''
    __slots__ = ('value', )
    safe = True

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return cgi.escape(str(self.value))


class unsafe_str(str):
    '''Creates a string that is explicity marked as unsafe'''

    def __str__(self):
        return cgi.escape(super().__str__())
