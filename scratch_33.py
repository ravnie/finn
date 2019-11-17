from bs4 import BeautifulSoup
import requests
import csv
import time

urls = []
base_url = "https://www.finn.no/bap/forsale/search.html?q="
search_url = "https://www.finn.no/bap/forsale/ad.html?finnkode="
page_num = 1
request = "baryton"
banned_url = ["hjelpesenter:", "twitter:", "bedrift:", "instagram:", "youtube:", "hjemmehos:"]
url = base_url + request + "&page=" + str(page_num)
response = requests.get(url)
csvfile = open('finn_dataset.csv', 'a', encoding='utf-8')
csvwriter = csv.writer(csvfile)
soup = BeautifulSoup(response.content, "html.parser")


def crawl_page(crawler):
    res = requests.get(search_url + crawler)
    soup = BeautifulSoup(res.content, "html.parser")
    for artikkel in soup.find_all("div", {"class": "panel u-mb16"}):
        tittel = artikkel.find("h1", {"class": "u-t2"})
        pris = artikkel.find("span", {"class": "u-t1"})
        now = time.strftime('%d-%m-%Y %H:%M:%S')
        path = soup.find("ul", {"class": "breadcrumbs"})
        for key, link in enumerate(path.find_all('a')):
            if key >= 2:
                print(link.text)

        try:
            print(crawler, tittel.text, pris.text, now, link.text)
            csvwriter.writerow([crawler, tittel.text, pris.text, now, link.text])
        except AttributeError:
            csvwriter.writerow([crawler, tittel.text, now, link.text])


while True:
    url = base_url + request + "&page=" + str(page_num)
    for a in soup.find_all('a', href=True):
        if "/bap/forsale/ad.html?finnkode=" not in a['href']:
            continue
        else:
            urls.append(a['href'])
            crawl_page(a['data-finnkode'])
        # crawl_page_one(a['data-finnkode'])
        print("crawling to" + url)
        next_page_link = soup.find('a', {'rel': 'next'})
