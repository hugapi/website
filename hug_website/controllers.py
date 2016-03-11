from blox.compile import filename
from blox.text import Text


def frame(data, template=filename('hug_website/views/frame.shpaml')):
    ui = template()
    return ui


def home(data, template=filename('hug_website/views/home.shpaml')):
    ui = template()
    return ui
