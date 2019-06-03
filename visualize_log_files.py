from visualization import Visualizer
from pathlib import Path

import argparse


def main(args):
    for logging_sub_directory in args.logging_directory.iterdir():
        Visualizer.from_logging_directory(logging_sub_directory).create_visualizations()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--logging-directory',
        type=Path,
        help='Path to the logging directory',
        default='logging',
        required=False,
    )
    main(parser.parse_args())
