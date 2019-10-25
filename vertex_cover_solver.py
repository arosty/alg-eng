import sys
import numpy as np

def read_data():
    input_data = sys.stdin
    for counter, line in enumerate(input_data):
        if counter == 0:
            num_of_edges = int(line.split()[1])
            edges = np.empty(num_of_edges, dtype=numpy.ndarray)
        else:
            current_edge = np.asarray(map(int, line.split()))       # TODO: maybe convert later to int (in np)
            edges[counter-1] = current_edge
    print(edges)

read_data()