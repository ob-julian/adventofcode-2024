import os
import re
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from numba import njit

def read_file(file):
    file_path = os.path.join(os.path.dirname(__file__), file)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def solve2(data):
    lines = data.split('\n')
    towels = [towel.strip() for towel in lines[0].split(', ')]
    count = 0
    # aprocah: convert the problem to a graph that if followed creates a valid pattern. Then search all possible paths for start to finish
    for i in range(2, len(lines)):
        pattern = lines[i].strip()
        alength = len(pattern) + 1 # every letter is a edge, so we need one more node
        # adjazenzmatrix
        accumulator = [[] for _ in range(alength - 1)]
        node_id = 2
        G = nx.DiGraph()
        G.add_node(0) # start
        G.add_node(1) # end
        for towel in towels:
            for match in re.finditer(re.escape(towel), pattern):
                start = match.start()
                end = match.end()
                G.add_node(node_id)
                accumulator[start].append((node_id, end))
                node_id += 1
        for start in accumulator[0]:
            start_id, _ = start
            G.add_edge(0, start_id)
        for end_array in accumulator:
            for end_tupple in end_array:
                end_id, end = end_tupple
                if end >= alength - 1:
                    G.add_edge(end_id, 1)
                else:
                    for start in accumulator[end]:
                        start_id, _ = start
                        G.add_edge(end_id, start_id)
        adj_matrix = np.array(nx.adjacency_matrix(G).todense(), dtype=np.float64)
        count += count_paths(adj_matrix, alength)
    return count

@njit
def count_paths(adj_matrix, deepth):
    count = 0
    cum_matrix = adj_matrix
    for _ in range(deepth):
        count += cum_matrix[0, 1]
        cum_matrix = cum_matrix.dot(adj_matrix)
    return count

#DATA = read_file('test.txt')
DATA = read_file('input.txt')

print("Advent of Code: 19th")
print("Part 2:", solve2(DATA))
# using numba 
# testcase: 1.2s -> 2.2s
# input   : 27 s -> 3.7s
# anwser still wrong though =(
