import argparse
from pathlib import Path


# logging.basicConfig(level=logging.INFO)
from test_collection import TestCollection


def main(args):
    """
    args contains the path to the task configuration as well as embedding file.
    :param args:
    :return:
    """
    test_collection = TestCollection.from_test_definition(args.test_set_config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--test-set-config',
        type=Path,
        help='Path to the configuration file of the test set',
        required=True
    )
    # parser.add_argument(
    #     "--embedding-file",
    #     type=Path,
    #     help="Path to the embedding vector file",
    #     required=True
    # )
    #
    # parser.add_argument(
    #     "--mapping-file",
    #     type=Path,
    #     help="Path to the file for mapping embedded entities to knowledge base entities",
    #     required=True
    # )
    main(parser.parse_args())
