import datetime
import sys
from post_extraction.twitterscraper.stream_query.config import consumer_key, consumer_secret
from post_extraction.twitterscraper.stream_query.config import access_token, access_token_secret
from TwitterSearch import TwitterSearchOrder, TwitterSearch
from TwitterSearch import TwitterSearchException


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


class Query():
    def __init__(self, keywords):
        self.keywords = keywords

    def search(self, media=True, urls=True, until=None,
               localization=False,  # TODO: Any tweets found with 'True'
               latitude=-31.4135000, longitude=-64.1810500, radius=50):
        """Query for tweets
        """
        keywords = self.keywords

        try:
            info_str = "Scrapping Tweets having: \n \
            Keywords: {} \n \
            Lat: {}  Long: {}  Radius {} \n \
            Tweets with urls: {} \n \
            Until: {} \n \
            And with media: {} \n"
            print(info_str.format(keywords, latitude,
                                  longitude, radius, urls, until, media))
            tso = TwitterSearchOrder()
            tso.set_keywords(keywords)  # we want to see 'keywords' tweets only
            tso.set_language('es')  # Only in Spanish
            tso.set_include_entities(media)  # all those entity information
            tso.set_geocode(latitude, longitude, radius, imperial_metric=False)
            if until is not None:
                until = datetime.datetime.strptime(until, "%Y-%m-%d").date()
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

            format_str = '{} tweets downloaded.'

            progress(format_str.format(0))
            # let's start the action
            tweets = 0
            metadata = True

            while(metadata):
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
                        # decrement to avoid seeing this tweet again
                        next_max_id -= 1
                    # Avoid extract retweets
                    if 'retweeted_status' in tweet.keys():
                        continue

                    if localization:
                        coordinates = tweet['coordinates'] is not None
                        geo = tweet['geo'] is not None
                        if not coordinates and not geo:
                            continue
                    tweets += 1
                    progress(format_str.format(tweets))
                    yield tweet

                    # set lowest ID as MaxID
                    tso.set_max_id(next_max_id)

        except TwitterSearchException as e:
            print(e)


if __name__ == '__main__':
    q = Query(["cristina", "macri"])
    for tweet in q.search(media=True, urls=True):
        pass
