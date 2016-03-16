"""Defines the controllers responsible for modifying hug's website UI based on the underlying API"""
from blox.compile import filename
from blox.text import Text
from blox.dom import A, LI

CONTRIBUTE_MD = Text(filename('hug_website/views/contribute.html')())
DOCUMENTATION = (('architecture', 'Architecture Overview'),
                 ('routing', 'Routing'),
                 ('type_annotation', 'Type Annotation'),
                 ('extending', 'Extending / New Plugins'))
DOCUMENTATION_TEMPLATES = {'architecture': Text(open('hug_website/views/architecture.html').read()),
                           'extending': Text(open('hug_website/views/extending.html').read()),
                           'routing': Text(open('hug_website/views/routing.html').read()),
                           'type_annotation': Text(open('hug_website/views/type_annotation.html').read())}


def frame(data, template=filename('hug_website/views/frame.shpaml')):
    ui = template()
    ui.version.text = data['version']
    ui.main_content(globals()[data['page']](data['content']))
    if hasattr(ui, data['page']):
        getattr(ui, data['page']).classes.add('selected')
    return ui


def home(data, template=filename('hug_website/views/home.shpaml')):
    ui = template()
    ui.slogan.text = data['slogan']
    ui.introduction.text = data['introduction']
    ui.example_header.text = data['example_header']
    ui.performance_header.text = data['performance_header']
    ui.performance_description.text = data['performance_description']
    ui.versioning_header.text = data['versioning_header']
    ui.versioning_description.text = data['versioning_description']
    ui.documentation_header.text = data['documentation_header']
    ui.documentation_description.text = data['documentation_description']
    ui.annotation_header.text = data['annotation_header']
    ui.annotation_description.text = data['annotation_description']
    ui.reuse_header.text = data['reuse_header']
    ui.reuse_description.text = data['reuse_description']
    ui.get_started_header.text = data['get_started_header']
    ui.get_started_description.text = data['get_started_description']
    return ui


def contribute(data, template=filename('hug_website/views/contribute.shpaml')):
    ui = template()
    ui.markdown_content(CONTRIBUTE_MD)
    return ui


def discuss(data, template=filename('hug_website/views/discuss.shpaml')):
    ui = template()
    return ui


def quickstart(data, template=filename('hug_website/views/quickstart.shpaml')):
    ui = template()
    ui.install_header.text = data['install_header']
    ui.install_description.text = data['install_description']
    ui.first_header.text = data['first_header']
    ui.first_description.text = data['first_description']
    ui.first_explaination.text = data['first_explaination']
    ui.http_header.text = data['http_header']
    ui.http_description.text = data['http_description']
    ui.cli_header.text = data['cli_header']
    ui.cli_description.text = data['cli_description']
    ui.wsgi_header.text = data['wsgi_header']
    ui.wsgi_description.text = data['wsgi_description']
    return ui


def not_found(data, template=filename('hug_website/views/not_found.shpaml')):
    ui = template()
    ui.not_found_header.text = data['not_found_header']
    ui.not_found_description.text = data['not_found_description']
    ui.home_link_description.text = data['home_link_description']
    return ui


def learn(data, template=filename('hug_website/views/learn.shpaml')):
    ui = template()
    for link, label in data['sections']:
        ui.sections(LI(A(text=label, href='/website/learn/{0}'.format(link),
                         classes=('selected', ) if link == data['section'] else ())))
    ui.content(DOCUMENTATION_TEMPLATES[data['section']])
    return ui

