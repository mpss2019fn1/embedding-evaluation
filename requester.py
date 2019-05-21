import argparse
from pathlib import Path

from sparql_endpoint import SparqlEndpoint


def main(args):
    for query_file in args.query_directory.iterdir():
        with query_file.open() as f:
            query = f.read()
        wikidata_query_endpoint = SparqlEndpoint("https://query.wikidata.org/sparql")
        with args.query_result_directory.joinpath(f'{query_file.stem}.csv').open('w+') as result_file:
            wikidata_query_endpoint.write_result_to_csv(result_file, query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query-directory",
        type=Path,
        help="Path to the query directory",
    )
    parser.add_argument(
        "--query-result-directory",
        type=Path,
        help="Path to the query result directory",
    )
    main(parser.parse_args())
