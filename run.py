import sys

sys.path.append('corenlp-python')

from common import common
from corenlp import StanfordCoreNLP

TRAIN = 'data/msr_paraphrase_train.txt'
TEST = 'data/msr_paraphrase_test.txt'

CORENLP_DIR = 'corenlp-python/stanford-corenlp-full-2015-01-29/'

