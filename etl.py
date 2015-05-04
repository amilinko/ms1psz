import os
import inspect
import sys
import sh

from common import common

PRJ_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

TRAIN = 'data/input/msr_paraphrase_train.txt'
TEST = 'data/input/msr_paraphrase_test.txt'

TRAIN_TEXT_FILE = 'data/text/train.txt'
TEST_TEXT_FILE = 'data/text/test.txt'

CORENLP_DIR = 'stanford-corenlp-full-2015-01-29/'

CORENLP = 'java -cp "*" -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file input.txt'

# EXTRACT
LINES_TRAIN = common.read_sentences(TRAIN)
LINES_TEST = common.read_sentences(TEST)

# TRANSFORM

PAIRS_TRAIN = []
PAIRS_TEST = []

TEXT_TRAIN = ''
TEXT_TEST = '' 

NUM_PAIRS_TRAIN = len(LINES_TRAIN)
NUM_PAIRS_TEST = len(LINES_TEST)

for i in range(1, NUM_PAIRS_TRAIN):
    NEW_PAIR = common.pair(LINES_TRAIN[i], i-1)
    PAIRS_TRAIN.append(NEW_PAIR)
    TEXT_TRAIN = TEXT_TRAIN + NEW_PAIR.pair_string()

with open (TRAIN_TEXT_FILE, 'w') as f:
    f.write(TEXT_TRAIN)

for i in range(1, NUM_PAIRS_TEST):
    NEW_PAIR = common.pair(LINES_TEST[i], i-1)
    PAIRS_TEST.append(NEW_PAIR)
    TEXT_TEST = TEXT_TEST + NEW_PAIR.pair_string()

with open (TEST_TEXT_FILE, 'w') as f:
    f.write(TEXT_TEST)


# LOAD
