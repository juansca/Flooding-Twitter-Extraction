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
python post_extraction/tweet_extract.py -n 30 -d '2015-02-10, 2015-02-20' -w 'inundación, Sierras Chicas, catastrofe, lluvia' -g 'Córdoba, Argentina, 200' -o holi
"""
from docopt import docopt
from post_extraction.twitterscraper.query import query_tweets
from post_extraction.format_input import create_query
import pickle


def textract(n, date, loc, words, filename):
    """Main script that extract and save tweets acording to the especifications.
    """
    # Just join everything and create the query

    adv_query = create_query(date, words, loc)

    # Collect and save tweets
    tweets = [tweet for tweet in query_tweets(adv_query, n)[:n]]
    filename = 'tweets/' + filename
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
    textract(n, date, loc, words, filename)
