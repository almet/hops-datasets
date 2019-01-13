from urllib.parse import urljoin

from slugify import slugify
from pyquery import PyQuery as pq

from hopsdb.scrappers.base import Scrapper


class BarthaasScrapper(Scrapper):
    def scrap(self):
        url = 'http://simplyhops.fr/hops/hop-pellets/'
        countries = ['german', 'american', 'english', 'australian', 'belgian',
                     'french', 'new-zealand', 'czech-republic', 'slovenian']

        varieties = {}
        for country in countries:
            self._display_progress()
            content = pq(url=urljoin(url, country))
            for product in content.find('#products-list>li').items():
                details = list(product('.attribute-group').items())[1]('.attr-value')
                name = product('.product-name>a').text().split('T90')[0].strip()
                varieties.setdefault(slugify(name), dict(
                    name=name,
                    description=product('.product-description').text().strip(),
                    alpha=details[0].text,
                    beta=details[1].text,
                    total_oils=details[2].text,
                    cohumulone=details[3].text,
                    region=country,
                    myrcene=details[4].text,
                    caryophyllene=details[5].text,
                    farnesene=details[6].text,
                ))
        return varieties
