from post_extraction.tweet_extract import textract
from post_extraction.getdata import FloodingData

if __name__ == '__main__':
    textract(30, "2015-02-10, 2015-02-20",
             "Córdoba, Argentina, 200",
             "inundación, Sierras Chicas, catastrofe, lluvia",
             "holi5")

    my_data4 = FloodingData("holi4")
    my_data5 = FloodingData("holi5")

    urls_4 = my_data4.urls_from_text()
    urls_5 = my_data5.urls_from_text()

    print("From shell")
    print(urls_4)

    print("\nFrom main")
    print(urls_5)
