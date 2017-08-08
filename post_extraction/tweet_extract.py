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
python post_extraction/tweet_dwnld.py -n 200 -d '2015-01-1, 2015-03-8' -w 'inundación, Sierras Chicas, catastrofe' -g 'Sierras Chicas, Argentina, 150' -o holi
"""
from docopt import docopt
from twitterscraper import query_tweets


if __name__ == '__main__':
    opts = docopt(__doc__)
    if opts['-n'] is not None:
        n = int(opts['-n'])
    else:
        n = None

    # Format the input to use in twitterscraper methods.
    # In https://github.com/taspinar/twitterscraper especifies that
    # to use advanced queries we have to respect the query format
    # implemented by twitter in his advanced search
    # (https://twitter.com/search-advanced)
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

    # Just join everything
    adv_query = query + location + date + '&src=typd'

    # Collect and save tweets
    filename = 'tweets/' + opts['-o']
    with open(filename, "w") as f:
        for tweet in query_tweets(adv_query, n)[:n]:
            print(tweet.text + 'EOT', file=f)
