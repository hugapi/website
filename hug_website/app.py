"""hug's website: hug.rest"""
from functools import partial

import hug

from hug_website import controllers

app = hug.get(output=hug.output_format.suffix({'/js': hug.output_format.json}, hug.output_format.html)).suffixes('/js')
html = partial(hug.transform.suffix, {'/js': None})


@hug.static('/static', cache=True)
def static_files():
    return ('hug_website/static', )


@app.transform(html(controllers.frame), urls=('/', '/website/{page_name}'), on_invalid=False)
def root(page_name:hug.types.one_of(('home', 'contribute', 'quickstart'))='home'):
    return {'label': 'hug', 'version': hug.__version__,
            'content': globals()[page_name](), 'page': page_name}


@app.transform(html(controllers.contribute))
def contribute():
    return {}


@app.transform(html(controllers.quickstart))
def quickstart():
    return {}


@app.transform(html(controllers.home))
def home():
    return {'slogan': 'Embrace the APIs of the future',
            'introduction': 'Drastically simplify API development over multiple interfaces. With hug you design '
                            'and develop your API once and then can easily expose it however your clients need to '
                            'consume it. Be it locally, over HTTP, or through the command line - hug is the fastest '
                            'and most modern way to create APIs on Python3.',
            'example_header': 'Obvious. Clean. Radically simple.',
            'performance_header': 'Unparalleled performance',
            'performance_description': 'hug has been built from the ground up with performance in mind. It is built '
                                       'to consume resources only when necessary and is then compiled with Cython '
                                       'to achieve amazing performance. As a result, hug consistently benchmarks as '
                                       'one of the fastest Python frameworks and without question takes the crown '
                                       'as the fastest high-level framwork for Python 3.',
            'versioning_header': 'Built in version management',
            'versioning_description': 'hug makes it easy to expose multiple versions of your API. With hug you can '
                                      'simply specify what version or range of versions an endpoint supports and then '
                                      'automatically have that enforced and communicated to your API\'s users.',
            'documentation_header': 'Automatic documentation',
            'documentation_description': 'Python makes it easy to document your APIs well using doc strings and types '
                                         'annotations. hug uses this information to automatically generate '
                                         'documentation for users of your API so you don\'t have to.',
            'annotation_header': 'Annotation powered validation',
            'annotation_description': 'hug leverages Python 3 type annotations to enable simple per argument '
                                      'validation and transformation. This leads to explicit and easy to follow '
                                      'endpoints.',
            'reuse_header': 'Write once. Use everywhere.',
            'reuse_description': 'With hug your API and business logic is cleanly separated from the interface your '
                                 'exposing it on, which means you can safely expose it over HTTP, CLI, and Python in '
                                 'one full swoop.',
            'get_started_header': 'What are you waiting for?',
            'get_started_description': 'Start writing world class APIs on top of Python 3 in no time. Use hug {0} to '
                                       'radically simplify your code base.'.format(hug.__version__)}
