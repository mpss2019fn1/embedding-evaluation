import requests
from pathlib import Path
from csv import DictWriter

query_directory = Path('wikidata_queries')
query_result_directory = Path('query_results')




def query_wikidata(name, query):
    wikidata_query_endpoint = "https://query.wikidata.org/sparql"
    r = requests.get(wikidata_query_endpoint, params={"format": "json", "query": query})
    with query_result_directory.joinpath(f'{name}.csv').open('w') as result_file:
        csv_writer = DictWriter(result_file, fieldnames=['a', 'b'])
        csv_writer.writeheader()
        for query_result in r.json()['results']['bindings']:
            csv_writer.writerow({'a': query_result['a']['value'], 'b': query_result['b']['value']})


def main():
    for query_file in query_directory.iterdir():
        with query_file.open() as f:
            query = f.read()
        query_wikidata(query_file.stem, query)


if __name__ == '__main__':
    main()