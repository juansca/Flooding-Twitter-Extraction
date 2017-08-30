import datetime
import sys
from config import consumer_key, consumer_secret
from config import access_token, access_token_secret
from TwitterSearch import TwitterSearchOrder, TwitterSearch
from TwitterSearch import TwitterSearchException


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


class Query():
    def __init__(self, keywords, ntweets=100):
        self.keywords = keywords
        self.ntweets = ntweets

    def search(self, media=True, urls=True, until=False,
               localization=False,  # TODO: Any tweets found with 'True'
               latitude=-31.4135000, longitude=-64.1810500, radius=50):
        keywords = self.keywords
        ntweets = self.ntweets

        try:
            tso = TwitterSearchOrder()
            tso.set_keywords(keywords)  # we want to see 'keywords' tweets only
            tso.set_language('es')  # Only in Spanish
            tso.set_include_entities(media)  # all those entity information
            tso.set_geocode(latitude, longitude, radius, imperial_metric=False)

            if until:
                until = datetime.datetime.strptime(until, "%Y-%m-%d").date()
                print(isinstance(until, datetime.date))
                tso.set_until(until)
            if urls:
                tso.set_link_filter()  # urls on tweets

            ts = TwitterSearch(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
             )

            next_max_id = 0

            format_str = '{} tweets downloaded. {} remaining'

            progress(format_str.format(0, ntweets))
            # let's start the action
            tweets = ntweets
            metadata = True
            print(metadata)
            while(tweets >= 0 and metadata):

                # Query the Twitter API
                response = ts.search_tweets(tso)
                # check if there are statuses returned and whether we still
                # have work to do. We NEED geolocalization of the tweets

                metadata = len(response['content']['search_metadata']) != 0

                # check all tweets according to their ID
                for tweet in response['content']['statuses']:
                    tweet_id = tweet['id']
                    # current ID is lower than current next_max_id?
                    if (tweet_id < next_max_id) or (next_max_id == 0):
                        next_max_id = tweet_id
                        next_max_id -= 1  # decrement to avoid seeing this tweet again

                    if localization:
                        coordinates = tweet['coordinates'] is not None
                        geo = tweet['geo'] is not None
                        if not coordinates and not geo:
                            continue
                    yield tweet

                # set lowest ID as MaxID
                tweets -= 1
                progress(format_str.format(ntweets - tweets, tweets))
                tso.set_max_id(next_max_id)

        except TwitterSearchException as e:
            print(e)


if __name__ == '__main__':
    q = Query(["cristina", "macri"])
    for tweet in q.search(media=True, urls=True):
        print(tweet['id'])
