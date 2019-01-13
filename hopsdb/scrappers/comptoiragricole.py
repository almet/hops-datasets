from urllib.parse import urljoin

from slugify import slugify
from pyquery import PyQuery as pq


from hopsdb.scrappers.base import Scrapper

# Utilities

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# Create some formatters for the data, which will ensure a consistent output.

def format_percentage(x):
    """Format text as "min-max%" value."""
    if '-' in x:
        value = x.replace('-', ' - ')
    else:
        number, _ = x.split('%')
        value = '{0} - {0}%'.format(number.replace(' ', ''))

    if '%' not in value:
        value = '{0}%'.format(value)
    return value


def format_quantity(text):
    """Format the text by removing the passed values"""
    def _inner(x):
        value = x.replace(text, '')
        if '-' in value:
            value = value.replace('-', ' - ')
        return value
    return _inner


class ComptoirAgricoleScrapper(Scrapper):

    def _get_details(self, url):
        """Get the details from a given URL"""
        content = pq(url=url)

        # What should we do when we encounter the following labels?
        # Input text : ('output-name', formatter_function).
        labels = {
                'Acides Alpha':             ('alpha', format_percentage),
                'Acides Beta':              ('beta', format_percentage),
                'Coluplone':                ('coluplone', format_percentage),
                'Huiles totales':           ('total_oils', format_quantity('ml/100g')),
                'Myrcène':                  ('myrcene', format_percentage),
                'Humulène':                 ('humulene', format_percentage),
                'Monoterpène':              ('monoterpene', format_percentage),
                'Sesquiterpène':            ('sesquiterpene', format_percentage),
                'Humulène / Caryophyllène': ('caryophyllene', format_percentage),
                'Linalool':                 ('linalool', format_quantity('mg/100g')),
                'Farnesène':                ('farmesene', format_quantity('mg/100g')),
                'Geraniol':                 ('geraniol', format_quantity('mg/100g')),
        }

        data = {
                'name': content('h1')[0].text,
                'description': content('.description').text().strip()
        }

        # Group every feature with its label.
        features = chunker(list(map(lambda x: x.text, content('div.features').find('td'))), 2)
        for feature_name, feature_value in features:
            if feature_name in labels.keys():
                # Iterate on it and populate the dataset accordingly to the labels.
                key, modifier = labels[feature_name]
                data[key] = self._clean_spaces(modifier(feature_value))

        self._display_progress()
        return data

    def scrap(self):
        url = 'https://www.comptoir-houblon.fr/'
        content = pq(url=url)

        varieties = {}
        for product in content.find('ul .row .buttons-list > li a').items():
            variety = self._get_details(product[0].get('href'))
            slug = slugify(variety['name'])
            varieties[slug] = variety
        return varieties
