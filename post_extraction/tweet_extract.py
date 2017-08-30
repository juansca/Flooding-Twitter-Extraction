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
from geopy.geocoders import Nominatim
from adv_query.query import query_tweets
from stream_query.query import Query
from format_input import create_query
import pickle


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def textract(n, date, loc, words, filename, stream=True):
    """Main script that extract and save tweets acording to the especifications.

    :param n: Only used if stream=False
    :param date: Only used if stream=False
    :param loc: Geolocalization coordinates in --> (City Country, radius)
                format.
    :param stream: Bool that specifies if Twitter streamming API or
                   twitterscraper library will be used to query tweets.
    """
    if not stream:
        # Just join everything and create the query
        adv_query = create_query(date, words, loc)
        tweets = [tweet for tweet in query_tweets(adv_query, n)[:n]]
        filename = 'tweets/from_adv_search/' + filename
        with open(filename, "wb") as f:
            pickle.dump(tweets, f)
        f.close()

    else:
        place = loc[0]
        geolocator = Nominatim()
        location = geolocator.geocode(place)
        latitude = location.latitude
        longitude = location.longitude
        radius = loc[1]
        words = words.split(', ')
        query = Query(words)

        i = 0
        try:
            # Collect and Save tweets
            for tweet in query.search(latitude=latitude,
                                      longitude=longitude,
                                      radius=radius):

                if i % 100 == 0:  # Save tweets
                    save_stream_data(filename, tweet, i)
                i += 1
        except KeyboardInterrupt:
            save_stream_data(filename, tweet, i)


def save_stream_data(filename, data, i):
    act_file = filename + '_' + str(i)
    act_file = 'tweets/from_stream/' + act_file
    t = AttrDict()
    t.update(data)
    with open(filename, "wb") as f:
        pickle.dump(t, f)
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
    textract(n, date, loc, words, filename)
