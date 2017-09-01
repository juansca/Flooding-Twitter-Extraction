from os import listdir
from os.path import isfile, join
import re
import pickle


class StreamFloodingData:
    def __init__(self, path):
        filenames = [f for f in listdir(path) if isfile(join(path, f))]
        self.filenames = [path + f for f in filenames]

    def _load_from_pickle(self, filename):
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def tweet_text(self):
        """All tweets texts"""
        filenames = self.filenames
        tweet_text = []
        for f in filenames:
            for tweets in self._load_from_pickle(f):
                text = [tweet.text + "EOT" for tweet in tweets
                              if tweet is not None]
                tweet_text += text
        return tweet_text

    def urls_from_text(self):
        """Search urls in the text correspondly to tweets saved on the
        given file.
        """
        filenames = self.filenames
        all_urls = []
        for f in filenames:
            for tweets in self._load_from_pickle(f):
                urls = [re.search("(?P<url>https?://[^\s]+)",
                        tweet.text) for tweet in tweets]
                all_urls += [url.group("url") for url in urls if url
                             is not None]
        return all_urls

    def url_from_entity(self):
        """Search urls in the entity url correspondly to tweets saved on the
        given file.
        """
        filenames = self.filenames
        urls = []
        for f in filenames:
            for tweets in self._load_from_pickle(f):
                for tweet in tweets:
                    if tweet is not None:
                        urls += [url['url'] for url in
                                 tweet.entities['urls'] if url is not None]
        return urls

    def simple_media_urls(self):
        """Search media urls attached in to tweets saved on the given
        file.
        """
        filenames = self.filenames
        media_urls = []
        for f in filenames:
            for tweets in self._load_from_pickle(f):
                for tweet in tweets:
                    if tweet is not None:
                        try:
                            for media in tweet.entities['media']:
                                media_urls.append(media['media_url'])
                        except KeyError:
                            continue
        return media_urls

    def extended_media_urls(self):
        """Search media urls attached in to tweets saved on the given
        file.
        """
        filenames = self.filenames
        media_urls = []
        for f in filenames:
            for tweets in self._load_from_pickle(f):
                for tweet in tweets:
                    if tweet is not None:
                        try:
                            for media in tweet.extended_entities['media']:
                                if media['type'] == 'video':
                                    url_media = media['expanded_url']
                                    url_media = url_media[:8] + "mobile." + \
                                                url_media[8:]
                                else:
                                    url_media = media['expanded_url']
                                my_media = (media['type'], url_media)
                                media_urls.append(my_media)
                        except KeyError:
                            continue
                        except AttributeError:
                            continue
        return media_urls
