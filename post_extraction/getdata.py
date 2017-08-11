import re
import pickle


class FloodingData:
    def __init__(self, filename):
        self.filename = filename

    def _load_from_pickle(self, filename):
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def urls_from_text(self):
        filename = 'tweets/' + self.filename
        for tweets in self._load_from_pickle(filename):
            urls = [re.search("(?P<url>https?://[^\s]+)",
                    tweet.text) for tweet in tweets]
            urls = [url.group("url") for url in urls if url is not None]
        return urls

    def images_urls(self):
        filename = 'tweets/' + self.filename
        for tweets in self._load_from_pickle(filename):
            images_urls = [tweet.photo for tweet in tweets]

        return images_urls
        
    def videos(self):
        pass
