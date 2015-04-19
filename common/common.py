import sys

def read_sentences(input_file):
	"""
	Read all sentences from file and store them into list
	"""	
	with open (input_file) as f:
		lines = f.read().splitlines()
	return lines

class pair (object):
    """
    Pair of sentences 
    """
    def __init__ (self, line):
        self.__data = line.split('\t')

    def similar(self):
        return self.__data[0]

    def id1(self):
        return self.__data[1]

    def id2(self):
        return self.__data[2]

    def string1(self):
        return self.__data[3]

    def string2(self):
        return self.__data[4]


