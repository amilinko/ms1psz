import sys

sys.path.append('corenlp-python')

from common import common
from corenlp import StanfordCoreNLP, batch_parse

TRAIN = 'data/msr_paraphrase_train.txt'
TEST = 'data/msr_paraphrase_test.txt'

CORENLP_DIR = 'corenlp-python/stanford-corenlp-full-2015-01-29/'

corenlp = StanfordCoreNLP(CORENLP_DIR)

# EXTRACT
LINES = common.read_sentences(TRAIN)

PAIRS = []

for i in range(1,len(LINES)):
    NEW_PAIR = common.pair(LINES[i])
    PAIRS.append(NEW_PAIR)
    
# TRANSFORM

# LOAD
