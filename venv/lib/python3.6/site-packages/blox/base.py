'''blox/base.py

The base for all blox

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
from collections import OrderedDict
import re
from itertools import chain

from connectable import Connectable
from connectable.base import CombineSignals
from blox.attributes import (AbstractAttribute, Attribute, RenderedDirect, SetAttribute,
                             BooleanAttribute, IntegerAttribute, DirectAttribute, BlokAttribute,
                             AccessorAttribute, NestedBlokAttribute)

from io import StringIO

UNDERSCORE = (re.compile('(.)([A-Z][a-z]+)'), re.compile('([a-z0-9])([A-Z])'))


class Blox(list):

    def __getitem__(self, index):
        if type(index) in (int, slice):
            return super().__getitem__(index)

        return self and self[0][index]

    def __setitem__(self, index, value):
        if type(index) in (int, slice):
            return super().__setitem__(index, value)

        for blok in self:
            blok[index] = value

    def get(self, index, default=None):
        if type(index) in (int, slice):
            return self[index] if (self and index > 0 and index < len(self)) else default

        return self[0].get(index, default) if self else default

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        for blok in self:
            blok.output(to, *args, **kwargs)
        return self

    def render(self, *args, **kwargs):
        '''Renders as a str'''
        render_to = StringIO()
        self.output(render_to, *args, **kwargs)
        return render_to.getvalue()

    def __str__(self):
        return self.render(formatted=True)

    def __getattr__(self, attribute):
        return self and getattr(self[0], attribute, None)

    def __setattr__(self, attribute, value):
        for blok in self:
            setattr(self, attribute, value)

    def first(self):
        return self.__class__((self[:1], ))

    def last(self):
        return self.__class__((self[-1:], ))

    def __call__(self, *blox, position=None):
        for blok in self:
            if callable(blok):
                blok(*blox, position=None)
        return self

    def add_class(self, class_name):
        for blok in self:
            if hasattr(blok, 'classes'):
                blok.classes.add(class_name)
        return self

    def remove_class(self, class_name):
        for blok in self:
            if hasattr(blok, 'classes'):
                blok.classes.discard(class_name)
        return self

    def filter(self, **attributes):
        return self.__class__((blok for blok in self if self._matches(blok, **attributes)))

    def _matches(self, blok, **attributes):
        for attribute, expected_value in attributes.items():
            if type(expected_value) in (list, tuple):
                check_in = getattr(blok, attribute, ())
                for value in expected_value:
                    if not value in check_in:
                        return False

            elif getattr(blok, attribute, None) != expected_value:
                return False

        return True

    def walk(self):
        for blok in self:
            yield blok
            if hasattr(blok, '_blox'):
                for item in blok.blox.walk():
                    yield item

    def all(self):
        return self.__class__(self.walk())

    def query(self, **attributes):
        return self.__class__((blok for blok in self.walk() if self._matches(blok, **attributes)))


class TagAttributes(CombineSignals):
    '''A meta class to automatically register signals for tag attributes'''

    def __new__(metaclass, name, parents, class_dict, *kargs, **kwargs):
        '''Updates a tag class to automatically register all signals'''
        attributes = {name: attribute for name, attribute in class_dict.items() if isinstance(attribute,
                                                                                              AbstractAttribute)}
        if attributes:
            if hasattr(parents[0], 'attribute_descriptors'):
                full_attributes = parents[0].attribute_descriptors.copy()
                full_attributes.update(attributes)
                attributes = full_attributes

            blok_attributes = {}
            render_attributes = []
            direct_attributes = []
            init_attributes = []
            accessor_attributes = []
            attribute_map = {}
            for attribute_name, attribute in attributes.items():
                if not hasattr(attribute, 'name'):
                    attribute.name = attribute_name
                if isinstance(attribute, DirectAttribute):
                    direct_attributes.append(attribute)
                    if hasattr(attribute, 'render'):
                        render_attributes.append(attribute)
                    if not hasattr(attribute, 'object_attribute'):
                        attribute.object_attribute = '_{0}'.format(attribute_name)
                    if getattr(attribute, 'init', False):
                        init_attributes.append(attribute_name)
                if isinstance(attribute, (BlokAttribute, NestedBlokAttribute)) and hasattr(attribute.type, 'tag'):
                    blok_attributes[attribute.type.tag] = attribute
                if isinstance(attribute, AccessorAttribute):
                    accessor_attributes.append(attribute)
                    if not hasattr(attribute, 'parent_attribute'):
                        attribute.parent_attribute = '_{0}_parent'.format(attribute_name)
                attribute_map[attribute.name] = attribute_name

            if direct_attributes and not name == 'AbstractTag' and '__slots__' in class_dict:
                class_dict['__slots__'] += tuple(attribute.object_attribute for attribute in direct_attributes)
                class_dict['__slots__'] += tuple(attribute.parent_attribute for attribute in accessor_attributes)

            if render_attributes:
                if hasattr(parents[0], 'render_attributes'):
                    render_attributes = list(parents[0].render_attributes) + render_attributes
                class_dict['render_attributes'] = set(render_attributes)

            if init_attributes:
                if hasattr(parents[0], 'init_attributes'):
                    init_attributes = list(parents[0].init_attributes) + init_attributes
                class_dict['init_attributes'] = init_attributes


            if blok_attributes:
                if hasattr(parents[0], 'blok_attributes'):
                    full_blok_attributes = dict(parents[0].blok_attributes)
                    full_blok_attributes.update(blok_attributes)
                    blok_attributes = full_blok_attributes
                class_dict['blok_attributes'] = blok_attributes

            if attribute_map:
                if hasattr(parents[0], 'attribute_map'):
                    full_attribute_map = dict(parents[0].attribute_map)
                    full_attribute_map.update(attribute_map)
                    attribute_map = full_attribute_map
                class_dict['attribute_map'] = attribute_map

            class_dict['attribute_descriptors'] = attributes
            attribute_signals = (attribute.signal for attribute in attributes.values() if getattr(attribute, 'signal'))
            if attribute_signals:
                class_dict['signals'] = class_dict.get('signals', ()) + tuple(attribute_signals)

        return super(TagAttributes, metaclass).__new__(metaclass, name, parents, class_dict, *kargs, **kwargs)


class Blok(Connectable, metaclass=TagAttributes):
    '''Defines the base blox blok object which can render itself and be instanciated'''
    __slots__ = ()

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        to.write('')
        return self

    def render(self, *args, **kwargs):
        '''Renders as a str'''
        render_to = StringIO()
        self.output(render_to, *args, **kwargs)
        return render_to.getvalue()

    def __str__(self):
        return self.render(formatted=True)

    def __repr_self__(self, identifiers=()):
        return "{0}({1})".format(self.__class__.__name__, " ".join(identifiers))

    def __repr__(self):
        return self.__repr_self__()


class Invalid(Blok):
    '''Defines how the lack of a vaild Blok should be rendered'''
    __slots__ = ()

    def output(self, to=None, *args, **kwargs):
        to.write('<h2>Invalid</h2>')
        return self


class Container(Blok):
    '''A Block that can contain child blocks'''
    __slots__ = ('_blox', )

    def __init__(self, *blox):
        super().__init__()
        if hasattr(self, 'init_attributes'):
            for attribute_name in self.init_attributes:
                getattr(self, attribute_name)
        for blok in blox:
            self(blok)

    @property
    def blox_container(self):
        '''Returns the container that should be responsible adding children, outside of init'''
        return self

    @property
    def blox(self):
        '''Lazily creates and returns the list of child blox'''
        if not hasattr(self, '_blox'):
            self._blox = Blox()
        return self._blox

    def __call__(self, *blox, position=None):
        '''Adds a nested blok to this blok'''
        if position is not None:
            for blok in blox:
                self.blox_container.blox.insert(position, blok)
        else:
            for blok in blox:
                self.blox_container.blox.append(blok)
        return blok

    def __iter__(self):
        return self.blox_container.blox.__iter__()

    def __contains__(self, blok):
        return blok in self.blox_container.blox

    def get(self, index, default=None):
        return self[index] if (len(self) and index > 0 and index < len(self)) else default

    def __getitem__(self, index):
        return self.blox_container.blox[index]

    def __setitem__(self, index, value):
        self.blox_container.blox.__setitem__(index, value)

    def __delitem__(self, index):
        return self.blox_container.blox.__delitem__(index)

    def __isub__(self, blok):
        self.blox_container.blox.remove(blok)
        return self

    def __iadd__(self, blok):
        self(blok)
        return self

    def __len__(self):
        return len(self.blox_container.blox)

    def __repr__(self):
        representation = [self.__repr_self__()]
        for child in self:
            for index, line in enumerate(repr(child).split("\n")):
                representation.append(("|---" if index == 0 else "|  ") + line)
        return "\n".join(representation)

    def output(self, to=None, formatted=False, indent=0, indentation='  ', *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        if formatted and self.blox:
            self.blox[0].output(to=to, formatted=True, indent=indent, indentation=indentation, *args, **kwargs)
            for blok in self.blox[1:]:
                to.write('\n')
                to.write(indent * indentation)
                blok.output(to=to, formatted=True, indent=indent, indentation=indentation, *args, **kwargs)
            if not indent:
                to.write('\n')
        else:
            for blok in self.blox:
                blok.output(to=to, *args, **kwargs)

        return self


class AbstractTag(Blok):
    '''A Blok that renders a single tag'''
    __slots__ = ()
    tag_self_closes = True
    tag = ""
    id = RenderedDirect()
    classes = SetAttribute(name="class")
    accesskey = Attribute()
    contenteditable = BooleanAttribute(default=True)
    contextmenu = Attribute()
    dir = Attribute()
    draggable = BooleanAttribute()
    dropzone = Attribute()
    hidden = BooleanAttribute()
    lang = Attribute()
    spellcheck = BooleanAttribute()
    style = Attribute()
    tabindex = IntegerAttribute()
    translate = BooleanAttribute(true_string="yes", false_string="no")
    render_attributes = ()

    def __init__(self, **attributes):
        super().__init__()
        for name, value in attributes.items():
            setattr(self, name, value)

    @property
    def attributes(self):
        '''Lazily creates and returns a tags attributes'''
        if not hasattr(self, '_attributes'):
            self._attributes = {}

        return self._attributes

    @property
    def start_tag(self):
        '''Returns the elements HTML start tag'''
        direct_attributes = (attribute.render(self) for attribute in self.render_attributes)
        attributes = ()
        if hasattr(self, '_attributes'):
            attributes = ('{0}="{1}"'.format(key, value)
                                             for key, value in self.attributes.items() if value)

        rendered_attributes = " ".join(filter(bool, chain(direct_attributes, attributes)))
        return '<{0}{1}{2}{3}>'.format(self.tag, ' ' if rendered_attributes else '',
                                       rendered_attributes, ' /' if self.tag_self_closes else "")

    @property
    def end_tag(self):
        '''Returns the elements HTML end tag'''
        if self.tag_self_closes:
            return ''

        return "</{0}>".format(self.tag)

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        to.write(self.start_tag)
        if not self.tag_self_closes:
            to.write(self.end_tag)

    def get(self, attribute, default=None):
        if attribute in self.attribute_descriptors.keys():
            return getattr(self, attribute, default)
        else:
            return self.attributes.get(default)

    def __contains__(self, attribute):
        return attribute in self.attributes

    def __getitem__(self, attribute):
        if attribute in self.attribute_descriptors.keys():
            return getattr(self, attribute)
        else:
            return self.attributes[attribute]

    def __setitem__(self, attribute, value):
        if attribute in self.attribute_descriptors.keys():
            setattr(self, attribute, value)
        else:
            self.attributes[attribute] = value

    def __delitem__(self, attribute):
        del self.attributes[attribute]

    def __repr_self__(self, identifiers=()):
        if getattr(self, '_id', None):
            identifiers = ('id="{0}"'.format(self.id), ) + identifiers
        return super().__repr_self__(identifiers)


class Tag(AbstractTag):
    '''A Blok that renders a single tag'''
    __slots__ = ('_attributes', '_id', '_classes')


class NamedTag(Tag):
    '''A Tag with an attached name'''
    __slots__ = ('_name', )
    name = RenderedDirect()

    def __repr_self__(self, identifiers=()):
        if getattr(self, '_name', None):
            identifiers += ('name="{0}"'.format(self.name), )
        return super().__repr_self__(identifiers)


class TagWithChildren(Container, AbstractTag):
    '''Defines a tag that can contain children'''
    __slots__ = ('_attributes', '_id', '_classes')
    tag = ""
    tag_self_closes = False

    def __init__(self, *blox, **attributes):
        super().__init__()
        for blok in blox:
            self(blok)
        for name, value in attributes.items():
            setattr(self, name, value)

    def output(self, to=None, formatted=False, indent=0, indentation='  ', *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        if formatted:
            to.write(self.start_tag)
            to.write('\n')
            if not self.tag_self_closes:
                for blok in self.blox:
                    to.write(indentation * (indent + 1))
                    blok.output(to=to, indent=indent + 1, formatted=True, indentation=indentation, *args, **kwargs)
                    to.write('\n')

            to.write(indentation * indent)
            to.write(self.end_tag)
            if not indentation:
                to.write('\n')
        else:
            to.write(self.start_tag)
            if not self.tag_self_closes:
                for blok in self.blox:
                    blok.output(to=to, *args, **kwargs)
            to.write(self.end_tag)

    def __contains__(self, attribute_or_blok):
        return Container.__contains__(self, attribute_or_blok) or AbstractTag.__contains__(self, attribute_or_blok)

    def get(self, attribute_or_blok, default=None):
        if type(attribute_or_blok) == int:
            return Container.get(self, attribute_or_blok, default)
        else:
            return AbstractTag.get(self, attribute_or_blok, default)

    def __getitem__(self, attribute_or_blok):
        if type(attribute_or_blok) in (int, slice):
            return Container.__getitem__(self, attribute_or_blok)
        else:
            return AbstractTag.__getitem__(self, attribute_or_blok)

    def __setitem__(self, attribute_or_blok, value):
        if type(attribute_or_blok) in (int, slice):
            return Container.__setitem__(self, attribute_or_blok, value)
        else:
            return AbstractTag.__setitem__(self, attribute_or_blok, value)

    def __delitem__(self, attribute_or_blok):
        if type(attribute_or_blok) in (int, slice):
            return Container.__delitem__(self, attribute_or_blok)
        else:
            return AbstractTag.__delitem__(self, attribute_or_blok)


class Wildcard(TagWithChildren):
    '''Can represent any element that does not have a built in representation, not very efficient'''
    __slots__ = ('tag', )

    def __init__(self, tag, *kargs, **kwargs):
        self.tag = tag

