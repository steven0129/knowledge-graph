from heapq import *
from collections import defaultdict
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

dependencyLists = [dependencyLists[18]]
for dependencies in dependencyLists:
    length = len(dependencies) + 1
    edges = []
    for tail, (head, relation) in enumerate(dependencies):
        edges.append((str(head), str(tail + 1), 1))
        edges.append((str(tail + 1), str(head), 1))
    
    print(dijkstra(edges, '1', '5'))
    print(dijkstra(edges, '0', '2'))