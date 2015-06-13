import sys
from sim import *

def lcsubstring_length(a, b):
    table = {}
    l = 0
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            if ca == cb:
                table[i, j] = table.get((i - 1, j - 1), 0) + 1
                if table[i, j] > l:
                    l = table[i, j]
    return l

# Lexical similarity between two words
def lex_sim(s1, s2):
    if type(s1) is not str or type(s2) is not str or len(s1)==0 or len(s2)==0:
        return 0
    return float(lcsubstring_length(s1, s2)**2)/(len(s1)*len(s2))

# Shallow parsing
def lex_max(w, st):
    sim = []
    for word in st:
        sim.append(lex_sim(w, word))
    return max(sim)

def lex_shallow(st1, st2):
    if type(st1) is not frozenset or type(st2) is not frozenset:
        print "Parameters must be sets!"
        sys.exit(-1)

    st = st1.union(st2)
    v1 = []
    v2 = []

    for w in st:
        v1.append(lex_max(w, st1))
        v2.append(lex_max(w, st2))

    return dotProduct(v1,v2)/(magnitude(v1)*magnitude(v2))

# Deep parsing
def lex_rel (rel1, rel2):
    return 0

def lex_deep (sr1, sr2):
    return 0
