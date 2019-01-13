from .barthaas import BarthaasScrapper
from .comptoiragricole import ComptoirAgricoleScrapper
from .ychops import YakimaHopsScrapper


SCRAPPERS = {
    'barthaas': BarthaasScrapper,
    'comtoiragricole': ComptoirAgricoleScrapper,
    'yakimahops': YakimaHopsScrapper,
}
