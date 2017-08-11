from datetime import datetime

from bs4 import BeautifulSoup
from coala_utils.decorators import generate_ordering


@generate_ordering('timestamp', 'id', 'text', 'user', 'replies', 'retweets', 'likes', 'photo')
class Tweet:
    def __init__(self, user, id, timestamp, fullname, text, replies, retweets, likes, photo):
        self.user = user
        self.id = id
        self.timestamp = timestamp
        self.fullname = fullname
        self.text = text
        self.replies = replies
        self.retweets = retweets
        self.likes = likes
        self.photo = photo

    @classmethod
    def from_soup_image(cls, tweet):
        return cls(
            user=tweet.find('span', 'username').text[1:],
            id=tweet['data-item-id'],
            timestamp=datetime.utcfromtimestamp(
                int(tweet.find('span', '_timestamp')['data-time'])),
            fullname=tweet.find('strong', 'fullname').text,
            text=tweet.find('p', 'tweet-text').text or "",
            replies=tweet.find('div', 'ProfileTweet-action--reply').find('span',
            'ProfileTweet-actionCountForPresentation').text or '0',
            retweets=tweet.find('div', 'ProfileTweet-action--retweet').find('span',
            'ProfileTweet-actionCountForPresentation').text or '0',
            likes=tweet.find('div', 'ProfileTweet-action--favorite').find('span',
            'ProfileTweet-actionCountForPresentation').text or '0',
            photo=tweet.find('div', 'AdaptiveMediaOuterContainer').find('div', 'AdaptiveMedia is-square ').find('div', 'AdaptiveMedia-container').find('div', 'AdaptiveMedia-singlePhoto').find('div', 'AdaptiveMedia-photoContainer js-adaptive-photo ').find('img', "")['src'] or ""
        )

    @classmethod
    def from_soup_text(cls, tweet):
        return cls(
            user=tweet.find('span', 'username').text[1:],
            id=tweet['data-item-id'],
            timestamp=datetime.utcfromtimestamp(
                int(tweet.find('span', '_timestamp')['data-time'])),
            fullname=tweet.find('strong', 'fullname').text,
            text=tweet.find('p', 'tweet-text').text or "",
            replies=tweet.find('div', 'ProfileTweet-action--reply').find('span',
            'ProfileTweet-actionCountForPresentation').text or '0',
            retweets=tweet.find('div', 'ProfileTweet-action--retweet').find('span',
            'ProfileTweet-actionCountForPresentation').text or '0',
            likes=tweet.find('div', 'ProfileTweet-action--favorite').find('span',
            'ProfileTweet-actionCountForPresentation').text or '0',
            photo=""
        )


    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, "lxml")
        tweets = soup.find_all('li', 'js-stream-item')
        if tweets:
            for tweet in tweets:
                try:
                    yield cls.from_soup_image(tweet)
                except AttributeError:
                    # If don't have image attached try getting without images
                    try:
                        yield cls.from_soup_text(tweet)
                    except AttributeError:
                        pass  # Incomplete info? Discard!
