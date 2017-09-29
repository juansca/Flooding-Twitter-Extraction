import urllib.request
from urllib.error import HTTPError, URLError
from imgkit import from_url
from post_extraction.tweet_extract import textract
from post_extraction.getdata_from_stream import StreamFloodingData
from image_classif.incep_classify import ImageClassifier
import time
from TwitterSearch import TwitterSearchException
from test.to_test import Test


pathDir = 'images/tweets_attached/'


def download_media(url, name):
    """Download a image from a url."""
    try:
        os.stat(pathDir)
    except FileNotFoundError:
        os.mkdir(pathDir)
    extension = url[len(url) - 4:len(url)]
    name = pathDir + name + extension
    urllib.request.urlretrieve(url, name)


def webpage_screenshot(url, name):
    """Take a screenshot from the page correspondly at the given url."""
    directory = 'images/webpages_shots/'
    try:
        os.stat(directory)
    except FileNotFoundError:
        os.mkdir(directory)

    filename = directory + name
    from_url(url, filename + '.jpg')


if __name__ == '__main__':
    model = Test(stream=True)
    # To test extract tweets
    model.extract_test(place="Texas USA, 1000",
                       keywords="Houston, Harvey, river, \
                                 USGS, hurricane, alert",
                       filename="holi22", many=False)

    # To test download media attached on tweets
#    model.dwnl_media_test()

    # To test classify media attached on tweets
#    model.classify_test()

    # To test screenshot from pages on tweets text
#    model.screenshot_test()
