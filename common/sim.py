from nltk.corpus import wordnet as wn
from math import sqrt
import sys

# Vector functions
def magnitude (vector):
    result = 0
    for v in vector:
       result = result + v**2
    return sqrt(result)

def dotProduct (vector1, vector2):
    if len(vector1) != len(vector2):
        print "Vectors must me the same size!"
        sys.exit(-1)
    result = 0
    for i in range(len(vector1)):
        result = result + vector1[i]*vector2[i]
    return result

# Lexical similarity
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

def lex_sim(s1, s2):
    if type(s1) is not str or type(s2) is not str or len(s1)==0 or len(s2)==0:
        return 0
    return float(lcsubstring_length(s1, s2)**2)/(len(s1)*len(s2))

# Semantical similarity
def sem_sim(a, b):
    x = wn.synsets(a)
    y = wn.synsets(b)
    if len(x) == 0 or  len(y) == 0:
        return lex_sim(a,b)
    res = x[0].path_similarity(y[0])
    return  res if res is not None else 0

# Shallow parsing
def sim_max(w, st, similarity):
    if type(st) is not frozenset:
        print "Parameter st must be a set!"
        sys.exit(-1)

    if similarity == 'lex':
        fun_sim = lex_sim
    elif similarity == 'sem':
        fun_sim = sem_sim
    else:
        print "Wrong similarity!"
        sys.exit(-1)

    sim = []
    for word in st:
        sim.append(fun_sim(w, word))
    return max(sim)

def sim_shallow(st1, st2, similarity):
    if type(st1) is not frozenset or type(st2) is not frozenset:
        print "Parameters must be sets!"
        sys.exit(-1)

    st = st1.union(st2)
    v1 = []
    v2 = []

    for w in st:
        v1.append(sim_max(w, st1, similarity))
        v2.append(sim_max(w, st2, similarity))

    return dotProduct(v1,v2)/(magnitude(v1)*magnitude(v2))

# Deep parsing
def sim_rel (rel1, rel2, similarity):
    return 0

def sim_deep (sr1, sr2, similarity):
    return 0
  
