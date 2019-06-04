import argparse


def main(args):
    from gensim.test.utils import datapath, get_tmpfile
    from gensim.models import KeyedVectors, Word2Vec
    from gensim.scripts.glove2word2vec import glove2word2vec

    glove_file = datapath(args.input_file)
    tmp_file = get_tmpfile("test_word2vec.txt")

    _ = glove2word2vec(glove_file, tmp_file)

    vectors = KeyedVectors.load_word2vec_format(tmp_file, binary=True)

    model = Word2Vec()
    model.wv = vectors

    model.save(args.output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file',
        type=str,
        help='Path to the input file in word2vec format',
        default='model/fasttext/cc.en.300.bin',
        required=False,
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Path to the output file",
        default="output.model",
        required=False
    )
    main(parser.parse_args())
