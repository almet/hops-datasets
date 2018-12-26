import codecs
from urllib.parse import urljoin

from slugify import slugify
from pyquery import PyQuery as pq
import yaml


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def scrap_yakima():
    def __get(e):
        return e.text().split(':')[1].strip()

    def _get_details(url):
        print('.', end='', flush=True)
        try:
            content = pq(url=url)
            details = list(content.find('.hop-composition__value').items())

            return {
                'description': list(content.find('p').items())[10].text().strip(),
                'myrcene': details[4].text(),
                'caryophyllene': details[5].text(),
                'farnesene': details[6].text(),
                'humulene': details[7].text(),
                'geraniol': details[8].text(),
            }
        except:
            return {}

    url = 'https://ychhops.com/varieties'
    content = pq(url=url)
    varieties = {}
    for product in content.find("[itemid='#product']").items():
        card_details = list(product('ul.card__data>li').items())
        variety = dict(
            name=product('a.card__name')[0].text.strip(),
            url=product('a.card__name')[0].get('href'),
            description=product('p.card__description')[0].text,
            region=__get(card_details[0]),
            alpha=__get(card_details[1]),
            beta=__get(card_details[2]),
            cohumulone=__get(card_details[3]),
            total_oils=__get(card_details[4]),
            aroma=__get(card_details[5]),
        )
        variety.update(_get_details(variety['url']))
        varieties.setdefault(slugify(variety['name']), variety)
    return varieties


def scrap_simplehops():
    url = 'http://simplyhops.fr/hops/hop-pellets/'
    countries = ['german', 'american', 'english', 'australian', 'belgian',
                 'french', 'new-zealand', 'czech-republic', 'slovenian']

    varieties = {}
    for country in countries:
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


def clean_value(value):
    return value.replace(' ', '')

def scrap_comptoir():
    def _get_details(url):
        content = pq(url=url)

        def PERCENTAGE(x):
            if '-' in x:
                value = x.replace('-', ' - ')
            else:
                number, _ = x.split('%')
                value = '{0} - {0}%'.format(number.replace(' ', ''))

            if '%' not in value:
                value = '{0}%'.format(value)
            return value


        def QUANTITY(text):
            def _inner(x):
                value = x.replace(text, '')
                if '-' in value:
                    value = value.replace('-', ' - ')
                return value
            return _inner


        labels = {
                'Acides Alpha':             ('alpha', PERCENTAGE),
                'Acides Beta':              ('beta', PERCENTAGE),
                'Coluplone':                ('coluplone', PERCENTAGE),
                'Huiles totales':           ('total_oils', QUANTITY('ml/100g')),
                'Myrcène':                  ('myrcene', PERCENTAGE),
                'Humulène':                 ('humulene', PERCENTAGE),
                'Monoterpène':              ('monoterpene', PERCENTAGE),
                'Sesquiterpène':            ('sesquiterpene', PERCENTAGE),
                'Humulène / Caryophyllène': ('caryophyllene', PERCENTAGE),
                'Linalool':                 ('linalool', QUANTITY('mg/100g')),
                'Farnesène':                ('farmesene', QUANTITY('mg/100g')),
                'Geraniol':                 ('geraniol', QUANTITY('mg/100g')),
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
                data[key] = clean_value(modifier(feature_value))

        print('.', end='', flush=True)
        return data

    url = 'https://www.comptoir-houblon.fr/'
    content = pq(url=url)

    varieties = {}
    for product in content.find('ul .row .buttons-list > li a').items():
        variety = _get_details(product[0].get('href'))
        slug = slugify(variety['name'])
        varieties[slug] = variety
    return varieties


def save_data(data, destination):
    with codecs.open(destination, 'w+') as f:
        f.write(yaml.dump(data, allow_unicode=True, default_flow_style=False))


# save_data(scrap_simplehops(), 'viz/data/barthhaasgroup.yaml')
# save_data(scrap_yakima(), 'viz/data/yakima.yaml')
save_data(scrap_comptoir(), 'viz/data/comptoir.yaml')
