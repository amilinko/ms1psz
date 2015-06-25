import os
import contextlib
import sys
import re

@contextlib.contextmanager
def cd(newPath):
    """Python snippet to CD into a directory"""
    savedPath = os.getcwd()
    os.chdir(newPath)
    yield
    os.chdir(savedPath)


POS = ['CC', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP',
       'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WDT', 'WRB']

DEPS = ['auxpass', 'cop', 'conj', 'cc', 'nsubj', 'csubj', 'dobj', 'iobj', 'pobj', 'attr', 'ccomp', 'xcomp', 'mark', 'rel',
		'acomp', 'agent', 'ref', 'expl', 'advcl', 'purpcl', 'tmod', 'rcmod', 'amod', 'infmod', 'partmod', 'num',
		'number', 'appos', 'advmod', 'neg', 'poss', 'possessive', 'prt', 'det', 'prep', 'xsubj']

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] 

def read_sentences(input_file):
	"""
	Read all sentences from file and store them into list
	"""	
	with open (input_file) as f:
		lines = f.read().splitlines()
	return lines

def prepare_string(string):
    """
    Eliminates special characters from a string
    """
    return re.sub(r'[^\w|\s|\'|\-]', '', string) 
 
class pair (object):
    """
    Pair of sentences 
    """
    def __init__ (self, line, num):
        self.__data = {}
        self.__data_list = line.split('\t')

        self.__data['pair_id'] = num
        self.__data['similar'] = self.__data_list[0]
        self.__data['id1'] = self.__data_list[1]
        self.__data['id2'] = self.__data_list[2]
        self.__data['string1'] = prepare_string(self.__data_list[3]) + '.'
        self.__data['string2'] = prepare_string(self.__data_list[4]) + '.'
        
        for pos in POS:
            self.__data[pos] = []
            self.__data[pos].append([])
            self.__data[pos].append([])

        for dep in DEPS:
            self.__data[dep] = []
            self.__data[dep].append([])
            self.__data[dep].append([])

    def __getitem__(self, key):
        return self.__data[key]

    def pair_string(self):
        return self.__data['string1'] + '\n' + self.__data['string2'] + '\n'

    def pos (self, tokens1, tokens2):
        for t in tokens1:
            if t['POS'] in POS:
                self.__data[t['POS']][0].append(t['word'].encode('utf-8'))
        
        for t in tokens2:
            if t['POS'] in POS:
                self.__data[t['POS']][1].append(t['word'].encode('utf-8'))

    def deps (self, deps1, deps2):
        for ds in deps1:
            for d in ds['dep']:
                if d['@type'] in DEPS:
                    self.__data[d['@type']][0].append((d['governor']['#text'].encode('utf-8'), d['dependent']['#text'].encode('utf-8')))

        for ds in deps2:
            for d in ds['dep']:
                if d['@type'] in DEPS:
                    self.__data[d['@type']][1].append((d['governor']['#text'].encode('utf-8'), d['dependent']['#text'].encode('utf-8')))


def diff(st1, st2):
    """
    Absolute length difference of two lists
    """
    return abs(len(st1)-len(st2))


