import sys
import re

POS = ['CC', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP',
       'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WDT', 'WRB']

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

        
    def __getitem__(self, key):
        return self.__data[key]

    def pair_string(self):
        return self.__data['string1'] + '\n' + self.__data['string2'] + '\n'


