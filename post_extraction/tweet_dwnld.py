"""Twiter data downloader.

Usage:
  tweet_dwnld.py -n <n> -d <date> -w <words> -g <geo> -o <file>
  tweet_dwnld.py -h | --help

Options:
  -n <n>        Number of tweets [default: 10]
  -d <date>     Date the tweets were (format: ).
  -w <words>    Keywords to lookfor (list of string)
  -g <geo>      Geolocalization for the tweets (City, Country)
  -o <file>     Output tweets file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from twitterscraper import query_tweets
# from twitterscraper import query_tweets_once


if __name__ == '__main__':
    opts = docopt(__doc__)
    n = int(opts['-n'])

    date = opts['-d'].split(', ')
    date = 'since%3A' + date[0] + ' until%3A' + date[1]

    loc = opts['-g'].split(', ')
    location = ' near%3A' + '"' + loc[0] + '%2C ' + loc[1] + '" ' + 'within%3A50mi '

    words = opts['-w'].split(', ')
    query = 'q=' + words[len(words) - 1:][0]
    for w in words[:len(words) - 1]:
        query += ' OR ' + w

    adv_query = query + location + date + '&src=typd'

    for tweet in query_tweets(adv_query, 10)[:n]:
        print("-------")
        print(tweet.text)

####################
# Another approach to scrap twits
# TODO: Ver bien el manejo y filtrado de twits con "twitterscraper"
# Ejemplo:
# for tweet in query_tweets("lunes OR fiaca", 10)[:10]:
#     print("-------")
#     print(tweet.text)
