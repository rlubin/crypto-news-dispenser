import requests
from bs4 import BeautifulSoup
import re


def scrape():
    '''
    return [(article title, article link), ...]
    '''
    URL = "https://www.coindesk.com"
    page = requests.get(URL)
    stories = []  # [(article title, article link), ...]

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all("div", class_=re.compile(
        "static-cardstyles__StaticCardWrapper", re.I))

    for result in results:
        title = result.a.div.h2.text
        link = URL + result.a.attrs["href"]
        stories.append((title, link))

    return stories
