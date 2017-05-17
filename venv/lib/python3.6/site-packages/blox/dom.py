'''blox/dom.py

Defines the basic HTML DOM elements as blox

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
from blox.attributes import (AbstractAttribute, Attribute, BlokAttribute, BooleanAttribute,
                             IntegerAttribute, RenderedDirect, SetAttribute, TextAttribute)
from blox.base import Blok, NamedTag, Tag, TagWithChildren
from blox.builder import Factory
from blox.text import Text

factory = Factory('dom')


class DocType(Blok):
    '''Defines the doctype of an HTML page'''
    __slots__ = ('_type', )
    signals = ('type_changed', )

    def __init__(self, type='html'):
        self._type = type

    @property
    def type(self):
        return self._type

    @type.setter
    def set_type(self, type):
        if type != self._type:
            self.emit('type_changed', type)
            self._type = type

    def output(self, to=None, formatted=False, *args, **kwargs):
        '''Outputs the set text'''
        to.write('<!DOCTYPE {0}>'.format(self.type))


@factory.add()
class A(TagWithChildren):
    '''Defines a link that when clicked changes the current viewed page'''
    __slots__ = ()
    tag = "a"
    href = Attribute()
    media = Attribute()
    rel = Attribute()
    target = Attribute()
    type = Attribute()
    text = TextAttribute(Text)


@factory.add()
class Abr(TagWithChildren):
    '''Defines  an abbreviation or an acronym'''
    __slots__ = ()
    tag = "abr"



@factory.add()
class Address(TagWithChildren):
    '''Defines contact info for the author of a document or article'''
    __slots__ = ()
    tag = "address"


@factory.add()
class Area(TagWithChildren):
    '''Defines an area inside of an image map'''
    __slots__ = ()
    tag = 'area'
    alt = Attribute()
    coords = Attribute()
    href = Attribute()
    hreflang = Attribute()
    media = Attribute()
    rel = Attribute()
    shape = Attribute()
    target = Attribute()
    type = Attribute()


@factory.add()
class Article(TagWithChildren):
    '''Defines an independent, self-contained content'''
    __slots__ = ()
    tag = "article"


@factory.add()
class Aside(TagWithChildren):
    '''Defines content as being aside from the content it is placed in'''
    __slots__ = ()
    tag = "aside"


@factory.add()
class Audio(TagWithChildren):
    '''Defines sound, such as music or other audio streams'''
    __slots__ = ()
    tag = "audio"
    autoplay = BooleanAttribute()
    controls = BooleanAttribute()
    loop = BooleanAttribute()
    src = Attribute()


@factory.add()
class B(TagWithChildren):
    '''Defines bold text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    '''
    __slots__ = ()
    tag = "b"
    text = TextAttribute(Text)


@factory.add()
class Base(TagWithChildren):
    '''Defines the base URL for all relative URLs in a document'''
    __slots__ = ()
    tag = 'base'
    href = Attribute()
    target = Attribute()


@factory.add()
class BDI(TagWithChildren):
    '''Defines a part of text that should be formatted in a different direction
        from the other text outside it
    '''
    __slots__ = ()
    tag = "bdi"
    text = TextAttribute(Text)


@factory.add()
class BDO(TagWithChildren):
    '''Defines an override of the current text-direction'''
    __slots__ = ()
    tag = "bdo"
    dir = Attribute()
    text = TextAttribute(Text)


@factory.add()
class BlockQuote(TagWithChildren):
    '''Defines a section that is quoted from another source'''
    __slots__ = ()
    tag = "blockquote"
    cite = Attribute()
    text = TextAttribute(Text)


@factory.add()
class Body(TagWithChildren):
    '''Defines the document's body - which contains all the visible parts of an HTML document'''
    __slots__ = ()
    tag = "body"


@factory.add()
class Br(Tag):
    '''Defines a single line break'''
    __slots__ = ()
    tag = "br"
    tag_self_closes = True


@factory.add()
class Button(TagWithChildren):
    '''Defines a click-able button'''
    __slots__ = ()
    tag = "button"
    autofocus = BooleanAttribute()
    disabled = BooleanAttribute()
    form = Attribute()
    formaction = Attribute()
    formenctype = Attribute()
    formnovalidate = BooleanAttribute()
    formtarget = Attribute()
    type = Attribute()
    value = Attribute()


@factory.add()
class Canvas(Tag):
    '''Defines an area of the screen to draw graphic on the fly'''
    __slots__ = ()
    tag = "canvas"
    height = IntegerAttribute()
    width = IntegerAttribute()


@factory.add()
class Caption(TagWithChildren):
    '''Defines a table caption'''
    __slots__ = ()
    tag = "caption"


@factory.add()
class Cite(TagWithChildren):
    '''Defines the title of a work'''
    __slots__ = ()
    tag = "cite"


@factory.add()
class Code(TagWithChildren):
    '''Defines a piece of programming code'''
    __slots__ = ()
    tag = "code"
    content = BlokAttribute(Text)


@factory.add()
class Col(TagWithChildren):
    '''Defines a table column'''
    __slots__ = ()
    tag = "col"
    span = IntegerAttribute()


@factory.add()
class ColGroup(TagWithChildren):
    '''Defines a group of one or more columns in a table'''
    __slots__ = ()
    tag = "colgroup"
    span = IntegerAttribute()


@factory.add()
class Command(TagWithChildren):
    '''Defines a click-able command button'''
    __slots__ = ()
    tag = "command"
    checked = BooleanAttribute()
    disabled = BooleanAttribute()
    icon = Attribute()
    label = Attribute()
    radiogroup = Attribute()
    type = Attribute()


@factory.add()
class DataList(TagWithChildren):
    '''Defines a list of pre-defined options for input controls'''
    __slots__ = ()
    tag = "datalist"


@factory.add()
class DD(TagWithChildren):
    '''Defines a description of an item in a definition list'''
    __slots__ = ()
    tag = "dd"
    text = TextAttribute(Text)


@factory.add()
class Del(TagWithChildren):
    '''Defines text that has been deleted from a document'''
    __slots__ = ()
    tag = "del"
    cite = Attribute()
    datetime = Attribute()
    text = TextAttribute(Text)


@factory.add()
class Details(TagWithChildren):
    '''Defines collapse-able details'''
    __slots__ = ()
    tag = "details"
    open = Attribute()
    text = TextAttribute(Text)


@factory.add()
class Dfn(TagWithChildren):
    '''Defines a definition term'''
    __slots__ = ()
    tag = "dfn"
    text = TextAttribute(Text)


@factory.add()
class Div(TagWithChildren):
    '''Defines a section of a document'''
    __slots__ = ()
    tag = "div"


@factory.add()
class DL(TagWithChildren):
    '''Defines a definition list'''
    __slots__ = ()
    tag = "dl"


@factory.add()
class DT(TagWithChildren):
    '''Defines a term (an item) in a definition list'''
    __slots__ = ()
    tag = "dt"
    text = TextAttribute(Text)


@factory.add()
class Em(TagWithChildren):
    '''Defines emphasized text'''
    __slots__ = ()
    tag = "em"
    text = TextAttribute(Text)


@factory.add()
class Embed(TagWithChildren):
    '''Defines a container for an external (non-HTML) application'''
    __slots__ = ()
    tag = "embed"
    height = Attribute()
    src = Attribute()
    types = Attribute()
    width = IntegerAttribute()


@factory.add()
class FieldSet(TagWithChildren):
    '''Defines a group of related elements in a form'''
    __slots__ = ()
    tag = "fieldset"
    disabled = BooleanAttribute()
    form = Attribute()


@factory.add()
class FigCaption(TagWithChildren):
    '''Defines a caption for a figure element'''
    __slots__ = ()
    tag = "figcaption"
    text = TextAttribute(Text)


@factory.add()
class Figure(TagWithChildren):
    '''Defines self-contained figure content'''
    __slots__ = ()
    tag = "figure"


@factory.add()
class Footer(TagWithChildren):
    '''Defines a footer for a document or section'''
    __slots__ = ()
    tag = "footer"


@factory.add()
class Form(TagWithChildren):
    '''Defines a form for user input'''
    __slots__ = ()
    tag = "form"
    accept = Attribute()
    accept_charset = Attribute(name='accept-charset')
    action = Attribute()
    autocomplete = BooleanAttribute()
    enctype = Attribute()
    method = Attribute()
    name = Attribute()
    novalidate = Attribute()
    target = Attribute()


@factory.add()
class H(TagWithChildren):
    '''Defines the abstract concept of an HTML header'''
    __slots__ = ()
    text = TextAttribute(Text)


@factory.add()
class H1(H):
    '''Defines the most important heading'''
    __slots__ = ()
    tag = "h1"


@factory.add()
class H2(H):
    '''Defines the 2nd most important heading'''
    __slots__ = ()
    tag = "h2"


@factory.add()
class H3(H):
    '''Defines the 3rd most important heading'''
    __slots__ = ()
    tag = "h3"


@factory.add()
class H4(H):
    '''Defines the 4th most important heading'''
    __slots__ = ()
    tag = "h4"


@factory.add()
class H5(H):
    '''Defines the 5th most important heading'''
    __slots__ = ()
    tag = "h5"


@factory.add()
class H6(H):
    '''Defines the least important heading'''
    __slots__ = ()
    tag = "h6"


@factory.add()
class Header(TagWithChildren):
    '''Defines a header for a document or section'''
    __slots__ = ()
    tag = "header"


@factory.add()
class HGroup(TagWithChildren):
    '''Defines a grouping of multiple header elements'''
    __slots__ = ()
    tag = "hgroup"


@factory.add()
class HR(Tag):
    '''Defines a thematic change in the content horizontally'''
    __slots__ = ()
    tag = "hr"
    tag_self_closes = True


@factory.add()
class I(TagWithChildren):
    '''Defines text that is in an alternate voice or mood
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    '''
    __slots__ = ()
    tag = "i"


@factory.add()
class IFrame(TagWithChildren):
    '''Defines an inline frame'''
    __slots__ = ()
    tag = "iframe"
    sandbox = Attribute()
    seamless = BooleanAttribute()
    src = Attribute()
    srcdoc = Attribute()
    width = IntegerAttribute()
    frameborder = Attribute()


@factory.add()
class Img(Tag):
    '''Defines an image'''
    __slots__ = ()
    tag = "img"
    tag_self_closes = True
    src = Attribute()
    alt = Attribute()
    crossorigin = Attribute()
    ismap = BooleanAttribute()
    width = IntegerAttribute()
    height = IntegerAttribute()


@factory.add()
class Input(NamedTag):
    '''Defines an input control'''
    __slots__ = ()
    tag = "input"
    tag_self_closes = True
    accept = Attribute()
    alt = Attribute()
    autocomplete = BooleanAttribute()
    autofocus = BooleanAttribute()
    checked = BooleanAttribute()
    disabled = BooleanAttribute()
    form = Attribute()
    formaction = Attribute()
    formenctype = Attribute()
    formmethod = Attribute()
    formnovalidate = Attribute()
    formtarget = Attribute()
    height = IntegerAttribute()
    list = Attribute()
    max = Attribute()
    maxlength = IntegerAttribute()
    min = Attribute()
    multiple = BooleanAttribute()
    pattern = Attribute()
    placeholder = Attribute()
    readonly = BooleanAttribute()
    required = BooleanAttribute()
    size = IntegerAttribute()
    src = Attribute()
    step = IntegerAttribute()
    type = RenderedDirect()
    value = Attribute()
    width = IntegerAttribute()


@factory.add()
class Ins(TagWithChildren):
    '''Defines text that has been inserted into a document'''
    __slots__ = ()
    tag = "ins"
    cite = Attribute()
    datetime = Attribute()
    text = TextAttribute(Text)


@factory.add()
class Kbd(TagWithChildren):
    '''Defines keyboard input'''
    __slots__ = ()
    tag = "kbd"


@factory.add()
class KeyGen(TagWithChildren):
    '''Defines a key-pair generator field'''
    __slots__ = ()
    tag = "keygen"
    autofocus = BooleanAttribute()
    challenge = BooleanAttribute()
    disabled = BooleanAttribute()
    form = Attribute()
    keytype = Attribute()
    name = Attribute()


@factory.add()
class Label(TagWithChildren):
    '''Defines a label for an input element'''
    __slots__ = ()
    tag = "label"
    for_ = RenderedDirect(name="for")
    form = Attribute()
    text = TextAttribute(Text)


@factory.add()
class Legend(TagWithChildren):
    '''Defines a caption for a fieldset, figure or details element'''
    __slots__ = ()
    tag = "legend"
    text = TextAttribute(Text)


@factory.add()
class LI(TagWithChildren):
    '''Defines a list item'''
    __slots__ = ()
    tag = "li"
    value = IntegerAttribute()
    text = TextAttribute(Text)


@factory.add()
class Link(Tag):
    '''Defines the relationship between a document an external resource'''
    __slots__ = ()
    tag = "link"
    tag_self_closes = True
    charset = Attribute()
    src = Attribute()
    href = Attribute()
    hreflang = Attribute()
    media = Attribute()
    rel = Attribute()
    type = Attribute()
    sizes = Attribute()


@factory.add()
class Map(TagWithChildren):
    '''Defines a client side image map'''
    __slots__ = ()
    tag = "map"


@factory.add()
class Mark(TagWithChildren):
    '''Defines marked / highlighted text'''
    __slots__ = ()
    tag = "mark"
    text = TextAttribute(Text)


@factory.add()
class Meta(Tag):
    '''Defines metadata about an HTML document'''
    __slots__ = ()
    tag = "meta"
    tag_self_closes = True
    charset = Attribute()
    content = RenderedDirect()
    http_equiv = Attribute(name='http-equiv')


@factory.add()
class Meter(TagWithChildren):
    '''Defines a scalar measurement within a known range'''
    __slots__ = ()
    tag = "meter"
    form = Attribute()
    high = IntegerAttribute()
    low = IntegerAttribute()
    max = IntegerAttribute()
    min = IntegerAttribute()
    optimum = IntegerAttribute()
    value = IntegerAttribute()


@factory.add()
class Nav(TagWithChildren):
    '''Defines navigation links'''
    __slots__ = ()
    tag = "nav"


@factory.add()
class NoScript(TagWithChildren):
    '''Defines alternate content for users that do not support client side scripts'''
    __slots__ = ()
    tag = "noscript"


@factory.add()
class Object(TagWithChildren):
    '''Defines an embedded object'''
    __slots__ = ()
    tag = "object"
    form = Attribute()
    height = IntegerAttribute()
    type = Attribute()
    usemap = Attribute()
    width = IntegerAttribute()


@factory.add()
class OL(TagWithChildren):
    '''Defines an ordered list'''
    __slots__ = ()
    tag = "ol"
    reversed = BooleanAttribute()
    start = IntegerAttribute()
    type = Attribute()
    text = TextAttribute(Text)


@factory.add()
class OptGroup(TagWithChildren):
    '''Defines a group of related options in a drop-down list'''
    __slots__ = ()
    tag = "optgroup"
    disabled = BooleanAttribute()
    label = Attribute()


@factory.add()
class Option(TagWithChildren):
    '''Defines an option in a drop-down list'''
    __slots__ = ()
    tag = "option"
    disabled = BooleanAttribute()
    label = Attribute()
    selected = BooleanAttribute()
    value = RenderedDirect()
    text = TextAttribute(Text)


@factory.add()
class Output(TagWithChildren):
    '''Defines the result of a calculation'''
    __slots__ = ()
    tag = "output"
    for_ = Attribute(name="for")
    form = Attribute()


@factory.add()
class P(TagWithChildren):
    '''Defines a paragraph'''
    __slots__ = ()
    tag = "p"
    text = TextAttribute(Text)


@factory.add()
class Param(Tag):
    '''Defines a parameter for an object'''
    __slots__ = ()
    tag = "param"
    tag_self_closes = True
    value = RenderedDirect()


@factory.add()
class Pre(TagWithChildren):
    '''Defines pre formatted text'''
    __slots__ = ()
    tag = "pre"
    text = TextAttribute(Text)


@factory.add()
class Progress(TagWithChildren):
    '''Defines the progress of a task'''
    __slots__ = ()
    tag = "progress"
    max = IntegerAttribute()
    value = IntegerAttribute()


@factory.add()
class Q(TagWithChildren):
    '''Defines a short quotation'''
    __slots__ = ()
    tag = "q"
    cite = Attribute()
    text = TextAttribute(Text)


@factory.add()
class RP(TagWithChildren):
    '''Defines what to show in browsers that do not support ruby annotations'''
    __slots__ = ()
    tag = "rp"


@factory.add()
class RT(TagWithChildren):
    '''Defines an explanation / pronunciation of characters (for East Asian typography)'''
    __slots__ = ()
    tag = "rt"
    text = TextAttribute(Text)


@factory.add()
class Ruby(TagWithChildren):
    '''Defines ruby annotations (for East Asian typography)'''
    __slots__ = ()
    tag = "ruby"
    text = TextAttribute(Text)


@factory.add()
class S(TagWithChildren):
    '''Defines text that is no longer correct'''
    __slots__ = ()
    tag = "s"
    text = TextAttribute(Text)


@factory.add()
class Samp(TagWithChildren):
    '''Defines sample output from a computer program'''
    __slots__ = ()
    tag = "samp"
    text = TextAttribute(Text)


@factory.add()
class Script(TagWithChildren):
    '''Defines a client-side script'''
    __slots__ = ()
    tag = "script"
    async = BooleanAttribute()
    defer = BooleanAttribute()
    type = Attribute()
    charset = Attribute()
    src = Attribute()
    code = BlokAttribute(Text)


@factory.add()
class Section(TagWithChildren):
    '''Defines a section of the document'''
    __slots__ = ()
    tag = "section"


@factory.add()
class Select(TagWithChildren):
    '''Defines a drop-down list'''
    __slots__ = ()
    tag = "select"
    autofocus = BooleanAttribute()
    disabled = BooleanAttribute()
    form = Attribute()
    multiple = BooleanAttribute()
    size = IntegerAttribute()


@factory.add()
class Small(TagWithChildren):
    '''Defines smaller text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    '''
    __slots__ = ()
    tag = "small"
    text = TextAttribute(Text)


@factory.add()
class Source(TagWithChildren):
    '''Defines multiple media resources for media elements'''
    __slots__ = ()
    tag = "source"
    media = Attribute()
    src = Attribute()
    type = Attribute()


@factory.add()
class Span(TagWithChildren):
    '''Defines a section in a document'''
    __slots__ = ()
    tag = "span"


@factory.add()
class Strong(TagWithChildren):
    '''Defines important text'''
    __slots__ = ()
    tag = "strong"
    text = TextAttribute(Text)


@factory.add()
class Style(TagWithChildren):
    '''Defines style information for a document'''
    __slots__ = ()
    tag = "style"
    media = Attribute()
    scoped = BooleanAttribute()
    type = Attribute()
    css = BlokAttribute(Text)


@factory.add()
class Sub(TagWithChildren):
    '''Defines sub-scripted text'''
    __slots__ = ()
    tag = "sub"
    text = TextAttribute(Text)


@factory.add()
class Summary(TagWithChildren):
    '''Defines a visible heading for a details element'''
    __slots__ = ()
    tag = "summary"
    text = TextAttribute(Text)


@factory.add()
class Sup(TagWithChildren):
    '''Defines super-scripted text'''
    __slots__ = ()
    tag = "sup"
    text = TextAttribute(Text)


@factory.add()
class Table(TagWithChildren):
    '''Defines a table - should be used for tables of data only (not for layout)'''
    __slots__ = ()
    tag = "table"
    border = BooleanAttribute()


@factory.add()
class TBody(TagWithChildren):
    '''Defines a group of content within a table'''
    __slots__ = ()
    tag = "tbody"


@factory.add()
class TD(TagWithChildren):
    '''Defines a table cell'''
    __slots__ = ()
    tag = "td"
    colspan = IntegerAttribute()
    headers = Attribute()
    rowspan = IntegerAttribute()


@factory.add()
class TextArea(TagWithChildren):
    '''Defines multi-line text input'''
    __slots__ = ()
    tag = "textarea"
    name = RenderedDirect()
    autofocus = BooleanAttribute()
    cols = IntegerAttribute()
    disabled = BooleanAttribute()
    form = Attribute()
    maxlength = IntegerAttribute()
    placeholder = Attribute()
    readonly = BooleanAttribute()
    required = BooleanAttribute()
    rows = IntegerAttribute()
    wrap = Attribute()
    text = TextAttribute(Text)


@factory.add()
class TFoot(TagWithChildren):
    '''Defines the footer of a table'''
    __slots__ = ()
    tag = "tfoot"


@factory.add()
class TH(TagWithChildren):
    '''Defines the header cell within a table'''
    __slots__ = ()
    tag = "th"
    colspan = IntegerAttribute()
    headers = Attribute()
    rowspan = IntegerAttribute()
    scope = Attribute()
    text = TextAttribute(Text)


@factory.add()
class THead(TagWithChildren):
    '''Defines header content within a table'''
    __slots__ = ()
    tag = "thead"


@factory.add()
class Time(TagWithChildren):
    '''Defines a date / time'''
    __slots__ = ()
    tag = "time"
    datetime = Attribute()
    pubdate = Attribute()
    text = TextAttribute(Text)


@factory.add()
class Title(TagWithChildren):
    '''Defines the title of a document'''
    __slots__ = ()
    tag = "title"
    text = TextAttribute(Text)


@factory.add()
class Head(TagWithChildren):
    '''Defines information about the document'''
    __slots__ = ()
    tag = "head"
    title = BlokAttribute(Title)


@factory.add()
class TR(TagWithChildren):
    '''Defines a table row'''
    __slots__ = ()
    tag = "tr"


@factory.add()
class Track(TagWithChildren):
    '''Defines text tracks for media elements'''
    __slots__ = ()
    tag = "track"
    default = BooleanAttribute()
    kind = Attribute()
    label = Attribute()
    src = Attribute()
    srclang = Attribute()


@factory.add()
class U(TagWithChildren):
    '''Defines text that should be stylistically different from normal text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    '''
    __slots__ = ()
    tag = "u"
    text = TextAttribute(Text)


@factory.add()
class UL(TagWithChildren):
    '''
        Defines an unordered list
    '''
    __slots__ = ()
    tag = "ul"


@factory.add()
class Var(TagWithChildren):
    '''Defines a variable'''
    __slots__ = ()
    tag = "var"
    text = TextAttribute(Text)


@factory.add()
class Video(TagWithChildren):
    '''Defines a video or movie'''
    __slots__ = ()
    tag = "video"
    autoplay = BooleanAttribute()
    controls = BooleanAttribute()
    height = IntegerAttribute()
    loop = BooleanAttribute()
    muted = BooleanAttribute()
    poster = Attribute()
    preload = Attribute()
    src = Attribute()
    width = IntegerAttribute()


@factory.add()
class Wbr(TagWithChildren):
    '''Defines a possible line-break'''
    __slots__ = ()
    tag = "wbr"


class HTML(TagWithChildren):
    '''Defines the root of an HTML document'''
    __slots__ = ()
    tag = "html"
    manifest = Attribute()
    head = BlokAttribute(Head, position=0)
    body = BlokAttribute(Body, position=1)
