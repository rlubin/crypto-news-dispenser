import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.coindesk.com"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", class_=re.compile("static-cardstyles__StaticCardWrapper", re.I))

_file = open("scrapped.html", "w+")

for result in results:
  #article title
  print(result.a.div.h2.text)
  _file.write(result.a.div.h2.text + "\n")

  #article link
  print(URL + result.a.attrs["href"])
  _file.write(URL + result.a.attrs["href"] + "\n\n")
  print()

_file.close()