import urllib.request
from urllib.error import HTTPError, URLError
from imgkit import from_url
from post_extraction.tweet_extract import textract
from post_extraction.getdata_from_stream import StreamFloodingData
from image_classif.incep_classify import ImageClassifier
import time
from TwitterSearch import TwitterSearchException


pathDir = 'images/tweets_attached/'


def download_media(url, name):
    """Download a image from a url."""
    try:
        os.stat(pathDir)
    except FileNotFoundError:
        os.mkdir(pathDir)
    extension = url[len(url) - 4:len(url)]
    name = pathDir + name + extension
    urllib.request.urlretrieve(url, name)


def webpage_screenshot(url, name):
    """Take a screenshot from the page correspondly at the given url."""
    directory = 'images/webpages_shots/'
    try:
        os.stat(directory)
    except FileNotFoundError:
        os.mkdir(directory)

    filename = directory + name
    from_url(url, filename + '.jpg')


if __name__ == '__main__':
#    model = ImageClassifier('images/' + pathDir)
#    for classification in model.classify_dir():
#        print(classification)

    # Getting tweets
#    for i in range(10):
#        try:
#            textract(
#                     "Texas USA, 1000",
#                     "Houston, Harvey, river, flood, damage, rain, flooding, \
#                     USGS, hurricane, alert",
#                     "holi22", stream=True)
#        except TwitterSearchException as err:
#            print("\n\nSleep window from Twitter API. 15 mins left\n")
#            time.sleep(15 * 60)
#            print("Working again...\n\n")
#            pass


    textract(
             "Isla Guadalupe Caribe, 1000",
             "Irma, huracan, hurricane, alerta, alert, \
              huracán, poderoso, catastrofe",
             "holi7", stream=True)
#
#    # Getdata object
    mypath = 'tweets/from_stream/'
    my_data5 = StreamFloodingData(mypath)
    text_5 = my_data5.extended_media_urls()
#
#    # Save the screenshot correspondly with the urls
#    urls_5 = my_data5.urls_from_text()
#    urls_5 += my_data5.url_from_entity()
#    print(len(urls_5), "will be downloaded")
#    i = 0
#    for url in urls_5:
#        try:
#            webpage_screenshot(url, str(i))
#            i += 1
#        except:
#            continue
#
#    # Download media attached on the tweets
#    print(my_data5.urls_from_text())
#    print(my_data5.images_urls())
#    i = 0
#    errors = []
#    for url in text_5:
#        url = url[1]
#        i += 1
#        if url[:4] == 'http':
#            try:
#                download_media(url, str(i))
#            except HTTPError:
#                print("error in", url)
#                errors.append(url)
#            except URLError:
#                print("URLError", url)
#                errors.append(url)
#        if i % 20 == 0:
#            print(i, "images downloaded")
#    print("The number of erros in downloading all file is", len(errors))
#    print(errors)
