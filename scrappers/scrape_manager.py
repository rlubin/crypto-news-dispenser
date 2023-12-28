import scrappers.coindesk as coindesk

web_scrappers = [coindesk]

def scrape_all():
  '''
  return [(article title, article link), ...]
  '''
  stories = []

  for web_scrapper in  web_scrappers:
    stories = stories + web_scrapper.scrape()

  return stories