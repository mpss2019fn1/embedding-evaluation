import re
from csv import DictWriter

import requests


def query_values(query):
    value_regex = '(?<=SELECT).*(?=WHERE)'
    match = re.search(value_regex, query)
    if not match:
        raise QueryMalformedError(f'The query "{query}" has no select values.')
    value_string = match.group(0)
    return [value[1:] for value in value_string.split()]


class QueryMalformedError(Exception):
    pass


class SparqlEndpoint:

    def __init__(self, remote_url):
        self.remote_url = remote_url

    def query(self, query):
        request = requests.get(self.remote_url, params={"format": "json", "query": query})
        for query_result in request.json()['results']['bindings']:
            yield {value: query_result[value]['value'] for value in query_values(query)}

    def write_result_to_csv(self, csv_file, query):
        csv_writer = DictWriter(csv_file, fieldnames=query_values(query))
        csv_writer.writeheader()
        for result in self.query(query):
            csv_writer.writerow(result)
