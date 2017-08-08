from twitterscraper import query_tweets


def create_query(date, words, geoloc):
    # Format the input to use in twitterscraper methods.
    # In https://github.com/taspinar/twitterscraper especifies that
    # to use advanced queries we have to respect the query format
    # implemented by twitter in his advanced search
    # (https://twitter.com/search-advanced)

    date = date.split(', ')
    date = 'since%3A' + date[0] + ' until%3A' + date[1]

    geoloc = geoloc.split(', ')
    location = ' near%3A' + '"' + geoloc[0] + '%2C ' + geoloc[1] + '" '
    radio = 'within%3A' + geoloc[2] + 'mi '
    location += radio

    words = words.split(', ')
    query = 'q=' + words[len(words) - 1:][0]
    for w in words[:len(words) - 1]:
        query += ' OR ' + w

    # Just join everything
    adv_query = query + location + date + '&src=typd'

    return adv_query


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
