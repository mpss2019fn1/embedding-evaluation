import argparse
import logging
from configparser import ConfigParser
from pathlib import Path

from tasks import AnalogyTask, NeighborhoodTask
from gensim_loader import GensimLoader
from metrics import metrics

task_mapping = {'analogy': AnalogyTask, 'neighborhood': NeighborhoodTask}

logging.basicConfig(level=logging.INFO)


def main(args):
    config = ConfigParser()
    gensim_loader = GensimLoader(args.embedding_file)
    config.read(args.config_file)
    tasks = [section for section in config.sections() if section.startswith('Task.')]
    for task_name in tasks:
        logging.info(f'Execute task: {task_name}')
        task_properties = dict(config.items(task_name))
        task_class = task_mapping[task_properties['task_type']]
        with Path(task_properties['path']).open() as f:
            task = task_class(f, metrics[task_properties['metric']], gensim_loader)
            print(task())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config-file',
        type=Path,
        help='Path to the config file',
        required=True
    )
    parser.add_argument(
        "--embedding-file",
        type=str,
        help="Path to the embedding file directory",
        default="doc2vec.binary.model",
    )
    args = parser.parse_args()
    main(args)
