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

# Shallow parsing
def sem_max(w1, st1):
    sim = []
    for word in st:
        sim.append(sem_sim(w, word))
    return max(sim)

def sem_shallow(st1, st2):
    return 0

# Deep parsing
def sem_rel (rel1, rel2):
    return 0

def sem_deep (sr1, sr2):
    return 0

