def create_query(date, words, geoloc):
    """Format the input to use in twitterscraper methods.
    In https://github.com/taspinar/twitterscraper especifies that
    to use advanced queries we have to respect the query format
    implemented by twitter in his advanced search
    (https://twitter.com/search-advanced)
    """
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
