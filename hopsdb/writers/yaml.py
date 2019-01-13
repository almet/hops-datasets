import os.path
import codecs

import yaml


class YAMLWriter(object):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def write(self, data):
        output_filename = os.path.join(self.output_dir, 'data.yaml')
        with codecs.open(output_filename, 'w+') as f:
            f.write(yaml.dump(data, allow_unicode=True, default_flow_style=False))
