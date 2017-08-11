import requests
from imgkit import from_url
from post_extraction.tweet_extract import textract
from post_extraction.getdata import FloodingData


def download_image(url, name):
    """Download a image from a url."""
    img_data = requests.get(url).content
    name = 'images/tweets_attached/' + name
    with open(name + '.jpg', 'wb') as handler:
        handler.write(img_data)


def webpage_screenshot(url, name):
    """Take a screenshot from the page correspondly at the given url."""
    filename = 'images/webpages_shots/' + name
    from_url(url, filename + '.jpg')


if __name__ == '__main__':
    # Getting tweets
    textract(30, "2015-02-10, 2015-02-20",
             "Córdoba, Argentina, 200",
             "inundación, Sierras Chicas, catastrofe, lluvia",
             "holi5")

    # Getdata object
    my_data5 = FloodingData("holi5")
    text_5 = my_data5.tweet_text()
    print(len(text_5))
    print(text_5)

    # Save the screenshot correspondly with the urls
    urls_5 = my_data5.urls_from_text()
    i = 0
    for url in urls_5:
        try:
            webpage_screenshot(url, str(i))
            i += 1
        except:
            pass

    # Download the images attached on the tweets
    for url in my_data5.images_urls():
        name = url.split('/')
        name = name[4]
        name = name[:len(name) - 4]
        download_image(url, name)
