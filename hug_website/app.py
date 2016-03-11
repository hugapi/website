"""hug's website: hug.rest"""
from functools import partial

import hug

from hug_website import controllers

app = hug.get(output=hug.output_format.suffix({'/js': hug.output_format.json}, hug.output_format.html)).suffixes('/js')
html = partial(hug.transform.suffix, {'/js': None})


@hug.static('/static', cache=True)
def static_files():
    return ('hug_website/static', )


@app.transform(html(controllers.frame), urls=('/', '/website/{page_name}'))
def root(page_name:hug.types.one_of(('home', ))='home'):
    return {'label': 'hug', 'version': hug.__version__,
            'content': globals()[page_name]()}


@app.transform(html(controllers.home))
def home():
    return [{'text': 'hi!'}]
