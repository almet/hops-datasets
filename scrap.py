import codecs
from urllib.parse import urljoin

from slugify import slugify
from pyquery import PyQuery as pq
import yaml


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
                myrcene=details[4].text,
                caryophyllene=details[5].text,
                farnesene=details[6].text,
            ))
    return varieties


# with codecs.open('data/barthhaasgroup.yaml', 'w+') as f:
#     f.write(yaml.dump(scrap_simplehops(), allow_unicode=True, default_flow_style=False))


with codecs.open('viz/data/yakima.yaml', 'w+') as f:
    f.write(yaml.dump(scrap_yakima(), allow_unicode=True, default_flow_style=False))
