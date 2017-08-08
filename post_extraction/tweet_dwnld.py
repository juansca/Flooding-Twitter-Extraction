"""Twiter data downloader.

Usage:
  tweet_dwnld.py -n <n> -d <date> -w <words> -g <geo> -o <file>
  tweet_dwnld.py -h | --help

Options:
  -n <n>        Number of tweets [default: 10]
  -d <date>     Date the tweets were (format: 'yyyy1-mm1-dd1, yyyy2-mm2-dd2').
  -w <words>    Keywords to lookfor (format: 'kw1, kw2, ...')
  -g <geo>      Geolocalization for the tweets (format: 'City, Country, radio')
                [default: 'Córdoba, Argentina, 50']
  -o <file>     Output tweets file.
  -h --help     Show this screen.
"""
from docopt import docopt
from twitterscraper import query_tweets
import pickle
# from twitterscraper import query_tweets_once


if __name__ == '__main__':
    opts = docopt(__doc__)
    n = int(opts['-n'])

    date = opts['-d'].split(', ')
    date = 'since%3A' + date[0] + ' until%3A' + date[1]

    loc = opts['-g'].split(', ')
    location = ' near%3A' + '"' + loc[0] + '%2C ' + loc[1] + '" '
    radio = 'within%3A' + loc[2] + 'mi '
    location += radio

    words = opts['-w'].split(', ')
    query = 'q=' + words[len(words) - 1:][0]
    for w in words[:len(words) - 1]:
        query += ' OR ' + w

    adv_query = query + location + date + '&src=typd'

    # Collect and save tweets
    filename = 'tweets/' + opts['-o']
    with open(filename, "w") as f:
        for tweet in query_tweets(adv_query, n)[:n]:
            # pickle.dump(tweet, f)
            print(tweet.text, file=f)
