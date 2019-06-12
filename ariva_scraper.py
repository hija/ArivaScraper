
import requests
import logging
from bs4 import BeautifulSoup

class ArrivaScraper:

    BASE_URL = 'https://www.ariva.de/'

    def __init__(self):
        self.request_session = requests.Session()
        self.request_session.headers = {'User-Agent': 'Ariva Scraper 0.1'}

    def scrape(self, searchparameter):
        #stock_url = self._find_stock_url(searchparameter)
        stock_url = 'https://www.ariva.de/microsoft-aktie'

        scraped_content = {'price': None}

        ## Get Basic Information
        basic_data_src = self.request_session.get(stock_url)
        soup = BeautifulSoup(basic_data_src.text, 'html.parser')

        print('{0} {1}'.format(*ArrivaScraper._extract_price(soup)))


    @staticmethod
    def _extract_price(soupobj):
        price_obj = soupobj.find('span', attrs={'itemprop': 'price'})
        price = float(price_obj['content'].split('.')[0])/100
        currency_obj = soupobj.find('span', attrs={'itemprop': 'pricecurrency'})
        currency = currency_obj['content']
        return (price, currency)

    @staticmethod
    def _extract_wkn_isin(soupobj):
        description_obj = soupobj.find('meta', attrs={'name': 'description'})
        content_desc = description_obj['content']
        wkn = content_desc.split('WKN')[1].split('|')[0].strip()
        isin = content_desc.split('ISIN')[1].split('|')[0].strip()
        return (wkn, isin)

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
    scraper.scrape('APPLE')
