import os
import inspect
import sys

from xmltodict import parse
from fabricate import *
from common import common
from common.common import POS 

PRJ_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

INPUT = INPUT = sys.argv[1]
if os.path.isfile(INPUT) == False:
	print 'No such file!'
	sys.exit(-1)

INPUT_NAME = os.path.splitext(os.path.basename(INPUT))[0]

INPUT_TEXT_FILE = os.path.join(PRJ_ROOT, 'data/text/' + INPUT_NAME + '.txt')

CORENLP_DIR = os.path.join(PRJ_ROOT, 'stanford-corenlp-full-2015-01-29/')
XML_DIR = os.path.join(PRJ_ROOT, 'data/xml')

CORENLP_EXEC_ARGS = ['-cp', CORENLP_DIR + '*',  '-Xmx3g' , 'edu.stanford.nlp.pipeline.StanfordCoreNLP', 
                        '-annotators',  'tokenize,ssplit,pos,parse', '-file']

###########
# EXTRACT #
###########

LINES = common.read_sentences(INPUT)

#############
# TRANSFORM #
#############

# Create text file
PAIRS= []
TEXT= ''
NUM_PAIRS= len(LINES)

for i in range(1, NUM_PAIRS):
    NEW_PAIR = common.pair(LINES[i], i-1)
    PAIRS.append(NEW_PAIR)
    TEXT = TEXT + NEW_PAIR.pair_string()

with open (INPUT_TEXT_FILE, 'w') as f:
    f.write(TEXT)


# Run CoreNLP
with common.cd(XML_DIR):
    run('java', CORENLP_EXEC_ARGS,INPUT_TEXT_FILE)

# Input dictionary
with open(os.path.join(XML_DIR, INPUT_NAME + '.txt.xml'), 'r') as xmlfile:
    parsed = parse(xmlfile)


########
# LOAD #
########

SENTENCES = parsed['root']['document']['sentences']['sentence']

for i in range(NUM_PAIRS-1):
    TOKENS1 = SENTENCES[2*i]['tokens']['token']
    DEPS1 = SENTENCES[2*i]['dependencies']

    TOKENS2 = SENTENCES[2*i+1]['tokens']['token']
    DEPS2 = SENTENCES[2*i+1]['dependencies']

    PAIRS[i].pos(TOKENS1, TOKENS2)
    PAIRS[i].deps(DEPS1, DEPS2)

