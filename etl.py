import os
import inspect
import sys

from xmltodict import parse
from fabricate import *
from common import common

PRJ_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

TRAIN = os.path.join(PRJ_ROOT, 'data/input/msr_paraphrase_train.txt')
TEST = os.path.join(PRJ_ROOT, 'data/input/msr_paraphrase_test.txt')

TRAIN_TEXT_FILE = os.path.join(PRJ_ROOT, 'data/text/train.txt')
TEST_TEXT_FILE = os.path.join(PRJ_ROOT, 'data/text/test.txt')

CORENLP_DIR = os.path.join(PRJ_ROOT, 'stanford-corenlp-full-2015-01-29/')
XML_DIR = os.path.join(PRJ_ROOT, 'data/xml')

CORENLP_EXEC_ARGS = ['-cp', CORENLP_DIR + '*',  '-Xmx3g' , 'edu.stanford.nlp.pipeline.StanfordCoreNLP', 
                        '-annotators',  'tokenize,ssplit,pos,parse', '-file']

###########
# EXTRACT #
###########

LINES_TRAIN = common.read_sentences(TRAIN)
LINES_TEST = common.read_sentences(TEST)

#############
# TRANSFORM #
#############

# Create train test file
PAIRS_TRAIN = []
TEXT_TRAIN = ''
NUM_PAIRS_TRAIN = len(LINES_TRAIN)

for i in range(1, NUM_PAIRS_TRAIN):
    NEW_PAIR = common.pair(LINES_TRAIN[i], i-1)
    PAIRS_TRAIN.append(NEW_PAIR)
    TEXT_TRAIN = TEXT_TRAIN + NEW_PAIR.pair_string()

with open (TRAIN_TEXT_FILE, 'w') as f:
    f.write(TEXT_TRAIN)

# Create test text file
PAIRS_TEST = []
TEXT_TEST = ''
NUM_PAIRS_TEST = len(LINES_TEST)

for i in range(1, NUM_PAIRS_TEST):
    NEW_PAIR = common.pair(LINES_TEST[i], i-1)
    PAIRS_TEST.append(NEW_PAIR)
    TEXT_TEST = TEXT_TEST + NEW_PAIR.pair_string()

with open (TEST_TEXT_FILE, 'w') as f:
    f.write(TEXT_TEST)

# Run CoreNLP
with common.cd(XML_DIR):
    run('java', CORENLP_EXEC_ARGS,TRAIN_TEXT_FILE)
    run('java', CORENLP_EXEC_ARGS,TEST_TEXT_FILE)

# Train dictionary
with open(os.path.join(XML_DIR,'train.txt.xml'), 'r') as xmlfile:
    parsed_train = parse(xmlfile)

# Test dictionary
with open(os.path.join(XML_DIR,'test.txt.xml'), 'r') as xmlfile:
    parsed_test = parse(xmlfile)


########
# LOAD #
########
