###
# To extract image urls just search with google engine for search images
# by keywords. When it load the images, just press ctrl + shift + i, go to
# 'console' and paste the code below
# var cont=document.getElementsByTagName("body")[0];
# var imgs=document.getElementsByTagName("a");
# var i=0;var divv= document.createElement("div");
# var aray=new Array();var j=-1;
# while(++i<imgs.length){
#     if(imgs[i].href.indexOf("/imgres?imgurl=http")>0){
#       divv.appendChild(document.createElement("br"));
#       aray[++j]=decodeURIComponent(imgs[i].href).split(/=|%|&/)[1].split("?imgref")[0];
#       divv.appendChild(document.createTextNode(aray[j]));
#     }
#  }
# cont.insertBefore(divv,cont.childNodes[0]);
import urllib.request
from urllib.error import HTTPError, URLError


def download_image(dclass, url, name):
    """Download a image from a url."""
    name = 'data/' + dclass + '/' + name + '.jpg'
    urllib.request.urlretrieve(url, name)


if __name__ == '__main__':

    data_classes = ['data_flood', 'data_river']
    for dclass in data_classes:
        print("\n\nDownloading files from", dclass)
        with open(dclass + '.txt', 'r') as data:
            i = 0
            errors = []
            for url in data:
                i += 1
                if url[:4] == 'http':
                    try:
                        download_image(dclass, url, str(i))
                    except (HTTPError, URLError):
                        print("error in", url)
                        errors.append(url)
                if i % 20 == 0:
                    print(i, "images downloaded")
            print("The number of erros in downloading all file in", dclass,
                  "is", len(errors))
            print(errors)
