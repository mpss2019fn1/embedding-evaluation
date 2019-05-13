import argparse
import logging
import yaml
from pathlib import Path
from tasks import AnalogyTask, NeighborhoodTask, SimilarityTask
from gensim_loader import GensimLoader
from metrics import metrics
from cli_logger import CLILogger
from wikipedia_props_fetcher import WikipediaPropsFetcher


task_mapping = {'analogy': AnalogyTask, 'neighborhood': NeighborhoodTask, 'similarity': SimilarityTask}
source_type = {'csv': WikipediaPropsFetcher}

# logging.basicConfig(level=logging.INFO)


def main(args):
    gensim_loader = GensimLoader(args.embedding_file)
    with open(args.config_file, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    tasks = [*data_loaded]
    for task_name in tasks:
        logging.info((f'Execute task: {task_name}'))
        task_properties = data_loaded[task_name]
        task_class = task_mapping[task_properties['task_type']]
        source = task_properties['source']
        props_fetcher = source_type[source['source_type']]
        gensim_loader.props_fetcher = props_fetcher(source['props_fetcher'], source['props_delimiter'])
        with Path(source['filename']).open(encoding="utf8") as f:
            task = task_class(task_name, f, metrics[task_properties['metric']], gensim_loader, source, True)
            with CLILogger(task):
                print(task())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config-file',
        type=Path,
        help='Path to the config file',
        default="task_collection/similarity_task.yaml",
        required=False,
    )
    parser.add_argument(
        "--embedding-file",
        type=str,
        help="Path to the embedding file directory",
        default="model/doc2vec.binary.model",
    )
    main(parser.parse_args())
