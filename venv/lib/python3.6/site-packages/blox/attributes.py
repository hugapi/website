'''blox/attributes.py

Defines how Blox handles the setting of and definition of attributes

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


class AbstractAttribute(object):
    '''Defines the abstract Blok attribute concept'''
    __slots__ = ('name', 'signal', 'doc')

    def __init__(self, signal=False, doc="", name=None):
        self.signal = signal
        self.doc = ""
        if name:
            self.name = name

    def from_string(self, value):
        return value


class NestedAttribute(AbstractAttribute):
    '''Defines a reference to a nested attribute'''
    __slots__ = ('attribute', )

    def __init__(self, attribute, signal=False, doc="", name=None):
        super().__init__(signal=signal, doc=doc, name=name)
        self.attribute = attribute.split('.')

    def __get__(self, obj, cls):
        current_obj = obj
        for section in self.attribute[:-1]:
            current_obj = getattr(current_obj, section)
        return getattr(current_obj, self.attribute[-1])

    def __set__(self, obj, value):
        current_obj = obj
        for section in self.attribute[:-1]:
            current_obj = getattr(current_obj, section)
        return setattr(current_obj, self.attribute[-1], value)


class NestedBlokAttribute(NestedAttribute):
    '''Defines a reference to a nested attribute that is known to be representing a Blok type'''
    __slots__ = ('type', )

    def __init__(self, attribute, type, signal=False, doc="", name=None):
        super().__init__(attribute=attribute, signal=signal, doc=doc, name=name)
        self.type = type


class DirectAttribute(AbstractAttribute):
    '''Defines an attribute that is responsible for its own rendering, and modifies object attribute'''
    __slots__ = ('object_attribute', 'type')

    def __init__(self, signal=False, type=str, doc="", name=None):
        super().__init__(signal, doc=doc, name=name)
        self.type = type

    def __get__(self, obj, cls):
        if not hasattr(obj, self.object_attribute):
            setattr(obj, self.object_attribute, self.type())

        return getattr(obj, self.object_attribute)

    def from_string(self, value):
        return self.type(value)

    def __set__(self, obj, value):
        if type(value) == str:
            value = self.from_string(value)
        return setattr(obj, self.object_attribute, value)

    def __delete__(self, obj):
        delattr(obj, self.object_attribute)


class RenderedDirect(DirectAttribute):
    '''Defines a direct attribute that gets rendered as part of the start tag'''
    __slots__ = ('safe', )

    def __init__(self, signal=False, type=str, doc="", name=None, safe=False):
        super().__init__(signal, type=type, doc=doc, name=name)
        self.safe = safe

    def render_value(self, obj):
        return str(getattr(obj, self.object_attribute))

    def render(self, obj):
        if hasattr(obj, self.object_attribute):
            value = self.render_value(obj)
            if not self.safe:
                value = cgi.escape(value)
            return '{0}="{1}"'.format(self.name, value)


class ListAttribute(RenderedDirect):
    '''Defines an attribute that is exposed from Python as a list'''
    __slots__ = ()
    list_type = list

    def __init__(self, signal=False, doc="Takes a list of values", name=None):
        super().__init__(signal=signal, type=self.list_type, doc=doc, name=name)

    def render_value(self, obj):
        return " ".join(str(value) for value in getattr(obj, self.object_attribute))

    def from_string(self, value):
        return self.type((value, ))


class SetAttribute(ListAttribute):
    '''Defines an attribute that is exposed from Python as a set'''
    __slots__ = ()
    list_type = set


class BlokAttribute(DirectAttribute):
    '''Defines an automatically added nested Blok as a child attribute'''
    __slots__ = ('init', 'position')

    def __init__(self, type, init=False, position=None, signal=False, doc="A child blok", name=None):
        super().__init__(type=type, signal=signal, doc=doc, name=name)
        self.init = init
        self.position = position

    def __get__(self, obj, cls):
        if not hasattr(obj, self.object_attribute):
            add_object = self.type()
            position = getattr(self, 'position', None)
            if position is not None:
                obj.blox.insert(position, add_object)
            else:
                obj.blox.append(add_object)
            setattr(obj, self.object_attribute, add_object)

        return getattr(obj, self.object_attribute)

    def __set__(self, obj, value):
        self.__delete__(obj)
        if not hasattr(obj, self.object_attribute):
            position = getattr(self, 'position', None)
            if position is not None:
                obj.blox.insert(position, value)
            else:
                obj.blox.append(value)
            setattr(obj, self.object_attribute, value)
        return value

    def __delete__(self, obj):
        if hasattr(obj, self.object_attribute):
            obj.blox.remove(getattr(obj, self.object_attribute))
            delattr(obj, self.object_attribute)


class AccessorAttribute(DirectAttribute):
    '''Defines a blok accessed by a root attribute'''
    __slots__ = ('parent_attribute', )

    def __init__(self, type, signal=False, doc="An accessed blok attribute", name=None):
        super().__init__(type=type, signal=signal, doc=doc, name=name)

    def __get__(self, obj, cls):
        return getattr(obj, self.object_attribute, None)

    def parent(self, obj):
        return getattr(obj, self.parent_attribute)

    def instance(self, obj):
        return getattr(obj, self.object_attribute, None)

    def __set__(self, obj, value):
        if type(value) == str:
            value = self.type(value)

        parent = self.parent(obj)
        if value in parent:
            setattr(obj, self.object_attribute, value)
            return value

        position = None
        if hasattr(obj, self.object_attribute):
            position = parent.blox.index(self.instance(obj))
        self.__delete__(obj)
        if position is not None:
            parent.blox.insert(position, value)
        else:
            parent.blox.append(value)
        setattr(obj, self.object_attribute, value)
        return value

    def __delete__(self, obj):
        if hasattr(obj, self.object_attribute):
            self.parent(obj).blox.remove(self.instance(obj))
            delattr(obj, self.object_attribute)


class TextAttribute(BlokAttribute):
    __slots__ = ()

    def __get__(self, obj, cls):
        if not hasattr(obj, self.object_attribute):
            add_object = self.type()
            position = getattr(self, 'position', None)
            if position is not None:
                obj.blox.insert(position, add_object)
            else:
                obj.blox.append(add_object)
            setattr(obj, self.object_attribute, add_object)

        return getattr(obj, self.object_attribute)

    def __set__(self, obj, value):
        self.__delete__(obj)
        if not hasattr(obj, self.object_attribute):
            position = getattr(self, 'position', None)
            value = self.type(value)
            if position is not None:
                obj.blox.insert(position, value)
            else:
                obj.blox.append(value)
            setattr(obj, self.object_attribute, value)
        return getattr(obj, self.object_attribute)


class Attribute(AbstractAttribute):
    '''Defines a basic Blok attribute that is rendered by the framework and stores its data in a .attributes dict'''
    __slots__ = ()

    def __get__(self, obj, cls):
        return obj.attributes[self.name]

    def __set__(self, obj, value):
        if self.signal and (self.name not in obj.attributes or obj.attributes[self.name] != value):
            obj.emit(self.signal, value)
        obj.attributes[self.name] = value

    def __delete__(self, obj):
        obj.attributes.pop(self.name, None)


class AttributeTransform(Attribute):
    '''Defines an attribute that transforms values for Python and HTML use'''
    __slots__ = ('to_python', 'to_html')

    def __init__(self, signal=None, to_python=None, to_html=str, doc="", name=None):
        super().__init__(signal=signal, doc=doc, name=name)
        self.to_python = to_python
        self.to_html = to_html

    def __get__(self, obj, cls):
        value = super().__get__(obj, cls)
        return self.to_python(value) if self.to_python else value

    def __set__(self, obj, value):
        super().__set__(obj, self.to_html(value) if self.to_html else value)

    def from_string(self, value):
        return self.to_python(value)


class BooleanAttribute(AttributeTransform):
    '''Defines a boolean attribute'''
    __slots__ = ('default', 'true_string', 'false_string')

    def __init__(self, signal=None, default=False, true_string="true", false_string="false", doc="A true/false value", name=None):
        super().__init__(signal, self.as_boolean, self.as_string, doc=doc, name=name)
        self.default = default
        self.true_string = true_string
        self.false_string = false_string

    def as_boolean(self, value):
        if value.lower() == self.false_string:
            return True
        elif value.lower() == self.true_string:
            return False
        return self.default

    def as_string(self, value):
        return str(value or self.default).lower()


class IntegerAttribute(AttributeTransform):

    def __init__(self, signal=None, doc="A whole number"):
        super().__init__(signal, int)
