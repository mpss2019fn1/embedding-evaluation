import argparse
import logging
import yaml
from pathlib import Path
from tasks import AnalogyTask, NeighborhoodTask
from gensim_loader import GensimLoader
from metrics import metrics


task_mapping = {'analogy': AnalogyTask, 'neighborhood': NeighborhoodTask}

logging.basicConfig(level=logging.INFO)


def main(args):
    gensim_loader = GensimLoader(args.embedding_file)
    with open(args.config_file, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    tasks = [*data_loaded]
    for task_name in tasks:
        logging.info((f'Execute task: {task_name}'))
        task_properties = data_loaded[task_name]
        task_class = task_mapping[task_properties['type']]
        with Path(task_properties['filename']).open(encoding="utf8") as f:
            task = task_class(f, metrics[task_properties['metric']], gensim_loader)
            print(task())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config-file',
        type=Path,
        help='Path to the config file',
        default="config.yaml",
        required=False,
    )
    parser.add_argument(
        "--embedding-file",
        type=str,
        help="Path to the embedding file directory",
        default="doc2vec.binary.model",
    )
    main(parser.parse_args())
