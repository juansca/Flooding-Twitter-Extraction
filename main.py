import urllib.request
from urllib.error import HTTPError
from imgkit import from_url
from post_extraction.tweet_extract import textract
from post_extraction.getdata import FloodingData
from image_classif.incep_classify import ImageClassifier

pathDir = 'tweets_attached/'

def download_image(url, name):
    """Download a image from a url."""
    name = pathDir + name + '.jpg'
    urllib.request.urlretrieve(url, name)


def webpage_screenshot(url, name):
    """Take a screenshot from the page correspondly at the given url."""
    filename = 'images/webpages_shots/' + name
    from_url(url, filename + '.jpg')


if __name__ == '__main__':
    model = ImageClassifier('images/' + pathDir)
    for classification in model.classify_dir():
        print(classification)

#    # Getting tweets
#    textract(250, "2017-08-9, 2017-08-14",
#             "Córdoba, Argentina, 500",
#             "elecciones, macri, cristina",
#             "holi6")
#
#    # Getdata object
#    my_data5 = FloodingData("holi6")
#    text_5 = my_data5.tweet_text()
#    print(len(text_5))
#    print(text_5)
#
#    # Save the screenshot correspondly with the urls
#    urls_5 = my_data5.urls_from_text()
#    i = 0
#    for url in urls_5:
#        try:
#            webpage_screenshot(url, str(i))
#            i += 1
#        except:
#            continue
#
#    # Download the images attached on the tweets
#    print(my_data5.urls_from_text())
#    print(my_data5.images_urls())
#    i = 0
#    errors = []
#    for url in my_data5.images_urls():
#        i += 1
#        if url[:4] == 'http':
#            try:
#                download_image(url, str(i))
#            except HTTPError:
#                print("error in", url)
#                errors.append(url)
#        if i % 20 == 0:
#            print(i, "images downloaded")
#    print("The number of erros in downloading all file is", len(errors))
#    print(errors)
#
