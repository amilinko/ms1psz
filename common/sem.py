from nltk.corpus import wordnet as wn
from lex import lex_sim

# Semantic similarity between two words
def sem_sim(a, b):
    x = wn.synsets(a)
    y = wn.synsets(b)
    if len(x) == 0 or  len(y) == 0:
        return lex_sim(a,b)
    res = x[0].path_similarity(y[0])
    return  res if res is not None else 0

