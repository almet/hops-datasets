import pdfquery
from pdfquery.cache import FileCache
from slugify import slugify

import os.path

from hopsdb.scrappers.base import Scrapper


class YakimaHopsScrapper(Scrapper):

    def __init__(self, input_dir):
        self.input_dir = input_dir

    def scrap(self):
        pdf_file = os.path.join(self.input_dir, 'ychhops.pdf')
        pdf = pdfquery.PDFQuery(pdf_file, parse_tree_cacher=FileCache(".tmp"))
        pdf.load()
        # Reorganize data to be a dict.
        varieties = {}
        for page in range(1, 147):
            data = self.get_data(pdf, page)
            varieties[slugify(data['name'])] = data
        return varieties


    def get_data(self, pdf, page_number):
        extracted_data = pdf.extract([
            #('description', 'LTTextBoxHorizontal:in_bbox("36.0, 487.921, 330.223, 529.6")', lambda match: ''.join([c.text for c in match.getchildren()])),
            ('with_formatter', 'text'),
            ('name', 'LTTextLineHorizontal:in_bbox("36.0, 552.832, 350, 591.84")'),
            ('codename', 'LTTextLineHorizontal:in_bbox("36.0, 543.83, 100, 555.26")'),
            ('country', 'LTTextLineHorizontal:in_bbox("36.0, 443.417, 100.589, 477.289")', lambda match: match.text().replace('COUNTRY ', '')),
            ('alpha', 'LTTextLineHorizontal:in_bbox("255.343, 291.296, 370, 311.616")', lambda match: ' - '.join(match.text().split(' '))),
            ('cohumulone', 'LTTextLineHorizontal:in_bbox("36.0, 311.981, 163.75, 324.171")', lambda match: match.text().replace('ALPHA ACIDS', '').replace('CO-HUMULONE', '').replace('(', '').replace(')', '').strip()),
            ('beta', 'LTTextLineHorizontal:in_bbox("255.343, 242.755, 370, 263.075")', lambda match: ' - '.join(match.text().split(' '))),
            ('total_oils', 'LTTextLineHorizontal:in_bbox("255.343, 194.238, 370, 214.558")', lambda match: ' - '.join(match.text().replace('mL/100g', '').split(' '))),
            ('bpinene', 'LTTextLineHorizontal:in_bbox("115, 135.885, 210, 146.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('mircene', 'LTTextLineHorizontal:in_bbox("115, 125.885, 210, 136.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('linalool', 'LTTextLineHorizontal:in_bbox("115, 115.885, 210, 126.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('caryophyllene', 'LTTextLineHorizontal:in_bbox("115, 105.885, 210, 116.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('farnesene', 'LTTextLineHorizontal:in_bbox("115, 95.885, 210, 106.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('humulene', 'LTTextLineHorizontal:in_bbox("115, 85.885, 210, 96.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('geraniol', 'LTTextLineHorizontal:in_bbox("115, 75.885, 210, 86.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('selinene', 'LTTextLineHorizontal:in_bbox("115.927, 65.885, 210, 76.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),
            ('other_oils', 'LTTextLineHorizontal:in_bbox("115, 55.885, 210, 66.533")', lambda match: match.text().replace(' OF TOTAL OIL', '')),

        ], pdf.pq('LTPage[page_index="{0}"]'.format(page_number)))

        return extracted_data
