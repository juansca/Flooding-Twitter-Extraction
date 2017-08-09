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
from twitterscraper.query import query_tweets
from format_input import create_query


if __name__ == '__main__':
    opts = docopt(__doc__)
    if opts['-n'] is not None:
        n = int(opts['-n'])
    else:
        n = None
    date = opts['-d']
    loc = opts['-g']
    words = opts['-w']
    # Just join everything and create the query
    adv_query = create_query(date, words, loc)

    # Collect and save tweets
    filename = 'tweets/' + opts['-o']
    with open(filename, "w") as f:
        for tweet in query_tweets(adv_query, n)[:n]:
            print(tweet.text, tweet.timestamp, file=f)
