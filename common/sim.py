from math import sqrt
import sys

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
