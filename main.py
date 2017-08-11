import requests
from post_extraction.tweet_extract import textract
from post_extraction.getdata import FloodingData


def download_image(url, name):
    img_data = requests.get(url).content
    name = 'images/' + name
    with open(name + '.jpg', 'wb') as handler:
        handler.write(img_data)


if __name__ == '__main__':
    textract(30, "2015-02-10, 2015-02-20",
             "Córdoba, Argentina, 200",
             "inundación, Sierras Chicas, catastrofe, lluvia",
             "holi5")

    my_data5 = FloodingData("holi5")
    urls_5 = my_data5.urls_from_text()
    print(urls_5)
    for url in my_data5.images_urls():
        name = url.split('/')
        name = name[4]
        name = name[:len(name) - 4]
        download_image(url, name)
