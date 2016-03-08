"""hug's website: hug.rest"""
import hug


@hug.get('/')
def home():
    return "Website"
