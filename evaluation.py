import argparse
import logging
import yaml
from pathlib import Path
from tasks import task_mapping
from gensim_loader import VectorLoader
from metrics import metrics
from cli_logger import CLILogger

# logging.basicConfig(level=logging.INFO)


def main(args):
    gensim_loader = VectorLoader(args.embedding_file)
    with open(args.task_config, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    tasks = [*data_loaded]
    for task_name in tasks:
        logging.info((f'Execute task: {task_name}'))
        task_properties = data_loaded[task_name]
        task_class = task_mapping[task_properties['type']]
        source = task_properties['source']
        with Path(source['path']).open(encoding="utf8") as f:
            task = task_class(task_name, f, metrics[task_properties['metric']], gensim_loader, source, True)
            with CLILogger(task):
                print(task())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--task-config',
        type=Path,
        help='Path to the config file',
        required=True
    )
    parser.add_argument(
        "--embedding-file",
        type=Path,
        help="Path to the embedding vector file",
        required=True
    )
    main(parser.parse_args())
