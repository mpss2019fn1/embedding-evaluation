import re

import requests


class WikidataEntry:

    def __init__(self, wikidata_id):
        self.wikidata_id = wikidata_id
        self.fill_wikipedia_props()
        self.fill_wikipedia_page_id()

    def fill_wikipedia_props(self):
        request_url = 'https://www.wikidata.org/w/api.php?action=wbgetentities'
        r = requests.get(request_url,
                         params={'format': 'json', 'props': 'sitelinks/urls', 'ids': f'Q{self.wikidata_id}',
                                 'sitefilter': 'enwiki'})
        wikipedia_entry = r.json()['entities'][f'Q{self.wikidata_id}']['sitelinks']['enwiki']
        self.wikipedia_url = wikipedia_entry['url']
        self.title = wikipedia_entry['title']

    def fill_wikipedia_page_id(self):
        request_url = f'https://en.wikipedia.org/w/api.php'
        r = requests.get(request_url, params={'action': 'query', 'format': 'json', 'titles': self.title})
        self.wikipedia_page_id = int(next(iter(r.json()['query']['pages'].keys())))

    @property
    def identifier(self):
        clean_title_regex = re.compile(r'^(?P<title>[^(]+?)(\s\((?P<role>.+?)\))?$', re.IGNORECASE)
        match = clean_title_regex.search(self.title)
        title_part = match.group("title").replace(' ', '_')
        return f'{title_part}_{self.wikipedia_page_id}'