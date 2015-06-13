from math import sqrt
import sys
from lex import lex_sim
from sem import sem_sim

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

# Shallow parsing
def sim_max(w, st, similarity):
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
  
