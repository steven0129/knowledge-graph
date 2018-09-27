from heapq import *
from collections import defaultdict
from itertools import combinations
from collections import Counter
import ltp
import numpy as np

DATA_DIR = 'data'
DICT_DIR = 'dict'
S = ltp.Sentence()

with open(f'{DICT_DIR}/sky_dragon_name.txt') as f:
    names = list(map(lambda x: x.rstrip('\n'), f.readlines()))

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t:
                def tolist(path, init):
                    init = [path[0]] + init
                    if(path[1] == ()): 
                        return init
                    return tolist(path[1], init)

                return (cost, tolist(path, []))

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float('inf')

def is_name(word):
    result = False
    for name in names:
        if(word == name):
            result = True

    return result

with open(f'{DATA_DIR}/sky_dragon_abstract_simplified.txt') as f:
    contents = list(filter(lambda x: not x.startswith('['), f.readlines()))
    contents = list(map(lambda x: x.rstrip('\n'), list(contents)))
    wordLists = list(map(lambda x: x.split(' '), contents))
    dependencyLists = list(map(S.parse, wordLists))

with open('relation.csv', 'w') as f:
    for words, dependencies in zip(wordLists, dependencyLists):
        length = len(dependencies) + 1
        edges = []
        
        for tail, (head, relation) in enumerate(dependencies):
            edges.append((head, tail + 1, 1))
            edges.append((tail + 1, head, 1))
        
        filteredNames = list(filter(lambda x: x[1] in names, enumerate(words)))
        if(len(filteredNames) >= 2):
            for (idx1, name1), (idx2, name2) in combinations(filteredNames, 2):
                routes = dijkstra(edges, idx1, idx2)[1]
                routes.pop()
                routes.pop(0)
                relation = list(filter(lambda x: x[0] in routes, enumerate(words)))
                relation = list(map(lambda x: x[1], relation))
                relation = list(filter(lambda x: x != '。' and x !='，' and x != '、' and x != '“' and x != '"', relation))
                f.write(f'{name1},{name2},{"|".join(relation)}\n')