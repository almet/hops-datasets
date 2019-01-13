class Scrapper(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def _clean_spaces(self, input):
        return input.replace(' ', '')

    def _display_progress(self):
        print('.', end='', flush=True)
