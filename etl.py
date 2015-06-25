import os
import inspect
import sys
import arff

from xmltodict import parse
from fabricate import *
from common import common, sim

PRJ_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

INPUT = sys.argv[1]
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

RELATION = 'Short sentence similarity'
ATTRIBUTES = []
DATA = []

# Listing attributes and setting data

ATTRIBUTES.append(('similar', ['yes', 'no']))

for i in range(len(PAIRS)):

    if PAIRS[i]['similar'] == '1':
        DATA.append(['yes'])
    else:
        DATA.append(['no'])

# Shallow parsing

for pos in common.POS:
    ATTRIBUTES.append(("diff_Tag_" + pos, 'NUMERIC'))
    for i in range(len(PAIRS)):
        DATA[i].append(common.diff(PAIRS[i][pos][0], PAIRS[i][pos][1]))

for noun in common.NOUNS:
    ATTRIBUTES.append(("semSim_Tag_" + noun, 'NUMERIC'))
    for i in range(len(PAIRS)):
        DATA[i].append(sim.sim_shallow(frozenset(PAIRS[i][noun][0]), frozenset(PAIRS[i][noun][1]), 'sem'))

for verb in common.VERBS:
    ATTRIBUTES.append(("semSim_Tag_" + verb, 'NUMERIC'))
    for i in range(len(PAIRS)):
        DATA[i].append(sim.sim_shallow(frozenset(PAIRS[i][verb][0]), frozenset(PAIRS[i][verb][1]), 'sem'))

for pos in common.POS:
    ATTRIBUTES.append(("lexSim_Tag_" + pos, 'NUMERIC'))
    for i in range(len(PAIRS)):
        DATA[i].append(sim.sim_shallow(frozenset(PAIRS[i][pos][0]), frozenset(PAIRS[i][pos][1]), 'lex'))

ATTRIBUTES.append(('diffNouns', 'NUMERIC'))
ATTRIBUTES.append(('semSimNouns', 'NUMERIC'))
ATTRIBUTES.append(('lexSimNouns', 'NUMERIC'))

ATTRIBUTES.append(('diffVerbs', 'NUMERIC'))
ATTRIBUTES.append(('semSimVerbs', 'NUMERIC'))
ATTRIBUTES.append(('lexSimVerbs', 'NUMERIC'))

for i in range(len(PAIRS)):
    nouns0 = []
    nouns1 = []

    verbs0 = []
    verbs1 = []

    for n in common.NOUNS:
        nouns0 = nouns0 + PAIRS[i][n][0]
        nouns1 = nouns1 + PAIRS[i][n][1]

    for v in common.VERBS:
        verbs0 = verbs0 + PAIRS[i][v][0]
        verbs1 = verbs1 + PAIRS[i][v][1]

    DATA[i].append(common.diff(nouns0, nouns1))
    DATA[i].append(sim.sim_shallow(frozenset(nouns0), frozenset(nouns1), 'sem'))
    DATA[i].append(sim.sim_shallow(frozenset(nouns0), frozenset(nouns1), 'lex'))

    DATA[i].append(common.diff(verbs0, verbs1))
    DATA[i].append(sim.sim_shallow(frozenset(verbs0), frozenset(verbs1), 'sem'))
    DATA[i].append(sim.sim_shallow(frozenset(verbs0), frozenset(verbs1), 'lex'))

# Deep parsing

for dep in common.DEPS:
    ATTRIBUTES.append(("diff_Dep_" + dep, 'NUMERIC'))
    ATTRIBUTES.append(("semSim_Dep_" + dep, 'NUMERIC'))
    ATTRIBUTES.append(("lexSim_Dep_" + dep, 'NUMERIC'))

    for i in range(len(PAIRS)):
        DATA[i].append(common.diff(PAIRS[i][dep][0], PAIRS[i][dep][1]))
        DATA[i].append(sim.sim_deep(frozenset(PAIRS[i][dep][0]), frozenset(PAIRS[i][dep][1]), 'sem'))
        DATA[i].append(sim.sim_deep(frozenset(PAIRS[i][dep][0]), frozenset(PAIRS[i][dep][1]), 'lex'))

# General attributes 

ATTRIBUTES.append(("diff_All", 'NUMERIC'))
ATTRIBUTES.append(("overallLexsim", 'NUMERIC'))

for i in range(len(PAIRS)):
    DATA[i].append(common.diff(PAIRS[i]['string1'].split(), PAIRS[i]['string2'].split()))
    DATA[i].append(sim.sim_shallow(frozenset(PAIRS[i]['string1'].split()), frozenset(PAIRS[i]['string2'].split()), 'lex'))

# Write to arff file

arff_obj = {
    'relation':'Short sentence similarity!',
    'attributes': ATTRIBUTES,
    'data': DATA,
}

print arff.dumps(arff_obj)
