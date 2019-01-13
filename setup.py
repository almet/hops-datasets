# -*- coding: utf-8 -*-
import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding='utf-8') as f:
        content = f.read()
    return content


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    with open(filename) as lines:
        lineiter = (line.strip() for line in lines)
        return [line for line in lineiter if line and not line.startswith("#")]


README = read_file('README.md')
CHANGELOG = read_file('CHANGELOG.md')

ENTRY_POINTS = {
    'console_scripts': [
        'hopsdb = hopsdb:main'
    ],
}


setup(name='hopsdb',
      version='0.1',
      description='A tool to generate hops dataset from various sources.',
      long_description="{}\n\n{}".format(README.encode('utf-8'), CHANGELOG.encode('utf-8')),
      license='Custom BSD Beerware',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: Implementation :: CPython",
          "Topic :: Internet :: WWW/HTTP",
      ],
      keywords="hops dataset scrapping",
      author='Alexis Métaireau & contributors',
      author_email='alexis@notmyidea.org',
      url='https://github.com/almet/hops-dataset',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=parse_requirements('requirements.txt'),
      entry_points=ENTRY_POINTS)
