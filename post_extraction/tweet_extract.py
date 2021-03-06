"""Twitter data downloader.

Usage:
  tweet_extract.py [-n <n>] -d <date> -w <words> -g <geo> -o <file>
  tweet_extract.py -h | --help

Options:
  -n <n>        Number of tweets.
  -d <date>     Date the tweets were (format: 'yyyy1-mm1-dd1, yyyy2-mm2-dd2').
  -w <words>    Keywords to search (format: 'kw1, kw2, ...')
  -g <geo>      Geolocalization for the tweets (format: 'City, Country, radio')
                the radio is expresed in miles.
                [default: 'Córdoba, Argentina, 50']
  -o <file>     Output tweets file.
  -h --help     Show this screen.

Example:
python post_extraction/tweet_extract.py -n 30 -d '2015-02-10, 2015-02-20' -w 'inundación, Sierras Chicas, catastrofe, lluvia' -g 'Córdoba Argentina, 200' -o holi
"""
from docopt import docopt
import urllib
from geopy.geocoders import Nominatim
from post_extraction.twitterscraper.adv_query.query import query_tweets
from post_extraction.twitterscraper.stream_query.query import Query
from post_extraction.format_input import create_query
import pickle
import os


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def textract(loc, words, filename, n=10, date=None, stream=True):
    """Main script that extract and save tweets acording to the especifications.

    :param n: Only used if stream=False
    :param date: Only used if stream=False
    :param loc: Geolocalization coordinates in --> (City Country, radius)
                format.
    :param stream: Bool that specifies if Twitter streamming API or
                   twitterscraper library will be used to query tweets.
    """
    if not stream:
        print("Advanced Query scrapping starting...")
        # Just join everything and create the query
        directory = 'tweets/from_adv_search/'
        adv_query = create_query(date, words, loc)
        tweets = [tweet for tweet in query_tweets(adv_query, n)[:n]]
        filename = directory + filename
        try:
            os.stat(directory)
        except FileNotFoundError:
            os.mkdir(directory)
        with open(filename, "wb") as f:
            pickle.dump(tweets, f)
        f.close()

    else:
        print("Streamming scrapping starting...")
        directory = 'tweets/from_stream/'
        try:
            os.stat(directory)
        except FileNotFoundError:
            os.mkdir(directory)

        loc = loc.split(', ')
        place = loc[0]
        geolocator = Nominatim()
        location = geolocator.geocode(place, timeout=None)
        latitude = location.latitude
        longitude = location.longitude
        radius = int(loc[1])
        words = words.split(', ')
        query = Query(words)

        i = 1
        tweets = []
        try:
            # Collect and Save tweets
            for tweet in query.search(latitude=latitude,
                                      longitude=longitude,
                                      radius=radius, until=date):
                tweet['latitude'] = latitude
                tweet['longitude'] = longitude
                tweets.append(tweet)
                if i % 10 == 0:  # Save tweets
                    act_file = filename + '_' + str(i)
                    act_file = directory + act_file

                    save_stream_data(act_file, tweets)
                    tweets = []
                i += 1
        except KeyboardInterrupt as k:
            print("\nSaving the remaining tweets collected...")
            act_file = filename + '_' + str(i)
            act_file = directory + act_file

            if tweets != []:
                save_stream_data(act_file, tweets)


def save_stream_data(filename, data):
    tweets = [AttrDict() for _ in range(len(data))]
    for t, d in zip(tweets, data):
        t.update(d)
    with open(filename, "wb") as f:
        pickle.dump(tweets, f)
    f.close()


if __name__ == '__main__':
    opts = docopt(__doc__)
    if opts['-n'] is not None:
        n = int(opts['-n'])
    else:
        n = None
    date = opts['-d']
    loc = opts['-g']
    words = opts['-w']
    filename = opts['-o']
    textract(loc, words, filename, n=n, date=date, stream=False)
