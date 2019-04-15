import requests
import argparse
from pathlib import Path
from csv import DictWriter


def query_wikidata(args, name, query):
    wikidata_query_endpoint = "https://query.wikidata.org/sparql"
    r = requests.get(wikidata_query_endpoint, params={"format": "json", "query": query})
    with args.query_result_directory.joinpath(f'{name}.csv').open('w') as result_file:
        csv_writer = DictWriter(result_file, fieldnames=['a', 'b'])
        csv_writer.writeheader()
        for query_result in r.json()['results']['bindings']:
            csv_writer.writerow({'a': query_result['a']['value'], 'b': query_result['b']['value']})


def main(args):
    for query_file in args.query_directory.iterdir():
        with query_file.open() as f:
            query = f.read()
        query_wikidata(args, query_file.stem, query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-query_directory",
        type=Path,
        help="Path to the query directory",
        default=Path(__file__).absolute().parent / "wikidata_queries",
    )
    parser.add_argument(
        "-query_result_directory",
        type=Path,
        help="Path to the query result directory",
        default=Path(__file__).absolute().parent / "query_results",
    )
    args = parser.parse_args()
    main(args)

