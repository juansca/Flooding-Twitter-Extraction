import re
import pickle


class StreamFloodingData:
    def __init__(self, filename):
        self.filename = 'tweets/from_stream' + filename

    def _load_from_pickle(self, filename):
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def tweet_text(self):
        """All tweets texts"""
        filename = self.filename
        for tweets in self._load_from_pickle(filename):
            tweet_text = [tweet.text + "EOT" for tweet in tweets]
        return tweet_text

    def urls_from_text(self):
        """Search urls in the text correspondly to tweets saved on the
        given file.
        """
        filename = self.filename
        all_urls = []
        for tweets in self._load_from_pickle(filename):
            urls = [re.search("(?P<url>https?://[^\s]+)",
                    tweet.text) for tweet in tweets]
            all_urls += [url.group("url") for url in urls if url is not None]
        return all_urls

    def url_from_entity(self):
        """Search urls in the entity url correspondly to tweets saved on the
        given file.
        """
        filename = self.filename
        urls = []
        for tweet in self._load_from_pickle(filename):
            urls += [url['expanded_url'] for url in tweet.entities['urls']]
        return urls

    def media_urls(self):
        """Search media urls attached in to tweets saved on the given
        file.
        """
        filename = self.filename
        media_urls = []
        for tweet in self._load_from_pickle(filename):
            try:
                for media in tweet.entities['media']:
                    media_urls += media['media_url']
            except KeyError:
                continue
        return media_urls
