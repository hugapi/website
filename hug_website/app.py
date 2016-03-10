"""hug's website: hug.rest"""
import hug


@hug.static('/static', cache=True)
def static_files():
    return ('static', )


@hug.get('/')
def home():
    return "Website"
