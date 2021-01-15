#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import argparse
from pathlib import Path
import os

parser = argparse.ArgumentParser(description="Download images from a page")

images_source_url = {
    "google": "https://www.google.com/search?safe=off&hl=en&authuser=0&tbm=isch&sxsrf=ALeKk033jcDp2FsqreF9t462fVAxrkwRLg%3A1610584921197&source=hp&biw=1440&bih=821&ei=WZP_X6XGCZW80PEP1fKh2Ag&q=query&oq=query&gs_lcp=CgNpbWcQAzIECCMQJzIICAAQsQMQgwEyBQgAELEDMgUIABCxAzIFCAAQsQMyBQgAELEDMggIABCxAxCDATIFCAAQsQMyBQgAELEDMgUIABCxAzoHCCMQ6gIQJzoCCABQuBZYhB1gnB5oAXAAeAGAAewBiAHNBJIBBTYuMC4xmAEAoAEBqgELZ3dzLXdpei1pbWewAQo&sclient=img&ved=0ahUKEwjl1uywmJruAhUVHjQIHVV5CIsQ4dUDCAc&uact=5",
    "bing": "https://www.bing.com/images/search?q=query&qs=n&form=QBILPG&sp=-1&pq=query&sc=8-7&cvid=A6939D2F1C0047208F32FE76D80D7718&first=1&tsc=ImageBasicHover",
    "yahoo": "https://images.search.yahoo.com/search/images;_ylt=Awr9Fqrbkv9fcncAGmOLuLkF;_ylc=X1MDOTYwNTc0ODMEX3IDMgRmcgMEZ3ByaWQDRkdUb2pTa0NTS0tNUDBtcTczN2N4QQRuX3N1Z2cDMTAEb3JpZ2luA2ltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzcEcXVlcnkDcGlrYWNodQR0X3N0bXADMTYxMDU4NDc5OA--?fr2=sb-top-images.search&p=query&ei=UTF-8&iscqry=&fr=sfp"}

parser.add_argument("-q1", metavar="query", help="classification 1")
parser.add_argument("-q2", metavar="query", help="classification 2")

parser.add_argument("-d", metavar="directory name for dataset", help="just name it dataset", default="dataset")


def main():
    args = parser.parse_args()
    query1 = args.q1
    query2 = args.q2
    dirname = args.d

    Path(f"{dirname}/test/").mkdir(parents=True, exist_ok=True)

    download_photos(query1, dirname)
    download_photos(query2, dirname)


def download_photos(query, dirname):
    urls = [value.replace("query", query) for value in images_source_url.values()]

    results = [requests.get(url) for url in urls]

    html_pages = [BeautifulSoup(result.text, 'html.parser') for result in results]
    images = [html.find_all('img') for html in html_pages]
    images = [val for sublist in images for val in sublist]

    Path(f"{dirname}/train/{query}").mkdir(parents=True, exist_ok=True)
    Path(f"{dirname}/validation/{query}").mkdir(parents=True, exist_ok=True)

    testnum = len(os.listdir(dirname + "/test")) + 1

    for idx, image in enumerate(images):
        link = None
        if image.has_key("src") and image["src"].startswith("ht"):
            link = image["src"]
        elif image.has_key("data-src") and image["data-src"].startswith("ht"):
            link = image["data-src"]
        else:
            continue

        print(link + "\n")
        first_ten_percent = len(images) * .1
        if idx < first_ten_percent:
            full_path = f"{dirname}/validation/{query}"
        elif first_ten_percent < idx < first_ten_percent * 2:
            full_path = f"{dirname}/test/"
        else:
            full_path = f"{dirname}/train/{query}"

        if full_path == f"{dirname}/test/":
            with open(full_path + "/" + str(testnum) + ".jpg", "wb") as f:
                if link.endswith(".gif"):
                    continue
                img = requests.get(link)
                f.write(img.content)
            testnum += 1
        else:
            with open(full_path + "/" + str(idx) + ".jpg", "wb") as f:
                if link.endswith(".gif"):
                    continue
                img = requests.get(link)
                f.write(img.content)


if __name__ == "__main__":
    main()
