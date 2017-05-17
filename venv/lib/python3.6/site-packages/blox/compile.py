'''blox/compile.py

Creates an optimized programattically generated template from an html file

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
import json
from functools import partial
from xml.dom import minidom

from lxml.etree import HTMLParser
from lxml.html import fromstring

from blox import shpaml
from blox.all import factory
from blox.attributes import AccessorAttribute
from blox.base import Wildcard
from blox.containers import Container
from blox.text import Text

try:
    import Cython
except ImportError:
    Cython = False

SCRIPT_TEMPLATE = """# WARNING: DON'T EDIT AUTO-GENERATED

from blox.base import Blox, Wildcard
from blox.containers import Container
from blox.text import Text, UnsafeText
from blox.attributes import AccessorAttribute


class Template(Container):
{indent}__slots__ = tuple({accessors})
{indent}{attributes}


def build(factory):
{indent}template = Template()
{indent}{build_steps}
{indent}return template
"""


def string(html, start_on=None, ignore=(), use_shpaml=True, **queries):
    '''Returns a blox template from an html string'''
    if use_shpaml:
        html = shpaml.convert_text(html)
    return _to_template(fromstring(html), start_on=start_on,
                        ignore=ignore, **queries)


def file(file_object, start_on=None, ignore=(), use_shpaml=True, **queries):
    '''Returns a blox template from a file stream object'''
    return string(file_object.read(), start_on=start_on, ignore=ignore, use_shpaml=use_shpaml, **queries)


def filename(file_name, start_on=None, ignore=(), use_shpaml=True, **queries):
    '''Returns a blox template from a valid file path'''
    with open(file_name) as template_file:
        return file(template_file, start_on=start_on, ignore=ignore, use_shpaml=use_shpaml, **queries)


def _to_python(dom, factory=factory, indent='    ', start_on=None, ignore=(), **queries):
    if start_on:
        dom = dom.cssselect(start_on)[0]

    ignored = set()
    for query in ignore if type(ignore) in (list, tuple) else (ignore, ):
        ignored.update(dom.cssselect(query))

    current = [0]
    def increment(element_name=''):
        current[0] += 1
        return ('{0}{1}'.format(element_name, current[0]), factory.get(element_name))

    lines = []
    accessors = list(queries.keys())
    attributes = []

    matches = {}
    for accessor, query in queries.items():
        lines.append('template.{0} = Blox()'.format(accessor))
        for match in dom.cssselect(query):
            matches[match] = accessor

    def compile_node(node, parent='template'):
        if node in ignored or type(node.tag) != str:
            return

        blok_name, blok = increment(node.tag)
        lines.append("{0} = {1}({2}('{3}'))".format(blok_name, parent, 'factory' if blok else 'Wildcard', node.tag))
        if not blok:
            blok = Wildcard
        if node in matches:
            lines.append('template.{0}.append({1})'.format(matches[node], blok_name))

        text = (node.text or "").strip().replace('"', '\\"')
        if text:
            if 'text' in dir(blok):
                lines.append('{0}.text = """{1}"""'.format(blok_name, text))
            else:
                lines.append('{0}(Text("""{1}"""))'.format(blok_name, text))

        if 'id' in node.keys() and not 'accessor' in node.keys():
            node.set('accessor', node.get('id'))
        for attribute_name, attribute_value in node.items():
            attribute_name = getattr(blok, 'attribute_map', {}).get(attribute_name, attribute_name)
            if attribute_name == 'accessor':
                attribute_value = attribute_value.replace('-', '_')
                attributes.append("{0} = AccessorAttribute(Text)".format(attribute_value))
                lines.append('template._{0}_parent = {1}'.format(attribute_value, parent))
                lines.append('template.{0} = {1}'.format(attribute_value, blok_name))
            else:
                lines.append('{0}["{1}"] = "{2}"'.format(blok_name, attribute_name.replace('"', '\\"'),
                                                         attribute_value.replace('"', '\\"')))

        for child_node in node:
            if child_node.tag in getattr(blok, 'blok_attributes', {}):
                attached_child = "{0}.{1}".format(blok_name, blok.blok_attributes[child_node.tag].name)
                for nested_child_node in child_node:
                    compile_node(nested_child_node, parent=attached_child)
                attached_text = (child_node.text or "").strip().replace('"', '\\"')
                if attached_text:
                    if 'text' in dir(blok.blok_attributes[child_node.tag].type):
                        lines.append('{0}.text = """{1}"""'.format(attached_child, attached_text))
                    else:
                        lines.append('{0}(Text("""{1}"""))'.format(attached_child, attached_text))
            else:
                compile_node(child_node, parent=blok_name)

            tail = (child_node.tail or "").strip().replace('"', '\\"')
            if tail:
                lines.append('{0}(Text("""{1}"""))'.format(blok_name, tail))
    compile_node(dom)
    return SCRIPT_TEMPLATE.format(accessors=json.dumps(accessors),
                                  attributes="\n{indent}".join(attributes).replace("{indent}", indent),
                                  build_steps="\n{indent}".join(lines).replace("{indent}", indent),
                                  indent=indent)


def _to_template(dom, factory=factory, start_on=None, ignore=(), **queries):
    code = _to_python(dom, factory, indent='    ', start_on=start_on, ignore=ignore, **queries)
    if Cython and hasattr(Cython, 'inline'):
        name_space = Cython.inline(code)
    else:
        name_space = {}
        exec(compile(code, '<string>', 'exec'), name_space)
    return partial(name_space['build'], factory)
