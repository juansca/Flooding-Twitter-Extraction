import urllib.request
from urllib.error import HTTPError, URLError
from imgkit import from_url
from post_extraction.tweet_extract import textract
from post_extraction.getdata_from_stream import StreamFloodingData
from image_classif.incep_classify import ImageClassifier
import time
from TwitterSearch import TwitterSearchException
from utils import download_media, webpage_screenshot

pathDir = 'images/tweets_attached/'


class Test():
    def __init__(self, stream=True):
        self.stream = stream
        if stream:
            self.path = 'tweets/from_stream/'
        else:
            self.path = 'tweets/from_adv_search/'

    def extract_test(self, place=None, keywords=None,
                     filename=None, many=False):
        stream = self.stream
        # Getting tweets
        if many:
            for i in range(10):
                try:
                    textract(place, keywords, filename, stream)
                except TwitterSearchException as err:
                    print("\n\nSleep window from Twitter API. 15 mins left\n")
                    time.sleep(15 * 60)
                    print("Working again...\n\n")
                    pass
        else:
            textract(place, keywords, filename, stream)

    def classify_test(self):
        model = ImageClassifier('images/' + pathDir)
        for classification in model.classify_dir():
            print(classification)

    def screenshot_test(self):
        directory = 'images/webpages_shots/'
        # Save the screenshot correspondly with the urls
        data = StreamFloodingData(self.path)
        urls = data.urls_from_text()
        urls += data.url_from_entity()
        print(len(urls), "will be downloaded")
        i = 0
        for url in urls:
            try:
                self._webpage_screenshot(url, str(i), directory)
                i += 1
            except URLError:
                continue

    def dwnl_media_test(self):
        # Download media attached on the tweets
        data = StreamFloodingData(self.path)
        media_urls = data.extended_media_urls()
        i = 0
        errors = []
        for url in media_urls:
            url = url[1]
            i += 1
            if url[:4] == 'http':
                try:
                    download_media(url, str(i), pathDir)
                except HTTPError:
                    print("error in", url)
                    errors.append(url)
                except URLError:
                    print("URLError", url)
                    errors.append(url)
            if i % 20 == 0:
                print(i, "images downloaded")
        print("The number of erros in downloading all file is", len(errors))
        print(errors)
