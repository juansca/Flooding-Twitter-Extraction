'''Use example:

exit or more> more
number of twits> 20
daterange of twits> '2015-02-1, 2015-02-10'
keywords> 'inundación, Sierras Chicas'
geolocalization> 'Córdoba, Argentina, 100'
filename where save twits> twit
exit or more> exit
'''
from twitterscraper import query_tweets
from format_input import create_query


def ask(name):
    arg_str = input(name + '> ')
    return eval(arg_str)


while True:
    try:
        fstr = input('exit or more> ')
        if fstr == 'exit':
            exit()
        elif fstr == 'more':
            n = ask('number of twits')
            if n == 'all':
                n = None
            d = ask('daterange of twits')
            w = ask('keywords')
            g = ask('geolocalization')

            adv_query = create_query(d, w, g)
            filename = input('filename where save twits> ')

            # Collect and save tweets
            filename = 'tweets/' + filename
            with open(filename, "w") as f:
                for tweet in query_tweets(adv_query, n)[:n]:
                    print(tweet.text + 'EOT', file=f)

    except (SyntaxError, TypeError, NameError) as err:
        print(err)
    except KeyboardInterrupt:
        exit()
    except EOFError:
        exit()
