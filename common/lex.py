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
