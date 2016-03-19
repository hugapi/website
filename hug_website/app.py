"""hug's website: hug.rest"""
from functools import partial

import hug

from hug_website import controllers

dual_output = hug.output_format.suffix({'/js': hug.output_format.json}, hug.output_format.html)
app = hug.get(output=dual_output, on_invalid=hug.redirect.not_found).suffixes('/js')
html = partial(hug.transform.suffix, {'/js': None})


@hug.static('/static', cache=True)
def static_files():
    return ('hug_website/static', )


@hug.not_found(transform=html(controllers.frame), output=dual_output)
def drop_bear():
    return root('not_found')


@app.transform(html(controllers.frame), urls=('/', '/website/{page_name}/{section}', '/website/{page_name}'))
def root(page_name: hug.types.one_of(('home', 'contribute', 'quickstart', 'discuss', 'not_found', 'learn',
                                      'acknowledge', 'latest'))='home',
         section: hug.types.one_of(controllers.DOCUMENTATION_TEMPLATES.keys())=controllers.DOCUMENTATION[0][0]):
    if page_name == 'learn' and section:
        content = globals()[page_name](section)
    else:
        content = globals()[page_name]()
    return {'label': 'hug', 'version': hug.__version__,
            'content': content, 'page': page_name}


@app.transform(html(controllers.contribute))
def contribute():
    return {}


@app.transform(html(controllers.latest))
def latest():
    return {}


@app.transform(html(controllers.acknowledge))
def acknowledge():
    return {}


@app.transform(html(controllers.discuss))
def discuss():
    return {}


@app.transform(html(controllers.learn))
def learn(section: hug.types.one_of(controllers.DOCUMENTATION_TEMPLATES.keys())=controllers.DOCUMENTATION[0][0]):
    return {'sections': controllers.DOCUMENTATION, 'section': section}


def not_found():
    return {'not_found_header': '404 - BEWARE OF DROP BEARS',
            'not_found_description': "You don't belong around these parts. Do yourself a favor: ",
            'home_link_description': 'GO HOME.'}


@app.transform(html(controllers.quickstart))
def quickstart():
    return {'install_header': 'Installing hug',
            'install_description': 'The first step to get started is to install hug. hug has very minimal base system '
                                   'requirements - a local installation of Python3.3+, optionally inside a virtualenv. '
                                   'Additionally, pip is required, but this should be included with most Python3 '
                                   'installations by default. Once the base system is in good shape, run the following '
                                   'command to install the latest version of hug:',
            'first_header': 'First hug API',
            'first_description': 'To start off, we are going to make a simple API with local access only, but which '
                                 'demonstrates a couple of basic hug features: annotation-based validation and '
                                 'directives. Our first API will simply return a happy birthday message to the '
                                 'user, along with the time it took to generate the message:',
            'first_explaination': "In this example: hug's built-in type annotation automatically validates and "
                                  "converts incoming inputs while hug's directives automatically replace the hug_timer "
                                  'argument with a HugTimer object that keeps track of how long the function has been '
                                  'running. hug type annotations are, at their core, simply functions or objects which '
                                  'take a value as input, cast that value as something (raising on errors), and then '
                                  'return it. As a result of this, most built-in Python cast functions (int, str, etc.) '
                                  'are valid annotations in hug out of the box. You can also use Marshmallow schemas '
                                  'and types as hug type annotations without modification.',
            'http_header': 'Exposing our API as an HTTP micro-service',
            'http_description': 'To expose our API over HTTP, all we need to do is apply a hug HTTP route decorator to '
                                'the function, in addition to the local decorator. hug includes convience decorators '
                                'for all common HTTP methods (GET, POST, PUT, etc). In this case we will apply a get '
                                'decorator to specify that the function should return on an HTTP GET request. We will '
                                'also supply an example set of parameters to lead our users in the correct direction:',
            'cli_header': 'Enabling command line interaction',
            'cli_description': 'What if we want to allow users to interact with our API from the command line, as well? '
                               "No problem! All that's necessary is adding a hug.cli route decorator to our API "
                               'function:',
            'wsgi_header': 'Final step: Production HTTP use',
            'wsgi_description': "Finally, it's important to note that it's generally never a good idea to use a "
                                "development server (like hug's, Flask's, etc.) directly in production. Instead, "
                                'a WSGI-compatible server (such as uwsgi or Gunicorn) is recommended. Every hug API that '
                                'contains an http endpoint automatically exposes a `__hug_wsgi__` WSGI-compatible API '
                                '- making integration of our above example a breeze:'}


@app.transform(html(controllers.home))
def home():
    return {'slogan': 'Embrace the APIs of the future',
            'introduction': 'Drastically simplify API development over multiple interfaces. With hug, design '
                            'and develop your API once, then expose it however your clients need to consume it. '
                            'Be it locally, over HTTP, or through the command line - hug is the fastest '
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
                                 'one fell swoop.',
            'get_started_header': 'What are you waiting for?',
            'get_started_description': 'Start writing world class APIs on top of Python 3 in no time. Use hug {0} to '
                                       'radically simplify your code base.'.format(hug.__version__)}
