
import requests
import logging
from bs4 import BeautifulSoup

class ArrivaScraper:

    BASE_URL = 'https://www.ariva.de/'

    def __init__(self):
        self.request_session = requests.Session()
        self.request_session.headers = {'User-Agent': 'Ariva Scraper 0.1'}

    def _find_stock_url(self, searchparameter):
        ariva_urls = self.request_session.get('https://www.ariva.de/search/livesearch.m', params={'searchname':searchparameter})
        soup = BeautifulSoup(ariva_urls.text, 'html.parser')
        all_links = soup.find_all(class_='liveSearchLinkText')
        if len(all_links) == 0:
            logging.error('No stock url has been found!')
            return None
        elif len(all_links) > 1:
            logging.info('More than one stock url has been found! Returning the first one!')

        return requests.compat.urljoin(ArrivaScraper.BASE_URL, all_links[0].a['href'])

if __name__ == '__main__':
    scraper = ArrivaScraper()
    scraper._find_stock_url('APPLE')
