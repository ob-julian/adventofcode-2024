import os
import networkx as nx

# pylint: disable=missing-function-docstring

def read_file(file):
    file_path = os.path.join(os.path.dirname(__file__), file)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_data(data):
    return [line.split("-") for line in data.split("\n")]

def generate_graph(data):
    graph = nx.Graph()
    for line in data:
        node1, node2 = line
        graph.add_edge(node1, node2)
    return graph

def find_cliques_of_size(graph, size):
    # assumes nx finds cliques in descending order of size
    cliques = []
    for clique in nx.enumerate_all_cliques(graph): # thx ai for this function name
        if len(clique) == size:
            cliques.append(clique)
        elif len(clique) > size:
            break
    return cliques

def solve1(graph):
    # find cliques of size 3
    cliques_of_size_3 = find_cliques_of_size(graph, 3)
    adder = 0
    for clique in cliques_of_size_3:
        if clique[0].startswith("t") or clique[1].startswith("t") or clique[2].startswith("t"):
            adder += 1
    return adder

def solve2(graph):
    cliques = nx.find_cliques(graph)
    maximum = 0
    clique = None
    for c in cliques:
        if len(c) > maximum:
            maximum = len(c)
            clique = c
    sorted_clique = sorted(clique)
    return ",".join(sorted_clique)

DATA = generate_graph(parse_data(read_file("input.txt")))
#DATA = generate_graph(parse_data(read_file("test.txt")))

print("Advent of Code: 19th")
print("Part 1:", solve1(DATA))
print("Part 2:", solve2(DATA))
