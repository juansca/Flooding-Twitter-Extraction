import urllib.request
from urllib.error import HTTPError, URLError
from imgkit import from_url
import os


def download_media(url, name, pathdir):
    """Download a image from a url."""
    try:
        os.stat(pathdir)
    except FileNotFoundError:
        os.mkdir(pathdir)
    extension = url[len(url) - 4:len(url)]
    name = pathdir + name + extension
    urllib.request.urlretrieve(url, name)


def webpage_screenshot(url, name, directory):
    """Take a screenshot from the page correspondly at the given url."""
    try:
        os.stat(directory)
    except FileNotFoundError:
        os.mkdir(directory)

    filename = directory + name
    from_url(url, filename + '.jpg')
