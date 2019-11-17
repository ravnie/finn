from bs4 import BeautifulSoup
import requests

base_url = "https://www.finn.no/bap/forsale/search.html?q="
page_num = "&page=1"
request = "jean paul"
banned_url = ["hjelpesenter:", "twitter:", "bedrift:", "instagram:", "youtube:", "hjemmehos:"]



url = base_url + request + page_num
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

for a in soup.find_all('a', href=True):
    print ("Found the URL:", a['href'])