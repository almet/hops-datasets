import codecs




def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


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





# save_data(scrap_simplehops(), 'viz/data/barthhaasgroup.yaml')
save_data(scrap_yakima(), 'viz/data/yakima.yaml')
save_data(scrap_comptoir(), 'viz/data/comptoir.yaml')
