import re

class FloodingData:
    def __init__(self, filename):
        pass

    def urls_from_text(self):
        # get tweets
        urls = [re.search("(?P<url>https?://[^\s]+)",
                tweet).group("url") for tweet in tweets]

        return urls

    def images_urls(self):
        images = [tweet.photo for tweet in tweets]

        return images

    def videos(self):
        pass
